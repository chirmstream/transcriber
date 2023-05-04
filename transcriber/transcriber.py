import os
#import whisper

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.exceptions import abort
from werkzeug.utils import secure_filename
from datetime import datetime

from transcriber.auth import login_required
from transcriber.db import get_db

bp = Blueprint('transcriber', __name__)

ALLOWED_EXTENSIONS = {'mp3', 'flac', 'wav', 'pdf', 'zip'}


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


@bp.route('/process', methods=('GET', 'POST'))
def process():
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
            file.filename = str(user_id) + '_' + str(date) + file.filename
            file.save(os.path.join(current_app.instance_path, 'uploads', file.filename))

            # Perform transcription
            #model = whisper.load_model("base")
            #audio = whisper.load_audio("OSR_us_000_0010_8k.wav")
            #result = model.transcribe(audio)
            #transcription = result["text"]
            transcription = "this is a transcript"

            # Record to database
            db = get_db()
            db.execute("INSERT INTO files (user_id, file_name, transcription) VALUES (?, ?, ?)", (user_id, file.filename, transcription))
            db.commit()

        else:
            return redirect('/error')


        


    return render_template('transcriber/process.html',)





@bp.route('/transcript', methods=('GET', 'POST'))
def transcript():
    return render_template('transcriber/transcript.html')


@bp.route('/error')
def error():
    return render_template('transcriber/error.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Convert images or files data to binary format
def convert_data(file_name):
    with open(file_name, 'rb') as file:
        binary_data = file.read()
    return binary_data

    





















@bp.route('/blog')
def blog():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('transcriber.index'))

    return render_template('blog/create.html')


def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    return post


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('transcriber.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('transcriber.index'))