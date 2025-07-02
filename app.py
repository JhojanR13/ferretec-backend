## backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from models.tienda import Tienda

app = Flask(__name__)
CORS(app)

tienda = Tienda()

@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    try:
        productos = tienda.mostrar_productos()
        return jsonify({'success': True, 'productos': productos})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/productos', methods=['POST'])
def crear_producto():
    try:
        data = request.get_json()
        nombre = data.get('nombre', '').strip()
        precio = float(data.get('precio', 0))
        stock = int(data.get('stock', 0))
        resultado = tienda.registrar_producto(nombre, precio, stock)
        return jsonify(resultado), 201 if resultado['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/clientes', methods=['GET'])
def obtener_clientes():
    try:
        clientes = tienda.mostrar_clientes()
        return jsonify({'success': True, 'clientes': clientes})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/clientes', methods=['POST'])
def crear_cliente():
    try:
        data = request.get_json()
        nombre = data.get('nombre', '').strip()
        email = data.get('email', '').strip()
        resultado = tienda.registrar_cliente(nombre, email)
        return jsonify(resultado), 201 if resultado['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/carrito/agregar', methods=['POST'])
def agregar_al_carrito():
    try:
        data = request.get_json()
        resultado = tienda.agregar_producto_a_carrito_cliente(
            int(data['cliente_id']), int(data['producto_id']), int(data['cantidad'])
        )
        return jsonify(resultado), 200 if resultado['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/carrito/<int:cliente_id>', methods=['GET'])
def obtener_carrito(cliente_id):
    try:
        resultado = tienda.obtener_carrito_detallado_cliente(cliente_id)
        return jsonify(resultado), 200 if resultado['success'] else 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/carrito/actualizar', methods=['PUT'])
def actualizar_carrito():
    try:
        data = request.get_json()
        resultado = tienda.actualizar_carrito_cliente(
            int(data['cliente_id']), int(data['producto_id']), int(data['cantidad'])
        )
        return jsonify(resultado), 200 if resultado['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/comprar', methods=['POST'])
def realizar_compra():
    try:
        data = request.get_json()
        resultado = tienda.realizar_compra(int(data['cliente_id']))
        return jsonify(resultado), 200 if resultado['success'] else 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    print("\n🔧 Iniciando Ferretec Backend...")
    print("📁 Los datos se guardan en archivos .txt en la carpeta 'data/'")
    print("🌐 API disponible en: http://localhost:5000\n")
    app.run(debug=True, port=5000)
