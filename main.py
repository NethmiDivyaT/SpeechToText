from google.cloud import speech
from flask import render_template, Flask, request
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/display',  methods=['GET', 'POST'])
def display():

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "auth.json"
    # Imports the Google Cloud client library
    from google.cloud import speech

    # Instantiates a client
    client = speech.SpeechClient()

    # The name of the audio file to transcribe
    gcs_uri = "gs://cloud-samples-data/speech/brooklyn_bridge.raw"

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    # Detects speech in the audio file
    response = client.recognize(config=config, audio=audio)

    for result in response.results:
        Transcript = format(result.alternatives[0].transcript)
        return render_template('main.html', name=Transcript)


if __name__ == '__main__':
    app.run(debug=True)
