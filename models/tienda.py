import json
import os
from datetime import datetime
from models.producto import Producto
from models.cliente import Cliente

class Tienda:
    def __init__(self):
        self.__lista_productos = []
        self.__lista_clientes = []
        self.__archivo_productos = 'data/productos.txt'
        self.__archivo_clientes = 'data/clientes.txt'
        self.__archivo_ventas = 'data/ventas.txt'
        self.__proximo_id_producto = 1
        self.__proximo_id_cliente = 1

        self.__crear_directorio_datos()
        self.__cargar_todos_los_datos()

    def __crear_directorio_datos(self):
        if not os.path.exists('data'):
            os.makedirs('data')

    def __cargar_todos_los_datos(self):
        self.__cargar_productos_desde_archivo()
        self.__cargar_clientes_desde_archivo()

    def __cargar_productos_desde_archivo(self):
        if os.path.exists(self.__archivo_productos):
            with open(self.__archivo_productos, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        prod = Producto.from_dict(json.loads(line))
                        self.__lista_productos.append(prod)
                        self.__proximo_id_producto = max(self.__proximo_id_producto, prod.id_producto + 1)

    def __cargar_clientes_desde_archivo(self):
        if os.path.exists(self.__archivo_clientes):
            with open(self.__archivo_clientes, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        cli = Cliente.from_dict(json.loads(line))
                        self.__lista_clientes.append(cli)
                        self.__proximo_id_cliente = max(self.__proximo_id_cliente, cli.id_cliente + 1)

    def __guardar_productos_en_archivo(self):
        with open(self.__archivo_productos, 'w', encoding='utf-8') as f:
            for p in self.__lista_productos:
                f.write(json.dumps(p.to_dict()) + '\n')

    def __guardar_clientes_en_archivo(self):
        with open(self.__archivo_clientes, 'w', encoding='utf-8') as f:
            for c in self.__lista_clientes:
                f.write(json.dumps(c.to_dict()) + '\n')

    def __guardar_venta_en_archivo(self, venta):
        with open(self.__archivo_ventas, 'a', encoding='utf-8') as f:
            f.write(json.dumps(venta) + '\n')

    def __buscar_producto_por_id(self, id_producto):
        return next((p for p in self.__lista_productos if p.id_producto == id_producto), None)

    def __buscar_cliente_por_id(self, id_cliente):
        return next((c for c in self.__lista_clientes if c.id_cliente == id_cliente), None)

    def registrar_producto(self, nombre, precio, stock):
        if not nombre.strip() or precio < 0 or stock < 0:
            return {'success': False, 'message': 'Datos inválidos'}
        if any(p.nombre.lower() == nombre.lower().strip() for p in self.__lista_productos):
            return {'success': False, 'message': 'Ya existe un producto con ese nombre'}

        nuevo = Producto(self.__proximo_id_producto, nombre.strip(), precio, stock)
        self.__lista_productos.append(nuevo)
        self.__proximo_id_producto += 1
        self.__guardar_productos_en_archivo()
        return {'success': True, 'producto': nuevo.to_dict()}

    def registrar_cliente(self, nombre, email):
        if not nombre.strip() or '@' not in email:
            return {'success': False, 'message': 'Datos inválidos'}
        if any(c.email.lower() == email.lower().strip() for c in self.__lista_clientes):
            return {'success': False, 'message': 'Email ya registrado'}

        nuevo = Cliente(self.__proximo_id_cliente, nombre.strip(), email.strip())
        self.__lista_clientes.append(nuevo)
        self.__proximo_id_cliente += 1
        self.__guardar_clientes_en_archivo()
        return {'success': True, 'cliente': nuevo.to_dict()}

    def mostrar_productos(self):
        return [p.to_dict() for p in self.__lista_productos]

    def mostrar_clientes(self):
        return [c.to_dict() for c in self.__lista_clientes]

    def agregar_producto_a_carrito_cliente(self, cliente_id, producto_id, cantidad=1):
        cliente = self.__buscar_cliente_por_id(cliente_id)
        producto = self.__buscar_producto_por_id(producto_id)
        if not cliente or not producto:
            return {'success': False, 'message': 'Cliente o producto no encontrado'}
        if not producto.tiene_stock_suficiente(cantidad):
            return {'success': False, 'message': 'Stock insuficiente'}
        cliente.agregar_al_carrito(producto_id, cantidad)
        self.__guardar_clientes_en_archivo()
        return {'success': True, 'message': 'Producto agregado'}

    def obtener_carrito_detallado_cliente(self, cliente_id):
        cliente = self.__buscar_cliente_por_id(cliente_id)
        if not cliente:
            return {'success': False, 'message': 'Cliente no encontrado'}

        carrito = cliente.mostrar_carrito()
        detallado = []
        total = 0
        for item in carrito:
            producto = self.__buscar_producto_por_id(item['producto_id'])
            if producto:
                subtotal = producto.precio * item['cantidad']
                detallado.append({'producto': producto.to_dict(), 'cantidad': item['cantidad'], 'subtotal': subtotal})
                total += subtotal

        return {
            'success': True,
            'cliente': cliente.to_dict(),
            'carrito': detallado,
            'total': total,
            'total_productos': cliente.calcular_total_productos_carrito()
        }

    def actualizar_carrito_cliente(self, cliente_id, producto_id, nueva_cantidad):
        cliente = self.__buscar_cliente_por_id(cliente_id)
        producto = self.__buscar_producto_por_id(producto_id)
        if not cliente or not producto:
            return {'success': False, 'message': 'Cliente o producto no encontrado'}
        if nueva_cantidad > producto.stock:
            return {'success': False, 'message': f'Solo hay {producto.stock} en stock'}
        cliente.actualizar_cantidad_carrito(producto_id, nueva_cantidad)
        self.__guardar_clientes_en_archivo()
        return {'success': True, 'message': 'Cantidad actualizada'}

    def realizar_compra(self, cliente_id):
        cliente = self.__buscar_cliente_por_id(cliente_id)
        if not cliente or not cliente.mostrar_carrito():
            return {'success': False, 'message': 'Cliente no válido o carrito vacío'}

        productos_compra = []
        total = 0
        for item in cliente.mostrar_carrito():
            producto = self.__buscar_producto_por_id(item['producto_id'])
            if not producto or not producto.tiene_stock_suficiente(item['cantidad']):
                return {'success': False, 'message': 'Producto no disponible o sin stock'}
            subtotal = producto.precio * item['cantidad']
            productos_compra.append({
                'producto': producto.to_dict(),
                'cantidad': item['cantidad'],
                'subtotal': subtotal
            })
            total += subtotal
            producto.actualizar_stock(-item['cantidad'])

        descuento = 0.1 * total if cliente.calcular_total_productos_carrito() > 5 else 0
        total_final = total - descuento

        venta = {
            'cliente_id': cliente_id,
            'cliente_email': cliente.email,
            'productos': productos_compra,
            'subtotal': total,
            'descuento': descuento,
            'total_final': total_final,
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        cliente.vaciar_carrito()
        self.__guardar_venta_en_archivo(venta)
        self.__guardar_productos_en_archivo()
        self.__guardar_clientes_en_archivo()

        return {'success': True, 'venta': venta}
