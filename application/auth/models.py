from application import db

class User(db.Model):
	__tablename__ = "account"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	posts = db.relationship("Post", backref="user", lazy=True)

	def __init__(self, name):
		self.name = name

	def get_id(self):
		return self.id

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True
