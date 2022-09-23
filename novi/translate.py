import webvtt
import requests
from tqdm import tqdm


class NllbTranslate():
    def __init__(self):
        self.domain = "https://hf.space/embed/0x7194633/nllb-1.3B-demo/+/api/predict"

    def translate(self, text, from_lang="English", to_lang="Russian"):
        response = requests.post(
            self.domain, json={"data": [from_lang, to_lang, text]})
        return response.json()['data'][0]['result']

    def translatevvt(self, path, **kwargs):
        new_vvt = "WEBVTT\n\n"
        for caption in tqdm(webvtt.read(path)):
            s = caption.start
            e = caption.end
            t = self.translate(caption.text, **kwargs)
            new_vvt += f"{s} --> {e}\n {t}\n\n"
            
        with open('new.vvt', 'a', encoding='utf-8') as f:
            f.write(new_vvt)


if __name__ == "__main__":
    n = NllbTranslate()
    print(n.translatevvt("video.vvt"))
