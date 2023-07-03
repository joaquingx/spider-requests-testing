from estela_requests import EstelaRequests
from estela_requests.estela_hub import EstelaHub
from bs4 import BeautifulSoup
from urllib.parse import urljoin

spider_name = "bbcnews"
with EstelaRequests.from_estela_hub(EstelaHub.create_from_settings()) as requests:
    #spider_name = "dora"
    def spider(url, depth=2):
        visited = set()
        queue = [(url, 0)]

        while queue:
            current_url, current_depth = queue.pop(0)

            if current_url in visited or current_depth > depth:
                continue

            try:
                response = requests.get(current_url)
            except requests.exceptions.RequestException:
                continue

            visited.add(current_url)

            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract information from the current page
            # You can customize this part to scrape the data you need
            # For example, find all <a> tags and extract their href attribute
            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href:
                    absolute_url = urljoin(current_url, href)
                    raro = {"url": absolute_url}
                    requests.send_item(raro)
                    print(raro)
                    # Add the new link to the queue
                    queue.append((absolute_url, current_depth + 1))

    # Start crawling from a specific URL with a depth of 2
    spider('https://example.com', depth=1)
