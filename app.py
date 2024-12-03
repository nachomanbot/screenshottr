# app.py
import streamlit as st
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
import time
import os
from PIL import Image

# Function to take screenshots using Selenium
def take_screenshots(urls, output_dir, mobile_view):
    firefox_options = Options()
    firefox_options.add_argument('--headless')  # Run in headless mode
    if mobile_view:
        firefox_options.set_preference("general.useragent.override", "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1")
    else:
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
    
    try:
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=firefox_options)
    except Exception as e:
        st.error(f"Failed to initialize the Firefox driver: {str(e)}. Please ensure Firefox and GeckoDriver are properly installed and compatible.")
        return

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
    st.write("Enter a list of URLs to take screenshots in either mobile or desktop view.")

    # Text input for URLs
    urls_input = st.text_area("Enter URLs (one per line)")

    # Checkbox to select mobile or desktop view
    view_options = st.multiselect("Select screenshot views:", ["Desktop", "Mobile"])
    take_desktop = "Desktop" in view_options
    take_mobile = "Mobile" in view_options

    # Text input to select output folder
    st.write("Enter the path to the folder where you want to save the screenshots. You can copy the path from your file explorer.")
    output_directory = st.text_input("Output folder path:", value=os.path.join(os.getcwd(), 'screenshots'))

    # Button to start the screenshot process
    if st.button("Take Screenshots"):
        urls = urls_input.splitlines()

        if urls:
            if not os.path.exists(output_directory):
                try:
                    os.makedirs(output_directory)
                except Exception as e:
                    st.error(f"Failed to create output directory: {str(e)}")
                    return

            try:
                if take_desktop:
                    take_screenshots(urls, output_directory, mobile_view=False)
                if take_mobile:
                    take_screenshots(urls, output_directory, mobile_view=True)
            except Exception as e:
                st.error(f"An unexpected error occurred during the screenshot process: {str(e)}")
        else:
            st.warning("Please enter at least one URL.")

# Run the app
if __name__ == "__main__":
    main()
