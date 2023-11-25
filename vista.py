from flask import Flask, render_template, request

## IMPORTAMOS LA LIBRERIA FLASK_MYSQL PARA CONECTARNOS CON LA DB
from flask_mysqldb import MySQL

### agregado para depurar la app
import traceback

app = Flask(__name__)
mysql = MySQL(app)

########################
# Flask requiere una clave secreta (secret_key) para manejar las sesiones de manera segura
app.secret_key = "udem.2023"
app.config["SESSION_TYPE"] = "filesystem"

################################################################
# DATOS DE ACCESO A LA BASE DE DATOS
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "contador_user"
app.config["MYSQL_PASSWORD"] = "666"
app.config["MYSQL_DB"] = "ContabilidadEmpresa"

print("Conexion exitosa")


################## LOGIN ###############
## MOSTRAR LANDING
@app.route("/")
def inicio():
    return render_template("index.html")


# Verificamos el inicio de sesión mediante Ajax
@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        # Obtener los datos del formulario
        email = request.form["email"].strip()  # quitamos espacios en blanco
        contrasena = request.form["contrasena"].strip()
        print(f"Intento de inicio de sesión. Email: {email}, Contraseña: {contrasena}")

        # Llamada al procedimiento almacenado
        cur = mysql.connection.cursor()
        cur.callproc("verificar_login", (email, contrasena))
        resultado = cur.fetchone()
        cur.close()

        print(f"Email: {email}, Contraseña: {contrasena}, Resultado: {resultado}")

        if resultado is not None and len(resultado) > 0:
            resultado = resultado[0]

            ## como sigue diciendo que el login es incorrecto,
            ## usemos valores booleanos
            if resultado:
                flash("Inicio de sesión exitoso", "success")
                response = jsonify({"resultado": "Inicio de sesión exitoso"})

                # Verificar si es una solicitud AJAX, Redirigir solo en solicitudes AJAX
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return response  # Respuesta JSON para solicitudes AJAX
                else:
                    print("Redirigiendo a home")
                    return redirect(url_for("home"))
            else:
                flash("Credenciales incorrectas", "error")
                return jsonify({"error": "Credenciales incorrectas"})
        else:
            return jsonify({"error": "Credenciales incorrectas"})

    except Exception as e:
        print(f"Error durante el inicio de sesión: {str(e)}")
        traceback.print_exc()  # Imprime la info completa

        return jsonify({"error": "Hubo un error durante el inicio de sesión"})

    return jsonify({"resultado": "Éxito"})


################### REGISTRO  #################
# Ruta de registro
@app.route("/registro")
def registro():
    return render_template("registro.html")


# Realizamos el registro mediante Ajax igual que el login
@app.route("/registrar_usuario", methods=["POST"])
def registrar_usuario():
    try:
        # Obtener datos del formulario
        nombre = request.form.get("nombre")
        appaterno = request.form.get("appaterno")
        apmaterno = request.form.get("apmaterno")
        correo = request.form.get("correo")
        contrasena = request.form.get("contrasena")

        # Validar que todos los campos necesarios estén presentes
        if not nombre or not appaterno or not apmaterno or not correo or not contrasena:
            return jsonify({"error": "Todos los campos son obligatorios"})

        # Llamada al procedimiento almacenado
        cur = mysql.connection.cursor()
        cur.callproc(
            "registroUsuario", (nombre, appaterno, apmaterno, correo, contrasena)
        )
        resultado = cur.fetchone()
        print(f"Después de llamar al procedimiento almacenado. Resultado: {resultado}")

        # Verificar si se obtuvieron resultados
        if resultado is not None and len(resultado) > 0:
            mensaje = resultado[0]
            return jsonify({"mensaje": mensaje})
        else:
            return jsonify({"error": "No se obtuvo un mensaje del servidor"})

    except Exception as e:
        print(f"Error durante el registro: {str(e)}")
        return jsonify({"error": "Hubo un error durante el registro"})
    finally:
        # Asegurarse de cerrar el cursor
        if cur:
            cur.close()
            # Hacer commit para confirmar los cambios
            mysql.connection.commit()

# hola aaaa
@app.route("/home")
def home():
    return render_template("home.html")


########################################


## ACCEDER A LA BASE DE DATOS Y MOSTRAR REGISTROS
@app.route("/verTransacciones", methods=["GET"])
def ver_datosTransacciones():
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT ID, Fecha, Descripcion, Monto, TipoTransaccion, MetodoPago FROM Transaccion"""
    )
    # NO SE PONE ;
    Transaccion = cursor.fetchall()
    return render_template("info_transacciones.html", Transaccion=Transaccion)


@app.route("/verCuentas", methods=["GET"])
def ver_datosCuentas():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT ID, NombreCuenta, Saldo FROM Cuenta""")
    # NO SE PONE ;
    Cuenta = cursor.fetchall()
    return render_template("info_cuentas.html", Cuenta=Cuenta)


@app.route("/verBalances", methods=["GET"])
def ver_datosBalances():
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT ID, Activos, Pasivos, PatrimonioNeto FROM BalanceDetalle"""
    )
    # NO SE PONE ;
    BalanceDetalle = cursor.fetchall()
    return render_template("info_balances.html", BalanceDetalle=BalanceDetalle)


@app.route("/verEstados", methods=["GET"])
def ver_datosEstados():
    cursor = mysql.connection.cursor()
    cursor.execute(
        """SELECT ID, Periodo, IDCuenta, IDBalance, Precio FROM EstadosFinancieros"""
    )
    # NO SE PONE ;
    EstadosFinancieros = cursor.fetchall()
    return render_template("info_estados.html", EstadosFinancieros=EstadosFinancieros)


## ACCEDER A SELECT
@app.route("/insertar")
def insertar():
    return render_template("insertar.html")


## GUARDAR DATOS DEL USUARIO
@app.route("/insertCuenta", methods=["GET", "POST"])
def insertCuenta():
    if request.method == "GET":
        return "M&eacture;todo err&oacute;neo, favor de usar el correcto"
    if request.method == "POST":
        ID = request.form["nombre"]  ## VARIABLE LOCAL
        NombreCuenta = request.form["id"]
        Saldo = request.form["nombrecuenta"]
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO Cuenta (ID, NombreCuenta, Saldo) VALUES (%s,%s,%s)""",
            (ID, NombreCuenta, Saldo),
        )
        mysql.connection.commit()
        cursor.close()
        return ver_datos()


@app.route("/insertTransaccion", methods=["GET", "POST"])
def insertTransaccion():
    if request.method == "GET":
        return "M&eacture;todo err&oacute;neo, favor de usar el correcto"
    if request.method == "POST":
        ID = request.form["id"]  ## VARIABLE LOCAL
        Fecha = request.form["fecha"]
        Descripcion = request.form["descripcion"]
        Monto = request.form["monto"]
        TipoTransaccion = request.form["tipotransaccion"]
        MetodoPago = request.form["metodopago"]


        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO Transaccion (ID, Fecha, Descripcion, Monto, TipoTransaccion, MetodoPago) VALUES (%s,%s,%s,%s,%s,%s)""",
            (ID, Fecha, Descripcion, Monto, TipoTransaccion, MetodoPago),
        )
        mysql.connection.commit()
        cursor.close()
        return ver_datos()



## BORRAR
@app.route("/borrar/<string:id>")
def borrar(id):
    cursor = mysql.connection.cursor()
    cursor.execute("""""", (id,))
    mysql.connection.commit()
    cursor.close()
    return ver_datos()


## ACTUALIZACION DE DATOS
@app.route("/editar/<string:id>")
def editar(id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT id, Nombre, Modelo, Anio, Precio FROM Autos WHERE id=%s", (id,)
    )  ## Select para recuperar el id
    autos = cursor.fetchall()
    return render_template("forma_update.html", autos=autos[0])


## ACTUALIZAR
@app.route("/actualizar/<string:id>", methods=["GET", "POST"])
def actualizar(id):
    if request.method == "GET":
        return "M&eacture;todo err&oacute;neo, favor de usar el correcto"
    if request.method == "POST":
        nombre = request.form["nombre"]  ## VARIABLE LOCAL
        precio = request.form["pre"]
        modelo = request.form["m"]
        anio = request.form["anio"]
        cursor = mysql.connection.cursor()
        cursor.execute(
            """""",
            (
                nombre,
                modelo,
                anio,
                precio,
                id,
            ),
        )
        mysql.connection.commit()
        cursor.close()
        return ver_datos()


@app.route("/selecciona")
def selecciona():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Categorias")
    categorias = cursor.fetchall()
    cursor.close()
    return render_template("selecciona.html", categorias=categorias)


@app.route("/productos/")
def productos():
    id = request.args.get("categoria")
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Productos WHERE Categoria_id=%s", [id])
    productos = cursor.fetchall()
    cursor.close()
    return render_template("productos.html", productos=productos)


@app.route("/buscar")
def buscar():
    return render_template("buscar.html")


@app.route("/autocomplete", methods=["POST"])
def autocomplete():
    input = request.form["input"]
    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT Nombre FROM Productos WHERE Nombre LIKE %s", ("%" + input + "%",)
    )
    resultado = cursor.fetchall()
    cursor.close()
    return render_template("autocomplete.html", resultado=resultado)



if __name__ == "__main__":
    app.run(debug=True)
