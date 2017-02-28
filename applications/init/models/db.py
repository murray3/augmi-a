# coding: utf8
import uuid
import datetime
import time; # 
now=datetime.datetime.today() 

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
#########################################################################

if request.env.web2py_runtime_gae:            # if running on Google App Engine
    db = DAL('gae')                           # connect to Google BigTable
    session.connect(request, response, db=db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db=MEMDB(Client())
else:                                         # else use a normal relational database
    db = DAL('sqlite://storage.sqlite')       # if not, use SQLite or other DB
## if no need for session
# session.forget()

#########################################################################
## Here is sample code if you need for 
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - crud actions
## comment/uncomment as needed
# from applications.init.modules.rpxauth import RPXAuth
from gluon.tools import *
auth=Auth(globals(),db)  
# auth=RPXAuth(globals(),db)                      # authentication/authorization
#auth.settings.hmac_key='sha512:dcda9600-d23b-4983-9951-d20342365db6'   
# auth.settings.actions_disabled=['register']                   # 
# auth.settings.rpx_key='4ef7f97b6cb5a679e4c5c486e1b7da786b88219d'
# auth.settings.rpx_realm = 'augmi'
# auth.settings.rpx_language_preference='en'
# auth.settings.rpx_login_domain= 'http://localhost:8000' # 'http://www.augmi-a.appspot.com'
# auth.settings.table_profile_name = 'profile'
# auth.settings.expiration = 2*3600 # 2 timer
# auth.settings.mailer=mail                     # for user email verification
from gluon.contrib.login_methods.rpx_account import RPXAccount

auth.settings.actions_disabled=['register','change_password','request_reset_password']
auth.settings.login_form = RPXAccount(request,
api_key="4ef7f97b6cb5a679e4c5c486e1b7da786b88219d",
domain="augmi",
url = "http://localhost:8000/%s/default/user/login" %
request.application) 
auth.define_tables()                         # creates all needed table  
crud=Crud(globals(),db)                      # for CRUD helpers using auth
crud.settings.auth=auth  
# crud.settings.auth=auth                      # enforces authorization on crud
# mail=Mail()                                  # mailer
# mail.settings.server='smtp.gmail.com:587'    # your SMTP server
# mail.settings.sender='you@gmail.com'         # your email
# mail.settings.login='username:password'      # your credentials or None
# auth.settings.mailer=mail                    # for user email verification
# auth.settings.registration_requires_verification = True
# auth.settings.registration_requires_approval = True
# auth.messages.verify_email = \
#  'Click on the link http://.../user/verify_email/%(key)s to verify your email'
## more options discussed in gluon/tools.py
#########################################################################

#########################################################################
## Define your tables below, for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

# from applications.init.modules.rpxauth import RPXAuth
# rpxAuth = RPXAuth(auth)
# rpxAuth.embed = True
# rpxAuth.allow_local = False
# rpxAuth.api_key = "4ef7f97b6cb5a679e4c5c486e1b7da786b88219d"
# rpxAuth.realm = "augmi"
# rpxAuth.token_url = "http://localhost:8000/init/default/myAugmi"


response.files.append("http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/jquery-ui.js")
#response.files.append("http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/ui-darkness/jquery-ui.css")


def slider_widget(f,v,**attr):
    wrapper = DIV(_id="slider_wrapper",_style="margin-left:30px;margin-bottom:5px;width: 20px;align:center;text-align:center;color:black;")
    inp = SQLFORM.widgets.string.widget(f,v, **attr)
    sld = DIV(_id='slider_' + inp['_id'])
    sldval = SPAN(inp['_value'],_id=sld['_id']+'_val')
    scr1 = "jQuery('#%s').hide();" % inp['_id']
    scr2 = "jQuery('#%s').val(ui.value);jQuery('#%s').text(ui.value);" % (inp['_id'], sldval['_id'])
    jqscr = SCRIPT(scr1,"jQuery('#%s').slider({orientation: 'vertical', min: 1, max: 7, value: '%s',stop: function(event, ui) {%s}});" % \
                    (sld['_id'],inp['_value'],scr2),_type="text/javascript")
    wrapper.components.extend([sld,sldval,inp,jqscr])
    return wrapper
    
def slider_widget2(f,v,**attr):
    wrapper = DIV(_id="slider_wrapper",_style="margin-left:5px;margin-bottom:5px;width: 300px;align:center;text-align:center;color:black;")
    inp = SQLFORM.widgets.string.widget(f,v, **attr)
    sld = DIV(_id='slider_' + inp['_id'])
    sldval = SPAN(inp['_value'],_id=sld['_id']+'_val',_style="color:yellow;")
    scr1 = "jQuery('#%s').hide();" % inp['_id']
    scr2 = "jQuery('#%s').val(ui.value);jQuery('#%s').text(ui.value);" % (inp['_id'], sldval['_id'])
    jqscr = SCRIPT(scr1,"jQuery('#%s').slider({orientation: 'horizontal', min: 1, max: 10, value: '%s',stop: function(event, ui) {%s}});" % \
                    (sld['_id'],inp['_value'],scr2),_type="text/javascript")
    wrapper.components.extend([sld,sldval,inp,jqscr])
    return wrapper
    
# def my_string_widget(field,value):
   # wrapper = INPUT(_name=field.name,_id="%s_%s\" % (field._tablename, field.name),_class=field.type,_value=value,requires=field.requires)
    # return wrapper


db.define_table('mindbeat',
    SQLField('uuid',length=128,writable=False,default=str(uuid.uuid4())),
    SQLField('timestamp','datetime',default=now),
    SQLField('user_id',),
    SQLField('user_name',),
    SQLField('provider',),
    SQLField('pic_url',),
    SQLField('active','boolean',default=False),
    SQLField('Mood','integer',label=T('Mood'),widget=slider_widget,default=4),
    SQLField('Stress','integer',label=T('Stress'),widget=slider_widget,default=4),
    SQLField('Focus','integer',label=T('Focus'),widget=slider_widget,default=4),
    SQLField('Energy','integer',label=T('Energy'),widget=slider_widget,default=4),
    SQLField('UTD','integer',label=T('Up-To-Date'),widget=slider_widget,default=4),
    SQLField('Optimism','integer',label=T('Optimism'),widget=slider_widget,default=4),
    SQLField('html','string'),
    SQLField('Location','string'),
    SQLField('Message','string',label=T('Micro-Blog'),widget=SQLFORM.widgets.string.widget,default=""))
    
db.define_table('q',
    SQLField('uuid',length=128,writable=False,default=str(uuid.uuid4())),
    SQLField('timestamp','datetime',default=now),
    SQLField('give_user_id',length=128),
    SQLField('take_user_id',length=128),
    SQLField('message_give','string'),
    SQLField('message_take','string'),
    SQLField('message_admin','string'),
    SQLField('q','integer',label=T('EMP'),widget=slider_widget2,default=1))
