# Transcriber

## Description

Transcriber is a web application that allows a user to upload an audio clip, and receive a transcription of what was spoken.


## About
---
Transcriber is built using the Flask framework with a sqlite3 database.  Flask was chosen due to its simplicity, scalability, and I was already familiar with it.  sqlite3 was chosen for similar reasons, it is simple, quick, and I was already familiar with it.  It should not be too difficult to use a more production oriented database such as mariadb if needed, but at this time it is not supported.

Openai/whisper is what is being used under the hood to perform the transcription.  Transcriber is currently set to use the 'base' model, but it would not be hard to modify the code to use a different model if needed.  You can read more about openai/whisper [here](https://github.com/openai/whisper).


## Features
---
- Transcribe mp3, wav, aac, flac audio files
- Transcribe multiple languages (only english tested)


## Getting Started
---
### Requirements
- Flask framework
- openai-whisper
- ffmpeg
- ffmpeg-python

## About
---
Transcriber is built using the Flask framework with a sqlite3 database.  Flask was chosen due to its simplicity, scalability, and I was already familiar with it.  sqlite3 was chosen for similar reasons, it is simple, quick, and I was already familiar with it.  It should not be too difficult to use a more production oriented database such as mariadb if needed, but at this time it is not supported.

Openai/whisper is what is being used under the hood to perform the transcription.  Transcriber is currently set to use the 'base' model, but it would not be hard to modify the code to use a different model if needed.  You can read more about openai/whisper [here](https://github.com/openai/whisper).

## Installation Guide
---
Create a virtual Python enviroment (Linux/MacOS command):

    mkdir transcriber
    cd transcriber
    python3 -m venv venv

Activate the Python virtual enviroment

    . venv/bin/activate

Install Transcriber project using pip

    pip install -e .

Install openai-whisper

    pip install -U openai-whisper

Install ffmpeg (ubuntu)

    sudo apt install ffmpeg

Install ffmpeg-python

    pip install ffmpeg-python

Initiate the project database

    flask --app transcriber init-db

Start Flask development server

    flask --app transcriber run --debug

## Help:
---
If you need to restart the development server after installation simply reactivate the virtual python enviroment and restart the server

    . venv/bin/activate
    flask --app transcriber run --debug

If the default port 5000 is in use run:

    flask --app transcriber run --debug -p <port>

If you run into an issue with torch not being found try reinstalling via pip

    pip uninstall torch
    pip install torch

If you are on MacOS you will need openssl 1.1

    brew install openssl@1.1

If that doesn't work you can try:

    python3 -m pip install urllib3==1.26.6


## Authors
---
* chirmstream


## License
---
Transcriber's code is released under the MIT license.  See [LICENSE](https://github.com/chirmstream/transcriber/blob/main/LICENSE) for further details.


## Acknowledgments
---
* Havard CS50
* [Flask tutorial](https://flask.palletsprojects.com/en/2.3.x/tutorial/)

## Roadmap
---
Currently the web server is very simple and is only being used as a proof of concept to see if if my idea would even work.  Afterall it is more of an exercise in testing my programming abilities than anything else.  Since I started the front end with Flask's tutorial flaskr (a very simple blog site) and modified it to fit my needs, in the future I would like to redo the entire front end from scratch to attempt a more modern look.