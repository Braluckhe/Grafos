import heapq
from Utils import haversine

class Grafo:
    def __init__(self):
        self.vertices = {}  # Usaremos un diccionario para almacenar los vértices
        self.aristas = {}  # Usaremos un diccionario para almacenar las aristas y sus pesos

    def agregar_vertice(self, aeropuerto):
        self.vertices[aeropuerto] = aeropuerto
        self.aristas[aeropuerto] = {}  # Crea un diccionario vacío para las aristas de este vértice

    def agregar_arista(self, aeropuerto1, aeropuerto2):
        peso = haversine(aeropuerto1.latitud, aeropuerto1.longitud, aeropuerto2.latitud, aeropuerto2.longitud)
        self.aristas[aeropuerto1.codigo][aeropuerto2.codigo] = peso
        self.aristas[aeropuerto2.codigo][aeropuerto1.codigo] = peso

    def obtener_vertice_por_codigo(self, codigo_aeropuerto):
        if codigo_aeropuerto in self.vertices:
            return self.vertices[codigo_aeropuerto]
        else:
            return None

    def obtener_vertices(self):
        return list(self.vertices.values())

    def obtener_aristas(self):
        return self.aristas

    def dijkstra(self, inicio):
        distancia = {v: float('inf') for v in self.vertices}
        distancia[inicio] = 0
        cola = [(0, inicio)]
        while cola:
            distancia_actual, vertice_actual = heapq.heappop(cola)

            if distancia_actual > distancia[vertice_actual]:
                continue

            for vecino, peso in self.aristas[vertice_actual].items():
                distancia_total = distancia_actual + peso
                if distancia_total < distancia[vecino]:
                    distancia[vecino] = distancia_total
                    heapq.heappush(cola, (distancia_total, vecino))
        return distancia

    def camino_minimo(self, origen, destino):
        distancias = self.dijkstra(origen)

        # Verificar si el destino es alcanzable desde el origen
        if destino not in distancias:
            return None  # No hay un camino

        # Reconstruir el camino mínimo
        camino = []
        actual = destino
        while actual != origen:
            camino.insert(0, self.obtener_vertice_por_codigo(actual))
            actual = min(self.aristas[actual], key=lambda vecino: distancias.get(vecino, float('inf')))
        
        camino.insert(0, origen)
        return camino