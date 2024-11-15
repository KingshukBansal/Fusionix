import os, gridfs, pika, json
from flask import Flask,request, send_file
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from bson import ObjectId
from storage import util
from flask_cors import CORS


server = Flask(__name__)
CORS(server)

mongo_video = PyMongo(server,uri="mongodb://host.minikube.internal:27017/videos")
mongo_mp3 = PyMongo(server,uri="mongodb://host.minikube.internal:27017/mp3s")


fs_videos = gridfs.GridFS(mongo_video.db)
fs_mp3s = gridfs.GridFS(mongo_mp3.db)


connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
channel = connection.channel()


@server.route('/register',methods=(['POST']))
def register():
    text, err = access.register(request)

    if not err:
        return "Successfully Registered",200
    else:
        return f"Error: {err}",401
    

@server.route('/login',methods=(['POST']))
def login():
    token, err = access.login(request)

    if not err:
        return token,200
    else:
        print(f"Login Error:{err}")
        return f"Invalid Credentials:{err}",401
    
@server.route('/upload',methods=(['POST']))
def upload():
    access,err = validate.token(request)
    if err:
        return err
    if access:
        access = json.loads(access)
    else:
        return "Not Authorized",401
    if access["admin"]:
        if len(request.files) > 1 or len(request.files)<1 :
            return "Only 1 file required",400
        
        for _,f in request.files.items():
            err = util.upload(f,fs_videos,channel,access)

            if err:
                return err
        return "success!",200
    else:
        return "Not Authorized",401

@server.route('/download',methods=(['GET']))
def download():
    access,err = validate.token(request)
    if err:
        return err, 401
    if access:
        access = json.loads(access)
    else:
        return "Not Authorized",401
    if access["admin"]:
        fid_string = request.args.get("fid")

        if not fid_string:
            return "fid is required",400
        try:
            out = fs_mp3s.get(ObjectId(fid_string))
            return send_file(out,download_name=f"{fid_string}.mp3")
        except Exception as err:
            print(err)
            return f"Download internal server error:{err}",500
    else:
        return "Not Authorized",401

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=8080)