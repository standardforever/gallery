from uuid import uuid4
from datetime import datetime
from app import app, db


class Message(db.Model):
    """ Add picture db Table
    """
    id = db.Column(db.String(120), primary_key=True)
    message = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(210), nullable=False)
    phone = db.Column(db.String(20), nullable=True)    
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
        picture = db.session.query(cls).order_by(cls.created_at.desc()).paginate(page=page, per_page=6)
        if (picture is None):
            return (None)
        return (picture) 

    @classmethod
    def delete(cls, id) -> None:
        """ Delete record form database
        """
        picture = db.session.query(cls).filter(cls.id == id).first()
        if (picture is not None):
            db.session.delete(picture)
            db.session.commit()



with app.app_context():   # all database operations under with
    db.create_all()

