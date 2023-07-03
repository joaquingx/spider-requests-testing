import time
from bs4 import BeautifulSoup

from estela_requests import EstelaRequests
from estela_requests.estela_hub import EstelaHub

with EstelaRequests.from_estela_hub(EstelaHub.create_from_settings()) as requests:
    spider_name = "quotes_toscrape"
    # Send a GET request to the website
    for i in range(1, 4):
        print(f"page {i}")
        url = "http://quotes.toscrape.com/page/{page}/"
        response = requests.get(url.format(page=i))

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract the desired information from the parsed HTML
        quotes = []
        for quote in soup.find_all("div", class_="quote"):
            text = quote.find("span", class_="text").text
            author = quote.find("small", class_="author").text
            tags = [tag.text for tag in quote.find_all("a", class_="tag")]
            quotes.append({"text": text, "author": author, "tags": tags})

        # Print the extracted information
        for quote in quotes:
            item = {
                "quote": quote["text"],
                "author": quote["author"],
                "tags": ','.join(quote["tags"]),
            }
            requests.send_item(item)
            time.sleep(1)

