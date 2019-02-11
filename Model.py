from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()

class ContentType(db.Model):
    __tablename__ = "content_type"
    content_type_id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.Boolean,nullable=False)
    content_type = db.Column(db.String(80),nullable = False)
    created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    modified = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self,content_type,status):
        self.content_type = content_type
        self.status = status

class ContentTypeSchema(ma.Schema):
    content_type_id =  fields.Integer(dump_only=True)
    content_type = fields.String(required=True, validate=validate.Length(1))
    status =  fields.Boolean(required=False)
    created = fields.DateTime()
    modified = fields.DateTime()

    class Meta:
        fields = ('content_type_id','content_type')



class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(80),nullable = False)
    parent_category_id = db.Column(db.Integer, nullable=True)
    created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    modified = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self,category_name,parent_category_id=0):
        self.category_name = category_name
        self.parent_category_id = parent_category_id

class CategorySchema(ma.Schema):
    category_id = fields.Integer(dump_only=True)
    category_name = fields.String(required=True, validate=validate.Length(1))
    parent_category_id = fields.Integer(required=False)
    created = fields.DateTime()
    modified = fields.DateTime()

    class Meta:
        fields = ('category_id','category_name','parent_category_id',)




class Author(db.Model):
    __tablename__ = 'author'
    author_id = db.Column(db.Integer, primary_key = True)
    author_name = db.Column(db.String(80),nullable = False)
    user_id = db.Column(db.Integer,nullable = False)
    status = db.Column(db.Boolean,nullable=False)
    created = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    modified = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)


    def __init__(self,author_name,status,user_id):
        self.author_name =author_name
        self.status = status
        self.user_id =user_id
  

class AuthorSchema(ma.Schema):
    author_id = fields.Integer(dump_only=True)
    user_id= fields.Integer(required=True)
    author_name = fields.String(required=True, validate=validate.Length(1))
    status =  fields.Boolean(required=False)
    created = fields.DateTime()
    modified = fields.DateTime()

    class Meta:
        fields = ('author_id','author_name','status','user_id')
