from flask import Flask,request,jsonify,send_file
from flask_cors import CORS
from chat import chat
from transcription_service import create_transcript_whisperx
import uuid 
import threading
import os
import logging

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB limit
CORS(app,origins=["http://localhost:3000"])
logging.basicConfig(filename='output.log', level=logging.INFO)


ALLOWED_EXTENSIONS = {'mp4'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/upload",methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"messege" : "Please Input File"}),400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file and allowed_file(file.filename) and file.seek(0,os.SEEK_END) <= app.config['MAX_CONTENT_LENGTH']:
        
        # Replace back the pointer to the starting
        file.seek(0,os.SEEK_SET)
        
        filename = file.filename
        unique_ext = str(uuid.uuid1()) + ".mp4"
        
        # Audio File path
        audio_file_path = app.config['UPLOAD_FOLDER']+"/"+unique_ext

        # Save the file to file System 
        file.save(audio_file_path)
        
        # Initialize the Transcription thread
        transcription_thread  = threading.Thread(target=create_transcript_whisperx,args=(audio_file_path,))
        
        # Start the Transcription Thread
        transcription_thread.start()
        
        return jsonify({'message': 'File successfully uploaded', 'filename': unique_ext}), 200
    
    else:
        return jsonify({'message': 'Only Mp4 is Allowed'}), 400
    

@app.route("/chat",methods=['POST'])
def chat_video():
    
    # Check if the id Exist in the From
    if 'id' not in request.form:
        return jsonify({"messege" :  "Please Input the ID you want to chat with"}),400
    
    # Check if the id is Null
    if request.form['id'] == '':
        return jsonify({"messege" : "Please Input the Id"}),400
    
    # Fetch the Id from the Request Body
    video_id  = request.form['id']
    
    # Check if the video Exist for the inputted id
    if not os.path.exists(f'./uploads/{video_id}.mp4'):
        return jsonify({"messege" : "Video Does not Exist"}),400
    
    # Check if transcription have been processed or not
    if not os.path.exists(f'./uploads/{video_id}.txt'):
        return jsonify({"messege" : "Please Wait Video is getting Proccessed..."}),400
    
    # Check Whether the status file Exist from ingestion
    if os.path.exists(f'./db/{video_id}.txt'):
        return jsonify({"messege" : "Video Will be shortly available for Chat"}),400
    
    # Check if Prompt Exist in form
    if 'prompt' not in request.form:
        return jsonify({"messege" :  "Please Input a prompt"}),400
    
    # Check if Prompt is Null or not
    if request.form['prompt'] == '' :
        return jsonify({"messege" :  "Please Input a prompt"}),400
    
    # Call the chat service
    response = chat(video_id=video_id,prompt=request.form['prompt'])
    
    # Return the JSON
    return jsonify({"response" : response}),200    



    
@app.route("/transcription",methods=['POST'])
def get_transcription():
    # Check if the id Exist in the From
    if 'id' not in request.form:
        return jsonify({"messege" :  "Please Input the ID you want to transcription of"}),400
    
    # Check if the id is Null
    if request.form['id'] == '':
        return jsonify({"messege" : "Please Input the Id"}),400
    
    # Fetch the Id from the Request Body
    video_id  = request.form['id']
    
    # Check If transcription Exist or not
    if not os.path.exists(f'./uploads/{video_id}.txt'):
        return jsonify({"messege" : "Transcription Does not Exist Yet"}),400
    
    # Get the Transcript from file
    transcript = ""
    with open(f'./uploads/{video_id}.txt', 'r') as f:
            transcript = f.read()
            f.close()
            
    # Return the Response
    return jsonify({"transcript" : transcript}),200
    

    
    
@app.route("/getVideo/<id>",methods=['GET'])
def get_video(id):
    if not os.path.exists(f'./uploads/{id}.mp4'):
        return "File Not Found",404
    return send_file(f'./uploads/{id}.mp4')