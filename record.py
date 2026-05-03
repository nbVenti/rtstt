import queue; from queue import Queue
import speech_recognition as sr
import pyaudio
import time
import wave
import os

p = pyaudio.PyAudio()

rec = sr.Recognizer()

def record_mic():
    data_queue = Queue()
    
    rec.dynamic_energy_threshold = False
    
    mic_index = 1

    output = sr.Microphone(device_index=mic_index)
    
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print(f"Using microphone: {sr.Microphone.list_microphone_names()[mic_index]}") 
            audio = rec.listen(source, timeout=5)
            print("Audio recorded")
    except:
        print("No microphone found")    
        return
    
    def callback(_, audio):
        raw = audio.get_raw_data()
        sample_rate = audio.sample_rate
        sample_width = audio.sample_width
        data_queue.put((raw, sample_rate, sample_width))
        with open("test_audio.wav", "wb") as f:
            f.write(raw)

    
    stop_listening = rec.listen_in_background(output, callback, phrase_time_limit=5)
    try:
        raw, sample_rate, sample_width = data_queue.get(timeout=6)
        audio = sr.AudioData(raw, sample_rate, sample_width)
        try:
            text = rec.recognize_google(audio)
            print(text)
        
        except queue.Empty:
            pass
            
        except sr.UnknownValueError:
            print("Could not understand audio. Try speaking louder or more clearly.")
        time.sleep(0.1)
    except KeyboardInterrupt:
        stop_listening(wait_for_stop=False)


DEVICE_INDEX = 13
FORMAT = pyaudio.paInt16
CHANNELS = 8
RATE = 44100
CHUNK = 1024 
RECORD_SECONDS = 5
OUTPUT_DIR = "recorded_wavs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def record_audio():
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=DEVICE_INDEX)
    
    print("Recording...")
    frames = []
    
    for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("Recording complete.")
    stream.stop_stream()
    stream.close()
    return convert_to_wav(frames)


def convert_to_wav(frames):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    wav_filename = os.path.join(OUTPUT_DIR, f"audio_{timestamp}.wav")
    
    with wave.open(wav_filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
    
    print(f"WAV file saved as: {wav_filename}")
    return wav_filename

# for mic_id, name in enumerate(sr.Microphone.list_microphone_names()):
#     print(mic_id , name)


def main():
    while True:
        file_name = record_audio()
        print(f"Recorded audio saved as: {file_name}")
        

if __name__ == '__main__':
    main()