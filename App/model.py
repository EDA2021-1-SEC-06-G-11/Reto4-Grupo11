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
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.DataStructures import mapentry as me
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
               'LP_NtoI': None
             }
    
    catalog['connections_graph']=gr.newGraph(datastructure='ADJ_LIST', directed=True, size=10, comparefunction=compareOrigin)
    catalog['landing_points']=mp.newMap(maptype='PROBING', loadfactor=0.5)
    catalog['LP_NtoI']=mp.newMap(maptype='PROBING', loadfactor=0.5)
    catalog['countries']=mp.newMap(maptype='PROBING', loadfactor=0.5)
    catalog['connections']=mp.newMap(maptype='PROBING', loadfactor=0.5)
    return catalog

# Funciones para agregar informacion al catalogo
def addConnection(catalog, con):
    origin=getOrigin(con)
    destination=getDestination(con)
    name=getName(con).lower().strip()

    addToCMAP(catalog, name, origin, destination, con)

    addLP(catalog, origin)
    addLP(catalog, destination)

    distance=getDistance(con)
    
    gr.addEdge(catalog['connections_graph'], origin, destination, distance)

def addCountry(catalog, country):
    c=getCountry(country).strip().lower()
    country['landing_points']=lt.newList()
    country['connections']=lt.newList()

    mp.put(catalog['countries'], c, country)


def addLandingPoint(catalog, lp):
    name=getLPname(lp)
    name=name['name'].lower().strip()
    id=int(getLPid(lp))

    mp.put(catalog['LP_NtoI'], name, id)
    mp.put(catalog['landing_points'], id, lp)


def addLP(catalog, vertex):
    if not gr.containsVertex(catalog['connections_graph'], vertex):
        gr.insertVertex(catalog['connections_graph'], vertex)
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
def getDistance(connection):
    thing=connection['cable_length']
    a=thing.strip().split()
    distance=a[0]

    return distance

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
    a=a.strip().lower().split()
    k=len(a)-1
    b={'name':a[0], 'country':a[k]}
    return b

def getLPid(landing_point):
    a=landing_point['landing_point_id']
    return a

def getCountry(country):
    a=country['CountryName']
    return a


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
