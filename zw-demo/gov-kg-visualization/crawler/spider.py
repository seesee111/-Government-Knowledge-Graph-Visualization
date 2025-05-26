import requests
from bs4 import BeautifulSoup
import json

class GovernmentCrawler:
    def __init__(self, start_urls):
        self.start_urls = start_urls
        self.data = []

    def fetch_page(self, url):
        response = requests.get(url, proxies={"http": None, "https": None})
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve {url}")
            return None

    def parse_page(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        # Example parsing logic (this should be customized based on the actual structure of the target pages)
        for item in soup.find_all('div', class_='gov-info'):
            title = item.find('h2').text
            content = item.find('p').text
            self.data.append({'title': title, 'content': content})

    def run(self):
        for url in self.start_urls:
            html = self.fetch_page(url)
            if html:
                self.parse_page(html)

    def save_data(self, filename='government_data.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    start_urls = [
        'https://www.lnzwfw.gov.cn/wyk/fwqd/sxml/',
        # 'https://example.gov/info2',
        # Add more URLs as needed
    ]
    crawler = GovernmentCrawler(start_urls)
    crawler.run()
    crawler.save_data()