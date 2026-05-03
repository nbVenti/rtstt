from faster_whisper import WhisperModel
import tkinter as tk
import os

model = WhisperModel("large-v2", device="cuda", compute_type="float16")

def transcribe_audio(file_path):
    segments, info = model.transcribe(file_path, beam_size=5)
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    # for segment in segments:
    #     print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        
    return segments

def subtitle(segments)
    text_data = segments
    
def main():
    audio_folder = "recorded_wavs" 
    
    for filename in os.listdir(audio_folder):
        file_path = os.path.join(audio_folder, filename)
        print(f"Transcribing {file_path}...")
        segments = transcribe_audio(file_path)
        os.remove(file_path)
        
    print("All audio files transcribed and folder removed.")

if __name__ == "__main__":
    main()
    