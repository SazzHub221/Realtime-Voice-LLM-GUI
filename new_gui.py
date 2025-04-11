import tkinter as tk
from tkinter import scrolledtext
import threading
import pyaudio
import wave
import whisper
import os
import time
from gtts import gTTS
import pygame
from groq import Groq
import warnings
from dotenv import load_dotenv  # Add this import

# Load environment variables
load_dotenv()  # Add this line

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Whisper + Groq + pygame setup
model = whisper.load_model("base")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # Modified this line
pygame.mixer.init()

history = []
is_playing = False
is_recording = False  # Flag to track recording state

# Audio recording
def record_audio(filename="input.wav"):
    global is_recording
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    frames = []
    is_recording = True
    update_history("🎙️ Recording... Press 'Stop' to finish.")
    
    # Update button text
    record_btn.config(text="⏹️ Stop", command=stop_recording)
    
    while is_recording:
        data = stream.read(CHUNK)
        frames.append(data)
        root.update()  # Update GUI while recording
    
    stream.stop_stream()
    stream.close()
    audio.terminate()
    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    update_history("🛑 Recording stopped.")
    return filename

def stop_recording():
    global is_recording
    is_recording = False
    # Reset button to original state
    record_btn.config(text="🎙️ Record", command=lambda: threading.Thread(target=handle_conversation).start())

# Transcription
def transcribe(audio_path):
    result = model.transcribe(audio_path)
    return result['text']

# Groq LLM
def chat_with_llm(message):
    history.append({"role": "user", "content": message})
    chat_completion = client.chat.completions.create(
        messages=history,
        model="llama3-8b-8192",
    )
    reply = chat_completion.choices[0].message.content
    history.append({"role": "assistant", "content": reply})
    return reply

# Play audio
def play_audio(text):
    global is_playing
    if os.path.exists("response.mp3"):
        try:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
        except:
            pass
        try:
            os.remove("response.mp3")
        except:
            time.sleep(0.5)
            os.remove("response.mp3")
    
    tts = gTTS(text=text)
    tts.save("response.mp3")
    pygame.mixer.music.load("response.mp3")
    pygame.mixer.music.play()
    is_playing = True
    
    # Show interrupt button and update status
    interrupt_btn.grid(row=0, column=2, padx=10)
    update_history("🔊 Playing response... Press 'Interrupt' to stop.")
    
    # Check if music is playing in a loop
    while pygame.mixer.music.get_busy() and is_playing:
        root.update()
        time.sleep(0.1)
    
    # Hide interrupt button when done
    interrupt_btn.grid_forget()
    is_playing = False

def interrupt_audio():
    global is_playing
    if is_playing:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        update_history("⛔ Response interrupted.")
        is_playing = False
        # Hide interrupt button
        interrupt_btn.grid_forget()

# Update GUI history
def update_history(text):
    history_box.configure(state='normal')
    history_box.insert(tk.END, text + "\n\n")
    history_box.configure(state='disabled')
    history_box.see(tk.END)

def save_chat():
    with open("chat_history.txt", "w", encoding="utf-8") as f:
        for item in history:
            role = item['role'].capitalize()
            f.write(f"{role}: {item['content']}\n\n")
    update_history("📄 Chat saved to chat_history.txt")

# Full flow
def handle_conversation():
    try:
        record_audio("input.wav")
        user_input = transcribe("input.wav").strip()
        if not user_input:
            update_history("❗ Could not understand. Please retry.")
            return
        update_history(f"🧠 You: {user_input}")
        response = chat_with_llm(user_input)
        update_history(f"🤖 Bot: {response}")
        play_audio(response)
        update_history("🎤 Ready for next input...\n")
    except Exception as e:
        update_history(f"❌ Error: {e}")
        # Reset button in case of error
        record_btn.config(text="🎙️ Record", command=lambda: threading.Thread(target=handle_conversation).start())

# GUI setup
root = tk.Tk()
root.title("TensorGo Voice Assistant (Whisper + gTTS + Groq)")
root.geometry("700x500")

label = tk.Label(root, text="🎤 TensorGo Voice Assistant", font=("Helvetica", 16, "bold"))
label.pack(pady=10)

history_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Helvetica", 12), height=20)
history_box.pack(padx=10, pady=10)
history_box.configure(state='disabled')

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

record_btn = tk.Button(button_frame, text="🎙️ Record", font=("Helvetica", 14), command=lambda: threading.Thread(target=handle_conversation).start())
record_btn.grid(row=0, column=0, padx=10)

exit_btn = tk.Button(button_frame, text="❌ Exit", font=("Helvetica", 14), command=root.quit)
exit_btn.grid(row=0, column=1, padx=10)

save_btn = tk.Button(button_frame, text="💾 Save", font=("Helvetica", 14), command=save_chat)
save_btn.grid(row=0, column=2, padx=10)

# Create interrupt button but don't place it yet
interrupt_btn = tk.Button(button_frame, text="🛑 Interrupt", font=("Helvetica", 14), command=interrupt_audio)
# It will be grid-placed only when audio is playing

update_history("🤖 Welcome to TensorGo!\nClick '🎙️ Record' to start and 'Stop' to finish recording.")

root.mainloop()