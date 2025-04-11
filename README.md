# 🎙️ TensorGo Voice Assistant (Whisper + gTTS + Groq)

A simple yet powerful voice assistant built with Python, leveraging OpenAI's Whisper for speech-to-text, Google Text-to-Speech (gTTS) for text-to-speech, and Groq's LLaMA 3 model for intelligent responses.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python&logoColor=white)

## ✨ Features

*   **Voice Recording:** Record your voice input directly through the application.
*   **Accurate Transcription:** Utilizes OpenAI's Whisper model for high-quality speech-to-text conversion.
*   **Intelligent Conversation:** Interacts with Groq's fast LLaMA 3 8B model for generating responses.
*   **Text-to-Speech:** Converts the bot's responses into audible speech using gTTS.
*   **Audio Playback:** Plays the generated speech using Pygame.
*   **Interactive GUI:** Simple and intuitive interface built with Tkinter.
*   **Conversation History:** Displays the ongoing conversation.
*   **Interrupt Functionality:** Stop the bot's audio playback midway.
*   **Save Chat:** Option to save the conversation history to a text file (`chat_history.txt`).

## 🛠️ Technologies Used

*   **Python:** Core programming language.
*   **Tkinter:** GUI framework.
*   **PyAudio:** Audio recording.
*   **Wave:** Saving audio files.
*   **OpenAI Whisper:** Speech-to-Text model.
*   **gTTS (Google Text-to-Speech):** Text-to-Speech engine.
*   **Pygame:** Audio playback.
*   **Groq API:** Access to LLaMA 3 language model.
*   **python-dotenv:** Environment variable management.

## 🚀 Setup and Installation

1.  **Clone the repository (or download the files):**
    ```bash
    # If using Git
    git clone <your-repository-url>
    cd <repository-directory>
    ```

2.  **Create a virtual environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up API Key:**
    *   You need an API key from [Groq](https://console.groq.com/keys).
    *   Create a file named `.env` in the project root directory.
    *   Add your API key to the `.env` file like this:
        ```
        GROQ_API_KEY=your_groq_api_key_here
        ```

## ▶️ How to Use

1.  **Run the application:**
    ```bash
    python new_gui.py
    ```
2.  **Click the "🎙️ Record" button:** Start speaking your query or message.
3.  **Click the "⏹️ Stop" button:** Finish recording.
4.  **Wait:** The application will:
    *   Transcribe your speech.
    *   Send the transcription to the Groq LLM.
    *   Receive the response.
    *   Convert the response to speech (TTS).
    *   Play the audio response.
5.  **Interact:** Continue the conversation by repeating steps 2-4.
6.  **Interrupt (Optional):** Click the "🛑 Interrupt" button while the bot is speaking to stop the audio playback.
7.  **Save (Optional):** Click the "💾 Save" button to save the current conversation history to `chat_history.txt`.
8.  **Exit:** Click the "❌ Exit" button to close the application.

---

Enjoy your TensorGo Voice Assistant! 