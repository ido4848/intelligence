import imp
from MIDIFile import MIDIFile


def create_midi_from_pitches(pitch_lst):
    # CREATE MEMORY FILE
    midi_object = MIDIFile(1)
    track = 0
    time = 0
    channel = 0
    duration = 1
    volume = 100
    midi_object.addTrackName(track, time, "Sample Track")
    midi_object.addTempo(track, time, 120)

    midi_object.addNote(track, channel, pitch_lst[0], time, duration, volume)
    for pitch in pitch_lst[1:]:
        time += duration
        midi_object.addNote(track, channel, pitch, time, duration, volume)

    return midi_object


def create_midi():
    # CREATE MEMORY FILE
    midi_object = MIDIFile(2)
    track = 0
    time = 0
    channel = 0
    pitch = 60
    duration = 1
    volume = 100
    midi_object.addTrackName(track, time, "Sample Track")
    midi_object.addTempo(track, time, 120)

    # WRITE A SCALE
    step_lst = [2, 2, 1, 2, 2, 2, 1, 3, 4]

    midi_object.addNote(track, channel, pitch, time, duration, volume)
    for notestep in step_lst:
        time += duration
        pitch += notestep
        midi_object.addNote(track, channel, pitch, time, duration, volume)

    track = 1
    time = 0
    channel = 0
    pitch = 40
    duration = 0.7
    volume = 100
    midi_object.addTrackName(track, time, "Sample Track 2")
    midi_object.addTempo(track, time, 120)

    # WRITE A SCALE
    step_lst = [2, 2, 1, 2, 2, 2, 1, 3, -4, 5, -6, 3, 2, -1, 1, 2]

    midi_object.addNote(track, channel, pitch, time, duration, volume)
    for notestep in step_lst:
        time += duration
        pitch += notestep
        midi_object.addNote(track, channel, pitch, time, duration, volume)

    # midi_object.addNote(0, 0, 73, 5, 1, 100)
    return midi_object


def save_midi(midi_object, file_path):
    binfile = open(file_path, 'wb')
    midi_object.writeFile(binfile)
    binfile.close()
