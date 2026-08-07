import os
import wave
import tempfile
import time
import contextlib
import pyaudio
from pywhispercpp.model import Model
import pyttsx3


@contextlib.contextmanager
def _suppress_stderr():
    """Redirect C-level stderr (fd 2) to devnull to silence whisper.cpp logs."""
    devnull_fd = os.open(os.devnull, os.O_WRONLY)
    old_stderr_fd = os.dup(2)
    try:
        os.dup2(devnull_fd, 2)
        yield
    finally:
        os.dup2(old_stderr_fd, 2)
        os.close(old_stderr_fd)
        os.close(devnull_fd)



class Speech:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            try:
                with _suppress_stderr():
                    cls._model = Model('tiny', n_threads=4)
            except Exception:
                import traceback
                traceback.print_exc()
                raise
        return cls._model

    @staticmethod
    def record_audio(output_path, silence_threshold=500, silence_duration=1.0, sample_rate=16000):
        audio = pyaudio.PyAudio()
        # Capture sample width BEFORE terminating PyAudio
        sample_width = audio.get_sample_size(pyaudio.paInt16)

        stream = audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=sample_rate,
            input=True,
            frames_per_buffer=1024,
        )

        frames = []
        silent_chunks = 0
        input("Press Enter to start recording...")

        while True:
            data = stream.read(1024, exception_on_overflow=False)
            frames.append(data)

            # Compute volume from the chunk
            volume = max(abs(int.from_bytes(data[i:i+2], "little", signed=True)) for i in range(0, len(data), 2))

            if volume < silence_threshold:
                silent_chunks += 1
            else:
                silent_chunks = 0

            if silent_chunks > int(silence_duration * (sample_rate / 1024)):
                break

        stream.stop_stream()
        stream.close()
        audio.terminate()

        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(sample_width)  # use pre-captured value
            wf.setframerate(sample_rate)
            wf.writeframes(b"".join(frames))

        print("Recording saved to:", output_path)
        return output_path
    



    @staticmethod
    def stt(audio_path=None):
        if audio_path is None:
            temp_dir = tempfile.gettempdir()
            audio_path = os.path.join(temp_dir, "support_ai_voice.wav")
            Speech.record_audio(audio_path, silence_threshold=500, silence_duration=2.0, sample_rate=16000)


        try:
            model = Speech.get_model()
            with _suppress_stderr():
                segments = model.transcribe(audio_path)
            text = " ".join(seg.text.strip() for seg in segments).strip()
            return text
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("Transcription failed:", repr(e))
            return ""



    def speak_text(text):
        if not text:
            return

        if pyttsx3 is None:
            print("TTS:", text)
            return

        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()


# def get_ai_reply(text):
#     try:
#         from engine import generate_response
#         result = generate_response(text, chat_history=[])
#         return result.get("response", text)
#     except Exception as exc:
#         print("AI engine unavailable:", exc)
#         return text


# def run_voice_chat(duration=5):
#     temp_dir = tempfile.gettempdir()
#     audio_path = os.path.join(temp_dir, "support_ai_voice.wav")

#     record_audio(audio_path, duration=duration)
#     transcript = transcribe_audio(audio_path)

#     print("You said:", transcript)

#     if not transcript:
#         print("No speech detected.")
#         return

#     reply = get_ai_reply(transcript)
#     print("Assistant:", reply)


#     speak_text(reply)


if __name__ == "__main__":
    # text = Speech.stt()
    # print("Transcript:", text)

    text = "Hello, I am fine, how are you?"
    Speech.speak_text(text)
