import os, re
from pytube import Playlist, YouTube
import subprocess

p = Playlist("https://www.youtube.com/playlist?list=PLVVB8cn1-HNLWOKM9Et_7x4Mmc93THDUk")
print(p.title, "Length:", len(p.video_urls))

# Test if the playlist is valid / length must be bigger than 10...
for i in p.video_urls[:10]:
    print(i)

# download_path here.
download_path = "C:\\Python\\youtube"

# Downloading
for num, i in enumerate(p.video_urls):
    # use_oauth : for download YouTube_Music-only, if you have YouTube Music account.
    yt = YouTube(i, use_oauth=True)

    # to see what filter has the best quality : here
    print("Filters :", len(yt.streams.filter(only_audio=True)), yt.streams.filter(only_audio=True).order_by("abr"))

    # the best quality : ~160kbps of webm, or the best of existing filters.
    audio = yt.streams.filter(only_audio=True).order_by("abr")[-1]

    # download to the path, you can change this.
    out_file = audio.download(output_path=download_path)

    # change name to, base + " by " + author, without any error.
    base, ext = os.path.splitext(out_file)
    print(yt.author, base, ext)

    # replace any forbidden_chars in author name.
    forbidden_chars = '*\\/|?:<>'
    author = ''.join([x if x not in forbidden_chars else ' ' for x in yt.author])

    # delete author name from video title.
    author_list = re.split(" |\.|,|\[|]|\(|\)|-|\*|<|>|〔|〕|【|】|（|）|／|｢|｣|『|』|「|」|　", author)
    base = str(base).replace(download_path+"\\", "")
    for sentence in author_list:
        base = base.replace(sentence, "")

    # trim author name.
    author.replace("- Topic", "")
    author.replace("Official", "")
    author.replace("Channel", "")
    author.replace("YouTube", "")
    author.strip()

    # make new name(address) with author and song name
    new = download_path + "\\" + author + " - " + base
    new = new.strip()

    os.rename(out_file, new+".webm")

    # ADDITIONAL : change webm to 320kbps mp3, by using pre-installed ffmpeg
    # This action needs a pre-installation of ffmpeg
    print(new)
    print(subprocess.run(f'ffmpeg -i "{new}.webm" -codec:a libmp3lame -b:a 320k "{new}.mp3"', shell=True,
                         capture_output=True).stdout)
    print(f"{num+1}/{len(p.video_urls)} = {round((num+1)/len(p.video_urls)*100, 2)}% finished.")
    os.remove(new+".webm")
    print("\n")


file_list = os.listdir(download_path)

for file in file_list:
    original = file
    file = file.replace("- Topic", "")
    file = file.replace("YouTube", "")
    file = file.replace("Video", "")
    file = file.replace("MV", "")
    file = file.replace("OFFICIAL", "")
    file = file.replace("Official", "")
    file = file.replace("Channel", "")
    file = file.replace("Music ", "")

    file = file.replace("　", "")
    file = file.replace("  ", " ")
    file = file.replace("  ", " ")
    file = file.replace("–", "-")
    file = file.replace("- -", "-")
    file = file.replace("--", "")

    os.rename(download_path+"\\"+original, download_path+"\\"+file)
