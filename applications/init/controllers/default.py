# coding: utf8

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################  

response.files.append(URL(r=request,c='static',f='jquery-ui-1.7.2.custom.min.js'))
response.files.append(URL(r=request,c='static',f='jquery.ui.core.js'))
response.files.append(URL(r=request,c='static',f='jquery-ui.css'))

def profile():
    try: thisprof=db(db.profile.name==request.args[0]).select()[0]
    except: redirect(URL(r=request,c='default',f='index'))
    userprofile=request.args(0)
    return dict(userprofile=userprofile) 

def twitter_post(username,password,message):
    import urllib, urllib2, base64, gluon.contrib.simplejson
    args= urllib.urlencode([('status',message)])
    headers={}
    # username=""
    # password=""
    # message="augmi test!"
    headers['Authorization'] = 'Basic '+base64.b64encode(username+':'+password)
    request = urllib2.Request('http://twitter.com/statuses/update.json', args, headers)
    return  gluon.contrib.simplejson.loads(urllib2.urlopen(request).read()) 

def data():
    return dict(form=crud())
	
def trafiki():
    return dict()
	
def update_target():
  return """jQuery("#target").html(%s);""" % repr("""<a href='#' id='test' onclick="ajax('{{=URL(r=request,f='update_target')}}',[],':eval');"><img src="{{=URL(r=request,c='static/images',f='emp.gif')}}" style="height: 72px; width: 28px;"  TITLE="Send Empathy Again"></a>""" ) 
	
def update_target2():
  return """jQuery("#target").html(%s);""" % repr("""<a href='#' id='test' onclick="ajax('{{=URL(r=request,f='update_target')}}',[],':eval');">EMP</a>""") 
	
def login():
    return dict()
	
	
#def list_beats():
    beats=db(db.mindbeat.id>0).select(db.mindbeat.ALL,orderby=~db.mindbeat.timestamp)
    # for b in beats:
       # if b.Mood==5:
          # b.html="""<div  id="rounded" $(this).corner(); style="border: 2px solid #C0C0C0; background-color: black; margin-right: 0px; margin-left: 0px; margin-bottom: 2px; width: 46px; height: 46px;">
# <img src="{{=URL(r=request,c='static/images',f='clear.png')}}" style="height: 42px; width: 42px; background-image: url(http://localhost:8000/init/static/images/throbber3.gif) ;  margin-left: 2px;  margin-top: 2px; position: relative; background-position: -50px 0;" TITLE="My Mood Level is {{=b.Mood}}">
# </div>"""
    #return dict(beats=beats)

def index3():
    d = DIV("Click Me", _id="clickme")
    event.listen("click", d, handle_it)
    return dict(d=d)



def handle_it():
    return("alert('Thanks for clicking');")

def index():
    #d = DIV("Click Me", _id="clickme")
    #event.listen("click", d, handle_it)
    beats=db(db.mindbeat.id>0).select(db.mindbeat.ALL,orderby=~db.mindbeat.timestamp,limitby=(0,20))
    if auth.is_logged_in():
        flash = "%s %s" % (T('Welcome to Augmi: '), auth.user.first_name)
    else:
        flash = T('Welcome to Augmi, Please Login to use features!')
    id = ['Mood_html','Stress_html','Focus_html','Energy_html','UTD_html','Optimism_html']
    id1 = ['Mood','Stress','Focus','Energy','UTD','Optimism']
    beats1 = {'Mood_html':"",'Stress_html':"",'Focus_html':"",'Energy_html':"",'UTD_html':"",'Optimism_html':""}
    s_score = {1:"0px",2:"-48px",3:"-96px",4:"-140px",5:"-186px",6:"-233px",7:"-278px"}
    all_score = {1:"0px",2:"-50px",3:"-100px",4:"-150px",5:"-200px",6:"-250px",7:"-300px"}
    #all_score = {1:"0px",2:"-48px",3:"-96px",4:"-144px",5:"-192px",6:"-240px",7:"-288px"}
    for bb in beats:
        for cc in id:
            bb[cc]="0px"
    # for b in beats:
		# x=0
		# for i in id1:
			# ii=id[x]
			# if i=="Stress":
				# score=s_score
			# else:
				# score=all_score
			# for k, v in score.iteritems():
				# if b[i]==k:
					# b[ii]=v
		# x=x+1
		
	for b in beats:
		for kk,vv in s_score.items():
			if b['Stress']==kk:
				b['Stress_html']=vv
		for k,v in all_score.items():
			if b['Mood']==k:
				b['Mood_html']=v
			if b['Focus']==k:
				b['Focus_html']=v
			if b['Energy']==k:
				b['Energy_html']=v
			if b['UTD']==k:
				b['UTD_html']=v
			if b['Optimism']==k:
				b['Optimism_html']=v
    response.flash=flash
#-------------------------------------------------------------------------------
  # send empathy form
    form=SQLFORM.factory(Field('a'),Field('b'),db.q,fields=['q'])

  # then update db
    if form.accepts(request.vars,session):
        #@auth.requires_login()
        db.profile.user_id.default=auth.user.id
        q_give_user_id=request.vars.q_user_id
        q_take_user_id=auth.user.id
        q_give=int(form.vars.q)
        q_new=db.profile.q+q_give
        q_take=int(form.vars.q)*10
        message_give_text="You have recieved Empathy (q: " + str(q_give) +") from User: " + auth.user.first_name
        message_take_text="You gave Empathy (q: " + str(q_give) +") to User: " + request.vars.q_user_name + "this has cost you q: " + str(q_take)
        # qval=db.q.q+form.vars.q
        db.q.insert(message_give=message_give_text,message_take=message_take_text,give_user_id=q_give_user_id,take_user_id=q_take_user_id,q=form.vars.q)
        #db.profile.id.default=form.vars.b
        #qval2 = db.profile.q
        #db.profile.update(q = q_new)
        #db.q.user_id.default=form.vars.b
        #qval=int(form.vars.q)*10
        #db.q.insert(message_give=message_give_text+request.vars.b,user_id=request.vars.b,q=form.vars.q)

        for row in db(db.profile.user_id==request.vars.q_user_id).select():
            row.update_record(q = int(row.q) + (form.vars.q)) 

        for row in db(db.profile.user_id==auth.user.id).select():
            row.update_record(q = int(row.q) - (form.vars.q*10)) 
        session.flash=DIV("Sent EMP:")   
    elif form.errors:
        response.flash=DIV(T('Error: did not SEND EMP'),_class="error")
    return dict(form=form,beats=beats)
	

def user():
    return dict(form=auth())
def jq():
    return dict()

def send():
    from google.appengine.api import xmpp
    user_address = 'chrisjmurray3@gmail.com'
    xmpp.send_invite(user_address)
    msg = "test"
    status_code = xmpp.send_message(user_address, msg)
    return dict(status_code=status_code) 


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()

def feed():
    return dict(title="Augmi",
                link="http://augmi.appspot.com", 
                description="Augmi openMind",
                items=[
                  dict(title="cjm",
                       link="http://augmi.appspot.com", 
                       description="cjm")
                ])
				

@auth.requires_login()
def my_augmi():
  from urllib2 import URLError, HTTPError
  q_take_messages=db(db.q.take_user_id==auth.user.id).select(orderby=~db.q.timestamp)
  q_give_messages=db(db.q.give_user_id==auth.user.id).select(orderby=~db.q.timestamp)
#-------------------------------------------------------------------------------
  form1=SQLFORM.factory(db.profile,fields=['pic_url','name','country','email'])
  if form1.accepts(request.vars, formname='form_one'):
    db.profile.user_id.default=auth.user.id
    for row in db(db.profile.user_id==auth.user.id).select():
        row.update_record(pic_url = form1.vars.pic_url, name = form1.vars.name, country = form1.vars.country, email = form1.vars.email) 
    session.flash=DIV("UPDATED YOUR PROFILE DATA : due to bug please logout then login to take effect")  
    redirect(URL(r=request,c='default',f='my_augmi'))
  elif form1.errors:
    response.flash=DIV(T('Error: did not update profile'),_class="error")

  
  # create form
  form2=SQLFORM.factory(Field('no_table_username',default=session.no_table_username),Field('no_table_password',default=session.no_table_password),
      db.mindbeat,fields=['Mood','Stress','Focus','Energy','UTD','Optimism','Message']
      )

  # update db
  if form2.accepts(request.vars, formname='form_two'):
    session.no_table_username = request.vars.no_table_username
    session.no_table_password = request.vars.no_table_password
    if not (session.no_table_username=="" and session.no_table_password=="") :
       try:twitter_post(session.no_table_username,session.no_table_password,form2.vars.Message) 
       except:
         session.flash=DIV("Returned Error Code " )
    LocationString=request.vars._City+" "+request.vars._Country
    db.mindbeat.insert(user_id=auth.user.id,user_name=auth.user.first_name,provider=auth.userprofile.provider,pic_url=auth.userprofile.pic_url,active=True,Mood=form2.vars.Mood,Stress=form2.vars.Stress,Focus=form2.vars.Focus,Energy=form2.vars.Energy,UTD=form2.vars.UTD,Optimism=form2.vars.Optimism,Message=form2.vars.Message,Location=LocationString ) 
    session.flash=DIV("UPDATED YOUR MINDBEAT")   
    redirect(URL(r=request,c='default',f='my_augmi'))
  elif form2.errors:
    response.flash=DIV(T('Error: did not create new mindbeat'),_class="error")

  return dict(form1=form1,form2=form2,q_take_messages=q_take_messages,q_give_messages=q_give_messages)
  
def callback():
    value=request.vars.value 
    return "jQuery('#dialog').html(%s)" % repr(str(value)) 
	
def give_emp():
    form=SQLFORM.factory(Field('val'),db.q,fields=['q','user_id'])

  # update db
    if form.accepts(request.vars,session):
        #db.q.user_id.default=form.vars.user_id
        db.q.user_id.default=request.args[0]
        message_give_text="You have recieved Empathy from User"
        # qval=db.q.q+form.vars.q
        # db.q.insert(q=qval,message_give=message_give_text)
        for row in db(db.q.user_id==form.vars.user_id).select():
            row.update_record(q = row.q + form.vars.q) 

    return dict(form=form)
	
def more():
    return dict()
