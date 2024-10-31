from shop import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin
import json
from sqlalchemy.orm import Mapped, mapped_column


@login_manager.user_loader
def user_loader(user_id):
    return Register.query.get(user_id)

class Register(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    country: Mapped[str]
    city: Mapped[str]
    contact: Mapped[str]
    address: Mapped[str]
    zipcode: Mapped[str]
    profile: Mapped[str] = mapped_column(default='profile.jpg')
    date_created: Mapped[datetime] = mapped_column(default=datetime.now)

    def __repr__(self):
        return '<Register %r>' % self.name


class JsonEcodedDict(db.TypeDecorator):
    impl = db.Text
    def process_bind_param(self, value, dialect):
        if value is None:
            return '{}'
        else:
            return json.dumps(value)
    def process_result_value(self, value, dialect):
        if value is None:
            return {}
        else:
            return json.loads(value)

class CustomerOrder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invoice = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    customer_id = db.Column(db.Integer, unique=False, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    orders = db.Column(JsonEcodedDict)

    def __repr__(self):
        return'<CustomerOrder %r>' % self.invoice



with app.app_context():
    db.create_all()




    


