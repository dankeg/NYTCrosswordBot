# NYTCrosswordBot
Solves the NYT Crossword Mini using Selenium and the ChatGPT API.
Current version is designed for Chrome on MacOS. 

## How it Works
This script follows these basic step.
1. Use Selenium to launch Chrome
2. Find all of the clues by their HTML xpath, and scrape them
3. Provide the ChatGPT API these clues, and ask for the answers in a specific format
4. Paste these answers into the puzzle

If the responses are correct, the puzzle will be solved!
If not, a 300 second wait will keep the chrome browser alive, and let you fix any mistakes.

## Run Instructions
1. Clone the repository
2. Download the dependencies using `pip install -r requirements.txt"
3. Under `if __name__ == "__main__":`, replace the `url` and `key` fields with the puzzle URL, and the API key
4. Execute the script, and wait!