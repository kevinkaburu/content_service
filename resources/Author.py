from flask import request,  render_template, g
from flask import current_app
from flask_restful import Resource
from Model import db, Author, AuthorSchema
import utils


authors_schema = AuthorSchema(many=True)
author_schema = AuthorSchema()

class author(Resource):

    @utils.login_required
    def delete(self,author_id=None):
        if author_id is None:
            return {"status":"fail","message":"AuthorId needed"},400

        this_author = Author.query.filter_by(author_id=author_id).first()
        this_author.status=False
        db.session.commit()
        author_data = author_schema.dump(this_author).data
        return {"status":"success","data":author_data},201







    @utils.login_required
    def post(self,author_id=None):
        json_data = request.get_json(force=True)
        #{'exp': 1550758701, 'iat': 1549549101, 'function': 'auth', 'user': {'user_id': 40, 'status': True, 'role': {'role_name': 'Admin', 'role_id': 1}}}

        if not json_data:
            return {"status":"fail","message":"Payload empty"},400
        

        data, errors = author_schema.load(json_data)
        if errors:
            return {"status":"fail","reasons":errors}, 422
        
        if int(g.user['user']['user_id']) is not int(json_data['user_id']):
            return {"status":"fail","message":"User not allowed to perform this request."}, 422

        if author_id is not None:
            this_author = Author.query.filter_by(author_id=author_id).first()
            if 'status' in data:
                this_author.status =bool(data['status'])
            if 'author_name' in data:
                this_author.author_name = data['author_name']
            db.session.add(this_author)
            db.session.commit()
            author_data = author_schema.dump(this_author).data
            return {"status":"success","data":author_data},201
            



        
        this_author = Author.query.filter_by(author_name=data['author_name'],status= True).first()
        if this_author:
            return {"status":"fail",'message': 'Author already exists.','author':author_schema.dump(this_author).data}, 400
        
        this_author = Author(
            author_name=data['author_name'],
            status=True,
            user_id=json_data['user_id']
        )
        db.session.add(this_author)
        db.session.commit()
        author_data = author_schema.dump(this_author).data
        return {"status":"success","data":author_data},201


    def get(self,author_id=None,query=None):
        """Query for all authors or specific author"""
        if author_id is not None:
            author = Author.query.filter_by(author_id=author_id).first()
            author_data = author_schema.dump(author).data
        elif query is not None:
            authors = Author.query.filter(Author.author_name.like("%{0}%".format(query))).all()
            author_data = authors_schema.dump(authors).data
         
        else:
            authors = Author.query.all()
            author_data = authors_schema.dump(authors).data
    
        return {"status":"success","data":author_data},200

    


        
