from src.audio.recording import Recording
import numpy as np
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


def test_from_list():
    rate = 1
    frames = [13, 17, 21]
    rec = Recording.from_list(frames, rate)


def test_appending():
    rate = 1
    frames = [13, 17, 21]
    other_frames = [3, 4]
    rec = Recording.from_list(frames, rate)
    other_rec = Recording.from_list(other_frames, rate)
    rec.append_recording(other_rec)
    new_frame_array = rec.get_frames_as_int16()
    assert list(new_frame_array) == list([13, 17, 21, 3, 4])


def test_correlation():
    rate = 1
    signal = [0, 1, 2, 3.5, 1, 1.5] # [1, 2, 3] + an echo of half magnitude and 2 sample delay
    reference = [1, 2, 3]

    signal_rec = Recording.from_list(signal, rate)
    reference_rec = Recording.from_list(reference, rate)

    correlation = signal_rec.correlate(reference_rec)
    index_of_max = np.argmax(correlation)
    assert index_of_max == 3
