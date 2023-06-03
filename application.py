from flask import Flask, request, render_template
from selenium import webdriver
import time
from selenium.webdriver.chrome.service import Service
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

def get_driver():
    service = Service(ChromeDriverManager(path='/tmp/').install())
    options = webdriver.ChromeOptions()
    options.add_argument("--verbose")
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument("--window-size=1920, 1200")
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=service, options=options)
    return driver

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the search criterion from the form
        search_string = request.form['search_string']
        
        # Run the scraping script
        driver = get_driver()
        res_data = scrape_google_maps(search_string, driver)
        time.sleep(2)
        
        # Return the results to the template for rendering
        return render_template('results.html', res_data=res_data)
    
    return render_template('index.html')

def scrape_google_maps(search_string, driver):
    # Opening google maps website
    driver.get('https://www.google.com/maps?q=' + search_string + "&start=" + str(0))

    # Define Database to store result values
    # Title = Name of restaurant
    # rating = Star rating of restaurant out of 5
    # nor = Total number of reviews of restaurant
    # link = link to restaurant page
    column_names = ['Title', 'rating', 'nor', 'link']
    res_data = pd.DataFrame(columns=column_names)

    # Define loop to scroll the webpage to load all the restaurants on one page
    k = 0
    while k < 20:
        temp_res = driver.find_elements("xpath", "//div[contains(@aria-label, 'Results')]/div//a[contains(@href, 'http')]")
        action = ActionChains(driver)
        action.move_to_element(temp_res[(len(temp_res)) - 1]).perform()
        temp_res[(len(temp_res)) - 1].location_once_scrolled_into_view
        k += 1

    # Waiting to load
    time.sleep(1)

    # Scrape result list from the results page
    res_list = driver.find_elements(By.CLASS_NAME, 'Nv2PK.THOPZb.CpccDe')

    # Loop to save data of each result in a dataframe
    for i in range(len(res_list)):
        try:
            # Check for the required data and save it to the dataframe.
            # If no data available, continue to the next iteration
            title = res_list[i].find_element(By.CSS_SELECTOR, 'div.NrDZNb').text
            rating = res_list[i].find_element(By.CSS_SELECTOR, 'span.MW4etd').text
            NOR = int(res_list[i].find_element(By.CSS_SELECTOR, 'span.UY7F9').text.replace("(", "").replace(")",
                                                                                                             "").replace(
                ",", ""))
            link = res_list[i].find_element(By.CSS_SELECTOR, 'a.hfpxzc').get_attribute('href')
            temp_data = pd.DataFrame({'Title': [title], 'rating': [rating], 'nor': [NOR], 'link': [link]})
            res_data = pd.concat([res_data, temp_data], ignore_index=True)
        except:
            continue
    
    # Sort the data by 'nor' (total number of reviews)
    res_data = res_data.apply(pd.to_numeric, errors='ignore')
    res_data = res_data.sort_values(by='nor', axis=0, ascending=False, ignore_index=True)
    
    return res_data

if __name__ == '__main__':
    app.run(debug=True, port=5000)
