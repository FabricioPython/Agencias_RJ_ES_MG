from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from rich.console import Console





class Scraping:
    
    def __init__(self, url:str):
        self.console = Console()
        self.url = url
        self.options = chrome_options = Options()

        self.options.add_argument(
            "--headless=new"
            )
        
        self.options.add_argument(
            "--disable-gpu")
        #self.options.timeouts = {'script':3, 'implicit':3}
        
    def __enter__(self):
        self.service = Service(
            ChromeDriverManager().install()
            )
        self.scraping = webdriver.Chrome(
            service=self.service, options=self.options
            )
        self.scraping.implicitly_wait(5)
        self.scraping.get(self.url)
        return self.scraping

    def __exit__(self, exc_type, exc_value, exc_trace):
        if exc_type != None:
            self.console.print(
                f"Erro do tipo:{exc_type} | {exc_value}, {exc_trace}", style="red"
                )
        else:    
            self.scraping.quit()




'''with Scraping(url='sua url') as driver:
    # identificar
    # selecionar
    # tratar
    ...'''
    