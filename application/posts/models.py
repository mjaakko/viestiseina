from application import db

from sqlalchemy.sql import text, desc
from sqlalchemy.orm import backref

from datetime import datetime, timedelta

association_table = db.Table('post_hashtag', db.Model.metadata,
    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
    db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id'))
)

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	# Parent id is the id of the post this post is a reply to
	parent_id = db.Column(db.Integer, db.ForeignKey("post.id"))
	create_time = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
	modify_time = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
	content = db.Column(db.String(3000), nullable=False)
	replies = db.relationship("Post", backref=backref("parent", remote_side=id), cascade="all, delete-orphan", order_by= lambda: desc(Post.create_time))
	hashtags = db.relationship("Hashtag",
		secondary=association_table,
		back_populates="posts")

	def __init__(self, user_id, content, reply_to):
		self.user_id = user_id
		self.content = content
		self.hashtags = list(map(lambda hashtag: Hashtag.get_or_create(name=hashtag), filter(lambda word: word.startswith("#") and len(word) <= 40, content.split())))
		self.parent_id = reply_to

	# Finds the first post in the thread
	def find_top(self):
		if self.parent:
			return self.parent.find_top()
		else:
			return self

	def reply_count(self):
		stmt = text("""WITH RECURSIVE replies AS (
					SELECT id, parent_id, id as root_id
					FROM post
					WHERE root_id IS :post_id
					UNION ALL
					SELECT c.id, c.parent_id, p.root_id
					FROM post c
					JOIN replies p ON c.parent_id = p.id
				) SELECT root_id AS post_id, count(*) AS reply_count FROM replies WHERE id <> root_id""").params(post_id = self.id)
		res = db.engine.execute(stmt)

		return res.fetchone()['reply_count']

class Hashtag(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(40), nullable=False, unique=True)
	posts = db.relationship("Post",
		secondary=association_table,
		back_populates="hashtags", order_by= lambda: desc(Post.create_time))

	def __init__(self, name):
		self.name = name

	@staticmethod
	def get_or_create(**kwargs):
		instance = Hashtag.query.filter_by(**kwargs).first()
		if instance:
			return instance
		else:
			instance = Hashtag(**kwargs)
			db.session.add(instance)
			db.session.commit()
			return instance

	@staticmethod
	def get_total_hashtag_counts():
		stmt = text("SELECT hashtag.id, hashtag.name, COUNT(hashtag.id) FROM hashtag, post_hashtag, post WHERE hashtag.id = post_hashtag.hashtag_id AND post_hashtag.post_id = post.id GROUP BY hashtag.id ORDER BY COUNT(hashtag.id) DESC")
		res = db.engine.execute(stmt)
		
		response = []
		for row in res:
			response.append({"id": row[0], "name": row[1], "count": row[2]})

		return response

	@staticmethod
	def get_trending_hashtags(days, count):
		time = datetime.now() - timedelta(days=days)
		stmt = text("SELECT hashtag.id, hashtag.name, COUNT(hashtag.id) FROM hashtag, post_hashtag, post WHERE hashtag.id = post_hashtag.hashtag_id AND post_hashtag.post_id = post.id AND post.create_time >= :time GROUP BY hashtag.id ORDER BY COUNT(hashtag.id) DESC LIMIT :count").params(time = time.strftime('%Y-%m-%d %H:%M:%S'), count = count)
		res = db.engine.execute(stmt)
		
		response = []
		for row in res:
			response.append({"id": row[0], "name": row[1], "count": row[2]})

		return response
