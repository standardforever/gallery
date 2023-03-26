# from sqlalchemy import Column, String, Text, DateTime
from uuid import uuid4
from datetime import datetime
from app import app, db

""" Db for addPicture
"""


class AddPicture(db.Model):
    """ Add picture db Table
    """
    id = db.Column(db.String(120), primary_key=True)
    text = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(210), nullable=False)
    category_id = db.Column(db.String(120), db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', backref=db.backref('addpicture', lazy=True))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def create(cls, **kwargs) -> None:
        """ Create record
        """
        kwargs['id'] = uuid4().hex
        new_picture = cls(**kwargs)
        db.session.add(new_picture)
        db.session.commit()

    @classmethod
    def update(cls, **kwargs) -> None:
        """ Update record from database
        """
        picture = db.session.query(cls).filter(cls.id == kwargs.get("id")).first()
        if (picture == None):
            return (None)
        picture(**kwargs)
        db.session.commit()

    @classmethod
    def delete(cls, id) -> None:
        """ Delete record form database
        """
        picture = db.session.query(cls).filter(cls.id == id).first()
        if (picture is not None):
            db.session.delete(picture)
            db.session.commit()

    @classmethod
    def get(cls, id):
        """ Get a record by ID
        """
        picture = db.session.query(cls).filter(cls.id == id).first()
        if (picture is None):
            return (None)
        return (picture) 

    @classmethod
    def get_all(cls, page):
        """ Get a record by ID
        """
        picture = db.session.query(cls).order_by(cls.created_at.desc()).paginate(page=page, per_page=5)
        if (picture is None):
            return (None)
        return (picture) 


class Category(db.Model):
    """ Add picture db Table
    """
    id = db.Column(db.String(120), primary_key=True)
    category = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


    @classmethod
    def create(cls, **kwargs) -> None:
        """ Create record
        """
        kwargs['id'] = uuid4().hex
        new_picture = cls(**kwargs)
        db.session.add(new_picture)
        db.session.commit()

    @classmethod
    def update(cls, **kwargs) -> None:
        """ Update record from database
        """
        picture = db.session.query(cls).filter(cls.id == kwargs.get("id")).first()
        if (picture == None):
            return (None)
        picture(**kwargs)
        db.session.commit()

    @classmethod
    def delete(cls, id) -> None:
        """ Delete record form database
        """
        picture = db.session.query(cls).filter(cls.id == id).first()
        if (picture is not None):
            db.session.delete(picture)
            db.session.commit()

    @classmethod
    def get(cls, id):
        """ Get a record by ID
        """
        picture = db.session.query(cls).filter(cls.id == id).first()
        if (picture is None):
            return (None)
        return (picture) 

    @classmethod
    def get_all(cls):
        """ Get a record by ID
        """
        picture = db.session.query(cls).all()
        if (picture is None):
            return (None)
        return (picture)

    @classmethod
    def save(cls):
        db.session.commit()

with app.app_context():   # all database operations under with
    db.create_all()
