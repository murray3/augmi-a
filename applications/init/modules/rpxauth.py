#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
RPXAuth Copyright 2009 Niels Bjerre <niels@bjerre.net>
version 1.0
Extension to web2py Web Framework (Copyrighted, 2007)
Developed by Massimo Di Pierro <mdipierro@cs.depaul.edu>
License: GPL v2

Class RPXAuth
    extends gluon.tools: Auth
    exposes:
    - http://.../{application}/{controller}/user/login   #interface to OpenID (etc.) login
    - http://.../{application}/{controller}/user/rpxresponse  #recieves token from RPX - and redirects user
    - http://.../{application}/{controller}/user/plogin   #allows traditional (password) login

    usage:
        MODEL:
            from gluon.rpxauth import RPXAuth
            auth=RPXAuth(globals(),db)
        CONTROLLER:
            def user(): return dict(form=auth())
    warning:
        Users may login without registration - thats the idea!  
        User may create more than 1 user-account by logging ind with different profiles
        If logged in the user logs ind with second profile: the accounts are
        "consolidated": Second profile are attached to the user and the "other user" are deleted!

OK: Mapping: use user-uuid to secure persistent mapping after export-import and db sync
OK  : save profile in session  
OK  : Consolidate userprofiles for 1 user
TODO: add profile information in login-form
TODO: Redirect to profile-form if email missing - after login and when checking for logged-in
TODO: Facebook: No email -> Require email or send confirmation etc. through Facebook?
"""
import uuid
import datetime
import re
from gluon.storage import Storage, Settings
from gluon.validators import *
from gluon.html import *
from gluon.sqlhtml import *
from gluon.http import *
from gluon.tools import Auth
import gluon.contrib.simplejson as json
import urllib
import urllib2

DEFAULT = lambda : None

class RPXAuth(Auth):
    """
    extends gluon.tools: Auth
    exposes:
    - http://.../{application}/{controller}/user/rpxlogin
    - http://.../{application}/{controller}/user/rpxresponse
    usage:
        MODEL:
            from gluon.rpxauth import RPXAuth
            auth=RPXAuth(globals(),db)
        CONTROLLER:
            def user(): return dict(form=auth())
    warning:
        Users may login without registration - thats the idea!  
        User may create more than 1 user-account by logging ind with different profiles
        If logged in the user logs ind with second profile: the accounts are
        "consolidated": Second profile are attached to the user and the "other user" are deleted!

    """
    def __init__(self, environment, db=None):
        Auth.__init__(self, environment, db=None)
        self.environment = Storage(environment)
        self.db = db
        request = self.environment.request
        session = self.environment.session
        app = request.application
        auth = session.auth
        if auth and auth.last_visit and auth.last_visit\
             + datetime.timedelta(days=0, seconds=auth.expiration)\
             > request.now:
            self.userprofile = auth.userprofile
        else:
            self.user = None
            self.userprofile = None
            session.auth = None


        self.settings.expiration = 2*3600
        self.settings.table_person = None
        self.settings.table_profile_name = 'auth_profile'
        self.settings.table_person_name = 'auth_person'
        self.settings.add_person_log = 'Person %(person_id)s created'
        self.settings.rpxlogin_log = 'RPX user %(id)s Logged-in'
        self.settings.rpxlogin_next = URL(r=request, f='index')
        self.settings.rpxlogin_onvalidation = None
        self.settings.rpxlogin_onaccept = None


    def define_tables(self,migrate=True):
        """
        user: first- & last_name not required
        add auth_profile table
        call Auth.define_tables
        """        
        db = self.db
        if not self.settings.table_user:
            password = self.settings.password_field
            self.settings.table_user = db.define_table(
                self.settings.table_user_name,
                db.Field('uuid',length=64,default=uuid.uuid4(),readable=False,writable=False,unique=True),
                db.Field('first_name', length=128,default=''),
                db.Field('last_name', length=128,default=''),
                db.Field('email', length=128,default=''),
                db.Field(password, 'password', readable=False,
                         label='Password'),
                db.Field('registration_key', length=128, writable=False, readable=False,default=''),
                migrate=migrate)
            table = self.settings.table_user
            #table.first_name.requires = IS_NOT_EMPTY()
            #table.last_name.requires = IS_NOT_EMPTY()
            table[password].requires = CRYPT()
            table.email.requires = [IS_EMAIL(), IS_NOT_IN_DB(db, '%s.email'
                                 % self.settings.table_user._tablename)]
            table.registration_key.default = ''
     
        if not self.settings.table_profile:
            # users can have more (profiles)!
            self.settings.table_profile = db.define_table(
                self.settings.table_profile_name,
                db.Field('user_id',self.settings.table_user),
                db.Field('provider', length=128,default=''),
                db.Field('identifier', length=256,default=''),
                db.Field('name', length=128,default=''),
                db.Field('pic_url', length=256,default=''),
                db.Field('email', length=128,default=''),
                db.Field('country', length=128,default=''),
                db.Field('postalcode', length=64,default=''),
                db.Field('registration_key', length=128, writable=False, readable=False,default=''),
                db.Field('q', length=64,default='5000'),
                migrate=migrate)
            table = self.settings.table_profile
            table.user_id.requires = IS_IN_DB(db, '%s.id' % self.settings.table_user._tablename,
                '%(id)s: %(first_name)s %(last_name)s')
            table.provider.requires = IS_NOT_EMPTY()
            table.identifier.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, '%s.identifier'
                                 % self.settings.table_profile._tablename)]
            table.email.requires = [IS_EMAIL()]   #facebook don't have email
            table.registration_key.default = ''

        Auth.define_tables(self,migrate)

    def rpxlogin(
        self,
        next=DEFAULT,
        onvalidation=DEFAULT,
        onaccept=DEFAULT,
        log=DEFAULT,
        ):
        request = self.environment.request
        session = self.environment.session

        rpxurl = 'https://%s.rpxnow.com/openid/embed' % (self.settings.rpx_realm)
        src= "%s?realm=%s&language_preference=%s&token_url=%s%s" % \
                      (rpxurl,self.settings.rpx_realm,self.settings.rpx_language_preference, \
                       self.settings.rpx_login_domain,URL(r=request,args=['rpxresponse']))
        form = IFRAME("",_src=src,_scrolling="no",_frameBorder="no",_style="width:400px;height:340px;")        
        return form

    def rpxmap(self,identifier,iduser):
         #map userid to RPX profile
         api_params = {'apiKey': self.settings.rpx_key,'identifier' : identifier,'primaryKey' : iduser,'format': 'json',}                    
         http_response = urllib2.urlopen('https://rpxnow.com/api/v2/map', urllib.urlencode(api_params))
         auth_info_json = http_response.read()
         auth_info = json.loads(auth_info_json)
         return auth_info['stat']
         #if auth_info['stat'] != 'ok': #RollBack ??
         #session.flash = 'Warning: RPX mapping failed'
         #    #self.db(tuser.id==iduser).delete()  #cascade delete profile
         #    next = URL(r=request, f=next.replace('[id]', str(iduser)))
         #    redirect(next)
         ##    return


    def rpxresponse(self,
        next=DEFAULT,
        onvalidation=DEFAULT,
        onaccept=DEFAULT,
        log=DEFAULT,
        ):
        """
        retrieves a RPX login form: https://rpxnow.com/docs
        """

        request = self.environment.request
        session = self.environment.session
        if not request.vars._next:
            request.vars._next = request.env.http_referer or ''
        if next == DEFAULT:
            next = self.settings.login_next or request.vars._next
        if onvalidation == DEFAULT:
            onvalidation = self.settings.rpxlogin_onvalidation
        if onaccept == DEFAULT:
            onaccept = self.settings.login_onaccept
        if log == DEFAULT:
            log = self.settings.rpxlogin_log


        if request.vars.token:     #token in request URL from RPX
            token = request.vars.token
            api_params = {
                'token': request.vars.token,
                'extended' : 'true',
                'apiKey': self.settings.rpx_key,
                'format': 'json',
            }
            #send request for profile
            http_response = urllib2.urlopen('https://rpxnow.com/api/v2/auth_info', urllib.urlencode(api_params))
            auth_info_json = http_response.read()
            auth_info = json.loads(auth_info_json)
            if auth_info['stat'] != 'ok':        
                return dict(message = 'An error occured: '+auth_info['err']['msg'])
                print 'An error occured: '+auth_info['err']['msg']                
            else:    #profile received fro RPX
                tuser = self.settings.table_user
                tprofile = self.settings.table_profile

                profile = auth_info['profile']
                identifier = profile.get('identifier')
                provider = profile.get('providerName')
                userID = profile.get('primaryKey')
                name = profile.get('displayName')
                email = profile.get('email')
                profile_pic_url = profile.get('photo')
                address = profile.get('address')
                if address:
                    postalcode = address.get('postalCode')
                    country = address.get('country')
                else:
                    postalcode = ""
                    country = ""
                try:
                    rprofile = self.db(tprofile.identifier==identifier).select()[0]
                except:
                    rprofile = ""
                if session.auth: #User logged in
                    #relogin same profile, other profile / consolidate?
                    iduser = session.auth.user.id
                    uuid = session.auth.user.uuid
                    ruser = self.db(tuser.id==iduser).select()
                    if len(ruser)==0:
                          iduser = tuser.insert(first_name=name,email=email,uuid=uuid)
                          ruser = self.db(tuser.id>0).select()[0]

                    if not userID or not rprofile:  #New profile
                        idprofile=tprofile.insert(user_id=iduser,identifier=identifier,provider=provider,name=name, \
                                pic_url=profile_pic_url,email=email,postalcode=postalcode,country=country)
                        self.rpxmap(identifier,uuid)
                    elif userID == uuid:     #update profile
                        rprofile.update_record(user_id=iduser,identifier=identifier,provider=provider,name=name, \
                                pic_url=profile_pic_url,email=email,postalcode=postalcode,country=country)
                    else:     #userID != uuid: CONSOLIDATE update OLD profiles - DELETE USER
                        oldid = rprofile.user_id
                        rprofile.update_record(user_id=iduser,identifier=identifier,provider=provider,name=name, \
                                pic_url=profile_pic_url,email=email,postalcode=postalcode,country=country)
                        self.rpxmap(identifier,uuid)
                        oldprof = self.db(tprofile.user_id==oldid).select()
                        for rec in oldprof:
                            rec.update_record(user_id=int(iduser))
                            self.rpxmap(rec.identifier,uuid)
                        self.db(tuser.id==oldid).delete()
                else:  #User NOT logged in
                    if not rprofile: # ADD USER and PROFILE
                        iduser = tuser.insert(first_name=name,email=email,)
                        ruser = self.db(tuser.id==iduser).select()[0]
                        uuid = ruser.uuid
                        self.rpxmap(identifier,uuid)
                        idprofile=tprofile.insert(user_id=iduser,identifier=identifier,provider=provider,name=name, \
                                pic_url=profile_pic_url,email=email,postalcode=postalcode,country=country)
                        rprofile = self.db(tprofile.identifier==identifier).select()[0]
                    else:
                        iduser = int(rprofile.user_id)
                        ruser = self.db(tuser.id==iduser).select()
                        if len(ruser)==0:
                            iduser = tuser.insert(first_name=name,email=email,)
                            ruser = self.db(tuser.id>0).select()[0]
                        else:
                            ruser = self.db(tuser.id==iduser).select()[0]
                        uuid = ruser.uuid
                        rprofile.update_record(user_id=iduser,provider=provider,name=name, \
                                pic_url=profile_pic_url,email=email,postalcode=postalcode,country=country)
                        if userID != uuid:
                            self.rpxmap(identifier,uuid)

                ruser = self.db(tuser.id==iduser).select()[0]
                rprofile = self.db(tprofile.identifier==identifier).select()[0]
                   
                iuser = ruser.items()
                iprof = rprofile.items()
                TYPES = (str,int,long,datetime.time,datetime.date,datetime.datetime,bool)                
                suser = Storage(dict([(k, v) for (k, v) in iuser if isinstance(v, TYPES)]))
                sprof = Storage(dict([(k, v) for (k, v) in iprof if isinstance(v, TYPES)]))
                session.auth = Storage(user=suser, userprofile=sprof, last_visit=request.now,
                       expiration=self.settings.expiration)
                self.user = suser
                self.userprofile = sprof
                session.flash = self.messages.logged_in

                log = self.settings.login_log
                if log:
                    self.log_event(log % self.user)
                if onaccept:
                    onaccept(form)
                if not next:
                    next = URL(r=request)
                elif next and not next[0] == '/' and next[:4] != 'http':
                    next = URL(r=request, f=next.replace('[id]', str(iduser)))
                redirect(next)
            #end auth_info['stat'] == 'ok':
        else: # end token
            session.flash = 'Warning: No Token from RPX!?'
 
    def profile(
        self,
        next=DEFAULT,
        onvalidation=DEFAULT,
        onaccept=DEFAULT,
        log=DEFAULT,
        ):
        """
        returns a form that lets the user change his/her profile
        """

        if not self.is_logged_in():
            redirect(self.settings.login_url)
        password = self.settings.password_field
        self.settings.table_user[password].writable = False
        request = self.environment.request
        session = self.environment.session
        if not request.vars._next:
            request.vars._next = request.env.http_referer or ''
        if next == DEFAULT:
            next = self.settings.profile_next or request.vars._next
        if onvalidation == DEFAULT:
            onvalidation = self.settings.profile_onvalidation
        if onaccept == DEFAULT:
            onaccept = self.settings.profile_onaccept
        if log == DEFAULT:
            log = self.settings.profile_log
        form = SQLFORM(
            self.settings.table_user,
            self.user.id,
            hidden=dict(_next=request.vars._next),
            showid=self.settings.showid,
            submit_button=self.settings.submit_button,
            delete_label=self.settings.delete_label,
            )
        rows=self.db(self.settings.table_profile.user_id==self.user.id).select()
        tr=TABLE(_class='sortable')
        for row in rows:
             if session.auth.userprofile.identifier==row.identifier:
                 current = '*'
             else:
                 current = ''
             tr.append(TR(TD(current),TD(row.provider),TD(row.identifier),TD(row.name)))
        div = DIV(form,H2('Profiles'),tr)
        if form.accepts(request.vars, session,
                        formname='profile',
                        onvalidation=onvalidation):
            session.flash = self.messages.profile_updated
            log = self.settings.profile_log
            if log:
                self.log_event(log % self.user)
            if onaccept:
                onaccept(form)
            if not next:
                next = URL(r=request)
            elif next and not next[0] == '/' and next[:4] != 'http':
                next = URL(r=request, f=next.replace('[id]',
                           str(form.vars.id)))
            redirect(next)
        return div

    def __call__(self):
        """
        usage:

        def authentication(): return dict(form=auth())
        """
        request = self.environment.request
        args = request.args
        if not args:
            redirect(URL(r=request, args='login'))
        if args[0] == 'login':
            return self.rpxlogin()
        elif args[0] == 'passwd_login':
            return Auth.login(self)
        elif args[0] == 'rpxresponse':
            return self.rpxresponse()
        elif args[0] == 'logout':
            return self.logout()
        elif args[0] == 'register':
            return self.register()
        elif args[0] == 'verify_email':
            return self.verify_email()
        elif args[0] == 'retrieve_username':
            return self.retrieve_username()
        elif args[0] == 'retrieve_password':
            return self.retrieve_password()
        elif args[0] == 'change_password':
            return self.change_password()
        elif args[0] == 'profile':
            return self.profile()
        elif args[0] == 'groups':
            return self.groups()
        else:
            raise HTTP(404)



