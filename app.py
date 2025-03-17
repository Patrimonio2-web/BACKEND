from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos local
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Rocko345@localhost/patrimonio'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#base en render
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://patrimonio_ppfk_user:SabopRq1mqHqRXBZaZBaWsEcqfHYJWM2@dpg-cv8oiprqf0us73bbbbfg-a.oregon-postgres.render.com/patrimonio_ppfk'

db = SQLAlchemy(app)

# Modelo de la tabla personas
class Persona(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Persona {self.nombre} {self.apellido}>'

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()

# Ruta para la página principal
@app.route('/')
def index():
    personas = Persona.query.all()
    return render_template('index.html', personas=personas)

# Ruta para agregar una nueva persona
@app.route('/add', methods=['POST'])
def add_persona():
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    nueva_persona = Persona(nombre=nombre, apellido=apellido)
    db.session.add(nueva_persona)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)