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
        return f"Department: {self.name}, uuid: {self.uuid}"

    def check_if_exists(self):
        department = db.session.query(Department).filter_by(name=self.name).first()
        if department is None:
            return False
        else:
            return True

    @classmethod
    def find_by_name(self, name: str):
        department = db.session.query(Department).filter_by(name=name).first()
        return department

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()




    @classmethod
    def get_all(cls):
        return db.session.query(Department).all()

    @classmethod
    def get_department(cls, uuid):
        department = db.session.query(Department).filter_by(uuid=uuid).first()
        if department is None:
            raise ValueError('Invalid department uuid')
        return department

    @classmethod
    def delete_department(cls, uuid):
        department = cls.get_department(uuid)
        if department is None:
            raise ValueError('Invalid department uuid')
        db.session.delete(department)
        db.session.commit()
