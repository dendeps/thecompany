from thecompany_app import db
import uuid


class Department(db.Model):
    __tablename__ = 'department'

    # id of the department in the table
    id = db.Column(db.Integer, primary_key=True)

    #: UUID of the department
    uuid = db.Column(db.String(36), unique=True)

    # Name of the department
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name
        self.uuid = str(uuid.uuid4())

    def __repr__(self):
        return f"Department {self.name}"
