# Importamos la clase Blueprint del módulo flask

import os
import uuid
from flask import Blueprint, flash, redirect, render_template, request, url_for

# Importamos login_required, current_user de flask_security
from flask_security import login_required, current_user

# Importamos el decorador login_required de flask_security
from flask_security.decorators import roles_required
from project.models import Role, videojuegos


from werkzeug.utils import secure_filename

# Importamos el objeto de la BD desde __init__.py
from . import db

main = Blueprint("main", __name__)


@main.errorhandler(404)
def error_404_handler(e):
    return render_template("404.html"), 404


# Definimos la ruta a la página principal
@main.route("/")
def index():
    return render_template("index.html")


# Definimos la ruta a la página de perfil
@main.route("/administrador")
@login_required
@roles_required("admin")
def admin():

    juegos = videojuegos.query.all()
    return render_template("videojuegosCRUD.html", juegos=juegos)


@main.route("/administrador", methods=["POST"])
@login_required
@roles_required("admin")
def admin_post():
    juegos = videojuegos.query.all()
    nombre = request.form.get("txtNombre")
    descripcion = request.form.get("txtDescripcion")
    precio = request.form.get("txtPrecio")
    img = str(uuid.uuid4()) + ".png"
    imagen = request.files["imagen"]
    ruta_imagen = os.path.abspath("project\\static\\img")
    imagen.save(os.path.join(ruta_imagen, img))

    new_videojuego = videojuegos(nombre, descripcion, precio, img)

    db.session.add(new_videojuego)

    db.session.commit()
    print(img)

    flash("El juego se guardo correctamente")

    return redirect(url_for("main.admin"))


@main.route("/delete/<id>")
@login_required
def delete(id):
    videojuego = videojuegos.query.get(id)
    imagen = videojuegos.query.get(id)
    os.remove("project/static/img/{}".format(str(imagen.img)))
    db.session.delete(videojuego)
    db.session.commit()
    flash("se elimino correctamente")
    return redirect(url_for("main.admin"))


@main.route("/update/<id>")
@login_required
def update(id):
    videojuego = videojuegos.query.get(id)
    imagen = videojuegos.query.get(id)
    print(videojuego.id)

    return render_template(
        "videojuegosCRUD.html",
        nombre=videojuego.name,
        precio=int(videojuego.precio),
        descripcion=str(videojuego.description),
        imagen=imagen.img,
        update=True,
        id=videojuego.id,
    )


@main.route("/updateCom/<id>", methods=["POST"])
@login_required
def updateComfim(id):

    img = request.form.get("img")
    os.remove("project/static/img/{}".format(str(img)))
    imagen = request.files["imagen"]
    ruta_imagen = os.path.abspath("project\\static\\img")
    imagen.save(os.path.join(ruta_imagen, img))

    idjuego = id
    videojuego = videojuegos.query.get(idjuego)
    videojuego.name = request.form.get("txtNombre")
    videojuego.description = request.form.get("txtDescripcion")
    videojuego.precio = request.form.get("txtPrecio")
    db.session.commit()

    print(videojuego.id)

    flash("El videojuego se modifico correctamente")
    return redirect(url_for("main.admin"))


@main.route("/galeria")
@login_required
def galeria():
    juegos = videojuegos.query.all()

    if len(juegos) == 0:
        juegos = 0

    print(current_user.admin)

    return render_template("galeria.html", juegos=juegos)
