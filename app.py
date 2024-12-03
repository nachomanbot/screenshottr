# requirements.txt
streamlit
selenium
webdriver-manager
pillow

# app.py
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from PIL import Image

# Function to take screenshots using Selenium
def take_screenshots(urls, output_dir, mobile_view):
    chrome_options = Options()
    if mobile_view:
        chrome_options.add_experimental_option("mobileEmulation", {"deviceName": "iPhone X"})
    else:
        chrome_options.add_argument("--window-size=1920,1080")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    for index, url in enumerate(urls):
        if url.strip():
            try:
                # Create sub-folder for each URL based on its domain
                domain = url.split("//")[-1].split("/")[0]
                domain_folder = os.path.join(output_dir, domain)
                if not os.path.exists(domain_folder):
                    os.makedirs(domain_folder)
                
                # Load URL and take screenshot
                driver.get(url)
                time.sleep(2)  # Allow the page to load
                screenshot_path = os.path.join(domain_folder, f'screenshot_{index + 1}.png')
                driver.save_screenshot(screenshot_path)
                
                # Display screenshot in Streamlit
                image = Image.open(screenshot_path)
                st.image(image, caption=f'Screenshot {index + 1} - {url}', use_column_width=True)
            except Exception as e:
                st.error(f"Failed to capture screenshot for {url}: {str(e)}")

    driver.quit()

# Main function
def main():
    st.title("Screenshottr - Automated Screenshot Tool")
    st.write("Upload a list of URLs or enter them manually to take screenshots in mobile or desktop view.")

    # Text input for URLs
    urls_input = st.text_area("Enter URLs (one per line)")

    # Checkbox to select mobile or desktop view
    view_option = st.radio("Select screenshot view:", ("Desktop", "Mobile"))
    mobile_view = True if view_option == "Mobile" else False

    # Output folder selection
    output_directory = st.text_input("Enter the output folder path for screenshots", value="screenshots")

    # Button to start the screenshot process
    if st.button("Take Screenshots"):
        urls = urls_input.splitlines()

        if urls:
            if not os.path.exists(output_directory):
                os.makedirs(output_directory)

            try:
                take_screenshots(urls, output_directory, mobile_view)
            except Exception as e:
                st.error(f"An unexpected error occurred: {str(e)}")
        else:
            st.warning("Please enter at least one URL.")

# Run the app
if __name__ == "__main__":
    main()
