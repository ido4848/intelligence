import numpy
import pydub
import wave
import os
import subprocess
import struct
import numpy
import csv
import sys


class IFeatureExtractor(object):
    def extract(self, song):
        raise NotImplementedError()


'''
    def _split_song(self, song):
        offset = 0
        duration = self._duration_seconds * 1000
        song_segments = []
        while offset + duration < song.duration_seconds * 1000:
            song_segments.append(song[offset:offset + duration])
            offset = offset + duration
        if duration < song.duration_seconds:
            song_segments.append(song[-duration])

        return song_segments
'''


class RawDataFeatureExtractor(object):
    def extract(self, song):
        raw_data_list = list(song.raw_data)
        half = len(raw_data_list) / 2
        return [ord(c) for c in raw_data_list][half:half + 5]


class ChristianPecceiFeatureExtractor(object):
    @staticmethod
    def moments(x):
        mean = x.mean()
        std = x.var() ** 0.5
        skewness = ((x - mean) ** 3).mean() / std ** 3
        kurtosis = ((x - mean) ** 4).mean() / std ** 4
        return [mean, std, skewness, kurtosis]

    @staticmethod
    def fftfeatures(wavdata):
        f = numpy.fft.fft(wavdata)
        f = f[2:(f.size / 2 + 1)]
        f = abs(f)
        total_power = f.sum()
        f = numpy.array_split(f, 10)
        return [e.sum() / total_power for e in f]

    @staticmethod
    def features(x):
        x = numpy.array(x)
        f = []

        xs = x
        diff = xs[1:] - xs[:-1]
        f.extend(ChristianPecceiFeatureExtractor.moments(xs))
        f.extend(ChristianPecceiFeatureExtractor.moments(diff))

        xs = x.reshape(-1, 10).mean(1)
        diff = xs[1:] - xs[:-1]
        f.extend(ChristianPecceiFeatureExtractor.moments(xs))
        f.extend(ChristianPecceiFeatureExtractor.moments(diff))

        xs = x.reshape(-1, 100).mean(1)
        diff = xs[1:] - xs[:-1]
        f.extend(ChristianPecceiFeatureExtractor.moments(xs))
        f.extend(ChristianPecceiFeatureExtractor.moments(diff))

        xs = x.reshape(-1, 1000).mean(1)
        diff = xs[1:] - xs[:-1]
        f.extend(ChristianPecceiFeatureExtractor.moments(xs))
        f.extend(ChristianPecceiFeatureExtractor.moments(diff))

        f.extend(ChristianPecceiFeatureExtractor.moments(x))
        return f

    @staticmethod
    def read_wav(wav_file):
        """Returns two chunks of sound data from wave file."""
        w = wave.open(wav_file)
        n = 100000
        if w.getnframes() < 100000:
            raise ValueError('Wave file too short (less than 10 seconds)')
        frames = w.readframes(n)
        wav_data = struct.unpack('%dh' % n, frames)
        return wav_data

    @staticmethod
    def compute_features(mp3_file):
        """Return feature vectors for one chunk of an MP3 file."""
        # Extract MP3 file to a mono, 10kHz WAV file
        out_file = 'temp.wav'
        mpg123_command = 'mpg123 -q -w {} -r 10000 -m {}'.format(out_file, mp3_file)
        temp = os.system(mpg123_command)
        # Read in chunks of data from WAV file
        wav_data = ChristianPecceiFeatureExtractor.read_wav(out_file)
        # We'll cover how the features are computed in the next section!
        return ChristianPecceiFeatureExtractor.features(wav_data)

    def extract(self, song):
        song.export("temp.mp3", format="mp3")
        features = ChristianPecceiFeatureExtractor.compute_features("temp.mp3")

        os.remove("temp.mp3")
        os.remove("temp.wav")
        return features
