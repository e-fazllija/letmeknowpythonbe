from flask import Flask
from flask_restx import Api
from endpoint.whisper import transcribe_ns

app = Flask(__name__)
api = Api(app,
          title='Whisper Transcription API',
          version='1.0',
          description='API per trascrivere file audio utilizzando il modello Whisper')

# Registra il namespace per la trascrizione
api.add_namespace(transcribe_ns, path='/transcribe')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5097)
