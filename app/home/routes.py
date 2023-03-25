#!/usr/bin/env python3

from app import app
from flask import render_template, request
from app.admin.models import AddPicture, Category
from app.home.models import Message

@app.route('/')
def home():
    categories = Category.get_all()
    for category in categories:
        category.addpicture.reverse()
    return render_template("home/index.html", title="ForeverSammy", categories=categories)
@app.route('/gallery')
def gallery():
    page = request.args.get('page', 1, type=int)
    pictures = AddPicture.get_all(page=page)
    return render_template("home/gallery.html", title="gallery", pictures=pictures)

@app.route('/contact', methods=["GET", "POST"])
def contact():
    if (request.method == "POST"):
        email = request.form.get("email")
        phone = request.form.get("phone")
        message = request.form.get("message")
        Message.create(email=email, phone=phone, message=message)

    return render_template("home/contact.html", title="contact")


@app.route('/about')
def about():
    return render_template("home/about.html", title="about")