from flask import request, jsonify, request, make_response, current_app, g
import boto3
import utils


@utils.resource_login_required
def uplink():

    json_data = request.get_json(force=True)
    if 'user_id' not in json_data:
        return jsonify({"status":"fail","reasons":"User required"}),422

    if int(g.user['user']['user_id']) is not int(json_data['user_id']):
            return {"status":"fail","message":"User not allowed to perform this request."}, 422
    
    

    s3_con = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY'], 
        aws_secret_access_key=current_app.config['AWS_SECRET'],
        config=Config(signature_version='s3v4'), 
        region_name=AWS_SETUP['S3']['region']
    )
    url = s3_con.generate_presigned_url(
        'put_object', Params={
            'Bucket':AWS_SETUP['S3']['audio.log'], 
            'Key':key,
            'ContentType':'image/jpg'
        },
        ExpiresIn=AWS_SETUP['S3']['expiresInsecs'],
        HttpMethod='PUT'
    )
    return jsonify({"status":"sucess","url":url}),200
