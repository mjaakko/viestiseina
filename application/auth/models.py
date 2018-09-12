class User(db.Model):
	__tablename__ = "account"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	posts = db.relationship("Post", backref="user", lazy=True)

	def __init__(self, name):
		self.name = name
