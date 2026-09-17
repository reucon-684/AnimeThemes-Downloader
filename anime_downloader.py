import os
import re
import shutil
import subprocess
import requests

# ==================== CONFIGURATION ====================
OUTPUT_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")
# =======================================================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

if not shutil.which("ffmpeg"):
    print("[-] CRITICAL ERROR: 'ffmpeg' executable not found in system PATH.")
    print("    Install FFmpeg or add its path to environment variables.")
    exit(1)

def sanitize_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "", name)

def extract_slug(url_or_slug):
    cleaned = url_or_slug.strip().rstrip('/')
    if 'animethemes.moe/anime/' in cleaned:
        return cleaned.split('animethemes.moe/anime/')[-1].split('/')[0]
    elif '/' in cleaned:
        return cleaned.split('/')[-1]
    return cleaned

def download_anime_themes(anime_input):
    slug = extract_slug(anime_input)
    if not slug:
        print("[-] Invalid URL or anime slug provided.")
        return

    api_url = f"https://api.animethemes.moe/anime/{slug}"
    params = {
        "include": "animethemes.animethemeentries.videos,images"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AniListDownloader/1.0"
    }

    try:
        res = requests.get(api_url, params=params, headers=headers, timeout=10)
        if res.status_code == 404:
            print(f"[-] Anime not found on AnimeThemes for slug: '{slug}'")
            return
        elif res.status_code != 200:
            print(f"[-] API HTTP {res.status_code} error.")
            return

        target_anime = res.json().get("anime", {})
    except Exception as e:
        print(f"[-] Network Exception: {e}")
        return

    anime_name = target_anime.get('name', slug)
    print(f"\n[+] Found Anime: {anime_name}")

    # Extract Cover Image URL
    images = target_anime.get("images", [])
    cover_url = None
    for img in images:
        if img.get("facet") in ["Large Cover", "Small Cover"]:
            cover_url = img.get("link")
            break
    if not cover_url and images:
        cover_url = images[0].get("link")

    temp_cover_path = os.path.join(OUTPUT_FOLDER, "_temp_cover.jpg")
    has_cover = False
    if cover_url:
        try:
            img_res = requests.get(cover_url, headers=headers, timeout=10)
            if img_res.status_code == 200:
                with open(temp_cover_path, "wb") as f:
                    f.write(img_res.content)
                has_cover = True
        except Exception:
            has_cover = False

    themes = target_anime.get("animethemes", [])
    if not themes:
        print("[-] No themes found for this anime.")

    for theme in themes:
        theme_type = theme.get("slug", "") or theme.get("type", "")

        # Includes OP (Openings), ED (Endings), and IN (Insert Songs)
        if not (theme_type.startswith("OP") or theme_type.startswith("ED") or theme_type.startswith("IN")):
            continue

        for entry in theme.get("animethemeentries", []):
            for video in entry.get("videos", []):
                audio_url = video.get("link")
                if not audio_url:
                    continue

                song_name = sanitize_filename(f"{anime_name} - {theme_type}")
                output_path = os.path.join(OUTPUT_FOLDER, f"{song_name}.mp3")

                if os.path.exists(output_path):
                    print(f"    [~] Already downloaded: {song_name}")
                    break

                print(f"    [!] Downloading: {song_name}")

                if has_cover:
                    cmd = [
                        "ffmpeg", "-y",
                        "-i", audio_url,
                        "-i", temp_cover_path,
                        "-map", "0:a",
                        "-map", "1:v",
                        "-q:a", "0",
                        "-c:v", "mjpeg",
                        "-disposition:v", "attached_pic",
                        "-id3v2_version", "3",
                        "-metadata", f"title={song_name}",
                        "-metadata", f"artist={anime_name}",
                        output_path
                    ]
                else:
                    cmd = [
                        "ffmpeg", "-y",
                        "-i", audio_url,
                        "-vn",
                        "-q:a", "0",
                        "-id3v2_version", "3",
                        "-metadata", f"title={song_name}",
                        "-metadata", f"artist={anime_name}",
                        output_path
                    ]

                result = subprocess.run(cmd, capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"    [-] FFmpeg Error: {result.stderr.strip()[-150:]}")
                else:
                    print(f"    [+] Saved: {song_name}.mp3")
                break

    if os.path.exists(temp_cover_path):
        try:
            os.remove(temp_cover_path)
        except Exception:
            pass

    print(f"\n[+] Processing complete for '{anime_name}'. Files saved to {OUTPUT_FOLDER}")

def main():
    print("==================================================")
    print("             AnimeThemes Downloader       ")
    print("==================================================")

    while True:
        url_input = input("\nEnter AnimeThemes URL (e.g. https://animethemes.moe/anime/oshi_no_ko): ").strip()
        if url_input:
            download_anime_themes(url_input)

        again = input("\nDo you want to download another anime OP/ED/IN? (y/n): ").strip().lower()
        if again not in ['y', 'yes']:
            print("\n[+] Exiting program. Enjoy your songs!")
            break

if __name__ == "__main__":
    main()