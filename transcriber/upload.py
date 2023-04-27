import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.utils import secure_filename

from transcriber.db import get_db

bp = Blueprint('upload', __name__, url_prefix='/upload')


@bp.route('/upload', methods=('GET', 'POST'))
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename != '':
            f.save(os.path.join(app.instance_path, 'transcriber', secure_filename(f.filename)))
            return 'file uploaded successfully'


    return render_template('transcriber/transcript.html')