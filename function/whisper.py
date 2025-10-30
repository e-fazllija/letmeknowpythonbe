import whisper
from pathlib import Path

# Forza l'utilizzo della CPU (se non disponi di una GPU)
device = "cpu"

# Lista dei modelli validi
valid_models = ["tiny", "base", "large", "turbo"]

# Specifica il percorso della cartella in cui scaricare i modelli
# Usa un percorso relativo alla posizione di questo file, così funziona ovunque
BASE_DIR = Path(__file__).resolve().parent.parent  # cartella 'whisper_api'
DOWNLOAD_FOLDER = BASE_DIR / "models"
# Assicura che la cartella esista
DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

def load_whisper_model(model_name: str):
    """
    Carica il modello Whisper specificato.
    Se il modello non è valido, utilizza 'large' come default.
    """
    if model_name not in valid_models:
        print("Modello non valido. Verrà utilizzato il modello 'large' di default.")
        model_name = "large"
    model = whisper.load_model(model_name, device=device, download_root=str(DOWNLOAD_FOLDER))
    return model

def transcribe_audio_file(audio_file_path: str, model) -> str:
    """
    Esegue la trascrizione del file audio e restituisce il testo.
    """
    result = model.transcribe(audio_file_path)
    return result["text"]
 
