# Transcriber
Transcriber is a web application that allows a user to upload an audio clip, and receive a transcription of what was spoken.

## Features
---
- Transcribe mp3, wav, aac, flac audio files
- Transcribe multiple languages (only english tested)

## Requirements
---
- Flask framework
- openai-whisper
- ffmpeg
- ffmpeg-python

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

## Other notes:
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

### License
---
Transcriber's code is released under the MIT license.  See [LICENSE](https://github.com/chirmstream/transcriber/blob/main/LICENSE) for further details.