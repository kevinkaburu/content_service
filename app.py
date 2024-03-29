from flask import Blueprint
from flask_restful import Api
from resources.Author import author
from resources.Category import category
from resources.ContentType import content_type
from resources.Content import content

api_bp = Blueprint('content', __name__)
api = Api(api_bp)

# Routes
api.add_resource(author,'/author/', '/author/<int:author_id>', '/author/<string:query>')
api.add_resource(category,'/category/', '/category/<int:category_id>','/category/<string:query>')
api.add_resource(content_type,'/content_type/','/content_type/<int:content_type_id>')
api.add_resource(content,'/','/<int:content_id>')


# api_bp.add_url_rule('/sendmail/','sendmail', sendmail, methods=['POST'])
# api_bp.add_url_rule('/update/', 'user_update', user_update,methods=['POST'])
# api_bp.add_url_rule('/change_password/', 'change_password', change_password,methods=['POST'])




