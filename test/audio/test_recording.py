from src.audio.recording import Recording
from config import DATA_DIR
import os


def test_from_mic():
    recording = Recording.from_mic(0.1)


def test_from_file():
    clap_file = os.path.join(DATA_DIR, "/clap.wav")