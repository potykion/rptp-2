from rptp.common.models import ActressProxy
from web_app import db


class Actress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.Integer, default=0)
    name = db.Column(db.String(80))
    image = db.Column(db.String(80))
    debut_year = db.Column(db.Integer)
    url = db.Column(db.String(80))

    def __init__(self, **kwargs):
        for field, value in kwargs.items():
            setattr(self, field, value)

    @classmethod
    def create_from_json(cls, actress_json):
        """
        Create actress from json.
        :param actress_json: Actress json, example:
        {
            "priority": 0,
            "name": "Kandi Quinn",
            "image": "/images/models/kandi-quinn.jpg",
            "debut_year": 2017,
            "url": "/model/kandi-quinn.html"
        }

        :return: New actress
        """

        exists = db.session.query(db.exists().where(Actress.url == actress_json['url'])).scalar()
        if not exists:
            actress = cls(**actress_json)
            db.session.add(actress)
            db.session.commit()
            return actress


class ActressManager(ActressProxy):
    def fetch(self):
        return Actress.query.all()

    def serialize(self, actress):
        return {
            "priority": actress.priority,
            "name": actress.name,
            "image": actress.image,
            "debut_year": actress.debut_year,
            "url": actress.url
        }