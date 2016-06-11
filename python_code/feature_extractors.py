

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
        return [ord(c) for c in raw_data_list][half:half + 10]
