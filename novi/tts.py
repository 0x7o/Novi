import time
import wave
import json
import torch
import webvtt
import datetime
import subprocess
import contextlib
from tqdm import tqdm
from IPython.display import Audio


class TTS():
    def __init__(self, language, model_id):
        device = torch.device('cuda')

        self.model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                                  model='silero_tts',
                                                  language=language,
                                                  speaker=model_id)

        self.model.to(device)

    def wav(self, text, speaker, wav_path):
        audio = self.model.apply_tts(text=text,
                                     speaker=speaker,
                                     sample_rate=48000)
        audio = Audio(audio, rate=48000)
        with open(wav_path, 'wb') as f:
            f.write(audio.data)

    def sayvvt(self, vvt_path):
        l = []
        for idx, caption in enumerate(tqdm(webvtt.read(vvt_path))):
            s = caption.start.split('.')[0]
            e = caption.end.split('.')[0]
            t = caption.text
            s_s = time.strptime(s, '%H:%M:%S')
            s_s = datetime.timedelta(
                hours=s_s.tm_hour, minutes=s_s.tm_min, seconds=s_s.tm_sec).total_seconds()
            s_e = time.strptime(e, '%H:%M:%S')
            s_e = datetime.timedelta(
                hours=s_e.tm_hour, minutes=s_e.tm_min, seconds=s_e.tm_sec).total_seconds()
            total_seconds = s_e - s_s
            self.wav(caption.text, 'eugene', f'tts_cache/{"{0:03}".format(idx)}.wav')
            with contextlib.closing(wave.open(f'tts_cache/{"{0:03}".format(idx)}.wav', 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                duration = round(frames / float(rate))
            f = ""
            if duration > total_seconds and total_seconds != 0:
                h = duration / total_seconds
                print(h)
                subprocess.run(["ffmpeg", "-i", f'tts_cache/{"{0:03}".format(idx)}.wav', "-af",
                                f"atempo={h}", f'tts_cache/{"{0:03}".format(idx)}_speed.wav'])
                f = f'_speed.wav'
            else:
                f = f'.wav'

                #subprocess.run(["ffmpeg", "-i", j, "-i", f"tts_cache/{idx}{f}", "-filter_complex",
                                #f"[0]adelay={adelay1}|{adelay1}[s0]; [1]adelay={s_s*1000}|{s_s*1000}[s1]; [s0][s1]amix=2[mixout]",
                                #"-map", "[mixout]", "-c:v", "copy", f"process/{idx}.wav"])
            l.append({'name': f'tts_cache/{"{0:03}".format(idx)}{f}', 's': s_s})
        with open('data.json', 'a') as o:
            json.dump(l, o)

if __name__ == '__main__':
    t = TTS('ru', 'v3_1_ru')
    t.sayvvt('new.vvt')
