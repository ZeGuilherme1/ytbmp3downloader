from flask import Flask, request, send_file, jsonify, Response
from flask_cors import CORS
import yt_dlp
import os
import uuid

app = Flask(__name__)
CORS(app)

registered_files = {}

@app.route("/url", methods=['POST'])
def sendurl():
    global registered_files
    form = request.form
    if 'url' not in form:
        return 'Missing url'
    
    url = request.form['url'] 
    ytdl_options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ytdl_options) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info).replace('.webm', '.mp3')
        file_id = str(uuid.uuid4())
        registered_files[file_id] = filename

    return {"id": file_id, "filename": filename}, 200

@app.route("/download", methods=['GET'])
def download():
    global registered_files
    # localhost:5050/download?id=meuid
    file_id = request.args.get('id')
    if not file_id:
        return Response(response="Missing ID", status=400)

    if file_id not in registered_files.keys():
        return Response(response="ID was not processed yet", status=400)

    return send_file(registered_files[file_id])

