from flask import Flask, render_template, request, send_file
from pytube import YouTube
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        # Get the YouTube URL from the form
        url = request.form['url']

        # Create a YouTube object
        yt = YouTube(url)

        # Get the highest resolution stream
        video_stream = yt.streams.get_highest_resolution()

        # Download the video to a temporary folder
        temp_path = 'temp'
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        video_path = os.path.join(temp_path, yt.title + '.mp4')
        video_stream.download(temp_path)

        # Send the file as a response to trigger download
        return send_file(video_path, as_attachment=True)

    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
