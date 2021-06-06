"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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

import config as cf
import sys
import controller
import model
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.ADT import list as lt
from DISClib.ADT import stack
from DISClib.DataStructures import mapentry as me
assert cf
default_limit = 10000
sys.setrecursionlimit(default_limit*10) 


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
line='-----------------------------------------------------'


def p_rq1(lp1,lp2,res):
    print('El numero total de clústeres presentes en la red es: ',res[1])
    if res[0] == True:
        print('Los landing points {0} y {1} estan conectados.'.format(lp1,lp2))
    else:
        print('Los landing points {0} y {1} no estan conectados.'.format(lp1,lp2))
    print('-----------------------------------------------')


def p_rq2(ans):
    print(line)
    main=mp.valueSet(ans['DC'])
    print('Se encontraron {0} landing points que sirven de interconexion para {1} cables'.format(lt.size(main), ans['k'])) 
    y=1

    while y<=lt.size(main):
        a=lt.getElement(main, y)
        print('Nombre: {0} || País: {1} || ID: {2}'
        .format(a['namee'], a['country'], a['landing_point_id']))

        y+=1
    print(line)

def p_rq3(res):
    print('El camino es de longitud: ',res[1])
    if res[0] is not None:
        while (not stack.isEmpty(res[0])):
            value = stack.pop(res[0])
            print(value)
    else:
        print('No hay camino')
    print('---------------------------------------------------------------------------')


def p_rq4(ans):
    print(line)
    print('Se encontraron {0} nodos,  ')

def p_rq5(ans):
    print('El numero de paises que se ven afectados es: ') 
    countries = []
    num = 0
    for i in lt.iterator(ans):
        if i not in countries:
            countries.append(i)
            num += 1
    print('El numero de paises afectados es: ', num)
    print('La lista de paises es: ', end='')
    for j in countries:
        print(j,', ',end='')
    print('')
    print('-----------------------------------------------------')
        

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Requerimiento 1- Landing points en el mismo clúster")
    print('3- Requerimiento 2- Landing points interconectados')
    print('4- Requerimiento 3- Ruta minima de un landing point a otro')
    print('5- Requerimiento 4- Evaluación de infraestructura crítica')
    print('6- Requerimiento 5- Impacto de fallo de un landing point')
    print(line)

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs[0]) == 1:
        print("Cargando información de los archivos ....")
        catalog=controller.init()
        
        print(line)
        print('Se cargaron: {0} Landing points, {1} Conexiones, {2} Paises'
        .format(gr.numVertices(catalog['connections_graph']), gr.numEdges(catalog['connections_graph']), lt.size(mp.keySet(catalog['countries']))))
        
        print('Informacion del primer landing point: ')
        a=mp.valueSet(catalog['landing_points'])
        a=lt.getElement(a, 1)
        print('ID: {0} || Nombre: {1} || Latitud: {2} || Longitud: {3}'
        .format(a['landing_point_id'], a['namee'], a['latitude'], a['longitude']))

        print('Información del último país: ')
        a=mp.valueSet(catalog['countries'])
        k=lt.size(a)
        a=lt.getElement(a,k)
        print('Pais: {0} || Población: {1} || Usuarios de internet {2}'
        .format(a['CountryName'], a['Population'], a['Internet users']))

    elif int(inputs[0]) == 2:
        lp1 = input('Escriba el primer landing point: ')
        lp2 = input('Escriba el segundo landing point: ')
        respuesta = controller.reque1(catalog,lp1,lp2)
        print('--------------------------------------')
        p_rq1(lp1,lp2,respuesta)

    elif int(inputs[0]) == 3:
        print('Calculando interconexión de landing points... ')
        ans=controller.reque2(catalog)
        p_rq2(ans)

    elif int(inputs[0]) == 4:
        paisA = input('Por favor digite el primer pais: ')
        paisB = input('Por favor digite el segundo pais: ')
        respuesta = controller.reque3(catalog,paisA,paisB)
        p_rq3(respuesta)
        
    
    elif int(inputs[0]) == 5:
        print('Calculando red de expasión minima... ')
        ans=controller.reque4(catalog)
        p_rq4(ans)

    elif int(inputs[0]) == 6:
        lp= str(input('Escriba el landing point que le interesa: '))
        ans=controller.reque5(catalog, lp)
        p_rq5(ans)



    else:
        sys.exit(0)
sys.exit(0)
