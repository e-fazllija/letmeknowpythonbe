import whisper

# Forza l'utilizzo della CPU (se non disponi di una GPU)
device = "cpu"

# Lista dei modelli validi
valid_models = ["tiny", "base", "large", "turbo"]

# Specifica il percorso della cartella in cui scaricare i modelli
DOWNLOAD_FOLDER = "C:/Users/SimoneDelleFratte/Desktop/LetMeNow/whisper_api/models"  # Sostituisci con il percorso desiderato

def load_whisper_model(model_name: str):
    """
    Carica il modello Whisper specificato.
    Se il modello non è valido, utilizza 'turbo' come default.
    """
    if model_name not in valid_models:
        print("Modello non valido. Verrà utilizzato il modello 'turbo' di default.")
        model_name = "turbo"
    model = whisper.load_model(model_name, device=device, download_root=DOWNLOAD_FOLDER)
    return model

def transcribe_audio_file(audio_file_path: str, model) -> str:
    """
    Esegue la trascrizione del file audio e restituisce il testo.
    """
    result = model.transcribe(audio_file_path)
    return result["text"]
 