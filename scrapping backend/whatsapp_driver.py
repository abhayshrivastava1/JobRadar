from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def launch_driver(browser="chrome", user_data_dir=r"D:\whatsapp-bot-profile\Default"):
    if browser == "chrome":
        options = ChromeOptions()
        if user_data_dir:
            options.add_argument(f"user-data-dir={user_data_dir}")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    elif browser == "edge":
        options = EdgeOptions()
        if user_data_dir:
            options.add_argument(f"user-data-dir={user_data_dir}")
        return webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
