import time
# Record the start time
start_time = time.time()

# Run code here:

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd

service = Service(ChromeDriverManager().install())

options = webdriver.ChromeOptions()
options.add_argument("headless")

browser = webdriver.Chrome(service=service)

url_home = "https://www.etfsbrasil.com.br/"
url_rk = "https://www.etfsbrasil.com.br/rankings"

#Get the website
browser.get(url_rk)

# Achando o texto de todas as "Tabs" na página ranking de ETF's Brasil
tabs = browser.find_elements(By.XPATH, "//div[@class='tabs_buttons__JknHt']/*")
tab_options = []
for tb in tabs:
    # Remove newline characters from the text using the replace() method
    tab_text = tb.text.replace("\n", "")
    tab_options.append(tab_text)

# Defining the function scrape_tab with parameter tab_name
def scrape_tab(tab_name):
    tab_choice = browser.find_element(By.XPATH, "//button[.='" + tab_name + "']")
    tab_choice.click()

    buttons = browser.find_elements(By.XPATH, '//button[contains(text(), "Ver todos")]')
    for btn in buttons:
        btn.click()

    # Find the "h3" tags on the page
    h3_tags = browser.find_elements(By.TAG_NAME, "h3")

    # Get the text of each "h3" tag
    h3_texts = []
    for h3_tag in h3_tags:
        h3_texts.append(h3_tag.text)

    # Getting the tables in the page
    tables = browser.find_elements(By.TAG_NAME, 'table')

    # Create an ExcelWriter object
    writer = pd.ExcelWriter('Tabelas ' + tab_name + '.xlsx', engine='xlsxwriter')
    sheet_index = 0

    # Read the first HTML table into a DataFrame
    header_df = pd.read_html(tables[0].get_attribute('outerHTML'))[0]

    # Loop through each table element, starting from the second one
    for table in tables[1:]:
        # Read the HTML table into a DataFrame
        df = pd.read_html(table.get_attribute('outerHTML'))[0]
        # Check if the DataFrame has more than one row
        if len(df) > 0:
            # Write the DataFrame to a sheet in the Excel file, with the first row as the header
            df.to_excel(writer, index=False, header=header_df.columns, startrow=1, sheet_name=f"{h3_texts[sheet_index]}")
            sheet_index += 1
    
    # Save the Excel file
    writer.save()

# Run code for tables on ETF's Brasil Ranking's Tab
for tab_name in tab_options:
    scrape_tab(tab_name)

# Run code for Web Site HOME tables - ETF's & BDR's

#Get the website
browser.get(url_home)




# Record the end time
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print('Elapsed time:', elapsed_time, 'seconds')