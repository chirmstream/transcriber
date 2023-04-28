import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'transcriber.sqlite'),
        
        #UPLOAD_FOLDER=os.path.config(app.instance_path['UPLOAD_FOLDER'], 'instance/files'),
        
        #UPLOAD_FOLDER = os.path.join(path, 'uploads')
        #UPLOAD_FOLDER = 'instance/files',
        #app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
        #path = app.instance_path,
        #path = str(path)
        #UPLOAD_FOLDER = os.path.join(path, 'uploads')
        #UPLOAD_FOLDER = 'instance/files',
        UPLOAD_FOLDER=os.path.join(app.instance_path, 'uploads')
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import transcriber
    app.register_blueprint(transcriber.bp)
    app.add_url_rule('/', endpoint='index')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    #UPLOAD_FOLDER = 'instance/files'
    #app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

    return app