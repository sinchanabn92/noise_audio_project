import os
import uuid
import whisper
from gtts import gTTS

model = whisper.load_model("base")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def process_chunk(audio_path, target_language="en"):

    # Step 1: Transcribe normally (auto detect spoken language)
    result = model.transcribe(audio_path, fp16=False)

    original_text = result.get("text", "").strip()
    detected_language = result.get("language")

    if original_text == "":
        return "", None

    # Step 2: If detected language same as target → no translation
    if detected_language == target_language:
        final_text = original_text

    else:
        # Step 3: Translate using whisper
        if target_language == "en":
            # translate everything to English
            translate_result = model.transcribe(
                audio_path,
                task="translate",
                fp16=False
            )
            final_text = translate_result.get("text", "").strip()

        else:
            # English → Hindi or any other to Hindi
            # Whisper translate only supports TO English
            # So we use gTTS trick via Google Translate
            from googletrans import Translator
            translator = Translator()
            translated = translator.translate(original_text, dest=target_language)
            final_text = translated.text

    # Step 4: Text to Speech
    unique_id = str(uuid.uuid4())
    tts_filename = unique_id + ".mp3"
    tts_path = os.path.join(UPLOAD_FOLDER, tts_filename)

    tts = gTTS(text=final_text, lang=target_language)
    tts.save(tts_path)

    return final_text, tts_filename