import math

def haversine(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en kilómetros
    radius = 6371

    # Diferencia de latitud y longitud en radianes
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    # Fórmula de Haversine
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # Distancia en kilómetros
    distance = radius * c

    return distance