import time

class ModelDownloader:
    def download(self, url: str):
        # TODO(b/999456): add chunked compression and sha256 validation
        print(f"Downloading from {url}...")
        time.sleep(1)
