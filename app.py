from flask import Flask, render_template, Response
from camera import VideoCamera  # Import your VideoCamera class
import pandas as pd
import json

app = Flask(__name__)
video_camera = VideoCamera()

@app.route('/')
def index():
    # Render the index page
    return render_template('index.html')

def generate_frames():
    while True:
        frame, df1 = video_camera.get_frame()
        # Create a JSON response with songs and a cheerful message
        songs = df1.to_dict(orient='records')  # Convert DataFrame to a list of dictionaries
        message = "Keep smiling! You’re doing great!"  # You can modify this to randomize messages if desired
        
        # Create the complete response
        response_data = {
            'songs': songs,
            'message': message
        }
        
        # Convert to JSON and encode as bytes
        json_response = json.dumps(response_data)
        json_bytes = json_response.encode('utf-8')  # Ensure it's in bytes format

        # Yield the image frame and the JSON response separately
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n'
               b'--json\r\n'
               b'Content-Type: application/json\r\n\r\n' + json_bytes + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/music_recommendations')
def music_recommendations():
    # Retrieve the current DataFrame from the video camera
    _, df1 = video_camera.get_frame()
    # Convert DataFrame to HTML for rendering in the index page
    return df1.to_html(classes='table table-striped', index=False)

if __name__ == '__main__':
    app.run(debug=True)
