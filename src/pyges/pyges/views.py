# -*- coding: utf-8 -*-

from models import *
from pyramid.httpexceptions import HTTPFound
firstp=False

def root_view(request):
	# show all pages
    p = Page.all()
    return { "pages":p,"langs": langs()}

def create_page_view(request):
    if request.method=="GET":
    	# first visit: show form
        return {"langs": langs()}
    # POST form: save page
    lang = request.POST.get("lang")
    title = request.POST.get("title")
    text = request.POST.get("text")
    page = Page(lang=lang,title=title,text=text)
    page.put() #desa a la BBDD
    page.idsec = int(page.key().id())
    page.put()
    return HTTPFound( "/" ) #request.application_url )

def view_page_view(request):
	# show a particular page
    id = int(request.matchdict['id'])
    #crear id2(copia id) + id idioma
    p = Page.get_by_id(id)
    return { "page": p, "langs":langs()}

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

# start translation functions

def trans_menu_view(request):
    pages = Page.all()
    ids = [] # list of secondary id (language group)
    tbl = [] # table id secondary, titles and id for each language
    count = 0 # counter of pages in database (not translates of same page)
    for page in pages:
        if not page.idsec in ids:
            ids.append(page.idsec)
            if page.lang == "en":
                tbl.append({"idsec":page.idsec,"title_en":page.title,"title_es":"","title_ca":"","id_en":page.key().id(),"id_es":"","id_ca":"","count":count})
            if page.lang == "es":
                tbl.append({"idsec":page.idsec,"title_en":"","title_es":page.title,"title_ca":"","id_en":"","id_es":page.key().id(),"id_ca":"","count":count})
            if page.lang == "ca":
                tbl.append({"idsec":page.idsec,"title_en":"","title_es":"","title_ca":page.title,"id_en":"","id_es":"","id_ca":page.key().id(),"count":count})
            count += 1
        else:
            for i in range(len(tbl)):
                if page.idsec == tbl[i]["idsec"]:
                    if page.lang == "en":
                        tbl[i]["title_en"] = page.title
                        tbl[i]["id_en"] = page.key().id()
                    if page.lang == "es":
                        tbl[i]["title_es"] = page.title
                        tbl[i]["id_es"] = page.key().id()
                    if page.lang == "ca":
                        tbl[i]["title_ca"] = page.title
                        tbl[i]["id_ca"] = page.key().id()
    return {"table":tbl,"langs":langs()}

def trans_edit_view(request):
    if request.method=="GET":
        # first visit: show form
        id = int(request.matchdict['id'])
        p = Page.get_by_id(id)
        return {"page":p,"langs":langs(),"id":id}
    # POST form: save translation page
    id = int(request.POST.get("id"))
    p = Page.get_by_id(id)
    p.title = request.POST.get("title")
    p.text = request.POST.get("text")
    p.put() #desa a la BBDD
    return HTTPFound( "/menu_trans" )#request.application_url )

def trans_create_view(request):
    if request.method=="GET":
        # first visit: show form
        ln = request.matchdict['ln'] # selected language
        id = int(request.matchdict['id']) # id secondary
        pages = Page.gql("WHERE idsec = :id2", id2 = id)
        exl = {} # existing languages
        for page in pages:
            exl[page.lang] = langs()[page.lang]
        return {"langs":langs(),"exl":exl,"ln":ln,"idsec":id}
    # POST form: save translation page
    idsec = int(request.POST.get("idsec"))
    lang = request.POST.get("lang")
    title = request.POST.get("title")
    text = request.POST.get("text")
    page = Page(idsec=idsec,lang=lang,title=title,text=text)
    page.put() #desa a la BBDD
    return HTTPFound( "/menu_trans" )#request.application_url )

def trans_view_view(request):
    if request.method=="GET":
        ln = request.matchdict['ln'] # selected language
        id = int(request.matchdict['id']) # id secondary
        pages = Page.gql("WHERE idsec = :id2", id2 = id)
        p = ""
        for page in pages:
            if page.lang == ln:
                p = page
                return {"page":p,"langs":langs()}

def trans_delete_view(request):
    if request.method=="GET":
        # first visit: show form
        fn = request.matchdict['fn'] # function one (delete language page), all (delete all pages)
        id = int(request.matchdict['id']) # function one (id), function all (idsec)
        p = []
        if fn == "one":
            page = Page.get_by_id(id)
            p.append(page)
        if fn == "all":
            pages = Page.gql("WHERE idsec = :id2", id2 = id)
            for page in pages:
                p.append(page)
        return {"pages":p,"langs":langs(),"fn":fn,"id":id}
    # POST form: delete translation page or page
    fn = request.POST.get("fn")
    id = int(request.POST.get("id"))
    confirm = request.POST.get("confirm")
    if confirm == "ok":
        if fn == "one":
            page = Page.get_by_id(id)
            page.delete()
        if fn == "all":
            pages = Page.gql("WHERE idsec = :id2", id2 = id)
            for page in pages:
                page.delete()
    return HTTPFound( "/menu_trans" )#request.application_url )	

def langs():
    #... change db to dictionary
    #l = {}
    #dblangs = DBlang.all()
    #for lang in dblangs:
    #    l[lang.lang] = dblangs[lang.lang]
    l = {"en":"English","es":"Español","ca":"Català"}
    return l

def current_lang(fn="get",ln="en"):
    if fn == "get":
        # ... return current lenguage
        return "en"
    if fn == "set":
        # ... set current lenguage
        return True

# end translation functions