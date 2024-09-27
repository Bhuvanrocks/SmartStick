import pyaudio
import wave
import speech_recognition as sr

# Audio recording settings
FORMAT = pyaudio.paInt16  # Audio format (16-bit)
CHANNELS = 1              # Mono audio
RATE = 44100              # Sample rate (44.1kHz)
CHUNK = 1024              # Chunk size for reading audio in chunks
RECORD_SECONDS = 5        # Duration of recording in seconds
OUTPUT_FILE = "output.wav"  # Output file name

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Open the microphone stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

print("Recording...")

# List to hold the recorded frames
frames = []

# Record the audio in chunks
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print("Recording finished")

# Stop and close the stream
stream.stop_stream()
stream.close()
audio.terminate()

# Save the recorded frames as a .wav file
waveFile = wave.open(OUTPUT_FILE, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

print(f"Audio saved as {OUTPUT_FILE}")

# Initialize the recognizer
recognizer = sr.Recognizer()

# Open the recorded audio file for speech recognition
with sr.AudioFile(OUTPUT_FILE) as source:
    print("Converting speech to text...")
    audio_data = recognizer.record(source)  # Read the entire audio file

    # Use Google Web Speech API to convert speech to text
    try:
        text = recognizer.recognize_google(audio_data)
        print("Text: " + text)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")

