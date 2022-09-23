import subprocess
import os


class VideoTools():
    def __init__(self):
        pass

    def video2audio(self, video_path, audio_path, audio_type="wav"):
        subprocess.run([f"ffmpeg", "-i", video_path, "-vn", "-ar",
                       "44100", "-ac", "2", "-ab", "192K", "-f", audio_type, audio_path])


if __name__ == '__main__':
    v = VideoTools()
    v.video2audio("video.mp4", "video.wav")