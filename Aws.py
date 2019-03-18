from flask import request, jsonify, request, make_response, current_app, g
import uuid
import boto3
from botocore.client import Config
import utils


def uplink( user_id, extention, content_id):

    if int(g.user['user']['user_id']) is not int(user_id):
            return {"status": "fail", "message": "User not allowed to perform this request."}, 422
    s3 = boto3.client('s3', aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
                      aws_secret_access_key=current_app.config['AWS_SECRET'],
                      region_name=current_app.config['AWS_REGION'],
                      config=Config(s3={'addressing_style': 'path'}, signature_version='s3v4'))
    uid = uuid.uuid4()
    content_key = "{}-{}.{}".format(content_id, user_id, extention)
    cover_key = "cover/{}".format(content_id,)
    content_url = s3.generate_presigned_url(ClientMethod='put_object', Params={
                                            'Bucket': current_app.config['AWS_BUCKET'], 'Key': content_key}, ExpiresIn=1800)
    cover_url = s3.generate_presigned_url(ClientMethod='put_object', Params={
                                          'Bucket': current_app.config['AWS_BUCKET'], 'Key': cover_key}, ExpiresIn=1800)
    return {"status": "sucess", "content_url": content_url, "content_key": content_key, "cover_key": cover_key, "cover_url": cover_url}




def downlink( content_key):

    
    s3 = boto3.client('s3', aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
                      aws_secret_access_key=current_app.config['AWS_SECRET'],
                      region_name=current_app.config['AWS_REGION'],
                      config=Config(s3={'addressing_style': 'path'}, signature_version='s3v4'))
    
    url = s3.generate_presigned_url(ClientMethod='get_object', Params={
                                          'Bucket': current_app.config['AWS_BUCKET'], 'Key': content_key}, ExpiresIn=3600)
    return url

