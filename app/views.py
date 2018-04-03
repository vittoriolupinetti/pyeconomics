from django.shortcuts import render_to_response,get_object_or_404,redirect,render
from django.template import RequestContext 
from django.conf import settings
from django.contrib.auth.views import login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.cache import cache_page
from aruta.mongodb import Connection
from .models import CostoStorage
from django.http.response import Http404

TIME_CACHE=300
FIELD_DATA = 'data'

@login_required
#@cache_page(TIME_CACHE)
def index(request):
    c = Connection()
    all = c.getall()
    
    prepagata = {}  
    utente = {}   
    for elem in all:
 
        if elem['Prepagata'] not in prepagata.keys():
            prepagata[elem['Prepagata']]={'price_':0,'size_':0}
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
            c = CostoStorage.objects.filter(dal__lte=elem[FIELD_DATA],al__gte=elem[FIELD_DATA],storage_level__iexact=elem['StorageLevel']).first()
            if c:
                try:
                    prepgata[elem['Prepagata']][elem['StorageLevel'].title()]['price']+= (int(elem['Size'])*c.costo)
                    prepagata[elem['Prepagata']]['All']['price']+= (int(elem['Size'])*c.costo)
                    prepagata[elem['Prepagata']]['price_']+=(int(elem['Size'])*c.costo)
                except:
                    pass
            
     
        if elem['Utente'] not in utente.keys():
            utente[elem['Utente']]={'price_':0,'size_':0}
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
            c = CostoStorage.objects.filter(dal__lte=elem[FIELD_DATA],al__gte=elem[FIELD_DATA],storage_level__iexact=elem['StorageLevel']).first()
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
            c = CostoStorage.objects.filter(dal__lte=elem[FIELD_DATA],al__gte=elem[FIELD_DATA],storage_level__iexact=elem['StorageLevel']).first()
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

