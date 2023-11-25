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
def ver_Bal():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * FROM BalanceDetalle""")
    BalanceDetalle = cursor.fetchall()
    return render_template("pagina_balances.html", BalanceDetalle=BalanceDetalle)


## ACCEDER A LA BASE DE DATOS Y MOSTRAR REGISTROS
@app.route("/verCuenta", methods=["GET"])
def ver_Cue():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * FROM Cuenta""")
    Cuenta = cursor.fetchall()
    return render_template("pagina_cuentas.html", Cuenta=Cuenta)


## ACCEDER A LA BASE DE DATOS Y MOSTRAR REGISTROS
@app.route("/verEstado", methods=["GET"])
def ver_Est():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * FROM EstadosFinancieros""")
    EstadosFinancieros = cursor.fetchall()
    return render_template("pagina_estados.html", EstadosFinancieros=EstadosFinancieros)


## ACCEDER A LA BASE DE DATOS Y MOSTRAR REGISTROS
@app.route("/verTransaccion", methods=["GET"])
def ver_Tran():
    cursor = mysql.connection.cursor()
    cursor.execute("""SELECT * FROM Transaccion""")
    Transaccion = cursor.fetchall()
    return render_template("pagina_transacciones.html", Transaccion=Transaccion)


## ACCEDER A SELECT
@app.route("/insertarCuenta")
def insertarCuenta():
    return render_template("insertar_cuentas.html")


## GUARDAR DATOS DEL USUARIO
@app.route("/insertCuenta", methods=["GET", "POST"])
def insertCuenta():
    if request.method == "GET":
        return "Método erróneo, favor de usar el correcto"
    if request.method == "POST":
        id = request.form["id"]
        nombre = request.form["nom"]
        saldo = request.form["sal"]
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO Cuenta (ID, NombreCuenta, Saldo) VALUES (%s,%s,%s)""",
            (id, nombre, saldo),
        )
        mysql.connection.commit()
        cursor.close()
        return ver_datos()


## ACCEDER A SELECT
@app.route("/insertarTransaccion")
def insertarTransaccion():
    return render_template("insertar_transacciones.html")


## GUARDAR DATOS DEL USUARIO
@app.route("/insertTransaccion", methods=["GET", "POST"])
def insertTransaccion():
    if request.method == "GET":
        return "Método erróneo, favor de usar el correcto"
    if request.method == "POST":
        id = request.form["id"]
        fecha = request.form["fec"]
        descripcion = request.form["des"]
        monto = request.form["mon"]
        tipotransaccion = request.form["tran"]
        metodopago = request.form["pag"]
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO Transaccion (ID, Fecha, Descripcion, Monto, TipoTransaccion, MetodoPago) VALUES (%s,%s,%s,%s,%s,%s)""",
            (id, fecha, descripcion, monto, tipotransaccion, metodopago),
        )
        mysql.connection.commit()
        cursor.close()
        return ver_datos()


## ACCEDER A UPDATE
@app.route("/updateCuenta")
def updateCuent():
    return render_template("update_cuentas.html")


@app.route("/actualizarCuenta", methods=["POST"])
def actualizarCuent():
    id = request.form["ID"]
    nombre = request.form["NombreCuenta"]
    saldo = request.form["Saldo"]
    cursor = mysql.connection.cursor()
    cursor.execute('''UPDATE Cuenta SET ID=%s, NombreCuenta=%s, Saldo=%s WHERE ID=%s''',(id, nombre, saldo, id))
    mysql.connection.commit()
    cursor.close()
    return ver_datos()


## ACCEDER A UPDATE
@app.route("/updateTransaccion")
def updateTran():
    return render_template("update_transacciones.html")


@app.route("/actualizarTransaccion", methods=["POST"])
def actualizarTran():
    id = request.form["id"]
    fecha = request.form["fec"]
    descripcion = request.form["des"]
    monto = request.form["mon"]
    tipotransaccion = request.form["tran"]
    metodopago = request.form["pag"]
    cursor = mysql.connection.cursor()
    cursor.execute(
        '''UPDATE Transaccion SET ID=%s, Fecha=%s, Descripcion=%s,Monto=%s, TipoTransaccion=%s, MetodoPago=%s WHERE ID=%s''',(id, fecha, descripcion, monto, tipotransaccion, metodopago, id))
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
