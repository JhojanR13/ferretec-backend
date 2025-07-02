class Producto:
    def __init__(self, id_producto, nombre, precio, stock):
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__precio = precio
        self.__stock = stock

    @property
    def id_producto(self):
        return self.__id_producto

    @property
    def nombre(self):
        return self.__nombre

    @property
    def precio(self):
        return self.__precio

    @property
    def stock(self):
        return self.__stock

    @nombre.setter
    def nombre(self, nuevo_nombre):
        if nuevo_nombre:
            self.__nombre = nuevo_nombre.strip()

    @precio.setter
    def precio(self, nuevo_precio):
        if nuevo_precio >= 0:
            self.__precio = nuevo_precio

    def actualizar_stock(self, cantidad):
        if self.__stock + cantidad >= 0:
            self.__stock += cantidad
            return True
        return False

    def tiene_stock_suficiente(self, cantidad):
        return self.__stock >= cantidad

    def mostrar_informacion(self):
        return {
            'id_producto': self.__id_producto,
            'nombre': self.__nombre,
            'precio': self.__precio,
            'stock': self.__stock
        }

    def to_dict(self):
        return self.mostrar_informacion()

    @classmethod
    def from_dict(cls, data):
        return cls(
            data['id_producto'],
            data['nombre'],
            data['precio'],
            data['stock']
        )
