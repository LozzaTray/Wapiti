from src.audio.recording import Recording
import os


def test_from_mic():
    recording = Recording.from_mic(0.01)
    assert recording.frames != None


def test_play():
    recording = Recording.from_mic(0.01)
    recording.play()


def test_save(tmpdir):
    rec = Recording.from_mic(0.01)
    filename = os.path.join(tmpdir, "test_save.wav")
    rec.save(filename)


def test_from_file(tmpdir):
    rec = Recording.from_mic(0.01)
    filename = os.path.join(tmpdir, "test_from_file.wav")
    rec.save(filename)

    retrieved_rec = Recording.from_file(filename)

    assert retrieved_rec.frames == rec.frames