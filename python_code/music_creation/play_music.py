import pygame
import random
from StringIO import StringIO
from time import sleep
import pygame.mixer
import midi_creation


def play_midi(midi_object):
    memFile = StringIO()
    midi_object.writeFile(memFile)

    # PLAYBACK
    pygame.init()
    pygame.mixer.init()
    memFile.seek(0)  # THIS IS CRITICAL, OTHERWISE YOU GET THAT ERROR!
    pygame.mixer.music.load(memFile)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        sleep(1)
    print "Done!"


def main():
    random_lst = [random.randrange(40, 80) for _ in range(30)]
    midi_object = midi_creation.create_midi_from_pitches(random_lst)
    midi_creation.save_midi(midi_object, "temp.midi")
    play_midi(midi_object)


if __name__ == "__main__":
    main()
