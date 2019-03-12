from flask import request, g
from flask import current_app
from flask_restful import Resource
from Model import db, Content, ContentSchema, Author, ContentType, Category, Contentcategory
import utils
import Aws


contents_schema = ContentSchema(many=True)
content_schema = ContentSchema()

class content(Resource):
    """This is where hot sex happens"""

    def get(self,content_id=None):
        if content_id is None:
            contents = Content.query.all()
            return_data = contents_schema.dump(contents).data
            return {'status':"sucess","data":return_data},200

        content = Content.query.filter_by(content_id=content_id).first()
        return_data = content_schema.dump(content).data
        return {'status':"sucess","data":return_data},200


    @utils.login_required
    def post(self,content_id=None):
        json_data = request.form
        if not json_data:
            return {"status":"fail","message":"Payload empty"},400
        

        data, errors = content_schema.load(json_data)
        if errors:
            return {"status":"fail","reasons":errors}, 422
        
        if int(g.user['user']['user_id']) is not int(json_data['user_id']):
            return {"status":"fail","message":"User not allowed to perform this request."}, 422

        if 'extention' not in json_data:
            return {"status":"fail","message":"Extention needed."}, 422


        """Check if the author exists"""
        the_author = Author.query.filter_by(author_id=json_data['author_id']).first()
        if not the_author:
            return {"status":"fail","message":"The author  {0} does not exists.".format(json_data['author_id'])}, 422

        """Check if the content_type_id exists"""
       
        content_type = ContentType.query.filter_by(content_type_id= json_data['content_type_id']).first()
        if not content_type:
            return {"status":"fail","message":"The content_type  {0} does not exists.".format(json_data['content_type_id'])}, 422

        
        content = Content(
            json_data['content_title'],
            json_data['content_type_id'],
            json_data['author_id'],
            json_data['user_id'],
            json_data['summary']
            )
        db.session.add(content)
        db.session.commit()
        db.session.flush()
        aws_data = Aws.uplink(json_data['user_id'],json_data['extention'],content.content_id)
        content.content_key = aws_data['content_key']
        content.cover_key = aws_data['cover_key']
        """Lets work on those categories"""
        categories = json_data['category_ids']
        is_categories = False
        for category_id in  categories.split(","):
            category = Category.query.filter_by(category_id=category_id).first()
            if category:
                is_categories =True
                content_category = Contentcategory(content.content_id,category_id)
                db.session.add(content_category)
        if not is_categories:
            return {"status":"fail","message":"categories [ {0} ] does not exists.".format(json_data['category_ids'])}, 422

        db.session.commit()
        cover_url = Aws.downlink(aws_data['cover_key'])

        content_data = content_schema.dump(content).data
        return {"status":"success","content":content_data,"content_upload":aws_data['content_url'],"cover_upload":aws_data['cover_url'],"cover_link":cover_url},201