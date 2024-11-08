import pytest
import cv2
from utils import WebcamVideoStream
from typing import Any

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

@pytest.fixture
def webcam_stream():
    # Initialize the WebcamVideoStream object
    stream = WebcamVideoStream(src=0)
    yield stream
    # Cleanup by stopping and releasing the video capture
    stream.stop()
    stream.stream.release()

def test_initialization(webcam_stream: Any):
    """Test that the stream initializes correctly."""
    assert webcam_stream.stream.isOpened() == True, "Failed to open video stream."
    assert webcam_stream.grabbed == True, "Failed to grab the first frame."
    assert webcam_stream.frame is not None, "First frame is None."

def test_start_stream(webcam_stream: Any):
    """Test that the stream starts correctly in a separate thread."""
    webcam_stream.start()
    assert webcam_stream.stopped == False, "Stream did not start correctly."

def test_read_frame(webcam_stream: Any):
    """Test that frames can be read from the stream."""
    webcam_stream.start()
    frame = webcam_stream.read()
    assert frame is not None, "Failed to read a frame from the stream."
    assert frame.shape == (webcam_stream.frame.shape), "Frame shape mismatch."

def test_stop_stream(webcam_stream: Any):
    """Test that the stream stops correctly."""
    webcam_stream.start()
    webcam_stream.stop()
    assert webcam_stream.stopped == True, "Stream did not stop correctly."

def test_frame_update(webcam_stream: Any):
    """Test that frames can be read in succession without failure."""
    webcam_stream.start()
    first_frame = webcam_stream.read()
    second_frame = webcam_stream.read()
    assert first_frame is not None, "First frame is None."
    assert second_frame is not None, "Second frame is None."
