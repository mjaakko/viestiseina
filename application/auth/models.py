from application import db

association_table = db.Table('user_role', db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('account.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

class User(db.Model):
	__tablename__ = "account"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False)
	password = db.Column(db.String(50), nullable=False)
	posts = db.relationship("Post", backref="user", lazy=True)
	roles = db.relationship("Role", secondary=association_table, back_populates="users")

	def __init__(self, name, password):
		self.name = name
		self.password = password
		self.roles.append(Role.query.filter_by(name="USER").first())

	def get_id(self):
		return self.id

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def is_authenticated(self):
		return True

	def has_role(self, role):
		for user_role in self.roles:
			if user_role.name == role:
				return True
		return False


class Role(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(20), nullable=False, unique=True)
	users = db.relationship("User", secondary=association_table, back_populates="roles")

	def __init__(self, name):
		self.name = name
