from application import db

association_table = Table('post_hashtag', db.Model.metadata,
    db.Column('post_id', Integer, db.ForeignKey('post.id')),
    db.Column('hashtag_id', Integer, db.ForeignKey('hashtag.id'))
)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	# Parent id is the id of the post this post is a reply to
	parent_id = db.Column(db.Integer, db.ForeignKey("post.id"))
	create_time = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
	modify_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
	content = db.Column(db.String(3000), nullable=False)
	replies = db.relationship("Post", cascade="all, delete-orphan")
        hashtags = db.relationship("Hashtag",
		secondary=association_table,
		back_populates="posts")

	def __init__(self, user_id, content, reply_to):
		self.user_id = user_id
		self.content = content
		self.parent_id = reply_to

class Hashtag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(40), nullable=False, unique=True)
        posts = db.relationship("Parent",
               secondary=association_table,
               back_populates="hashtags")

        def __init__(self, name):
                self.name = name
