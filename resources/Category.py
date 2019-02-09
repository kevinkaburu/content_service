from flask import request,  render_template, g
from flask import current_app
from flask_restful import Resource
from Model import db, Category, CategorySchema
import utils


categories_schema = CategorySchema(many=True)
category_schema = CategorySchema()

class category(Resource):

    def get(self,category_id=None,query=None):



        if category_id is None:
            categories = Category.query.all()
            return_data = categories_schema.dump(categories).data
            return {"status":"success","data":return_data},200
        elif query is not None:
            category = Category.query.filter(Category.category_name.like("%{0}%".format(query))).all()
            return_data = categories_schema.dump(category).data
            return {"status":"success","data":return_data},200

        category = Category.query.filter_by(category_id=category_id).first()
        return_data = category_schema.dump(category).data
        return {"status":"success","data":return_data},200


    @utils.login_required
    def post(self,category_id=None):
        request_data = request.get_json(force=True)
        if not request_data:
            return {"status":"fail","message":"Payload empty"},400

        data, errors = category_schema.load(request_data)
        if errors:
            return {"status":"fail","reasons":errors}, 422
        
        if category_id is not None:
            this_category = Category.query.filter_by(category_id=category_id).first()
            if 'category_name' in request_data:
                this_category.category_name = request_data['category_name']
            if 'parent_category_id' in request_data:
                this_category.parent_category_id = request_data['parent_category_id']
            db.session.commit()
            return_data = category_schema.dump(this_category).data
            return {"status":"success","data":return_data},201
        
        if 'category_name' not in request_data:
            return {"status":"fail","message":" Category Name needed"},400
        parent_category_id =0
        if 'parent_category_id' in request_data:
            parent_category_id =request_data['parent_category_id']

        this_category = Category.query.filter_by(category_name=request_data['category_name']).first()
        if this_category:
             return {"status":"fail",'message': 'Category already exists.','category':category_schema.dump(this_category).data}, 400

        
        
        category = Category(
            category_name = request_data['category_name'],
            parent_category_id=parent_category_id
        )
        db.session.add(category)
        db.session.commit()
        return_data = category_schema.dump(category).data
        return {"status":"success","data":return_data},201

        

