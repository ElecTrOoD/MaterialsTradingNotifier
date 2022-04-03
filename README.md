# How use it

1. Clone repository
2. Install python 3 from [python.org](https://www.python.org/)
3. Install requirements packages

 ```
 pip install -r requirements.txt
 ```

4. Install [Google Chrome Browser](https://www.google.com/chrome/)
5. Download [ChromeWebDriver](https://chromedriver.chromium.org/downloads) for your browser version and put it in the
   folder with the script
6. Generate a list of the required materials on the [Inara website](https://inara.cz/market-materials/), click the
   search button and copy the link of the page
7. Run script using shell

 ```
 python materials_notifier.py
 ```

8. Wait for the beep and then check the previously opened page

The script opens the browser in headless mode every 15 seconds, parses the data from the table of materials and closes
the browser, the load on the system should be minimal.