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
     message_body = "Hola,esto es una prueba del mail"
     message = mail.EmailMessage(
     sender='sundavar.l2@gmail.com',
     to='sundavar.l2@gmail.com',
     subject='Prueba enviar mail',
     body=message_body)
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
