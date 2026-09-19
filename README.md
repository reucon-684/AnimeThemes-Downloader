# AnimeThemes Downloader

A lightweight command-line utility to download anime opening and ending themes directly from AnimeThemes.moe using a single anime URL.

---

## Features

- **Single URL Fetching**: Pass any single anime URL from AnimeThemes.moe to download all associated themes.
- **MP3 Download**: Extracts audio directly to clean MP3 files.
- **Automated Organization**: Automatically names and structures output files by anime title and theme type (OP/ED).
- **Fast & Minimal**: Zero bloated GUI dependencies—pure CLI speed.

---

## Installation

### Prerequisites
- Python 3.8 or higher
- Ffmpeg

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/reucon-684/AnimeThemes-Downloader.git

2. **Install Ffmpeg**

   you can download it manually from the official FFmpeg download page, 
   extract the zip and then copy everything inside the bin folder and
   paste it in the Desktop along with url.py.

### How To Use

1. **Get The Link:**
 Go to AnimeThemes.moe and pick your desired anime such as Attack on Titan.
 Copy the URL from the address bar it will look something like this
 https://animethemes.moe/anime/shingeki_no_kyojin
 now we successfully got the link.

2. **Run The CLI:**
Either double click or
   ```bash
   python url.py

# Advanced Options & Video Support (Pro Version)

Looking for video downloads, advanced filtering, or an interactive interface? Check out AnimeThemes Downloader Pro available on Gumroad:

- **Video Support**: Download themes in MP4 and WebM formats alongside MP3.
- **Graphical User Interface (GUI)**: Full desktop UI for easy point-and-click operation alongside the command-line utility.
- **Advanced Filters**: Exclude specific theme types (e.g., skip EDs, NC, or specific video resolutions).
- **Enhanced Downloading**: Utilizes the Torrent Archive in my Server dedicated specifically for Downloading
  instead of the usual AnimeThemes.moe API.

👉[Get the Pro Edition](https://gumroad.com/) or get the complete [Batch + URL Bundle](https://gumroad.com/) on Gumroad to unlock everything!

## Batch AnimeThemes Downloader
🚀 Need to download an entire animelist worth of OPs and EDs at once? Skip the manual links and check out the [Batch AnimeThemes Downloader!](https://github.com/reucon-684/Batch-AnimeThemes-Downloader)

## Support Me
If you find this tool helpful and want to support my other development or 
need technical help, feel free to buy me a coffee!

## License
This project is licensed under the GPL v3 License - see the LICENSE file for details.
