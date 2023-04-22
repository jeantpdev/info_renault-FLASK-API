from flask import Flask, jsonify, request
#from flask_mysqldb import MySQL
import psycopg2
from flask_cors import CORS, cross_origin

app = Flask(__name__)

CORS(app)

#mysql = MySQL(app)

def get_db_connection():
    conn = psycopg2.connect(host='db.elofgzyhnliurwchnmse.supabase.co',
                            database='postgres',
                            port=5432,
                            user='postgres',
                            password='oxHcvidninh5Vh5s')
    return conn

conn = get_db_connection()


@app.route("/insertar_datos_vehiculo/", methods = ['POST'])
def insertar_datos_vehiculo():

    datos_usuario_temporal = []
    datos_usuario = {
        'modelo': request.json['campo_modelo'],
        'año': request.json['campo_año'],
        'kilometraje': request.json['campo_kilometraje'],
        'precio': request.json['campo_precio']
    }

    datos_usuario_temporal.append(datos_usuario)

    modelo = datos_usuario['modelo']
    año = datos_usuario['año']
    kilometraje = datos_usuario['kilometraje']
    precio = datos_usuario['precio']

    cur = conn.cursor()
    cur.execute("INSERT INTO tabla_renault (modelo, año, kilometraje, precio) VALUES (%s,%s,%s,%s)", (modelo, año, kilometraje, precio))
    cur.close()
    conn.commit()
    print("Datos añadidos a la BD ")
    return jsonify({"informacion":"Registro exitoso del usuario y sus respuestas"})

@app.route('/mostrar_registros/', methods=['GET'])
def registrar_db():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehiculos_renault')
    registros = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    resultado = []
    for registro in registros:
        resultado.append(dict(zip(columnas, registro)))
    insertar_datos_vehiculo(resultado[0])
    return jsonify(resultado)

@app.route("/modificar_datos_vehiculo", methods=['POST'])
def modificar_datos_vehiculo():

    datos_vehiculo = {
        'modificar_id': request.json['modificarId'],
        'modificar_kilometraje': request.json['modificarKilometraje'],
        'modificar_precio': request.json['modificarPrecio']
    }

    id = datos_vehiculo['modificar_id']
    kilometraje = datos_vehiculo['modificar_kilometraje']
    precio = datos_vehiculo['modificar_precio']

    cur = conn.cursor()
    sql = ("UPDATE vehiculos_renault SET precio = %s, kilometraje = %s WHERE id = %s")
    val = (precio, kilometraje, id)
    cur.execute(sql,val)
    cur.close()
    conn.commit()
    print("Modificación realizada ")
    return jsonify({"informacion":"Registro exitoso del usuario y sus respuestas"})

@app.route("/eliminar_datos_vehiculo/<id>", methods=['DELETE'])
def eliminar_datos_vehiculo(id):
    print(id)
    cur = conn.cursor()

    sql = ("DELETE FROM vehiculos_renault WHERE id = %s")
    val = (id,)
    cur.execute(sql,val)
    cur.close()
    conn.commit()
    print("eliminación realizada ")
    return jsonify({"informacion":"Registro exitoso del usuario y sus respuestas"})

@app.route('/consultar_datos_vehiculo/<id>', methods=['GET'])
def consultar_datos_vehiculo(id):
    try:
        cur = conn.cursor()
        cur.execute('SELECT * FROM vehiculos_renault WHERE id = %s', [id])
        rv = cur.fetchall()
        cur.close()
        return jsonify(rv)
    except Exception as e:
        print(e)
        return jsonify({"informacion":e})

@app.route('/iniciar_sesion', methods = ['POST'])
def iniciar_sesion():

    datos_usuario = {
        'usuario': request.json['correo'],
        'contrasena': request.json['contrasena']
    }

    usuario = datos_usuario['usuario']
    contrasena = datos_usuario['contrasena']

    cursor = conn.cursor()
    cursor.execute('SELECT usuario, contrasena FROM usuario WHERE usuario LIKE %s and contrasena = %s', (usuario, contrasena))
    registro = cursor.fetchall()
    return jsonify(len(registro))

#Mostrar los registros de la BD en la tabla
@app.route('/mostrar_registros_tabla/', methods=['GET'])
def mostrar_registros_tabla():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM vehiculos_renault')
    registros = cursor.fetchall()
    columnas = [desc[0] for desc in cursor.description]
    resultado = []
    for registro in registros:
        resultado.append(dict(zip(columnas, registro)))
    return jsonify(resultado)

if __name__ == '__main__':
    app.run(debug = True, port = 4000)