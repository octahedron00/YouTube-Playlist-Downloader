import os
from pytube import Playlist, YouTube
import subprocess

p = Playlist("https://www.youtube.com/playlist?list=PLVVB8cn1-HNLWOKM9Et_7x4Mmc93THDUk")
print(p.title, "Length:", len(p.video_urls))

# Test if the playlist is valid / length must be bigger than 10...
for i in p.video_urls[:10]:
    print(i)

# Downloading
for i in p.video_urls:
    # use_oauth : for download YouTube_Music-only, if you have YouTube Music account.
    yt = YouTube(i, use_oauth=True)

    # to see what filter has the best quality : here
    print("Filters : ", len(yt.streams.filter(only_audio=True)), yt.streams.filter(only_audio=True).order_by("abr"))

    # the best quality : ~160kbps of webm, or the best of existing filters.
    audio = yt.streams.filter(only_audio=True).order_by("abr")[-1]

    # download to the path, you can change this
    out_file = audio.download(output_path="C:\\Python\\youtube")

    # change name to, base + " by " + author, without any error.
    base, ext = os.path.splitext(out_file)
    print(yt.author, base, ext)
    forbidden_chars = '"*\\/\'|?:<>'
    author = ''.join([x if x not in forbidden_chars else '#' for x in yt.author])
    new = base + " by " + author
    os.rename(out_file, new+".webm")

    # ADDITIONAL : change webm to 320kbps mp3, by using pre-installed ffmpeg
    # This action needs a pre-installation of ffmpeg
    print(new)
    print(subprocess.run(f'ffmpeg -i "{new}.webm" -codec:a libmp3lame -b:a 320k "{new}.mp3"', shell=True,
                         capture_output=True).stdout)
