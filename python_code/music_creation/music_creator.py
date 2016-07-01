from pyevolve import G1DList
from pyevolve import GSimpleGA
from pyevolve import Selectors
from pyevolve import Statistics
from pyevolve import DBAdapters
import pyevolve
from pyevolve import Initializators, Mutators
import pydub
import shelve
import os
import imp

'''
    def save_song(self, raw_song, file_name, file_format):  # TODO: UGLY
        raw_song = ''.join([chr(c) for c in raw_song])
        with open("temp.raw", "wb") as f:
            f.write(raw_song)
        song_object = pydub.AudioSegment.from_raw(raw_song, channels=self._channels, frame_rate=self._frame_rate,
                                                  sample_width=self._sample_width)
        song_object.export(file_name, file_format)
        os.remove("temp.raw")




        # Genome instance, 1D List of 50 elements
        nframes = self._frame_rate * self._channels * self._sample_width * duration_seconds
        genome = G1DList.G1DList(nframes)

        # Sets the range max and min of the 1D List
        genome.setParams(rangemin=0, rangemax=255)



        def eval_func(raw_genome):  # TODO: UGLY
            raw_song = raw_g1d_song.genomeList
            raw_song = ''.join([chr(c) for c in raw_song])
            with open("temp.raw", "wb") as f:
                f.write(raw_song)
            song_object = pydub.AudioSegment.from_raw("temp.raw", channels=self._channels, frame_rate=self._frame_rate,
                                                      sample_width=self._sample_width)
            pred = self._music_detector.detect_from_song(song_object)
            print pred
            os.remove("temp.raw")
            return pred
'''


class MusicCreator(object):
    def __init__(self, music_detector, genome, genome_to_song_object):
        self._music_detector = music_detector
        self._genome = genome
        self._genome_to_song_object = genome_to_song_object

    def create(self, iterations, freq_stats=0):
        def eval_func(raw_genome):
            song_object, song_object_format = self._genome_to_song_object(raw_genome)
            pred = self._music_detector.detect_from_song(song_object, song_object_format)
            # print pred
            return pred

        # Enable the pyevolve logging system
        # pyevolve.logEnable("/dev/null")

        genome = self._genome
        # The evaluator function (evaluation function)
        genome.evaluator.set(eval_func)

        # Genetic Algorithm Instance
        ga = GSimpleGA.GSimpleGA(genome)

        # Set the Roulette Wheel selector method, the number of generations and
        # the termination criteria
        ga.selector.set(Selectors.GRouletteWheel)
        ga.setGenerations(iterations)
        ga.terminationCriteria.set(GSimpleGA.ConvergenceCriteria)

        # Sets the DB Adapter, the resetDB flag will make the Adapter recreate
        # the database and erase all data every run, you should use this flag
        # just in the first time, after the pyevolve.db was created, you can
        # omit it.
        # sqlite_adapter = DBAdapters.DBSQLite(identify="ex1", resetDB=True)
        # ga.setDBAdapter(sqlite_adapter)

        # Do the evolution, with stats dump
        # frequency of 20 generations
        ga.evolve(freq_stats=freq_stats)

        # Best individual
        best = ga.bestIndividual()
        return best
