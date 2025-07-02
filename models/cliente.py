class Cliente:
    def __init__(self, id_cliente, nombre, email):
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__email = email
        self.__carrito = []

    @property
    def id_cliente(self):
        return self.__id_cliente

    @property
    def nombre(self):
        return self.__nombre

    @property
    def email(self):
        return self.__email

    @property
    def carrito(self):
        return self.__carrito.copy()

    @nombre.setter
    def nombre(self, nuevo_nombre):
        if nuevo_nombre:
            self.__nombre = nuevo_nombre.strip()

    @email.setter
    def email(self, nuevo_email):
        if nuevo_email and '@' in nuevo_email:
            self.__email = nuevo_email.strip()

    def agregar_al_carrito(self, producto_id, cantidad=1):
        for item in self.__carrito:
            if item['producto_id'] == producto_id:
                item['cantidad'] += cantidad
                return True
        self.__carrito.append({'producto_id': producto_id, 'cantidad': cantidad})
        return True

    def mostrar_carrito(self):
        return self.__carrito.copy()

    def remover_del_carrito(self, producto_id):
        for i, item in enumerate(self.__carrito):
            if item['producto_id'] == producto_id:
                del self.__carrito[i]
                return True
        return False

    def actualizar_cantidad_carrito(self, producto_id, nueva_cantidad):
        for item in self.__carrito:
            if item['producto_id'] == producto_id:
                if nueva_cantidad <= 0:
                    return self.remover_del_carrito(producto_id)
                item['cantidad'] = nueva_cantidad
                return True
        return False

    def vaciar_carrito(self):
        self.__carrito = []

    def calcular_total_productos_carrito(self):
        return sum(item['cantidad'] for item in self.__carrito)

    def to_dict(self):
        return {
            'id_cliente': self.__id_cliente,
            'nombre': self.__nombre,
            'email': self.__email,
            'carrito': self.__carrito
        }

    @classmethod
    def from_dict(cls, data):
        cliente = cls(data['id_cliente'], data['nombre'], data['email'])
        cliente._Cliente__carrito = data.get('carrito', [])
        return cliente
