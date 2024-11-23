# from flask import Flask, render_template, request
# import requests
# from bs4 import BeautifulSoup
# import re

# app = Flask(__name__)

# # Function to scrape phone numbers
# def scrape_phone_numbers(url):
#     try:
#         # Make a GET request to the website
#         response = requests.get(url)
#         if response.status_code != 200:
#             return "Failed to retrieve the website"
        
#         # Parse the HTML content of the page
#         soup = BeautifulSoup(response.content, 'html.parser')

#         # Regex to find phone numbers (basic pattern for simplicity)
#         phone_numbers = re.findall(r'\+?\(?\d{1,4}?\)?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}', soup.get_text())

#         if phone_numbers:
#             return list(set(phone_numbers))  # Remove duplicates
#         else:
#             return "No phone numbers found"
#     except Exception as e:
#         return f"An error occurred while scraping: {e}"

# # Route to display the form and handle form submissions
# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         # Get the URL entered by the user
#         url = request.form.get("url")

#         if url:
#             # Scrape phone numbers from the provided URL
#             phone_numbers = scrape_phone_numbers(url)
#             return render_template("index.html", phone_numbers=phone_numbers, url=url)
#         else:
#             return render_template("index.html", error="Please provide a valid website link.")

#     return render_template("index.html")

# if __name__ == "__main__":
#     app.run(debug=True)






from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import vonage

app = Flask(__name__)

# Configure Vonage API
VONAGE_API_KEY = "your_vonage_api_key"
VONAGE_API_SECRET = "your_vonage_api_secret"
VONAGE_BRAND_NAME = "ScraperApp"

client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
voice = vonage.Voice(client)

# Function to scrape phone numbers
def scrape_phone_numbers(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return "Failed to retrieve the website"
        
        soup = BeautifulSoup(response.content, 'html.parser')
        phone_numbers = re.findall(r'\+?\(?\d{1,4}?\)?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}', soup.get_text())
        return list(set(phone_numbers)) if phone_numbers else "No phone numbers found"
    except Exception as e:
        return f"An error occurred while scraping: {e}"

# Route to handle scraping
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if url:
            phone_numbers = scrape_phone_numbers(url)
            return render_template("index.html", phone_numbers=phone_numbers, url=url)
        else:
            return render_template("index.html", error="Please provide a valid website link.")
    return render_template("index.html")

# Route to handle automated calls
@app.route("/automate_call", methods=["POST"])
def automate_call():
    phone_numbers = request.json.get("phone_numbers", [])
    if not phone_numbers:
        return jsonify({"error": "No phone numbers provided"}), 400

    results = []
    for number in phone_numbers:
        try:
            response = voice.create_call({
                "to": [{"type": "phone", "number": number}],
                "from": {"type": "phone", "number": VONAGE_BRAND_NAME},
                "ncco": [{"action": "talk", "text": "This is a test call from the ScraperApp."}]
            })
            results.append({"number": number, "status": "Success"})
        except Exception as e:
            results.append({"number": number, "status": f"Failed: {str(e)}"})

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
