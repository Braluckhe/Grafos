import json
import eel
import pandas as pd

from Aeropuertos import Aeropuerto
from Grafo import Grafo
from Utils import haversine
#cargar csv
data = pd.read_csv('flights_final.csv')


#poblacion de datos y creacion de grafos
aeropuertos = []  # La lista original de aeropuertos
aeropuertos_set = set()  # Un conjunto para mantener un registro de códigos de aeropuerto únicos
grafo = Grafo()
for _, row in data.iterrows():
    source_aeropuerto = Aeropuerto(row["Source Airport Code"], row["Source Airport Name"], row["Source Airport City"], row["Source Airport Country"], row["Source Airport Latitude"], row["Source Airport Longitude"])
    destination_aeropuerto = Aeropuerto(row["Destination Airport Code"], row["Destination Airport Name"], row["Destination Airport City"], row["Destination Airport Country"], row["Destination Airport Latitude"], row["Destination Airport Longitude"])
    # Verificar si el código de aeropuerto ya está en el conjunto
    if source_aeropuerto.codigo not in aeropuertos_set:
        aeropuertos.append(source_aeropuerto)
        aeropuertos_set.add(source_aeropuerto.codigo)
        grafo.agregar_vertice(source_aeropuerto.codigo)
    if destination_aeropuerto.codigo not in aeropuertos_set:
        aeropuertos.append(destination_aeropuerto)
        aeropuertos_set.add(destination_aeropuerto.codigo)
        grafo.agregar_vertice(destination_aeropuerto.codigo)
    grafo.agregar_arista(source_aeropuerto,destination_aeropuerto)
aeropuertos_data = [a.to_dict() for a in aeropuertos]
json_aeropuertos = json.dumps(aeropuertos_data)

def buscar_aeropuerto_por_codigo(lista_aeropuertos, codigo_buscar):
    aeropuerto_encontrado = next((aeropuerto for aeropuerto in lista_aeropuertos if aeropuerto.obtener_codigo() == codigo_buscar), None)
    return aeropuerto_encontrado

@eel.expose
def initdatos():
    global json_aeropuertos
    eel.setMarkers(json_aeropuertos)
@eel.expose
def caminoMinimo(origen, destino):
    aeropuerto_origen = grafo.obtener_vertice_por_codigo(str(origen))
    aeropuerto_destino = grafo.obtener_vertice_por_codigo(str(destino))
    resultados = []
    if aeropuerto_origen and aeropuerto_destino:
        camino = grafo.camino_minimo(aeropuerto_origen, aeropuerto_destino)
        if camino:
            for aeropuerto in camino:
                info = buscar_aeropuerto_por_codigo(aeropuertos,aeropuerto)
                resultados.append({"aeropuerto": info.to_dict()})
        else:
            print("No hay un camino entre los dos aeropuertos.")
    else:
        print("Aeropuertos de origen o destino no encontrados.")
    eel.mostrarMin(json.dumps(resultados))
@eel.expose
def masLejanos(cod_origen):
    global aeropuertos
    origen = grafo.obtener_vertice_por_codigo(str(cod_origen))
    distancias = grafo.dijkstra(origen)
    aeropuertos_ordenados = sorted(distancias.items(), key=lambda x: x[1], reverse=True)
    aeropuertos_lejanos = []
    origen = buscar_aeropuerto_por_codigo(aeropuertos, str(cod_origen))
    
    for aeropuerto, distancia in aeropuertos_ordenados:
        if aeropuerto != origen.nombre:
            info = buscar_aeropuerto_por_codigo(aeropuertos,aeropuerto)
            aeropuertos_lejanos.append({"aeropuerto": info.to_dict(), "distancia": haversine(origen.latitud, origen.longitud, info.latitud, info.longitud)})
    
    # Tomar los primeros n aeropuertos
    aeropuertos_lejanos = aeropuertos_lejanos[:10]
    
    # Convertir la lista de resultados en un JSON
    aeropuertos_lejanos_json = json.dumps(aeropuertos_lejanos)
    eel.mostrarLejanos(aeropuertos_lejanos_json)
# Inicializar UI
eel.init('ui')
eel.start('index.html')

