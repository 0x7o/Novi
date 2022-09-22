import subprocess
from vosk import Model, KaldiRecognizer, SetLogLevel
import json

SAMPLE_RATE = 16000

SetLogLevel(0)

model = Model(lang="en-us", model_name="vosk-model-en-us-0.22-lgraph")
rec = KaldiRecognizer(model, SAMPLE_RATE)
rec.SetWords(True)

with subprocess.Popen(["ffmpeg/bin/ffmpeg", "-loglevel", "quiet", "-i",
                            "test.wav",
                            "-ar", str(SAMPLE_RATE) , "-ac", "1", "-f", "s16le", "-"],
                            stdout=subprocess.PIPE) as process:
    res = []
    while True:
        data = process.stdout.read(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            r = rec.Result()
            print(r)
            res.append(json.loads(r))
    with open('test.json', 'a') as f:
        json.dump(res, f)