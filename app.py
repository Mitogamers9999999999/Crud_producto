from flask import Flask,render_template,request,redirect,url_for
import sqlite3

app = Flask(__name__)

# Creación de base de datos y tabla
def init_database():
    # Se crea la base de datos en caso de que no exista
    conn = sqlite3.connect("producto.db")
    
    cursor =  conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS producto(
            id INTEGER PRIMARY KEY,
            descripcion TEXT NOT NULL,
            cantidad INTEGER NOT NULL,
            precio FLOAT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
    
init_database()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/product")
def product():
    conn = sqlite3.connect("producto.db")
    # Permite manejar los registros como diccionarios
    conn.row_factory = sqlite3.Row
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM producto")
    productos = cursor.fetchall()
    return render_template("product/index.html",productos = productos)

@app.route("/product/create")
def create():
    return render_template('product/create.html')

@app.route("/product/create/save",methods=['POST'])
def product_save():
    descripcion =  request.form['descripcion']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    
    conn = sqlite3.connect("producto.db")
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO producto (descripcion,cantidad,precio) VALUES (?,?,?)", (descripcion,cantidad,precio))
    
    conn.commit()
    conn.close()
    return redirect('/product')

# Editar persona
@app.route("/product/edit/<int:id>")
def product_edit(id):
    conn =  sqlite3.connect("producto.db")
    conn.row_factory = sqlite3.Row
    cursor =  conn.cursor()
    cursor.execute("SELECT * FROM producto WHERE id = ?", (id,))
    productos = cursor.fetchone()
    conn.close()
    return render_template("product/edit.html",productos = productos)

@app.route("/product/update",methods=['POST'])
def product_update():
    id = request.form['id']
    descripcion = request.form['descripcion']
    cantidad = request.form['cantidad']
    precio = request.form['precio']
    
    conn  = sqlite3.connect("producto.db")
    cursor =  conn.cursor()
    
    cursor.execute("UPDATE producto SET descripcion=?,cantidad=?,precio=? WHERE id=?", (descripcion,cantidad,precio,id))
    conn.commit()
    conn.close()
    return redirect("/product")

# Eliminar registro
@app.route("/product/delete/<int:id>")
def product_delete(id):
    conn = sqlite3.connect("producto.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM producto WHERE id=?",(id,))
    conn.commit()
    conn.close()
    return redirect('/product')
    
if __name__ == "__main__":
    app.run(debug=True)

