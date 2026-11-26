import os
from pathlib import Path

from dotenv import load_dotenv
from selenium import webdriver

from utils import browser

load_dotenv()

ROOT_DIR = Path(__file__).parent.parent.parent
WEB_DRIVER_PATH = ROOT_DIR / "bin" / os.getenv("WEB_DRIVER", "")


def make_chrome_browser(*options: str) -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()

    if options:
        for option in options:
            chrome_options.add_argument(option)

    if os.getenv("SELENIUM_HEADLESS") == "1":
        chrome_options.add_argument("--headless")

    chrome_service = webdriver.ChromeService(executable_path=str(WEB_DRIVER_PATH))
    return webdriver.Chrome(options=chrome_options, service=chrome_service)


if __name__ == "__main__":
    options = [
        "--incognito",  # Start in private mode.
        "--headless",  # No HUD.
    ]
    browser = make_chrome_browser(*options)
    browser.get("https://www.google.com.br")
