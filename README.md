# Simple Audio Converter

## Description
- One-click audio converter from any audio file to `mp3/wav/flac/aac` with using python and pydub. Simple to use, absolutely free.
- I needed to convert a lot of files from `m4a` to `mp3` format, but didn't find a convenient free solution. I wrote this simple converter and hope it will help someone else.

## How to use
1. Select the files you want to convert;
2. Select the format you want to convert to;
3. Press convert!
4. The results will be in the folder `results/convert to $'selected format' $'date' $'time'`

## Supported formats
- input: all formats supported by ffmpeg
- output: mp3, wav, flac, aac

## How to install

### If you are on Windows:
- You can just download archive `converter.zip`, unpack all contents to some folder, and run `converter.exe`
- You can also run `application.py` with `python`, but need to install `requirements.txt` and `ffmpeg` ([link](https://ffmpeg.org/download.html))

### Else:
- You can run `application.py` with `python` after installing `requirements.txt` and `ffmpeg` (check [this page](https://github.com/jiaaro/pydub))