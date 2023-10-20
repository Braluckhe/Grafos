class Aeropuerto:
    def __init__(self, codigo, nombre, ciudad, pais, latitud, longitud):
        self.codigo = codigo
        self.nombre = nombre
        self.ciudad = ciudad
        self.pais = pais
        self.latitud = latitud
        self.longitud = longitud
    def str(self):
        return f"Código: {self.codigo} Nombre: {self.nombre} Ciudad: {self.ciudad} País: {self.pais} Latitud: {self.latitud} Longitud: {self.longitud} \n ___________"

    def to_dict(self):
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "ciudad": self.ciudad,
            "pais": self.pais,
            "latitud": self.latitud,
            "longitud": self.longitud,
            "busq": self.codigo +" - "+ self.nombre +" - "+ self.ciudad +" - "+self.pais
        }
    def obtener_codigo(self):
        return self.codigo
