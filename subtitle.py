from faster_whisper import WhisperModel
import os


model = WhisperModel("base", compute_type="int8", device="cuda")

mp3_folder = "recorded_wavs"

def get_file():
    """
    Get all .wav files in the specified folder.
    """

    files = [f for f in os.listdir(mp3_folder) if f.endswith('.wav')]
    
    if len(files) != 0:
        return os.path.join(mp3_folder, files[0])
    else:
        print("No .wav files found in the specified folder.")
        return None




def transcribe_audio(running=True):
    """
    Transcribe audio data using Whisper ASR.   
    
    """
    
    while running:
        try:
            file = get_file()
            if file:
                print(f'Transcribing {file}...')
                segments, info = model.transcribe(file, beam_size=5 , language="ja")
                
                print(info.language, info.language_probability)
                
                for segment in segments:
                    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text.strip()}")
                
                os.remove(file)
            else:
                print("No file")
                
        except Exception as e:
            print(f"Error during transcription: {e}")
            
    
        except KeyboardInterrupt:
            print("Transcription stopped by user.")
            break
    
    
    
if __name__ == "__main__":
    transcribe_audio()