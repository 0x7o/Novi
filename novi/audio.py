import subprocess
import json


class Audio():
    def __init__(self, path):
        with open(path, 'r') as f:
            self.waves = json.load(f)

    def split(self):
        i = ""
        a1 = ""
        a2 = ""
        for idx, w in enumerate(self.waves):
            i += f"-i {w['name']} "
            a1 += f"[{idx}]adelay={w['s']*1000}|0[s{idx}]; "
            a2 += f"[s{idx}]"
        subprocess.run(
            f'ffmpeg {i}-filter_complex "{a1}{a2}amix={len(self.waves)}[mixout]" -map "[mixout]" -c:v copy r.wav')
        subprocess.run(f'ffmpeg -y -hide_banner -i r.wav -c:v copy -c:a libmp3lame -b:a 160k -ar 48000 -ac 2 -af loudnorm=tp=-4.0 result.wav')

if __name__ == '__main__':
    a = Audio('data.json')
    a.split()
