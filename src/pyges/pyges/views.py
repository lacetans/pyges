# -*- coding: utf-8 -*-

from models import *
from pyramid.httpexceptions import HTTPFound
from google.appengine.api import mail
from google.appengine.api import users

def root_view(request):
	# show all pages
    p = Page.all()
    return { "pages":p }

def create_page_view(request):
    if request.method=="GET":
    	# first visit: show form
        return {}
    # POST form: save page
    title = request.POST.get("title")
    text = request.POST.get("text")
    page = Page(title=title,text=text)
    page.put()
    return HTTPFound( "/" )#request.application_url )
def send_mail(request):
     if request.method=="GET":
    	# first visit: show form
        return {}
     # POST form: send mail
     try:
     	fname=request.POST["firstname"]
 	sname=request.POST["surname"]
	email=request.POST["mail"]
	msg=request.POST["text"]
     except:
	return {'missatge':'Omple tots els camps'}
     message_body = "<h3>"+ fname + " " + sname + "</h3><h5>" + email + "</h5>" + msg
     mail.send_mail(
     sender='sundavar.l2@gmail.com',
     to='sundavar.l2@gmail.com',
     subject='Prueba enviar mail',
     body=fname+" "+sname+" "+email+" "+msg,     
     html=message_body)
     return{'missatge':'Misatge enviat'}
def view_page_view(request):
	# show a particular page
    id = int(request.matchdict['id'])
    p = Page.get_by_id(id)	
    return { "page": p }

def admin_config_view(request):
    # config should be a singleton
    config = GlobalConfig.all().get()
    if not config:
        print "creanting initial site config..."
        config = GlobalConfig(
            site_name = "Pyges Site",
            admin_users = []
        )
    # TODO: check singleton (only one instance)
    
    # data have been sent: update site config
    if request.method=="POST":
        site_name = request.POST.get("sitename")
        admin_users = request.POST.get("adminusers")
        config.site_name = site_name
        config.admin_users = admin_users.split()
        config.put()
    return {"config":config}
