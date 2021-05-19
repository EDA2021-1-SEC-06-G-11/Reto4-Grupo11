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
               
             }
    
    catalog['connections']=gr.newGraph(datastructure='ADJ_LIST', directed=True, size=10, comparefunction=compareOrigin)

    return catalog

# Funciones para agregar informacion al catalogo
def addConnection(catalog, con):
    origin=getOrigin(con)
    destination=getDestination(con)
    
    addLP(catalog, origin)
    addLP(catalog, destination)

    distance=getDistance(con)
    
    gr.addEdge(catalog['connections'], origin, destination, distance)


def addLP(catalog, vertex):
    if not gr.containsVertex(catalog['connections'], vertex):
        gr.insertVertex(catalog['connections'], vertex)
    return catalog

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
