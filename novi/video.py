import subprocess
import os


class VideoTools():
    def __init__(self, ffmpeg_path):
        self.ffmpeg_path = ffmpeg_path

    def video2audio(self, video_path, audio_path, audio_type="wav"):
        subprocess.run([f"{self.ffmpeg_path}ffmpeg", "-i", video_path, "-vn", "-ar",
                       "44100", "-ac", "2", "-ab", "192K", "-f", audio_type, audio_path])


if __name__ == '__main__':
    v = VideoTools("./ffmpeg/bin/")
    v.video2audio("test.mp4", "test.wav")