import os
import whisper
import ffmpeg

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from transcriber.auth import login_required
from transcriber.db import get_db

bp = Blueprint('transcriber', __name__)

ALLOWED_EXTENSIONS = {'mp3', 'wav', 'aac', 'flac', 'm4a'}


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


@bp.route('/history')
def history():
    user_id = session.get('user_id')
    user_id = str(user_id)
    db = get_db()
    record = db.execute("SELECT id, created, transcription FROM files WHERE user_id = ?", user_id)
    db.commit
    return render_template('transcriber/history.html', record=record)


@bp.route('/settings', methods=('GET', 'POST'))
def settings():
    # If not logged in show home page, otherwise show settings page
    user_id = session.get('user_id')
    if user_id is None:
        return render_template('transcriber/index.html')

    if request.method == 'POST':
        form_id = request.form['form_id']
        if form_id == '1':
            password = request.form['password']
            password_verify = request.form['password-verify']
            
            # Check for missing fields
            if not password:
                return redirect('/gerror')
            elif not password_verify:
                return redirect('/gerror')

            # Check for matching passwords
            if password != password_verify:
                return redirect('/gerror')

            # Update database with new password_hash
            db = get_db()
            db.execute("UPDATE user SET password = ? WHERE id = ?", (generate_password_hash(password), user_id))
            db.commit()
            return redirect('/')

        if form_id == '2':
            db = get_db()
            user_id = str(user_id)
            db.execute("DELETE FROM user WHERE id = ?", (user_id))
            db.commit()
            # Check for checked box
            if request.form['confirm-delete'] == True:
                return render_template('transcriber/process.html')

    return render_template('transcriber/settings.html')


@bp.route('/process')
def process():
    return render_template('transcriber/process.html')


@bp.route('/error')
def error():
    return render_template('transcriber/error.html')


@bp.route('/gerror')
def gerror():
    return render_template('transcriber/general_error.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS