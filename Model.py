from flask import Flask, current_app
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import Aws;


ma = Marshmallow()
db = SQLAlchemy()


class Contentcategory(db.Model):
    __tablename__ = "content_category"
    content_category_id = db.Column(db.Integer, primary_key = True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.content_id', ondelete='CASCADE'), nullable =False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id', ondelete='CASCADE'), nullable =False)
    
    def __init__(self,content_id,category_id):
        self.content_id = content_id
        self.category_id = category_id


class ContentcategorySchema(ma.Schema):
    content_category_id =  fields.Integer(dump_only=True)
    content_id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    content = fields.Nested('ContentSchema', many=True, only=('content_id', 'content_key','summary','cover_key','author_id','content_title'))
    category = fields.Nested('CategorySchema', many=True, only=('category_id', 'category_name','parent_category_id',))



class Content(db.Model):
    """The monster/beast is here"""
    __tablename__ = "content"

    content_id = db.Column(db.Integer, primary_key = True)
    content_title = db.Column(db.String(160),nullable = False)
    content_type_id = db.Column(db.Integer, db.ForeignKey('content_type.content_type_id', ondelete='CASCADE'), nullable =False)
    author_id = db.Column(db.Integer, db.ForeignKey('author.author_id', ondelete='CASCADE'), nullable =False)
    user_id = db.Column(db.Integer,nullable = False)
    cover_key =  db.Column(db.String(160))
    content_key = db.Column(db.String(160))
    summary = db.Column(db.Text)

    def __init__(self,content_title,content_type_id,author_id,user_id,summary=''):
        self.author_id =author_id
        self.content_title = content_title
        self.user_id = user_id
        self.content_type_id = content_type_id
        self.summary = summary


class ContentSchema(ma.Schema):
    content_id = fields.Integer(dump_only=True)
    content_title = fields.String(required=True, validate=validate.Length(2))
    cover_key = fields.String(required=False, validate=validate.Length(2))
    content_key = fields.String(required=False, validate=validate.Length(2))
    summary = fields.String(required=True, validate=validate.Length(10))
    content_type_id = fields.Integer(required=True)
    author_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    content_type = fields.Nested('ContentTypeSchema', many=False, only=('content_type_id', 'content_type',))
    author = fields.Nested('AuthorSchema', many=False, only=('author_id', 'author_name',))
    content_categories = fields.Nested('ContentcategorySchema', many=True, only=('content_category_id', 'category_id',))
    #cover_url = Aws.downlink(cover_key,current_app._get_current_object())

    class Meta:
        fields = ('content_id','content_title','summary','content_type','author','content_categories')






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
