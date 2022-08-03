from typing import BinaryIO, List

from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


class StampedWord:
    word: str
    start: float
    end: float

    def __init__(self, word: str, start: float, end: float):
        self.word = word
        self.start = start
        self.end = end


class Sentence:
    words: List[StampedWord]
    start: float
    end: float

    def __init__(self, words: List[StampedWord]):
        self.words = words
        self.start = words[0].start
        self.end = words[-1].end

    def __len__(self):
        return len(self.words)

    def __getitem__(self, item):
        return self.words[item]

    def __setitem__(self, key, value):
        self.words[key] = value

    def __delitem__(self, key):
        del self.words[key]


def process_results(results) -> List[Sentence]:
    final = []
    for result in results:
        alts = filter(lambda alt: alt.get('confidence') is not None, result['alternatives'])
        highest_confidence_alt = max(alts, key=lambda alt: alt['confidence'])
        stamps = highest_confidence_alt['timestamps']
        hesitation_removed = list(filter(lambda stamp: stamp[0] != "%HESITATION", stamps))
        words = list(map(lambda stamp: StampedWord(stamp[0], stamp[1], stamp[2]), hesitation_removed))
        if words is None or len(words) == 0:
            continue
        final.append(Sentence(words))
    return final


class Transcriber:

    def __init__(self, api_key: str, api_url: str):
        authenticator = IAMAuthenticator(api_key)
        self.speech_to_text = SpeechToTextV1(
            authenticator=authenticator
        )
        self.speech_to_text.set_service_url(api_url)

    def transcribe(self, audio: BinaryIO):
        speech_recognition_results = self.speech_to_text.recognize(
            audio=audio,
            content_type='audio/mp3',
            timestamps=True
        ).get_result()
        return process_results(speech_recognition_results['results'])
