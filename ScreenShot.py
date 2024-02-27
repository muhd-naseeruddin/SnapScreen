import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.service import Service
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from PIL import Image
import io



def init_driver():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.2277.112"
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    # "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    


    edge_driver_manager = EdgeChromiumDriverManager()
    edge_driver_path = edge_driver_manager.install()

    edge_service = Service(executable_path=edge_driver_path)
    options_ = Options()
    options_.use_chromium = True  # Use Chromium-based Edge
    options_.add_argument('--disable-notifications')
    options_.add_argument('--disable-infobars')
    options_.add_argument('--disable-extensions')
    options_.add_argument('--lang=en')
    options_.add_argument('--headless=new')
    options_.add_argument('--ignore-certificate-errors')
    options_.add_argument("--window-size=1920,1080")
    options_.add_argument(f"user-agent={user_agent}")
    driver = webdriver.Edge(service=edge_service, options=options_)
    
    return driver, edge_service

# Close the driver and service
def close_driver(driver, edge_service):
    # global driver, service
    if driver:
        driver.quit()
    
    if edge_service:
        edge_service.stop()
    

def create_folder_if_not_exists(name, folder_path):
    cleaned_name = name.replace("/", "")
    full_folder_path = os.path.join(folder_path, cleaned_name)
    base_folder_path = os.path.basename(folder_path)

    if base_folder_path.lower() == cleaned_name.lower():
        pass
    elif not os.path.exists(full_folder_path):
        os.makedirs(full_folder_path)

def screenshotPath(folder_path, name, screenshot_name):
    # cleaned_name = name.replace("'", "")
    cleaned_name = name.replace("/", "")
    screenshot_name = screenshot_name.replace("/", "")
    full_folder_path = os.path.join(folder_path, cleaned_name)
    base_folder_path = os.path.basename(folder_path)

    if base_folder_path.lower() == cleaned_name.lower():
        screenshot_path = os.path.join(folder_path, screenshot_name)
        return screenshot_path
    else:
        screenshot_path = os.path.join(full_folder_path, screenshot_name)
        return screenshot_path

def automate_website_sprm(name, folder_path):
    driver, edge_service = init_driver()
    try:
        url = r"https://www.sprm.gov.my/index.php?id=21&page_id=96"
        driver.get(url)

        input_xpath = "/html/body/div[3]/div[3]/div/form/div/div[3]/input"

        # Wait for a few seconds for website to load
        wait = WebDriverWait(driver, 10)
        input_element = wait.until(EC.visibility_of_element_located((By.XPATH, input_xpath)))
        carian_button = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[text()='Carian']")))

        input_element.clear()
        input_element.send_keys(name)

        driver.execute_script("arguments[0].click();", carian_button)

        time.sleep(2)
        container_divs = driver.find_elements(By.XPATH, "//div[@class='container']")
        if len(container_divs) >= 4:
            fourth_container_divs = container_divs[3]
            div_location = fourth_container_divs.location
            div_size = fourth_container_divs.size
            driver.execute_script("arguments[0].scrollIntoView();", fourth_container_divs)
            time.sleep(2)
            screenshot_name = fr"{name} - Malaysian Anti Corruption Commission.png" #Change this according to your path
            screenshot_path=screenshotPath(folder_path=folder_path, name=name, screenshot_name=screenshot_name)
            fourth_container_divs.screenshot(screenshot_path)
    finally:
        close_driver(driver, edge_service)

def automate_website_ccid(phone, name, folder_path):
    driver, edge_service = init_driver()
    try:

        ccid_url = 'https://semakmule.rmp.gov.my/'
        driver.get(ccid_url)

        # Handle SSL certificate error
        try:
            advanced_button = driver.find_element(By.ID, "details-button")
            advanced_button.click()

            proceed_link = driver.find_element(By.ID, "proceed-link")
            proceed_link.click()
        except NoSuchElementException:
            pass 

        # Wait for the iframe to be present
        wait = WebDriverWait(driver, 10)
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[@src='index0.cfm']")))

        # Switch to the iframe
        driver.switch_to.frame(iframe)

        kategori_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//select[@name='kategoriCARIAN']"))
        )

        select = Select(kategori_element)
        select.select_by_visible_text("Nombor Telefon")

        katakunci_element = driver.find_element(By.XPATH, "//input[@name='KeywordCARIAN']")
        katakunci_element.send_keys(phone)

        # Now you're inside the iframe, find the image element
        img_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'capcha')]"))
        )

        # Extract the last 4 characters from the src attribute
        src_attribute = img_element.get_attribute("src")
        dynamic_part = src_attribute[-8:-4]

        capcha_element = driver.find_element(By.XPATH, "//input[@name='KodKeselanatanCCIS']")
        capcha_element.send_keys(dynamic_part)
        semak_button = driver.find_element(By.XPATH, "//input[@name='CariMAklumatJSM']")
        driver.execute_script("arguments[0].click();", semak_button)

        center_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//center"))
        )
        screenshot_name = fr"{name} - Commercial Crime Investigation Department.png" #Change accordingly
        screenshot_path=screenshotPath(folder_path=folder_path, name=name, screenshot_name=screenshot_name)

        screenshot = driver.get_screenshot_as_png()
        screenshot_image = Image.open(io.BytesIO(screenshot))
        screenshot_width, screenshot_height = screenshot_image.size
        area_to_keep_height = 630

        # Calculate the coordinates for cropping
        crop_left = 530
        crop_upper = 0
        crop_right = 1770
        crop_lower = area_to_keep_height

        # Crop the image
        cropped_screenshot = screenshot_image.crop((crop_left, crop_upper, crop_right, crop_lower))

        # Save the cropped screenshot to a file
        cropped_screenshot.save(screenshot_path)


        driver.switch_to.default_content()
    
    finally:
        close_driver(driver, edge_service)

def automate_website_rmp(name, folder_path):
    driver, edge_service = init_driver()
    try:
        rmp_url = 'https://www.rmp.gov.my/'
        driver.get(rmp_url)
        cleaned_name = '"' + name.replace("'", "") + '"'

        main_window = driver.current_window_handle
        for window_handle in driver.window_handles:
            if window_handle != main_window:
                # Switch to the pop-up window
                driver.switch_to.window(window_handle)
                
                # Close the pop-up window
                driver.close()
                
                # Switch back to the main window
                driver.switch_to.window(main_window)
                break
        
        #Wait website to load
        wait = WebDriverWait(driver, 5)
        search_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@id='Contentplaceholder1_T9A41B79F003_ctl00_ctl00_searchTextBox']")))
        #Send name into search box
        search_box.send_keys(cleaned_name)
        #Click submit button
        search_button = driver.find_element(By.XPATH, "//input[@id='Contentplaceholder1_T9A41B79F003_ctl00_ctl00_searchButton']")
        driver.execute_script("arguments[0].click();", search_button)
        wait.until(EC.presence_of_element_located((By.XPATH, '//strong/span[contains(text(), "Keputusan Carian")]')))

        #Change accordingly screenshot path
        screenshot_name = fr"{name} - Royal Malaysia Police.png" #Change accordingly
        screenshot_path=screenshotPath(folder_path=folder_path, name=name, screenshot_name=screenshot_name)
        screenshot = driver.get_screenshot_as_png()
        screenshot_image = Image.open(io.BytesIO(screenshot))
        screenshot_width, screenshot_height = screenshot_image.size
        area_to_keep_height = 480
        # Calculate the coordinates for cropping
        crop_left = 500
        crop_upper = 0
        crop_right = 1820
        crop_lower = area_to_keep_height
        # Crop the image
        cropped_screenshot = screenshot_image.crop((crop_left, crop_upper, crop_right, crop_lower))
        # Save the cropped screenshot to a file
        cropped_screenshot.save(screenshot_path)
    finally:
        close_driver(driver, edge_service)

def automate_website_kehakiman(name, folder_path):
    driver, edge_service = init_driver()
    try:
        kehakiman_url = 'https://cms2.kehakiman.gov.my/CommonWeb/ejudgment/SearchPage.aspx?JurisdictionType=ALL'
        driver.get(kehakiman_url)
        wait = WebDriverWait(driver, 20)

        # Wait for the page to load
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-id='divEJudgmentPortalSearchPageControl']")))
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@data-resourceproviderkey='lblCourtCategory']")))

        #Save total record to compare later
        total_record_element = driver.find_element(By.XPATH, "//span[@data-id='TotalRecord']")
        initial_total_record = total_record_element.text

        #Select cari box
        cari_box = driver.find_elements(By.XPATH, "//input[@data-control='GenerateControlPlaceholder']")
        cari_box_1 = cari_box[1]
        cari_box_1.send_keys(name)

        #Click Cari button
        cari_button = driver.find_element(By.XPATH, "//input[@data-type='btnSearch']")
        cari_button.click()

        while True:
            total_record_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-id='TotalRecord']")))
            updated_total_record = total_record_element.text

            if updated_total_record != initial_total_record:
                break  # Exit the loop
                
            else:
                print("Total record has not changed. Current:", updated_total_record)


        #Select Mahkamah Persekutuan
        category_element = driver.find_element(By.XPATH, "//span[@data-type='ddlCourtCategory']")
        category_element.click()

        try:
            persekutuan_element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Mahkamah Persekutuan')]")))
        except Exception:
            # If the element is not found, find the "Federal Court" element
            persekutuan_element = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, "//li[contains(text(), 'Federal Court')]")))
        persekutuan_element.click()

        #Select Jenayah
        kes_element = driver.find_element(By.XPATH, "//span[@data-type='ddlCaseType']")
        kes_element.click()

        try:
            jenayah_element = driver.find_element(By.XPATH, "//li[contains(text(), 'Jenayah')]")
        except Exception:
            jenayah_element = driver.find_element(By.XPATH, "//li[contains(text(), 'Criminal')]")
        jenayah_element.click()

        total_record_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-id='TotalRecord']")))
        current_total_record = total_record_element.text
        #Click Cari button
        cari_button.click()

        screenshot_federal = fr"{name} - Federal Court.png" #Change this according to your path
        screenshot_path_federal=screenshotPath(folder_path=folder_path, name=name, screenshot_name=screenshot_federal)

        while True:
            total_record_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-id='TotalRecord']")))
            updated_total_record = total_record_element.text

            if updated_total_record == current_total_record:
                # Take a screenshot
                driver.save_screenshot(screenshot_path_federal)  # Replace with the desired screenshot filename
                
                break  # Exit the loop
                
            else:
                print("Total record has changed. Current:", updated_total_record)


        #Select Mahkamah Rayuan
        category_element.click()

        try:
            rayuan_element = driver.find_element(By.XPATH, "//li[contains(text(), 'Mahkamah Rayuan')]")
        except Exception:
            rayuan_element = driver.find_element(By.XPATH, "//li[contains(text(), 'Court of Appeal')]")
        rayuan_element.click()

        total_record_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-id='TotalRecord']")))
        current_total_record = total_record_element.text
        cari_button.click()

        screenshot_appeal = fr"{name} - Appeal Court.png" #Change this according to your path
        screenshot_path_appeal=screenshotPath(folder_path=folder_path, name=name, screenshot_name=screenshot_appeal)

        while True:
            total_record_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-id='TotalRecord']")))
            updated_total_record = total_record_element.text

            if updated_total_record == current_total_record:
                # Take a screenshot
                driver.save_screenshot(screenshot_path_appeal)  # Replace with the desired screenshot filename
                
                break  # Exit the loop
                
            else:
                print("Total record has changed. Current:", updated_total_record)


        #Select Mahkamah Tinggi
        category_element.click()
        try:
            tinggi_element = driver.find_element(By.XPATH, "//li[contains(text(), 'Mahkamah Tinggi')]")
        except Exception:
            tinggi_element = driver.find_element(By.XPATH, "//li[contains(text(), 'High Court')]")
        tinggi_element.click()
        total_record_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-id='TotalRecord']")))
        current_total_record = total_record_element.text
        cari_button.click()

        screenshot_high = fr"{name} - High Court.png" #Change this according to your path
        screenshot_path_high=screenshotPath(folder_path=folder_path, name=name, screenshot_name=screenshot_high)

        while True:
            total_record_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-id='TotalRecord']")))
            updated_total_record = total_record_element.text

            if updated_total_record == current_total_record:
                # Take a screenshot
                driver.save_screenshot(screenshot_path_high)  # Replace with the desired screenshot filename
                
                break  # Exit the loop
                
            else:
                print("Total record has changed. Current:", updated_total_record)


        #Select Mahkamah Sesyen
        category_element.click()
        try:
            sesyen_element = driver.find_element(By.XPATH, "//li[contains(text(), 'Mahkamah Sesyen')]")
        except Exception:
            sesyen_element = driver.find_element(By.XPATH, "//li[contains(text(), 'Sessions Court')]")
        sesyen_element.click()
        total_record_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-id='TotalRecord']")))
        current_total_record = total_record_element.text
        cari_button.click()

        screenshot_session = fr"{name} - Session Court.png" #Change this according to your path
        screenshot_path_session=screenshotPath(folder_path=folder_path, name=name, screenshot_name=screenshot_session)

        while True:
            total_record_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-id='TotalRecord']")))
            updated_total_record = total_record_element.text

            if updated_total_record == current_total_record:
                # Take a screenshot
                driver.save_screenshot(screenshot_path_session)  # Replace with the desired screenshot filename
                
                break  # Exit the loop
                
            else:
                print("Total record has changed. Current:", updated_total_record)


        #Select Mahkamah Majistret
        category_element.click()
        try:
            magistrate_element = driver.find_element(By.XPATH, "//li[contains(text(), 'Mahkamah Majistret')]")
        except Exception:
            magistrate_element = driver.find_element(By.XPATH, "//li[contains(text(), 'Magistrate Court')]")
        magistrate_element.click()
        total_record_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-id='TotalRecord']")))
        current_total_record = total_record_element.text
        cari_button.click()

        screenshot_magistrate = fr"{name} - Magistrate Court.png" #Change this according to your path
        screenshot_path_magistrate=screenshotPath(folder_path=folder_path, name=name, screenshot_name=screenshot_magistrate)

        while True:
            total_record_element = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@data-id='TotalRecord']")))
            updated_total_record = total_record_element.text

            if updated_total_record == current_total_record:
                # Take a screenshot
                driver.save_screenshot(screenshot_path_magistrate)  # Replace with the desired screenshot filename
                
                break  # Exit the loop
                
            else:
                print("Total record has changed. Current:", updated_total_record)
    finally:
        close_driver(driver, edge_service)



# close_driver()