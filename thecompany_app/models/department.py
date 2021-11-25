from thecompany_app import db


class Department(db.Model):
    __tablename__ = 'department'

    # id of the department in the table
    id = db.Column(db.Integer, primary_key=True)

    # Name of the department
    name = db.Column(db.String())

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Department {self.name}"
