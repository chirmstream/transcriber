# Transcriber
Transcriber is a web application that allows a user to upload an audio clip, and receive a transcription of what was spoken.

## Features
---
- Transcribe mp3, wav, aac, flac audio files
- Return copy-pastable text
- Highlight text during audio playback
- Downloadable transcription

## Requirements
---
- Flask framework
- openai-whisper
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

Flask Extensions to use:
- Flask-SQLAlchemy
- Flask-WTF?
- Flask-Mail
- Flask-Uploads
- Flask-Debugtoolbar?
- Flask-Admin
- Flask-Login
- Flask-Session
- Flask-Limiter

### License
---
<sup>
MIT License

Copyright (c) 2023 chirmstream

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
</sup>
https://medevel.com/flask-tutorial-upload-csv-file-and-insert-rows-into-the-database/

https://stackoverflow.com/questions/29277581/flask-nameerror-name-app-is-not-defined