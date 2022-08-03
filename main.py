import os
from datetime import timedelta

import dotenv
import sys
import glob

from io import BytesIO
from moviepy.editor import VideoFileClip
from pathlib import Path
from srt import Subtitle, compose

from transcriber import Transcriber, StampedWord
from translator import Translator
from utils import balance


def process_video(video_path: Path):
    video_name = video_path.stem
    video = VideoFileClip(str(video_path))

    try:
        os.makedirs("temp")
    except FileExistsError:
        # directory already exists
        pass

    try:
        os.makedirs("final")
    except FileExistsError:
        # directory already exists
        pass

    audioname = f'temp/{video_name}-audio.mp3'
    video.audio.write_audiofile(audioname)

    t = Transcriber(os.getenv("SPEECH_TO_TEXT_IAM_APIKEY"), os.getenv("SPEECH_TO_TEXT_URL"))
    tr = Translator('google-credentials.json')

    source = open(audioname, 'rb')
    data = t.transcribe(BytesIO(source.read()))
    source.close()

    for i, sentence in enumerate(data):
        joined = ' '.join(item.word for item in sentence.words)
        subtitle = tr.translate(joined)
        subtitle_words = subtitle.split(' ')

        lower = float(sentence.start)
        upper = float(sentence.end)
        length = len(subtitle_words) + 1
        even_range = [lower + x*(upper-lower)/length for x in range(length)]

        sentence.words = []
        for j, word in enumerate(subtitle_words):
            sentence.words.append(StampedWord(word, even_range[j], even_range[j+1]))

    subs = []

    for i, words in enumerate(balance(data, max_length=8)):
        section_start = words[0].start
        section_end = words[-1].end
        subtitle = ' '.join([word.word for word in words])
        print(f'Subtitle: {subtitle}')
        subs.append(Subtitle(i, timedelta(seconds=section_start), timedelta(seconds=section_end), subtitle))

    with open(f'final/{video_name}-subs.srt', 'w') as f:
        f.write(compose(subs))


if __name__ == '__main__':
    dotenv.load_dotenv('speech_credentials.env')
    pat = sys.argv[1]

    for file in glob.glob(pat):
        process_video(Path(file))
