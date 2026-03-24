import os
from pathlib import Path
from threading import Lock

import whisper

# Forza l'utilizzo della CPU (se non disponi di una GPU)
device = os.getenv("WHISPER_DEVICE", "cpu")

# Lista dei modelli validi
valid_models = ["tiny", "base", "large", "turbo"]

# Specifica il percorso della cartella in cui scaricare i modelli.
BASE_DIR = Path(__file__).resolve().parent.parent
DOWNLOAD_FOLDER = Path(os.getenv("WHISPER_MODELS_DIR", BASE_DIR / "models"))
DOWNLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

_loaded_models = {}
_model_lock = Lock()


def _normalize_model_name(model_name: str) -> str:
    requested_name = model_name or "turbo"
    if requested_name not in valid_models:
        print("Modello non valido. Verra utilizzato il modello 'turbo' di default.")
        return "turbo"
    return requested_name


def load_whisper_model(model_name: str):
    """
    Carica il modello Whisper specificato.
    Se il modello non e valido, utilizza 'turbo' come default.
    I modelli vengono mantenuti in cache in memoria per evitare reload a ogni richiesta.
    """
    normalized_name = _normalize_model_name(model_name)
    cached_model = _loaded_models.get(normalized_name)
    if cached_model is not None:
        return cached_model

    with _model_lock:
        cached_model = _loaded_models.get(normalized_name)
        if cached_model is not None:
            return cached_model

        model = whisper.load_model(normalized_name, device=device, download_root=str(DOWNLOAD_FOLDER))
        _loaded_models[normalized_name] = model
        return model


def preload_whisper_model():
    """
    Precarica il modello configurato all'avvio del processo, se richiesto.
    """
    preload_model_name = os.getenv("WHISPER_PRELOAD_MODEL", "").strip()
    if not preload_model_name:
        return None

    return load_whisper_model(preload_model_name)


def transcribe_audio_file(audio_file_path: str, model) -> str:
    """
    Esegue la trascrizione del file audio e restituisce il testo.
    """
    result = model.transcribe(audio_file_path)
    return result["text"]
