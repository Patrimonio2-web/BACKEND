from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Agregado para CORS
import os

app = Flask(__name__)
CORS(app)  # Permite peticiones desde cualquier origen (puedes restringirlo)

# Configuración de la base de datos en Render
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://patrimonio_ppfk_user:SabopRq1mqHqRXBZaZBaWsEcqfHYJWM2@dpg-cv8oiprqf0us73bbbbfg-a.oregon-postgres.render.com/patrimonio_ppfk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de la tabla personas
class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre, "apellido": self.apellido}

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

# Obtener todas las personas (ruta GET)
@app.route('/personas', methods=['GET'])
def get_personas():
    personas = Persona.query.all()
    return jsonify([p.to_dict() for p in personas])



# Agregar una nueva persona (ruta POST)
@app.route('/personas', methods=['POST'])
def add_persona():
    data = request.json
    nueva_persona = Persona(nombre=data['nombre'], apellido=data['apellido'])
    db.session.add(nueva_persona)
    db.session.commit()
    return jsonify(nueva_persona.to_dict()), 201

# Configuración para que Flask acepte el puerto de Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Render asigna un puerto dinámico
    app.run(host="0.0.0.0", port=port, debug=True)