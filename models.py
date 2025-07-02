
# models.py - Clases principales del sistema
import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class Producto:
    """Clase que representa un producto de la ferretería"""
    
    def __init__(self, id_producto: int, nombre: str, precio: float, stock: int):
        # Atributos privados (encapsulamiento)
        self.__id_producto = id_producto
        self.__nombre = nombre
        self.__precio = precio
        self.__stock = stock
    
    # Métodos públicos - Getters (acceso controlado a atributos privados)
    @property
    def id_producto(self) -> int:
        return self.__id_producto
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @property
    def precio(self) -> float:
        return self.__precio
    
    @property
    def stock(self) -> int:
        return self.__stock
    
    # Métodos públicos - Setters (modificación controlada)
    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        if nuevo_nombre and nuevo_nombre.strip():
            self.__nombre = nuevo_nombre.strip()
    
    @precio.setter
    def precio(self, nuevo_precio: float):
        if nuevo_precio >= 0:
            self.__precio = nuevo_precio
    
    # Método público requerido por las premisas
    def actualizar_stock(self, cantidad: int) -> bool:
        """Actualiza el stock del producto (+ para agregar, - para quitar)"""
        if self.__stock + cantidad >= 0:
            self.__stock += cantidad
            return True
        return False
    
    # Método público requerido por las premisas
    def mostrar_informacion(self) -> Dict:
        """Retorna la información completa del producto"""
        return {
            'id_producto': self.__id_producto,
            'nombre': self.__nombre,
            'precio': self.__precio,
            'stock': self.__stock
        }
    
    # Métodos públicos adicionales para funcionalidad
    def tiene_stock_suficiente(self, cantidad: int) -> bool:
        """Verifica si hay stock suficiente para una cantidad dada"""
        return self.__stock >= cantidad
    
    def to_dict(self) -> Dict:
        """Convierte el producto a diccionario para persistencia"""
        return self.mostrar_informacion()
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Crea una instancia de Producto desde un diccionario"""
        return cls(
            data['id_producto'],
            data['nombre'],
            data['precio'],
            data['stock']
        )


class Cliente:
    """Clase que representa un cliente de la ferretería"""
    
    def __init__(self, id_cliente: int, nombre: str, email: str):
        # Atributos privados (encapsulamiento)
        self.__id_cliente = id_cliente
        self.__nombre = nombre
        self.__email = email
        self.__carrito = []  # Lista de productos (como especifica las premisas)
    
    # Métodos públicos - Getters
    @property
    def id_cliente(self) -> int:
        return self.__id_cliente
    
    @property
    def nombre(self) -> str:
        return self.__nombre
    
    @property
    def email(self) -> str:
        return self.__email
    
    @property
    def carrito(self) -> List:
        return self.__carrito.copy()  # Retorna copia para mantener encapsulamiento
    
    # Métodos públicos - Setters
    @nombre.setter
    def nombre(self, nuevo_nombre: str):
        if nuevo_nombre and nuevo_nombre.strip():
            self.__nombre = nuevo_nombre.strip()
    
    @email.setter
    def email(self, nuevo_email: str):
        if nuevo_email and '@' in nuevo_email:
            self.__email = nuevo_email.strip()
    
    # Método público requerido por las premisas
    def agregar_al_carrito(self, producto_id: int, cantidad: int = 1) -> bool:
        """Agrega un producto al carrito del cliente"""
        # Verificar si el producto ya está en el carrito
        for item in self.__carrito:
            if item['producto_id'] == producto_id:
                item['cantidad'] += cantidad
                return True
        
        # Si no está, agregarlo como nuevo item
        self.__carrito.append({
            'producto_id': producto_id,
            'cantidad': cantidad
        })
        return True
    
    # Método público requerido por las premisas
    def mostrar_carrito(self) -> List:
        """Retorna el contenido actual del carrito"""
        return self.__carrito.copy()
    
    # Métodos públicos adicionales para funcionalidad completa
    def remover_del_carrito(self, producto_id: int) -> bool:
        """Remueve un producto específico del carrito"""
        for i, item in enumerate(self.__carrito):
            if item['producto_id'] == producto_id:
                del self.__carrito[i]
                return True
        return False
    
    def actualizar_cantidad_carrito(self, producto_id: int, nueva_cantidad: int) -> bool:
        """Actualiza la cantidad de un producto en el carrito"""
        for item in self.__carrito:
            if item['producto_id'] == producto_id:
                if nueva_cantidad <= 0:
                    return self.remover_del_carrito(producto_id)
                item['cantidad'] = nueva_cantidad
                return True
        return False
    
    def vaciar_carrito(self):
        """Vacía completamente el carrito del cliente"""
        self.__carrito = []
    
    def calcular_total_productos_carrito(self) -> int:
        """Calcula el total de productos en el carrito"""
        return sum(item['cantidad'] for item in self.__carrito)
    
    def to_dict(self) -> Dict:
        """Convierte el cliente a diccionario para persistencia"""
        return {
            'id_cliente': self.__id_cliente,
            'nombre': self.__nombre,
            'email': self.__email,
            'carrito': self.__carrito
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Crea una instancia de Cliente desde un diccionario"""
        cliente = cls(
            data['id_cliente'],
            data['nombre'],
            data['email']
        )
        # Acceso directo al atributo privado para cargar datos
        cliente._Cliente__carrito = data.get('carrito', [])
        return cliente


class Tienda:
    """Clase principal que maneja toda la ferretería Ferretec"""
    
    def __init__(self):
        # Atributos privados (encapsulamiento)
        self.__lista_productos = []  # Requerido por premisas
        self.__lista_clientes = []   # Requerido por premisas
        self.__archivo_productos = 'data/productos.txt'
        self.__archivo_clientes = 'data/clientes.txt'
        self.__archivo_ventas = 'data/ventas.txt'
        self.__proximo_id_producto = 1
        self.__proximo_id_cliente = 1
        
        # Crear directorio de datos si no existe
        self.__crear_directorio_datos()
        # Cargar datos existentes al inicializar
        self.__cargar_todos_los_datos()
    
    # Métodos privados (solo para uso interno de la clase)
    def __crear_directorio_datos(self):
        """Método privado para crear el directorio de datos"""
        if not os.path.exists('data'):
            os.makedirs('data')
    
    def __cargar_todos_los_datos(self):
        """Método privado para cargar todos los datos desde archivos"""
        self.__cargar_productos_desde_archivo()
        self.__cargar_clientes_desde_archivo()
    
    def __cargar_productos_desde_archivo(self):
        """Método privado para cargar productos desde archivo txt"""
        try:
            if os.path.exists(self.__archivo_productos):
                with open(self.__archivo_productos, 'r', encoding='utf-8') as file:
                    for line in file:
                        if line.strip():
                            data = json.loads(line.strip())
                            producto = Producto.from_dict(data)
                            self.__lista_productos.append(producto)
                            # Actualizar próximo ID
                            if producto.id_producto >= self.__proximo_id_producto:
                                self.__proximo_id_producto = producto.id_producto + 1
        except Exception as e:
            print(f"Error al cargar productos: {e}")
    
    def __cargar_clientes_desde_archivo(self):
        """Método privado para cargar clientes desde archivo txt"""
        try:
            if os.path.exists(self.__archivo_clientes):
                with open(self.__archivo_clientes, 'r', encoding='utf-8') as file:
                    for line in file:
                        if line.strip():
                            data = json.loads(line.strip())
                            cliente = Cliente.from_dict(data)
                            self.__lista_clientes.append(cliente)
                            # Actualizar próximo ID
                            if cliente.id_cliente >= self.__proximo_id_cliente:
                                self.__proximo_id_cliente = cliente.id_cliente + 1
        except Exception as e:
            print(f"Error al cargar clientes: {e}")
    
    def __guardar_productos_en_archivo(self):
        """Método privado para guardar productos en archivo txt"""
        try:
            with open(self.__archivo_productos, 'w', encoding='utf-8') as file:
                for producto in self.__lista_productos:
                    file.write(json.dumps(producto.to_dict(), ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Error al guardar productos: {e}")
    
    def __guardar_clientes_en_archivo(self):
        """Método privado para guardar clientes en archivo txt"""
        try:
            with open(self.__archivo_clientes, 'w', encoding='utf-8') as file:
                for cliente in self.__lista_clientes:
                    file.write(json.dumps(cliente.to_dict(), ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Error al guardar clientes: {e}")
    
    def __guardar_venta_en_archivo(self, venta: Dict):
        """Método privado para guardar una venta en archivo txt"""
        try:
            with open(self.__archivo_ventas, 'a', encoding='utf-8') as file:
                file.write(json.dumps(venta, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"Error al guardar venta: {e}")
    
    def __buscar_producto_por_id(self, id_producto: int) -> Optional[Producto]:
        """Método privado para buscar un producto por ID"""
        for producto in self.__lista_productos:
            if producto.id_producto == id_producto:
                return producto
        return None
    
    def __buscar_cliente_por_id(self, id_cliente: int) -> Optional[Cliente]:
        """Método privado para buscar un cliente por ID"""
        for cliente in self.__lista_clientes:
            if cliente.id_cliente == id_cliente:
                return cliente
        return None
    
    def __validar_stock_carrito(self, cliente: Cliente) -> Dict:
        """Método privado para validar el stock de todos los productos en el carrito"""
        productos_compra = []
        total = 0
        
        for item in cliente.mostrar_carrito():
            producto = self.__buscar_producto_por_id(item['producto_id'])
            if not producto:
                return {'success': False, 'message': f'Producto con ID {item["producto_id"]} no encontrado'}
            
            if not producto.tiene_stock_suficiente(item['cantidad']):
                return {'success': False, 'message': f'Stock insuficiente para {producto.nombre}'}
            
            subtotal = producto.precio * item['cantidad']
            productos_compra.append({
                'producto': producto.mostrar_informacion(),
                'cantidad': item['cantidad'],
                'subtotal': subtotal
            })
            total += subtotal
        
        return {'success': True, 'productos_compra': productos_compra, 'total': total}
    
    def __aplicar_descuento(self, total: float, total_productos: int) -> Dict:
        """Método privado para aplicar descuentos según las reglas de negocio"""
        descuento = 0
        if total_productos > 5:  # Descuento del 10% si compra más de 5 productos
            descuento = total * 0.1
        
        return {
            'subtotal': total,
            'descuento': descuento,
            'total_final': total - descuento
        }
    
    # Métodos públicos requeridos por las premisas
    def registrar_producto(self, nombre: str, precio: float, stock: int) -> Dict:
        """Método público requerido: registra un nuevo producto en la ferretería"""
        # Validaciones
        if not nombre or not nombre.strip():
            return {'success': False, 'message': 'El nombre del producto es requerido'}
        
        if precio < 0:
            return {'success': False, 'message': 'El precio no puede ser negativo'}
        
        if stock < 0:
            return {'success': False, 'message': 'El stock no puede ser negativo'}
        
        # Verificar si el producto ya existe (evitar duplicados)
        for producto in self.__lista_productos:
            if producto.nombre.lower() == nombre.lower().strip():
                return {'success': False, 'message': 'Ya existe un producto con ese nombre'}
        
        # Crear nuevo producto
        nuevo_producto = Producto(self.__proximo_id_producto, nombre.strip(), precio, stock)
        self.__lista_productos.append(nuevo_producto)
        self.__proximo_id_producto += 1
        
        # Persistir en archivo
        self.__guardar_productos_en_archivo()
        
        return {
            'success': True,
            'message': 'Producto registrado exitosamente',
            'producto': nuevo_producto.mostrar_informacion()
        }
    
    def registrar_cliente(self, nombre: str, email: str) -> Dict:
        """Método público requerido: registra un nuevo cliente"""
        # Validaciones
        if not nombre or not nombre.strip():
            return {'success': False, 'message': 'El nombre del cliente es requerido'}
        
        if not email or not email.strip() or '@' not in email:
            return {'success': False, 'message': 'Email válido es requerido'}
        
        # Verificar si el email ya existe
        for cliente in self.__lista_clientes:
            if cliente.email.lower() == email.lower().strip():
                return {'success': False, 'message': 'Ya existe un cliente con ese email'}
        
        # Crear nuevo cliente
        nuevo_cliente = Cliente(self.__proximo_id_cliente, nombre.strip(), email.strip())
        self.__lista_clientes.append(nuevo_cliente)
        self.__proximo_id_cliente += 1
        
        # Persistir en archivo
        self.__guardar_clientes_en_archivo()
        
        return {
            'success': True,
            'message': 'Cliente registrado exitosamente',
            'cliente': nuevo_cliente.to_dict()
        }
    
    def realizar_compra(self, cliente_id: int) -> Dict:
        """Método público requerido: procesa la compra de un cliente"""
        # Buscar cliente
        cliente = self.__buscar_cliente_por_id(cliente_id)
        if not cliente:
            return {'success': False, 'message': 'Cliente no encontrado'}
        
        # Verificar que el carrito no esté vacío
        carrito = cliente.mostrar_carrito()
        if not carrito:
            return {'success': False, 'message': 'El carrito está vacío'}
        
        # Validar stock para todos los productos
        validacion = self.__validar_stock_carrito(cliente)
        if not validacion['success']:
            return validacion
        
        productos_compra = validacion['productos_compra']
        total_productos = cliente.calcular_total_productos_carrito()
        
        # Aplicar descuentos
        descuentos = self.__aplicar_descuento(validacion['total'], total_productos)
        
        # Descontar stock de productos
        for item in carrito:
            producto = self.__buscar_producto_por_id(item['producto_id'])
            producto.actualizar_stock(-item['cantidad'])  # Usar método de la clase Producto
        
        # Crear registro de venta
        venta = {
            'cliente_id': cliente_id,
            'cliente_nombre': cliente.nombre,
            'cliente_email': cliente.email,
            'productos': productos_compra,
            'total_productos': total_productos,
            'subtotal': descuentos['subtotal'],
            'descuento': descuentos['descuento'],
            'total_final': descuentos['total_final'],
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Vaciar carrito del cliente
        cliente.vaciar_carrito()
        
        # Persistir cambios
        self.__guardar_venta_en_archivo(venta)
        self.__guardar_productos_en_archivo()  # Actualizar stock
        self.__guardar_clientes_en_archivo()   # Vaciar carrito
        
        return {
            'success': True,
            'message': 'Compra realizada exitosamente',
            'venta': venta
        }
    
    def mostrar_productos(self) -> List[Dict]:
        """Método público requerido: retorna todos los productos disponibles"""
        return [producto.mostrar_informacion() for producto in self.__lista_productos]
    
    def mostrar_clientes(self) -> List[Dict]:
        """Método público requerido: retorna todos los clientes registrados"""
        return [cliente.to_dict() for cliente in self.__lista_clientes]
    
    # Métodos públicos adicionales para funcionalidad completa
    def agregar_producto_a_carrito_cliente(self, cliente_id: int, producto_id: int, cantidad: int = 1) -> Dict:
        """Método público para agregar producto al carrito de un cliente"""
        # Buscar cliente
        cliente = self.__buscar_cliente_por_id(cliente_id)
        if not cliente:
            return {'success': False, 'message': 'Cliente no encontrado'}
        
        # Buscar producto
        producto = self.__buscar_producto_por_id(producto_id)
        if not producto:
            return {'success': False, 'message': 'Producto no encontrado'}
        
        # Validar stock disponible
        if not producto.tiene_stock_suficiente(cantidad):
            return {'success': False, 'message': f'Stock insuficiente. Disponible: {producto.stock}'}
        
        # Agregar al carrito usando método de la clase Cliente
        cliente.agregar_al_carrito(producto_id, cantidad)
        
        # Persistir cambios
        self.__guardar_clientes_en_archivo()
        
        return {'success': True, 'message': 'Producto agregado al carrito exitosamente'}
    
    def obtener_carrito_detallado_cliente(self, cliente_id: int) -> Dict:
        """Método público para obtener el carrito de un cliente con detalles de productos"""
        cliente = self.__buscar_cliente_por_id(cliente_id)
        if not cliente:
            return {'success': False, 'message': 'Cliente no encontrado'}
        
        carrito = cliente.mostrar_carrito()
        carrito_detallado = []
        total = 0
        
        for item in carrito:
            producto = self.__buscar_producto_por_id(item['producto_id'])
            if producto:
                subtotal = producto.precio * item['cantidad']
                carrito_detallado.append({
                    'producto': producto.mostrar_informacion(),
                    'cantidad': item['cantidad'],
                    'subtotal': subtotal
                })
                total += subtotal
        
        return {
            'success': True,
            'cliente': cliente.to_dict(),
            'carrito': carrito_detallado,
            'total': total,
            'total_productos': cliente.calcular_total_productos_carrito()
        }
    
    def actualizar_carrito_cliente(self, cliente_id: int, producto_id: int, nueva_cantidad: int) -> Dict:
        """Método público para actualizar cantidad de producto en carrito"""
        cliente = self.__buscar_cliente_por_id(cliente_id)
        if not cliente:
            return {'success': False, 'message': 'Cliente no encontrado'}
        
        if nueva_cantidad <= 0:
            cliente.remover_del_carrito(producto_id)
            mensaje = 'Producto removido del carrito'
        else:
            # Verificar stock disponible
            producto = self.__buscar_producto_por_id(producto_id)
            if producto and not producto.tiene_stock_suficiente(nueva_cantidad):
                return {'success': False, 'message': f'Stock insuficiente. Disponible: {producto.stock}'}
            
            cliente.actualizar_cantidad_carrito(producto_id, nueva_cantidad)
            mensaje = 'Cantidad actualizada en el carrito'
        
        # Persistir cambios
        self.__guardar_clientes_en_archivo()
        
        return {'success': True, 'message': mensaje}