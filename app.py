from flask import Flask, render_template, Response, request, redirect, session, url_for
from camera import VideoCamera  # Import your VideoCamera class
import pandas as pd
import json

app = Flask(__name__)
app.secret_key = '123abcd567efg890h'
video_camera = VideoCamera()

users = {
    "aleena" : "12345"
}

# Home page - requires login
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    else:
        return redirect(url_for('login'))  # Redirect to login if not logged in

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user is in the dictionary
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            message = "Invalid credentials or new user. Please register."
            return render_template('login.html', message=message)
    
    return render_template('login.html')

# Registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Store new user credentials in the dictionary
        users[username] = password
        session['username'] = username

        print("Current stored users: ", users)
        return redirect(url_for('index'))
    
    return render_template('register.html')

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

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
