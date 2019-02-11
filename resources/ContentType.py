from flask import request,  render_template, g
from flask import current_app
from flask_restful import Resource
from Model import db, ContentType, ContentTypeSchema
import utils


content_types_schema = ContentTypeSchema(many=True)
content_type_schema = ContentTypeSchema()


class content_type(Resource):

    @utils.login_required
    def post(self,content_type_id=None):

        request_data = request.get_json(force=True)
        if not request_data:
            return {"status":"fail","message":"Payload empty"},400

        data, errors = content_type_schema.load(request_data)
        if errors:
            return {"status":"fail","reasons":errors}, 422
        
        if content_type_id is not None:
            content_type = ContentType.query.filter_by(content_type_id= content_type_id).first()
            if not content_type:
                return {"status":"fail","message":"No content type with that ID."},402
            
            if 'content_type' in request_data:
                content_type.content_type = request_data['content_type']
            if 'status' in request_data:
                content_type.status - bool(request_data['status'])
            
            db.session.commit()
            return_data = content_type_schema.dump(content_type).data
            return {"status":"success",'data':return_data},201

        if 'content_type' not in request_data:
            return {"status":"fail","message":" Content_type expected."},400

        content_type = ContentType.query.filter_by(content_type=request_data['content_type']).first()
        if content_type:
            return {"status":"fail",'message': 'Content type already exists.','category':content_type_schema.dump(content_type).data}, 400
        
        content_type = ContentType(content_type=request_data['content_type'],status=True)
        db.session.add(content_type)
        db.session.commit()
        return_data = content_type_schema.dump(content_type).data
        return {"status":"success","data":return_data},201


    def get(self,content_type_id=None):
        if content_type_id is None:
            content_types = ContentType.query.all()
            return_data = content_types_schema.dump(content_types).data
            return {'status':"sucess","data":return_data},200

        content_type = ContentType.query.filter_by(content_type_id=content_type_id).first()
        return_data = content_type_schema.dump(content_type).data
        return {'status':"sucess","data":return_data},200



            

       

