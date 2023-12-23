from bs4 import BeautifulSoup
import requests
from common import ImageDownloaderBase
from postgres_connector import PostgreSQLConnector
import os

class GoogleImageDownloader(ImageDownloaderBase):
    def __init__(self, query, max_images=10):
        super().__init__(query, max_images)
        self.database_connection = PostgreSQLConnector("google", "alireza", "2873", "postgres", 5432)

    def db_manipulator(self):
        self.database_connection = PostgreSQLConnector("google", "alireza", "2873", "postgres", 5432)
        self.database_connection.connect()
        self.database_connection.execute_query(
            "CREATE TABLE IF NOT EXISTS image_table (id SERIAL PRIMARY KEY, title VARCHAR(255), image_file BYTEA);")

    def perform_search(self):
        search_url = f"https://www.google.com/search?q={self.query}&tbm=isch"
        response = requests.get(search_url, headers=self.headers)
        response.raise_for_status()
        return BeautifulSoup(response.text, 'html.parser')

    def download_images(self):
        soup = self.perform_search()
        img_tags = soup.find_all('img', {'class': 'Q4LuWd'})

        image_count = 0
        for img_tag in img_tags:
            if image_count >= self.max_images:
                break
            try:
                img_url = img_tag.get('data-src') or img_tag.get('src')
                response = requests.get(img_url)
                response.raise_for_status()

                self.database_connection.execute_query(
                    "INSERT INTO image_table (title, image_file) VALUES (%s, %s) ;",
                    (img_tag['alt'], psycopg2.Binary(response.content))
                )
                image_count += 1
            except Exception as e:
                print(f"Error downloading image: {e}")

        self.database_connection.disconnect()


def main():
    query = os.environ.get('IMAGE_NAME')
    max_images = int(os.environ.get('MAX_IMAGE'))

    downloader = GoogleImageDownloader(query, max_images)
    downloader.download_images()


if __name__ == "__main__":
    main()
