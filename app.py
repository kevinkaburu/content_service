from flask import Blueprint
from flask_restful import Api
from resources.Permission import permission
from resources.Role import role
from resources.User import user
from resources.Confirm import confirm
from resources.UserManager import login, user_update, change_password, sendmail

api_bp = Blueprint('user', __name__)
api = Api(api_bp)

# Routes
api.add_resource(permission,'/permission/', '/permission/<int:permission_id>')
api.add_resource(role,'/role/', '/role/<int:role_id>')
api.add_resource(user,'/', '/<int:user_id>')
api.add_resource(confirm,'/confirm/<string:jwt_token>')

api_bp.add_url_rule('/login/', 'login', login,methods=['POST'])
api_bp.add_url_rule('/sendmail/','sendmail', sendmail, methods=['POST'])
api_bp.add_url_rule('/update/', 'user_update', user_update,methods=['POST'])
api_bp.add_url_rule('/change_password/', 'change_password', change_password,methods=['POST'])




