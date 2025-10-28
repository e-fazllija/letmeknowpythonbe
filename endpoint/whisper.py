from flask_restx import Namespace, Resource, reqparse
from werkzeug.datastructures import FileStorage
from flask import request
try:
    from flask_cors import cross_origin  # type: ignore
except Exception:  # pragma: no cover
    def cross_origin(*args, **kwargs):  # type: ignore
        def _wrap(f):
            return f
        return _wrap
import tempfile
import os
from function.whisper import load_whisper_model, transcribe_audio_file

# Definisce il namespace per la trascrizione
transcribe_ns = Namespace("transcribe", description="Endpoint per trascrivere file audio con Whisper")

# Parser per gestire l'upload del file audio e il parametro opzionale model_name
upload_parser = reqparse.RequestParser()
upload_parser.add_argument(
    'audio_file',
    type=FileStorage,
    location='files',
    required=True,
    help="Carica un file audio (es. WAV, MP3, ecc.)"
)
upload_parser.add_argument(
    'model_name',
    type=str,
    location='form',
    required=False,
    help="Nome del modello da utilizzare (tiny, base, large, turbo). Default 'large' se non valido o non specificato."
)

@transcribe_ns.route("/")
class Transcribe(Resource):
    # Preflight (OPTIONS) per richieste CORS
    @cross_origin(origins="*", methods=["POST", "OPTIONS"], allow_headers=["Content-Type", "Authorization"])
    def options(self):
        return {"status": "ok"}, 204

    @transcribe_ns.expect(upload_parser)
    @transcribe_ns.response(200, "Successo")
    @transcribe_ns.response(400, "Errore nella richiesta")
    @cross_origin(origins="*", methods=["POST", "OPTIONS"], allow_headers=["Content-Type", "Authorization"])
    def post(self):
        """
        Carica un file audio e restituisce la trascrizione del contenuto.
        
        Il parametro 'model_name' è opzionale.
        """
        args = upload_parser.parse_args()
        audio_file = args.get("audio_file")
        model_name = args.get("model_name") or "large"  # Default su 'large' se non viene fornito
        
        if not audio_file:
            return {"error": "Nessun file audio fornito."}, 400
        
        try:
            # Salva il file audio in una posizione temporanea
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            audio_file.save(temp_file.name)
            temp_file.close()

            # Carica il modello richiesto (se non valido verrà usato 'large')
            model = load_whisper_model(model_name)
            
            # Esegui la trascrizione
            transcription = transcribe_audio_file(temp_file.name, model)
            
            # Rimuove il file temporaneo
            os.remove(temp_file.name)
            
            return {"transcription": transcription}, 200

        except Exception as e:
            return {"error": f"Errore durante la trascrizione: {str(e)}"}, 500
