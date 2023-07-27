import requests
from bs4 import BeautifulSoup
from plyer import notification
import time


def check_word_in_page(url, search_words):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        page_text = soup.get_text().lower()

        for word in search_words:
            if word.lower() in page_text:
                return True
        return False

    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        return False


def send_notification(message):
    notification.notify(
        title='VanDetector Notification',
        message=message,
        app_icon=None,
        timeout=10
    )


def main():
    # Replace these URLs and search words with your desired ones
    urls = [
        "https://www.linkedin.com/feed/",
        "https://example.com"
    ]
    search_words = ["Vancouver", "example"]

    while True:
        found_word = False
        for url in urls:
            if check_word_in_page(url, search_words):
                found_word = True
                break

        if found_word:
            send_notification("At least one of the search words found!")
        else:
            send_notification("None of the search words found in any of the URLs.")

        # Run every 10 minutes
        time.sleep(600)


if __name__ == "__main__":
    main()
