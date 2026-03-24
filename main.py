from flask import Flask
from flask_restx import Api
from endpoint.whisper import transcribe_ns
from function.whisper import preload_whisper_model

app = Flask(__name__)
api = Api(app,
          title='Whisper Transcription API',
          version='1.0',
          description='API per trascrivere file audio utilizzando il modello Whisper')

# Registra il namespace per la trascrizione
api.add_namespace(transcribe_ns, path='/transcribe')

# Precarica il modello all'avvio se configurato, evitando il download o il primo load durante una request.
preload_whisper_model()

if __name__ == '__main__': 
    app.run(debug=True, host='0.0.0.0', port=8000)
