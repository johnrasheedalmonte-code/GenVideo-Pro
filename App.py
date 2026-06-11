from flask import Flask, render_template, request, send_file
from moviepy.editor import *
from gtts import gTTS
import os, uuid

app = Flask(__name__)

OUTPUT = "output"
os.makedirs(OUTPUT, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    text = request.form["text"]

    # Convert text to speech
    audio_path = os.path.join(OUTPUT, "voice.mp3")
    tts = gTTS(text=text)
    tts.save(audio_path)

    audio = AudioFileClip(audio_path)
    duration = audio.duration

    # Background video (black screen)
    video = ColorClip((1280,720), color=(0,0,0), duration=duration)

    # Text overlay
    txt = TextClip(text, fontsize=50, color='white', method='caption')
    txt = txt.set_position('center').set_duration(duration)

    final = CompositeVideoClip([video, txt])
    final = final.set_audio(audio)

    output_path = os.path.join(OUTPUT, f"{uuid.uuid4()}.mp4")
    final.write_videofile(output_path, fps=24)

    return send_file(output_path, as_attachment=True)


if __name__ == "__main__":
    app.run()
