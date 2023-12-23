import os

class ImageDownloaderBase:
    def __init__(self, query, max_images=10):
        self.query = query
        self.max_images = max_images
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36'
        }

    def perform_search(self):
        raise NotImplementedError

    def download_images(self):
        raise NotImplementedError
