#!/usr/bin/env python3

from app import app
from flask import render_template, request
from app.admin.models import AddPicture, Category
from app.home.models import Message

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    per_page = 5

    # categories = Category.get_all()
    # for category in categories:
        # category.addpicture.reverse()
    # Retrieve all parent objects and their child objects
    parents = Category.query.all()
    categories = {}
    for parent in parents:
        children = (
            AddPicture.query
            .filter_by(category_id=parent.id)
            .order_by(AddPicture.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        categories[parent] = children
    return render_template("home/index.html", title="ForeverSammy", categories=categories)

@app.route('/paginate-home-pictures/<id>/')
def paginate_home_pictures(id):
    """ implementation of pagination for picture display
    """
    page = request.args.get('page', 1, type=int)
    per_page = 5
    # Retrieve all parent objects and their child objects
    parents = Category.query.all()
    target = Category.get(id)
    if (target == None):
        return (redirect(request.url))
    categories = {}
    for parent in parents:
        children = (
            AddPicture.query
            .filter_by(category_id=parent.id)
            .order_by(AddPicture.created_at.desc())
            .paginate(page=1, per_page=per_page, error_out=False)
        )
        if (parent.id == target.id):
            children = (
                AddPicture.query
                .filter_by(category_id=target.id)
                .order_by(AddPicture.created_at.desc())
                .paginate(page=page, per_page=per_page, error_out=False)
        )
        categories[parent] = children
    return render_template("home/index.html", title="admin", categories=categories)


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