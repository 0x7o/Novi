import whisper
import whisper.utils
import json

model = whisper.load_model("small", device="cuda")

result = whisper.transcribe(model, "video.wav", fp16=False, verbose=True)
print(result)
with open('video.vvt', 'a') as vvt:
    whisper.utils.write_vtt(result["segments"], file=vvt)