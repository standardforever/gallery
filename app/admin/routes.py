from flask import render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from app import app, photos, db
from app.admin.models import AddPicture, Category
import secrets, os
from app.utils.file_name_verify import allowed_file
from app.home.models import Message

@app.route('/admin')
def admin():
    page = request.args.get('page', 1, type=int)
    pictures = AddPicture.get_all(page)
    # pic_total = len(db.session.query(AddPicture).all())
    # not_total = len(db.session.query(Message).all())
    # pic_total = len(db.session.query(AddPicture).all())
    # not_total = len(db.session.query(Message).all())

    # pictures = AddPicture.query.paginate(page=page, per_page=5)
    return render_template("admin/dashboard.html", title="admin", pictures=pictures )

@app.route('/login')
def login():
    return render_template("admin/login.html", title="login")


@app.route('/setting')
def setting():
    return render_template("admin/setting_forms.html", title="admin")


@app.route('/notification')
def notification():
    page = request.args.get('page', 1, type=int)
    messages = Message.get_all(page)
    return render_template("admin/notification.html", title="admin", messages=messages)


@app.route('/deletenotification', methods=["POST"])
def deletenotification():
    id = request.form.get('item_id')
    Message.delete(id)
    print(id)
    return redirect(url_for('notification'))

@app.route('/getnotification/<id>')
def getnotification(id):
    notification = Message.get(id)
    return render_template('admin/view_notifica.html', notification=notification)

@app.route('/pictures')
def pictures():

    page = request.args.get('page', 1, type=int)
    per_page = 5

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
    return render_template("admin/pictures.html", title="admin", categories=categories)


@app.route('/paginatepictures/<id>/')
def paginatepictures(id):

    page = request.args.get('page', 1, type=int)
    per_page = 1
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
    return render_template("admin/pictures.html", title="admin", categories=categories)


@app.route('/addpicture/<id>', methods=["POST", "GET"])
def addpicture(id):
    categories = Category.get_all()
    for category in categories:
        category.addpicture.reverse()
    
    # category_id = request.form.get('category')
    if request.method == "POST":
        text = request.form.get('text')
        file = request.files.get("file")
        if (file.filename == ''):
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image = photos.save(file, name=secrets.token_hex(10) + ".")
            AddPicture.create(text=text, image=image, category_id=id)
        return redirect(url_for("pictures"))
    return render_template("admin/picture_form.html", title="admin", categories=categories)


@app.route('/view/<id>')
def view(id):
    picture = AddPicture.get(id)
    return render_template("admin/view.html", title="admin", picture=picture)

@app.route('/editpicture/<id>', methods= ["POST", "GET"])
def editpicture(id):
    picture = AddPicture.get(id)
    if (picture == None):
        return redirect(url_for("pictures"))

    if request.method == "POST":
        text = request.form.get('text')
        file = request.files.get("file")
        if (file.filename == ''):
            return redirect(request.url)
        if file and allowed_file(file.filename):
            os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'] + '/' + picture.image))
            filename = secure_filename(file.filename)
            image = photos.save(file, name=secrets.token_hex(10) + ".")
            picture.image = image
        if (text):
            picture.text = text
        if (text or file):
            db.session.commit()
            return redirect(url_for("pictures"))
        


    # if request.method == "POST":
    #     text = request.form.get('text')
    #     file = request.files.get("file")
    #     if (file):
    #         image = photos.save(file, name=secrets.token_hex(10) + ".")
    #         os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'] + '/' + picture.image))
    #         picture.image = image
    #     if (text):
    #         picture.text = text
    #     if (text or file):
    #         db.session.commit()

    #     return redirect(url_for("pictures"))
    return render_template("admin/edit_picture.html", title="admin", picture=picture)

@app.route('/deletepicture', methods=["POST"])
def deletepicture():
    id = request.form.get('item_id')
    picture = AddPicture.get(id)
    if (picture == None):
        return redirect(url_for("pictures"))

    os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'] + '/' + picture.image))
    picture.delete(id)
    return redirect(url_for("pictures"))



"""=============== Category ================"""

@app.route('/addcat', methods=["POST", "GET"])
def addcat():
    """Add New category to the database"""
    category = Category.get_all()
    if request.method == 'POST':
        category = request.form.get('category')
        cat = Category.create(category=category)
        flash(f'The Brand {category} was added to your database', 'success')
        return redirect(url_for('addcat'))

    return (render_template('admin/category.html', title="addcat", categories=category))


@app.route('/updatecategory/<id>', methods=["POST", "GET"])
def updatecategory(id):
    """Update category in the database"""

    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')

    if request.method == 'POST':
        updatecat.category = category
        flash(f'Your category has been updated', 'success')
        db.session.commit()
        return redirect(url_for('addcat'))
    return render_template('admin/update_category.html', title='Update category page', updatecat=updatecat)



@app.route('/deletecategory', methods=['POST'])
def deletecategory():
    """Delete category from the database"""
    id = request.form.get('item_id')
    category = Category.get(id)
    print(id)
    if (category is None):
        return (redirect(url_for('addcat')))

    for cat in category.addpicture:
        os.remove(os.path.join(app.config['UPLOADED_PHOTOS_DEST'] + '/' + cat.image))
        db.session.delete(cat)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('addcat'))
