import os
import whisper
import ffmpeg

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from datetime import datetime

from transcriber.auth import login_required
from transcriber.db import get_db

bp = Blueprint('transcriber', __name__)

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'aac', 'flac'}


@bp.route('/', methods=('GET', 'POST'))
def index():
    user_id = session.get('user_id')
    # If not logged in show home page, otherwise show upload page
    if user_id is None:
        return render_template('transcriber/index.html')
    # Else return upload
    else:
        #return redirect('file/upload.html')
        return render_template('transcriber/upload.html')


@bp.route('/transcript', methods=('GET', 'POST'))
def transcript():
    if request.method == 'POST':
        # Get file from html form
        file = request.files['file']
        # Check for valid file
        if file.filename == '':
            return redirect('/error')
        # Check for allowed file
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            # Save file to disk
            user_id = session.get('user_id')
            date = datetime.now()
            # Cleanses the filename before saving to disk
            file.filename = secure_filename(file.filename)
            file.filename = str(user_id) + '_' + str(date) + file.filename
            file.save(os.path.join(current_app.instance_path, 'uploads', file.filename))

            # Perform transcription
            model = whisper.load_model("base")
            audio = whisper.load_audio(current_app.instance_path + '/uploads/' + file.filename)
            result = model.transcribe(audio)
            transcription = result["text"]

            # Record to database
            db = get_db()
            db.execute("INSERT INTO files (user_id, file_name, transcription) VALUES (?, ?, ?)", (user_id, file.filename, transcription))
            db.commit()
        else:
            return redirect('/error')
    return render_template('transcriber/transcript.html', transcription=transcription)


@bp.route('/process', methods=('GET', 'POST'))
def process():
    return render_template('transcriber/process.html')


@bp.route('/error')
def error():
    return render_template('transcriber/error.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS