from flask import Flask, render_template, request

## IMPORTAMOS LA LIBRERIA FLASK_MYSQL PARA CONECTARNOS CON LA DB
from flask_mysqldb import MySQL


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


## ACCEDER A LA BASE DE DATOS Y MOSTRAR REGISTROS
@app.route("/verBalance", methods=["GET"])
def ver_datos():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * FROM BalanceDetalle""")
    BalanceDetalle = cursor.fetchall()
    return render_template("pagina_balances.html", BalanceDetalle=BalanceDetalle)


## ACCEDER A LA BASE DE DATOS Y MOSTRAR REGISTROS
@app.route("/verCuenta", methods=["GET"])
def ver_datos():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * FROM Cuenta""")
    Cuenta = cursor.fetchall()
    return render_template("pagina_cuentas.html", Cuenta=Cuenta)



## ACCEDER A LA BASE DE DATOS Y MOSTRAR REGISTROS
@app.route("/verEstado", methods=["GET"])
def ver_datos():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT id, Nombre, Modelo, Precio FROM Autos""")
    Autos = cursor.fetchall()
    return render_template("pagina_estados.html", Autos=Autos)



## ACCEDER A LA BASE DE DATOS Y MOSTRAR REGISTROS
@app.route("/verTransaccion", methods=["GET"])
def ver_datos():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT id, Nombre, Modelo, Precio FROM Autos""")
    Autos = cursor.fetchall()
    return render_template("pagina_transacciones.html", Autos=Autos)


## ACCEDER A SELECT
@app.route("/insertar")
def insertar():
    return render_template("insertar.html")


## GUARDAR DATOS DEL USUARIO
@app.route("/insert", methods=["GET", "POST"])
def insert():
    if request.method == "GET":
        return "Método erróneo, favor de usar el correcto"
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["pre"]
        modelo = request.form["m"]
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO Autos (Nombre, Modelo, Precio) VALUES (%s,%s,%s)""",
            (nombre, modelo, precio),
        )
        mysql.connection.commit()
        cursor.close()
        return ver_datos()



## ACCEDER A UPDATE
@app.route("/update")
def update():
    return render_template("update.html")


@app.route("/actualizar", methods=["POST"])
def actualizar():
    id = request.form["id"]
    nombre = request.form["nombre"]
    modelo = request.form["modelo"]
    precio = request.form["precio"]
    cursor = mysql.connection.cursor()
    cursor.execute(
        """UPDATE Autos SET Nombre=%s, Modelo=%s, Precio=%s WHERE id=%s""",
        (nombre, modelo, precio, id),
    )
    mysql.connection.commit()
    cursor.close()
    return ver_datos()


## ACCEDER A DELETE
@app.route("/delete")
def delete():
    return render_template("delete.html")


## BORRAR DATOS
@app.route("/borrar", methods=["POST"])
def borrar():
    id = request.form["id"]
    cursor = mysql.connection.cursor()
    cursor.execute("""DELETE FROM Autos WHERE id=%s""", (id,))
    mysql.connection.commit()
    cursor.close()
    return ver_datos()


if __name__ == "__main__":
    app.run(debug=True)
