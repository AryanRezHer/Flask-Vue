import os
from flask import Flask, render_template, jsonify, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'usuarios.db')

db = SQLAlchemy(app)

class usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

class numero(db.Model):
    num = db.Column(db.Integer, primary_key=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getData')
def datos():
    try:
        usuarios_lista = usuarios.query.all()
        data = [{'id': usuario.id, 'nombre': usuario.nombre} for usuario in usuarios_lista]
        return jsonify(data)
    except Exception as e:
        print(f"Error en la función datos(): {str(e)}")
        return jsonify({"error": "Internal Server Error"})
    
@app.route('/getNumero')
def numda():
    try:
        valor_num = numero.query.first()
        data = {'num': valor_num.num if valor_num else None}
        return jsonify(data)
    except Exception as e:
        print(f"Error en la función datos(): {str(e)}")
        return jsonify({"error": "Internal Server Error"})

@app.route('/actualizarBasedeDatos', methods=['POST'])
def updatedb():
    try:
        num = numero.query.first()
        if num:
            num.num +=1
        else:
            new_num = numero(num=1)
            db.session.add(new_num)
            return jsonify({'num': new_num.num})
        db.session.commit()
        return jsonify({'num': num.num})
    except Exception as e:
        print(f"Error en la función actualizar_basede_datos(): {str(e)}")
        return jsonify({'error': 'Error interno del servidor'})
    
@app.route('/actualizarBasedeDatosrest', methods=['POST'])
def updatedbrest():
    try:
        num = numero.query.first()
        if num:
            num.num -=1
        else:
            new_num = numero(num=1)
            db.session.add(new_num)
            return jsonify({'num': new_num.num})
        db.session.commit()
        return jsonify({'num': num.num})
    except Exception as e:
        print(f"Error en la función actualizar_basede_datos(): {str(e)}")
        return jsonify({'error': 'Error interno del servidor'})
    
@app.route('/actualizarBasedeDatosusuarios', methods=['POST'])
def updatedbusr():
    try:
        new_usr = request.json.get('nombre')
        if new_usr:
            nuevo_usuario = usuarios(nombre=new_usr)
            db.session.add(nuevo_usuario)
            db.session.commit()
            return jsonify({'id': nuevo_usuario.id, 'nombre': nuevo_usuario.nombre})
    except Exception as e:
        print(f"Error en la función actualizar_basede_datos(): {str(e)}")
        return jsonify({'error': 'Error interno del servidor'})
    
@app.route('/actualizarBasedeDatoseliminar', methods=['POST'])
def updatedbelim():
    try:
        id_usr = request.json.get('id')
        if id_usr:
            usr = usuarios.query.get(id_usr)
            if usr:
                db.session.delete(usr)
                db.session.commit()
                return jsonify({'message': 'hecho usuario eliminado'})
            else:
                return jsonify({'error': 'Usuario no encontrado'})
    except Exception as e:
        print(f"Error en la función actualizar_basede_datos(): {str(e)}")
        return jsonify({'error': 'Error interno del servidor'})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)