import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

json_file_path = 'ikea_price_changes.json'

# Ensure the JSON file exists
if not os.path.exists(json_file_path):
    try:
        with open(json_file_path, 'w') as file:
            json.dump([], file, indent=4)
    except IOError as e:
        print(f"Error creating JSON file: {e}")
        raise


def check_price(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the price on the IKEA product page using the updated selector
        price_element = soup.select_one('.pip-price-package .pip-temp-price-module__current-price .pip-temp-price__integer')
        if price_element:
            price = price_element.get_text().strip()
            price = float(price.replace(',', ''))  # Convert price to a float

            last_price = get_last_recorded_price()

            record_price(price, last_price)

            if last_price is not None and price < last_price:
                send_mail(url, price)
        else:
            print("Could not find the price on the page.")
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def send_mail(url, price):
    # Email details
    from_address = os.getenv('FROM_ADDRESS')
    from_password = os.getenv('FROM_PASSWORD')
    to_address = os.getenv('TO_ADDRESS')
    subject = "IKEA Price Alert!"
    body = f'The price of your IKEA product has dropped to {price} EGP. Check it out here: {url}'

    # SMTP server configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_user = from_address
    smtp_password = from_password
    
    # Create the email
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)
        text = msg.as_string()
        server.sendmail(from_address, to_address, text)
        server.quit()
        print(f"Email sent to {to_address}")
    except Exception as e:
        print(f"Failed to send email: {e}")
        
def get_last_recorded_price():
    try:
        with open(json_file_path, 'r') as file:
            price_data = json.load(file)
        if price_data:
            return price_data[-1]['price']
        return None
    except IOError as e:
        print(f"Error reading JSON file: {e}")
        return None
  
def record_price(current_price, last_price):
    data = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "price": current_price
    }

    try:
        with open(json_file_path, 'r') as file:
            price_data = json.load(file)

        # Update the last recorded price's date if the price is the same
        if price_data and current_price != last_price:
            price_data.append(data)
            with open(json_file_path, 'w') as file:
                json.dump(price_data, file, indent=4)
            #price_data[-1]['time'] = data['time']
        #else:
            #price_data.append(data)

        
            
    except IOError as e:
        print(f"Error updating JSON file: {e}")

if __name__ == '__main__':
    url = 'https://www.ikea.com/eg/ar/p/jaervfjaellet-office-chair-with-armrests-glose-black-80510639'
    check_price(url)
