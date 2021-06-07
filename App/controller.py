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
 """

from ipapi.ipapi import location
import config as cf
import model
import csv
import ipapi as ip


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

def init():
    catalog=model.newCatalog()
    loadData(catalog)
    return catalog

# Funciones para la carga de datos
def loadData(catalog):
    loadCountries(catalog)
    loadLandingPoints(catalog)
    loadConnections(catalog)


def loadConnections(catalog):
    c_file= cf.data_dir + 'connections.csv'
    input_file= csv.DictReader(open(c_file, encoding='utf-8'))

    for con in input_file:
        model.addConnection(catalog, con)

def loadCountries(catalog):
    c_file= cf.data_dir + 'countries.csv'
    input_file= csv.DictReader(open(c_file, encoding='utf-8'))
    
    for country in input_file:
        model.addCountry(catalog, country)

def loadLandingPoints(catalog):
    lp_file= cf.data_dir + 'landing_points.csv'
    input_file= csv.DictReader(open(lp_file, encoding='utf-8'))

    for lp in input_file:
        model.addLandingPoint(catalog, lp)


# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def reque1(catalog,lp1,lp2):
    ans = model.reque1(catalog,lp1,lp2)
    return ans

def reque2(catalog):
    ans=model.reque2(catalog)
    return ans

def reque3(catalog,paisA,paisB):
    
    ans = model.reque3(catalog,paisA,paisB)
    return ans
    
def reque4(catalog):
    ans=model.reque4(catalog)
    return ans

def reque5(catalog, lp):
    ans=model.reque5(catalog, lp)
    return ans

def reque7(catalog, ip1, ip2):
    l1=ip.location(ip1)
    l2=ip-location(ip2)
    ans=model.reque7(catalog, l1, l2)