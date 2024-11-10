from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/api/politic', methods=['GET'])
def get_politics():
    # URL of the news webpage (can change to a list and loop over)
    url = "https://www.foxnews.com/" # for now lets use fox news

    # Send a GET request to the URL
    response = requests.get(url)

    news_data = list() # will contain tuples of the form (title, link)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all news items; this will depend on the website's HTML structure
        articles = soup.find_all('h3', class_='title')  # Example: Find all <h3> tags with class 'title'

        # Iterate over the articles and extract titles and links
        for article in articles:
            a_tag = article.find('a')
            if (a_tag == None):
                continue

            title = a_tag.text.strip()  # Get the title text
            link = a_tag['href']  # Get the link (URL)
            
            news_data.append((title, link))
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

    return jsonify(news_data)

if __name__ == '__main__':
    port = 5555
    app.run(port = port)
