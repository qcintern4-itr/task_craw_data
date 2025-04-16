from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

class TokenHandler:
    def __init__(self):
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """Setup Chrome WebDriver"""
        options = webdriver.ChromeOptions()
        # Add any necessary options here
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.maximize_window()

    def login_and_get_tokens(self, username, password):
        """Login to eClinicalWorks and extract tokens"""
        try:
            # Setup driver if not already done
            if not self.driver:
                self.setup_driver()

            # Navigate to login page
            self.driver.get("https://nymegrapp.eclinicalweb.com/mobiledoc/jsp/webemr/login/newLogin.jsp")

            # Enter username
            username_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "doctorID"))
            )
            username_field.send_keys(username)

            # Click next button
            next_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='nextStep']"))
            )
            next_button.click()

            # Enter password
            password_field = self.wait.until(
                EC.presence_of_element_located((By.NAME, "passwordField"))
            )
            password_field.send_keys(password)

            # Click login button
            login_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='Login']"))
            )
            login_button.click()

            # Wait for disclaimer modal and click agree
            time.sleep(5)  # Wait for page to load
            agree_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//*[@id='agreeBtn']"))
            )
            agree_button.click()

            # Wait for page to load completely
            time.sleep(5)

            # Get X-CSRF-Token from meta tag
            csrf_token = self.driver.execute_script(
                'return document.querySelector("meta[name=\'csrf-token\']").getAttribute("content")'
            )

            # Get cookies
            cookies = self.driver.get_cookies()
            jsessionid = next((cookie['value'] for cookie in cookies if cookie['name'] == 'JSESSIONID'), None)
            affinity = next((cookie['value'] for cookie in cookies if cookie['name'] == 'ApplicationGatewayAffinity'), None)
            affinity_cors = next((cookie['value'] for cookie in cookies if cookie['name'] == 'ApplicationGatewayAffinityCORS'), None)

            # Format cookie string
            cookie_string = f"JSESSIONID={jsessionid}; ApplicationGatewayAffinityCORS={affinity_cors}; ApplicationGatewayAffinity={affinity}"

            # Get localStorage items if needed
            localStorage_items = self.driver.execute_script("""
                let items = {};
                for (let i = 0; i < localStorage.length; i++) {
                    let key = localStorage.key(i);
                    items[key] = localStorage.getItem(key);
                }
                return items;
            """)

            return {
                'csrf_token': csrf_token,
                'cookie_string': cookie_string,
                'local_storage': localStorage_items
            }

        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return None

    def update_config_file(self, tokens):
        """Update config.py with new token values"""
        try:
            with open('config.py', 'r') as file:
                config_content = file.read()

            # Update X-CSRF-Token in API_HEADERS_TABLE2
            config_content = config_content.replace(
                '"X-CSRF-Token": "771f0f6e-4b11-4137-b6f0-864702b11896"',
                f'"X-CSRF-Token": "{tokens["csrf_token"]}"'
            )

            # Update X-CSRF-Token in API_HEADERS_TABLE3
            config_content = config_content.replace(
                '"X-CSRF-Token": "519f25c9-a927-4eb1-8afe-013622b83047"',
                f'"X-CSRF-Token": "{tokens["csrf_token"]}"'
            )

            # Update Cookie in API_HEADERS_TABLE2
            config_content = config_content.replace(
                '"Cookie": "JSESSIONID=F2D544C4AD6E11D2BAFC9CDC157FC033; ApplicationGatewayAffinityCORS=124274af792cba06a0461a764f502f20; ApplicationGatewayAffinity=124274af792cba06a0461a764f502f20"',
                f'"Cookie": "{tokens["cookie_string"]}"'
            )

            # Update Cookie in API_HEADERS_TABLE3
            config_content = config_content.replace(
                '"Cookie": "JSESSIONID=310BE3CAFD63DA959F997972A7F3DB8D; ApplicationGatewayAffinityCORS=55188ab720fd86c8c53f4d3764729277; ApplicationGatewayAffinity=55188ab720fd86c8c53f4d3764729277"',
                f'"Cookie": "{tokens["cookie_string"]}"'
            )

            with open('config.py', 'w') as file:
                file.write(config_content)

            print("Config file updated successfully")

        except Exception as e:
            print(f"Error updating config file: {str(e)}")

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()

def main():
    token_handler = TokenHandler()
    try:
        tokens = token_handler.login_and_get_tokens(
            username="optimususer",
            password="9v7ouEVBAN1h^zHg3K"
        )
        
        if tokens:
            print("Tokens retrieved successfully:")
            print(f"CSRF Token: {tokens['csrf_token']}")
            print(f"Cookie String: {tokens['cookie_string']}")
            print("\nLocal Storage Items:")
            for key, value in tokens['local_storage'].items():
                print(f"{key}: {value}")
            
            # Update config file
            # token_handler.update_config_file(tokens)
        else:
            print("Failed to retrieve tokens")

    finally:
        token_handler.close()

if __name__ == "__main__":
    main() 