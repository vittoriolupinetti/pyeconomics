from django.shortcuts import render_to_response,get_object_or_404,redirect,render
from django.template import RequestContext 
from django.conf import settings
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_page
from pyeconomics.mongodb import Connection
from .models import *
from django.http.response import Http404

TIME_CACHE=300
FIELD_DATA = 'data'

@login_required
#@cache_page(TIME_CACHE)
def index(request):
    c = Connection()
    
    if not c.db:
        return render(request,'error_mongodb.html',{})
    
    all = c.getall()
    
    storage_level = StorageLevel.objects.all()
    
    l_sl = []
    cc = 0
    for elem in storage_level:
        if elem.nome not in l_sl:
            l_sl.append(elem.nome.lower())
            cc += 1  
    
    l_serv = []
    for elem in Servizio.objects.all():
        l_serv = elem.nome.lower()
    
    prepagata = {}  
    utente = {}   
    for elem in all:
        
        if elem['Servizio'].lower() in l_serv:
        
            if elem['StorageLevel'].lower() not in l_sl and elem['StorageLevel'].strip() != "" :
                cc = cc + 1
                s = StorageLevel()
                s.nome = elem['StorageLevel'].title()
                s.ordine = cc
                s.save()
                               
     
            if elem['Prepagata'] not in prepagata.keys():
                prepagata[elem['Prepagata']]={'price_':0,'size_':0}
                for sl in l_sl:
                    if sl.title() not in prepagata[elem['Prepagata']].keys():
                        prepagata[elem['Prepagata']][sl.title()]={'price':0,'size':0}            
                prepagata[elem['Prepagata']]['All']={'price':0,'size':0}
                
            if elem['StorageLevel'].title() not in prepagata[elem['Prepagata']].keys():
                prepagata[elem['Prepagata']][elem['StorageLevel'].title()]={'price':0,'size':0}
                        
            try:
                prepagata[elem['Prepagata']][elem['StorageLevel'].title()]['size']+=int(elem['Size'])
                prepagata[elem['Prepagata']]['All']['size']+=int(elem['Size'])
                prepagata[elem['Prepagata']]['size_']+=int(elem['Size'])
            except:
                pass
            
            
            if FIELD_DATA in elem.keys():
                c = CostoStorage.objects.filter(dal__lte=elem[FIELD_DATA],al__gte=elem[FIELD_DATA],servizio__nome__iexact=elem['Servizio'],storage_level__nome__iexact=elem['StorageLevel']).first()
                if c:
                    try:
                        prepgata[elem['Prepagata']][elem['StorageLevel'].title()]['price']+= (int(elem['Size'])*c.costo)
                        prepagata[elem['Prepagata']]['All']['price']+= (int(elem['Size'])*c.costo)
                        prepagata[elem['Prepagata']]['price_']+=(int(elem['Size'])*c.costo)
                    except:
                        pass
                
         
            if elem['Utente'] not in utente.keys():
                utente[elem['Utente']]={'price_':0,'size_':0}
                for sl in l_sl:
                    if sl.title() not in utente[elem['Utente']].keys():
                        utente[elem['Utente']][sl.title()]={'price':0,'size':0}
                utente[elem['Utente']]['All']={'price':0,'size':0}
                        
            if elem['StorageLevel'].title() not in utente[elem['Utente']].keys():
                utente[elem['Utente']][elem['StorageLevel'].title()]={'price':0,'size':0}            
                    
            try:
                utente[elem['Utente']][elem['StorageLevel'].title()]['size']+=int(elem['Size'])
                utente[elem['Utente']]['All']['size']+=int(elem['Size'])
                utente[elem['Utente']]['size_']+=int(elem['Size'])
            except:
                pass
            
            
            if FIELD_DATA in elem.keys():
                c = CostoStorage.objects.filter(dal__lte=elem[FIELD_DATA],al__gte=elem[FIELD_DATA],servizio__nome__iexact=elem['Servizio'],storage_level__nome__iexact=elem['StorageLevel']).first()
                if c:
                    try:
                        utente[elem['Utente']][elem['StorageLevel'].title()]['price']+= (int(elem['Size'])*c.costo)
                        utente[elem['Utente']]['All']['price']+= (int(elem['Size'])*c.costo)
                        utente[elem['Utente']]['price_']+= (int(elem['Size'])*c.costo)
                    except:
                        pass
            
    
    return render(request,'index.html',{
            'prepagata':prepagata,
            'utente':utente,
            'user_sel':request.GET.get('user_sel'),  
            'storage_level': storage_level,         
        })
    
    
@login_required
def dettaglio(request):    
    
    u = request.GET.get('u') 
    p = request.GET.get('p')
    s = request.GET.get('s')
    
    price = 0
    size = 0
    
    if not ( p or u ):
        raise Http404()
        
    user_sel = False
    
    c = Connection()
    if s.lower()!='all':
        if p:
            find = c.findPrepagata(p,s)
             
        if u:
            find = c.findUtente(u,s)
            user_sel = True
    else:
        if p:
            find = c.findPrepagata(p)
             
        if u:
            find = c.findUtente(u)
            user_sel = True  
            
    diz = []
    for elem in find:
        if FIELD_DATA in elem.keys():
            c = CostoStorage.objects.filter(dal__lte=elem[FIELD_DATA],al__gte=elem[FIELD_DATA],storage_level__name__iexact=elem['StorageLevel']).first()
            if c:
                try:                    
                    elem['price'] = (int(elem['Size'])*c.costo)
                    price += (int(elem['Size'])*c.costo)
                except:
                    pass
        try:
            size += int(elem['Size'])
        except:
            pass
         
        diz.append(elem)
    
    return render(request,'dettaglio.html',{
            'find':find,
            'diz':diz,
            'user_sel':user_sel,
            'p': p,
            's': s,
            'u': u,
            'size':size,
            'price':price,
        })

