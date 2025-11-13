import os, re, requests, instaloader

def download_instagram_video(url):
    try:
        shortcode = re.search(r"/(reel|p|tv)/([^/?]+)", url).group(2)
        loader = instaloader.Instaloader(dirname_pattern="downloads", filename_pattern=shortcode, save_metadata=False)
        loader.download_post(instaloader.Post.from_shortcode(loader.context, shortcode), target=".")
        for file in os.listdir("."):
            if file.startswith(shortcode) and file.endswith(".mp4"):
                return file
    except Exception as e:
        print("Error:", e)
        return None
