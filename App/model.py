"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import config as cf
from DISClib.Algorithms.Graphs import prim as p
from math import radians, cos, sin, asin, sqrt
from DISClib.Algorithms.Graphs import dijsktra as dj
from DISClib.ADT import graph as gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newCatalog():
    catalog= {
               'connections' : None,
               'landing_points':None,
               'LP_NtoI': None,
               'components': None,
               'paths': None
             }
    
    catalog['connections_graph']=gr.newGraph(datastructure='ADJ_LIST', directed=True, size=10, comparefunction=compareOrigin)
    catalog['landing_points']=mp.newMap(maptype='PROBING', loadfactor=0.5)
    catalog['LP_NtoI']=mp.newMap(maptype='PROBING', loadfactor=0.5)
    catalog['countries']=mp.newMap(maptype='PROBING', loadfactor=0.5)
    catalog['connections']=mp.newMap(maptype='PROBING', loadfactor=0.5)

    return catalog

# Funciones para agregar informacion al catalogo

# El autor de esta funcion es Michael Dunn sacada de internet porque pip no fue funcional en mi pc
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def addConnection(catalog, con):
    origin=int(getOrigin(con))
    destination=int(getDestination(con))
    name=getName(con).lower().strip()

    addToCMAP(catalog, name, origin, destination, con)

    addLP(catalog, origin)
    addLP(catalog, destination)

    distance=getDistance(catalog,con)
    
    if distance>0:
        gr.addEdge(catalog['connections_graph'], origin, destination, distance)
        gr.addEdge(catalog['connections_directed'], origin, destination, distance)

    
    
def addCountry(catalog, country):
    c=getCountry(country).strip().lower()
    country['landing_points']=lt.newList()
    country['connections']=lt.newList()

    mp.put(catalog['countries'], c, country)


def addLandingPoint(catalog, lp):
    name=getLPname(lp)

    lp['country']=name['country']
    lp['namee']=name['name']
    name=name['name'].lower().strip()

    latlp = float(lp['latitude'])
    lonlp = float(lp['longitude'])
    
    id=int(getLPid(lp))

    mp.put(catalog['LP_NtoI'], name, id)
    mp.put(catalog['landing_points'], id, lp)
    n = lp['country']
    c = mp.get(catalog['countries'],n)

    country = me.getValue(c)
    lista = me.getValue(c)['landing_points']
    latca = float(country['CapitalLatitude'])
    lonca = float(country['CapitalLongitude'])
    distance = haversine(lonca,latca,lonlp,latlp)
    res = {}
    landing = lp['landing_point_id']
    res[landing] = {}
    res[landing]['name'] = name
    res[landing]['distance'] = distance
    lt.addLast(lista,res)





def addLP(catalog, vertex):
    if not gr.containsVertex(catalog['connections_graph'], vertex):
        gr.insertVertex(catalog['connections_graph'], vertex)
    if not gr.containsVertex(catalog['connections_directed'],vertex):
        gr.insertVertex(catalog['connections_directed'],vertex)
    return catalog

def addToCMAP(catalog, name, origin, destination, con):

    if mp.contains(catalog['connections'], name) == True:
        a=mp.get(catalog['connections'], name)
        a=me.getValue(a)

        if mp.contains(a, origin)== True:
            b=mp.get(a,origin)
            b=me.getValue(b)

            mp.put(b, destination, con) 

        else:
            b=mp.newMap(maptype='PROBING', loadfactor=0.5)
            mp.put(b, destination, con)
            mp.put(a, origin, b)

    else:
        b=mp.newMap(maptype='PROBING', loadfactor=0.5)
        mp.put(b, destination, con)
        a=mp.newMap(maptype='PROBING', loadfactor=0.5)
        mp.put(a, origin, b)
        mp.put(catalog['connections'], name, a)
        

# Funciones de consulta
def getDistance(catalog,connection):
    '''thing=connection['cable_length']
    a=thing.strip().split()
    d=a[0]
    d=d.split(',')

    if d[0]=='n.a.':
        distance=0
    
    elif len(d)>1:
        distance=d[0]+d[1]
        distance=distance.strip()
        
    
    else:
        distance=d[0]'''
    
    origin = float(getOrigin(connection))
    destination = float(getDestination(connection))
    coororigin = getcoordinates(catalog, origin)
    coordestination = getcoordinates(catalog, destination)
    distance = haversine(coororigin[1],coororigin[0],coordestination[1],coordestination[0])



    return float(distance)

def getcoordinates(catalog, d):
    l = mp.get(catalog['landing_points'],d)
    lat = float(me.getValue(l)['latitude'])
    lon = float(me.getValue(l)['longitude'])
    coordinates = (lat,lon)
    return coordinates

def getOrigin(connection):
    a=connection['\ufefforigin']
    return a

def getDestination(connection):
    a=connection['destination']
    return a

def getName(connection):
    a=connection['cable_name']
    return a

def getLPname(landing_point):
    a=landing_point['name']
    a=a.strip().lower().split(', ')
    k=len(a)-1
    b={'name':a[0], 'country':a[k]}
    return b

def getLPid(landing_point):
    a=landing_point['landing_point_id']
    return a

def getCountry(country):
    a=country['CountryName']
    return a

def reque2(catalog):
    ans={'k':0, 'DC':mp.newMap(maptype='PROBING')}
    graph=catalog['connections_graph']
    v=gr.vertices(graph)

    y=1
    while y<=lt.size(v):
        v1=lt.getElement(v, y)
        ad_v1=gr.adjacents(graph, v1)

        if lt.size(ad_v1)>1:
            a1=sumando(graph, v1, ad_v1, ans)
            lp=mp.get(catalog['landing_points'], int(v1))
            lp=me.getValue(lp)
            mp.put(ans['DC'], v1, lp)
            a2=gr.degree(graph, v1)
            ans['k']+=a2+a1
            
        y+=1
    return ans

def reque4(catalog):
    main=catalog['connections_graph'].copy()
    a=p.PrimMST(main)
    ans={'nodes':0 , 'total_km': 0 , 'largest_branch':0}
    ans['nodes']=gr.numVertices(main)
    ans['total_km']=SUMKM(mp.valueSet(a['distTo']))
    ans['largest_branch']=LB(mp.valueSet(a['edgeTo']))
    return ans

    
def reque1(catalog,lp1,lp2):

    catalog['components'] = scc.KosarajuSCC(catalog['connections_directed'])
    num = scc.connectedComponents(catalog['components'])
    set1 = mp.get(catalog['LP_NtoI'],lp1)
    id1 = me.getValue(set1)
    set2 = mp.get(catalog['LP_NtoI'],lp2)
    id2 = me.getValue(set2)
    res = scc.stronglyConnected(catalog['components'],id1,id2)
    return res,num

def reque3(catalog,paisA,paisB):
    pais1 = menor(catalog,paisA)
    pais2 = menor(catalog,paisB)
    respuesta = (pais1,pais2)

    catalog['paths'] = dj.Dijkstra(catalog['connections_directed'],pais1)
    ruta = dj.pathTo(catalog['paths'],pais2)
    distancia = dj.distTo(catalog['paths'],pais2)

    return ruta,distancia

def menor(catalog,pais):
    PA = mp.get(catalog['countries'],pais)
    infoPA = me.getValue(PA)
    capitalP1 = (infoPA['CapitalName']).lower()
    capid = mp.get(catalog['LP_NtoI'],capitalP1)
    menor = 0
    id = ''
    name = ''
    respuesta = ''
    if capid == None:
        for i in lt.iterator(infoPA['landing_points']):
            for t in i:
                if menor == 0:
                    menor = float(i[t]['distance'])
                    id = t
                    name = i[t]['name']
                if float(i[t]['distance']) < menor:
                    menor = float(i[t]['distance'])
                    id = t
                    name = i[t]['name']
        respuesta = int(id)
    else:
        respuesta = me.getValue(capid)
    

    return respuesta


# Funciones utilizadas para comparar elementos dentro de una lista
def compareOrigin(origin ,con):
    alt_origin= con['key']


    if (origin==alt_origin):
        return 0

    elif(alt_origin < origin):
        return 1
    
    else:
        return -1



# Funciones de ordenamiento
def sumando(graph, v1, ad_v1, ans):
    m=ans['DC']
    y=1
    a=0

    while y<=lt.size(ad_v1):
        sub_v=lt.getElement(ad_v1, y)
        
        if mp.contains(m, sub_v)==True:

            if gr.getEdge(graph, v1, sub_v)!=None: a+=-1
            if gr.getEdge(graph, sub_v, v1)!=None: a+=-1
        
        y+=1
    return a

def SUMKM(l):
    y=1
    k=0

    while y<=lt.size(l):
        e=lt.getElement(l,y)
        k+=e
        y+=1
    return k

def LB(l):
    y=1
    w=0
    a=None

    while y<=lt.size(l):
        e=lt.getElement(l,y)
        ew=e['weight']

        if w<ew:
            w=ew
            a=e

        y+=1
    return a