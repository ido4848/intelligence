

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
        return [ord(c) for c in list(song.raw_data[0:10])]
