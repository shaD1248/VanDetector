import requests
from bs4 import BeautifulSoup
import schedule
import time
import androidhelper
import toga
from toga.style import Pack
from toga.style.pack import COLUMN

droid = androidhelper.Android()


class VanDetectorApp(toga.App):
    def __init__(self):
        super().__init__(name="VanDetector")

        self.urls_to_check = []
        self.search_words = []
        self.words_found = []


    def check_for_vancouver(self, dt=None):
        self.words_found = []
        for url in self.urls_to_check:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    found_words = [word for word in self.search_words if word in soup.get_text()]
                    if found_words:
                        self.words_found.extend(found_words)
            except requests.exceptions.RequestException as e:
                print(f"Error occurred while fetching '{url}': {e}")

        if self.words_found:
            unique_words_found = set(self.words_found)
            word_notification = ", ".join(unique_words_found)
            droid.makeToast(f"Notification: Search words found in at least one of the pages: {word_notification}")
        else:
            droid.makeToast("No search words found in any of the pages.")

    def startup(self):
        main_box = toga.Box(style=Pack(direction=COLUMN))

        input_urls = toga.MultilineTextInput(placeholder="Enter URLs (one URL per line)")
        input_search_words = toga.MultilineTextInput(placeholder="Enter the search words (one word per line)")
        btn_start = toga.Button("Start Checking", on_press=self.on_start_checking)

        main_box.add(input_urls)
        main_box.add(input_search_words)
        main_box.add(btn_start)

        self.main_window = toga.MainWindow(title=self.name)
        self.main_window.content = main_box
        self.main_window.show()

    def on_start_checking(self, widget):
        urls_input = self.main_window.content.children[0]
        search_words_input = self.main_window.content.children[1]

        self.urls_to_check = [url.strip() for url in urls_input.value.splitlines() if url.strip()]
        self.search_words = [word.strip() for word in search_words_input.value.splitlines() if word.strip()]

        # Run the function every ten minutes
        schedule.every(10).minutes.do(self.check_for_vancouver)

        # Start the schedule loop
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == '__main__':
    VanDetectorApp().main_loop()
