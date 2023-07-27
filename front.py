#IMPORTAR LIBRERIA PARA USAR FRAMEWORK FLASK
#Flask es un framework web ligero y flexible para Python que se utiliza para construir aplicaciones web.
from flask import Flask,request, session, redirect, url_for
from flask import render_template
import os
from flask import request
import pymysql
##llamado a flask
app = Flask(__name__)

IMG_FOLDER = os.path.join('static', 'img')
app.secret_key = 'my_secret_key'
app.config['UPLOAD_FOLDER'] = IMG_FOLDER

 # Establecer la conexión a la base de datos
connection = pymysql.connect(host='db4free.net',
                                user='admin12345',
                                password='admin12345',
                                db='sisedu12345')

##servicio web
@app.route('/', methods = ["GET","POST"])
def home():
    fondoP = os.path.join(app.config['UPLOAD_FOLDER'], 'cat-4.jpeg')
    return render_template('index.html',fondo=fondoP)

@app.route('/cursos', methods = ["GET","POST"])
def cursos():
    ad = os.path.join(app.config['UPLOAD_FOLDER'], 'disenio.jpeg')
    ml = os.path.join(app.config['UPLOAD_FOLDER'], 'ml.png')
    vc = os.path.join(app.config['UPLOAD_FOLDER'], 'vc.jpg')
    ig = os.path.join(app.config['UPLOAD_FOLDER'], 'ig.png')
    return render_template('cursos.html',ad=ad, ml=ml , vc=vc, ig=ig)

@app.route('/login', methods = ["GET","POST"])
def login():
   # Si el usuario envía el formulario
    if request.method == 'POST':
        # Obtener los datos del formulario
        username = request.form['username']
        password = request.form['password']
        # Crear un cursor
        cursor = connection.cursor()
        global cedula_est
        global valor_id 
        # Verificar si el nombre de usuario y la contraseña son válidos
        try:
            query = 'SELECT id_est, nombre, apellido FROM estudiante WHERE id_est = %s AND contrasenia = %s'
            connection.ping()
            cursor.execute(query, (username, password))
            result1 = cursor.fetchone()
            cedula_est = result1[0]
        except:
            print('sin resultado 1')
            pass
        
        # Crear un cursor
        cursor2 = connection.cursor()

        # Verificar si el nombre de usuario y la contraseña son válidos
        try:
            query2 = 'SELECT id_profesor, nombre, apellido FROM profesor WHERE id_profesor = %s AND contrasenia = %s'
            connection.ping()
            cursor2.execute(query2, (username, password))
            result2 = cursor2.fetchone()
            
            valor_id =  result2[0]
        except:
            print('sin resultado 2')
            pass

        # Crear un cursor3
        cursor3 = connection.cursor()

        # Verificar si el nombre de usuario y la contraseña son válidos
        try:

            query3 = 'SELECT * FROM administrador WHERE id_administrador = %s AND contrasenia = %s'
            connection.ping()
            cursor3.execute(query3, (username, password))
            result3 = cursor3.fetchone()
        except:
            print('sin resultado 3')
            pass

        # Cerrar la conexión
        connection.close()

        # Si se encuentra un usuario válido, iniciar sesión
        if result1:
            session['username'] = username
            return render_template('alumno1.html')
        elif result2:
            session['username'] = username
            return render_template('maestro.html')
        elif result3:
            session['username'] = username
            return render_template('administrador.html')
        else:
            # Si no se encuentra un usuario válido, mostrar un mensaje de error
            error = 'Cédula o contraseña invalidas'
    else:
        error = None

    # Mostrar el formulario de inicio de sesión
    return render_template('login.html', error=error)
    
@app.route('/inscribir_estudiante', methods = ["GET","POST"])
def inscribir_estudiante():
    # obtener los datos del formulario
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    cedula = request.form['cedula']
    contraseña = request.form['contrasenia']
    curso = request.form.get("inlineRadioOptions")
    # conectarse a la base de datos
    cur = connection.cursor()

    # ejecutar la consulta INSERT con parámetros de sustitución
    cur.execute('''INSERT INTO estudiante (id_est, contrasenia, nombre, apellido, curso) VALUES (%s, %s, %s,%s,%s)''', (cedula, contraseña, nombre,apellido,curso))
    connection.ping()
    # confirmar la transacción
    connection.commit()
    connection.ping()
    cur.close()
    connection.close()

    return render_template('insc.html',result = 'Usuario agregado exitosamente. Inicie Sesión')

@app.route('/inscripcion_estudiante_admin', methods = ["GET","POST"])
def inscripcion_estudiante_admin():
    # obtener los datos del formulario
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    cedula = request.form['cedula']
    contraseña = request.form['contrasenia']
    curso = request.form.get('inlineRadioOptions')
    # conectarse a la base de datos
    cur = connection.cursor()

    # ejecutar la consulta INSERT con parámetros de sustitución
    cur.execute('''INSERT INTO estudiante (id_est, contrasenia, nombre, apellido, curso) VALUES (%s, %s, %s,%s,%s)''', (cedula, contraseña, nombre,apellido,curso))
    connection.ping()
    # confirmar la transacción
    connection.commit()
    connection.ping()
    cur.close()
    connection.ping()
    connection.close()

    return render_template('inscribir_estudiante.html',result = 'Usuario agregado exitosamente. Inicie Sesión')

@app.route('/inscripcion_docente_admin', methods = ["GET","POST"])
def inscripcion_docente_admin():
    # obtener los datos del formulario
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    cedula = request.form['cedula']
    contraseña = request.form['contrasenia']
    curso = request.form.get('inlineRadioOptions')
    # conectarse a la base de datos
    cur = connection.cursor()

    # ejecutar la consulta INSERT con parámetros de sustitución
    cur.execute('''INSERT INTO profesor (id_profesor, contrasenia, nombre, apellido, curso_dirigido) VALUES (%s, %s, %s,%s,%s)''', (cedula, contraseña, nombre,apellido,curso))
    connection.ping()
    # confirmar la transacción
    connection.commit()
    connection.ping()
    cur.close()
    connection.ping()
    connection.close()

    return render_template('inscribir_docente.html',result = 'Usuario agregado exitosamente. Inicie Sesión')



@app.route('/inscripciones', methods = ["GET","POST"])
def inscripciones():
    return render_template('insc.html')

@app.route('/alumno1', methods = ["GET","POST"])
def alumno1():
    # Verificar si el usuario ha iniciado sesión
    if 'username' in session:
        # Mostrar la página de "home"
        return render_template('alumno1.html')
    else:
        # Redirigir al usuario al formulario de inicio de sesión
        return redirect(url_for('login'))
    

@app.route('/about', methods = ["GET","POST"])
def about():
    ericsson = os.path.join(app.config['UPLOAD_FOLDER'], 'ericsson.jpeg')
    stalin = os.path.join(app.config['UPLOAD_FOLDER'], 'stalin.jpg')
    mauricio = os.path.join(app.config['UPLOAD_FOLDER'], 'mauricio.jpeg')
    ronny = os.path.join(app.config['UPLOAD_FOLDER'], 'ronny.jpeg')
    return render_template('about.html',ericsson=ericsson, stalin=stalin , mauricio=mauricio, ronny=ronny)

@app.route('/docentes', methods = ["GET","POST"])
def docentes():
    profe1 = os.path.join(app.config['UPLOAD_FOLDER'], 'profe1.jpeg')
    profe2 = os.path.join(app.config['UPLOAD_FOLDER'], 'profe2.jpeg')
    profe3 = os.path.join(app.config['UPLOAD_FOLDER'], 'profe3.jpeg')
    profe4 = os.path.join(app.config['UPLOAD_FOLDER'], 'profe4.jpeg')
    
    return render_template('docentes.html',profe1=profe1, profe2=profe2 , profe3=profe3, profe4=profe4)

@app.route('/info', methods = ["GET","POST"])
def info():
    return render_template('info.html')

@app.route('/calificaciones', methods = ["GET","POST"])
def calificaciones():
    # Crear un cursor
    cursor = connection.cursor()
    # Verificar si el nombre de usuario y la contraseña son válidos
    query = 'select e.nombre, e.apellido , e.id_est from estudiante AS e where e.curso = (SELECT p.curso_dirigido from profesor AS p where p.id_profesor = %s);'
    connection.ping()
    cursor.execute(query, (valor_id))
    global estudiantes 
    estudiantes = cursor.fetchall()
    global tamaño_estudiantes 
    tamaño_estudiantes = len(estudiantes)
    return render_template('calificaciones.html', resultado = estudiantes, resultado2 = tamaño_estudiantes)
   

@app.route('/maestro', methods = ["GET","POST"])
def maestro():
    return render_template('maestro.html')

@app.route('/calificar', methods = ["GET","POST"])
def calificar():
    nota1 = request.form["calificacion_registro1"]
    nota2 = request.form["calificacion_registro2"]
    nota_final = (int(nota1)+int(nota2))/2
    nombre_completo = request.form.get("inlineRadioOptions")
    print('este es el nombre ', nombre_completo)
    nombre_split = nombre_completo.split(" ")
    nombre = nombre_split[0]
    apellido = nombre_split[1]

    # Crear un cursor
    cursor = connection.cursor()
    # Verificar si el nombre de usuario y la contraseña son válidos
    try:
        query = 'select e.id_est, e.curso from estudiante AS e where e.nombre = %s and e.apellido = %s;'
        connection.ping()
        cursor.execute(query, (nombre, apellido))
        result = cursor.fetchone()
        id_est = result[0]
        curso = result[1]
    except:
        pass
    
    # conectarse a la base de datos (Un cursor se crea para interactuar con bases de datos en lenguajes de programación. Facilita ejecutar consultas y recuperar, insertar o actualizar datos de manera eficiente.)  
    cur2 = connection.cursor()

    # ejecutar la consulta INSERT con parámetros de sustitución
    cur2.execute('''INSERT INTO calificaciones (id_est, nota1, nota2, nota_final, curso) VALUES (%s, %s, %s,%s,%s)''', (id_est, nota1,nota2,nota_final,curso))
    connection.ping()
    # confirmar la transacción
    connection.commit()
    connection.ping()
    cur2.close()
    connection.ping()
    connection.close()
    
    
    return render_template('calificaciones.html', resultado = estudiantes, resultado2 = tamaño_estudiantes)

@app.route('/administrador', methods = ["GET","POST"])
def administrador():
    return render_template('administrador.html')

@app.route('/inscribirEstudiante', methods = ["GET","POST"])
def inscribirEst():
    connection.ping()
    return render_template('inscribir_estudiante.html')

@app.route('/inscribirDocente', methods = ["GET","POST"])
def inscribirDoce():
    connection.ping()
    return render_template('inscribir_docente.html')

@app.route('/notas_estudiantes', methods = ["GET","POST"])
def notas_estudiantes():
    # Crear un cursor
    cursor = connection.cursor()
    # Verificar si el nombre de usuario y la contraseña son válidos
    query = 'select e.nota1, e.nota2 , e.nota_final from calificaciones AS e where e.id_est = %s;'
    connection.ping()
    cursor.execute(query, (cedula_est))
    result = cursor.fetchone()
    return render_template('notas_estudiantes.html', resultado = result)


##ejecutar el servicio web
if __name__=='__main__':
    #OJO QUITAR EL DEBUG EN PRODUCCION
    app.run(host='0.0.0.0', port=5000, debug=True)
