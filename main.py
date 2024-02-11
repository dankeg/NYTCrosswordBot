import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import time
import undetected_chromedriver as uc
from openai import OpenAI
from selenium.webdriver.common.action_chains import ActionChains
import json


class NYTCrosswordBot:
    """
    Solves the NYT Crossword Mini using Selenium and ChatGPT.

    Current iteration scrapes the horizontal clues, uses ChatGPT to get answers in a standardized manner,
    and inputs these answers to complete the puzzle.

    Future Avenues for Improvement:
        - Scrape how many characters are in each answer
        - Solve both vertical and horizonal clues, choose which one to use
        - Use vertical and horizontal answers to self-correct ChatGPT answers
            - Utilize the fact that 1 down and 1 across use the same letter to eliminate extraneous answers
        - Track already filled answer squares to avoid time-wasting mistypes
        - General speed improvements
    """

    def __init__(self, url: str, api_key: str):
        """
        Initializes the Selenium Webdriver for Chrome for use in other functions.

        Args:
            url (str): URL to the NYT crossword mini to solve
            api_key (str): ChatGPT API Key
        """
        self.url = url
        self.api_key = api_key
        self.driver = uc.Chrome(executable_path="/Applications/Google_Chrome.app")
        self.wait = WebDriverWait(self.driver, 5)
 
    def run_solver(self) -> None:
        """Runs the puzzle software with the initalized configurations."""
        self.launch_crossword(self.url)
        clue_list = self.scrape_clues()
        answer_list = self.query_chatgpt(clue_list)
        self.input_answers(answer_list)

    def launch_crossword(self, url: str) -> None:
        """
        Opens the crossword webpage, and starts the crossword.

        Args:
            url (str): URL of the crossword
        """
        self.driver.get(url)

        find_start = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "xwd__modal--subtle-button")))
        find_start = self.driver.find_element(By.CLASS_NAME, "xwd__modal--subtle-button")
        find_start.click()

    def scrape_clues(self) -> list[str]:
        """
        Scrapes the horizontal and vertical clues of the crossword.

        Does not collect the answer length, in chars, for each clue.
        Relies on the fact that all horizontal clues will be collected before all vertical by Selenium.

        Returns:
            list[str]: List of crossword hints from first to last (top to bottom).
        """
        find_clues = self.wait.until(EC.presence_of_element_located(("xpath", "//span[@class='xwd__clue--text xwd__clue-format']")))
        find_clues = self.driver.find_elements(By.XPATH, "//span[@class='xwd__clue--text xwd__clue-format']")

        clue_list = []
        for clue_html in find_clues:
            clue_list.append(clue_html.text)
        return clue_list

    def query_chatgpt(self, clues: list[str]) -> list[str]:
        """
        Queries ChatGPT with the scraped clues, returning the answers.

        Returns:
            list[str]: List of crossword answers from first to last (top to bottom).
        """
        client = OpenAI(api_key=self.api_key)

        completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": """You are a crossword puzzle solver. You are fed a list of crossword clues, 
            and output the answers as a json list of the answers as strings, in order, and nothing else. For example, ["apple", "dog", "frog"].""" },
            {"role": "user", "content": f"Solve this crossword:{str(clues)}"}
        ]
        )

        api_response = (completion.choices[0].message).content
        converted_obj = json.loads(api_response)
        return converted_obj

    def input_answers(self, answers: list[str]) -> None:
        """
        Inputs the answers to the crossword, solving the puzzle.

        Args:
            answers (list[str]): Answers to crossword hints, from top to bottom, starting with horizontal
        """
        find_clues = self.wait.until(EC.presence_of_element_located(("xpath", "//span[@class='xwd__clue--text xwd__clue-format']")))
        find_clues = self.driver.find_elements(By.XPATH, "//span[@class='xwd__clue--text xwd__clue-format']")

        for clues, answer in zip(find_clues, answers):
            clues.click()
            time.sleep(0.05)
            actions = ActionChains(self.driver)
            actions.send_keys(answer)
            actions.perform()
            time.sleep(0.05)


if __name__ == "__main__":
    url = "https://www.nytimes.com/crosswords/game/special/themed-mini"
    key = ""
    solver = NYTCrosswordBot(url=url, api_key=key)
    solver.run_solver()
