from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# Function to scrape phone numbers
def scrape_phone_numbers(url):
    try:
        # Make a GET request to the website
        response = requests.get(url)
        if response.status_code != 200:
            return "Failed to retrieve the website"
        
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Regex to find phone numbers (basic pattern for simplicity)
        phone_numbers = re.findall(r'\+?\(?\d{1,4}?\)?[-.\s]?\(?\d{1,4}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}', soup.get_text())

        if phone_numbers:
            return list(set(phone_numbers))  # Remove duplicates
        else:
            return "No phone numbers found"
    except Exception as e:
        return f"An error occurred while scraping: {e}"

# Route to display the form and handle form submissions
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get the URL entered by the user
        url = request.form.get("url")

        if url:
            # Scrape phone numbers from the provided URL
            phone_numbers = scrape_phone_numbers(url)
            return render_template("index.html", phone_numbers=phone_numbers, url=url)
        else:
            return render_template("index.html", error="Please provide a valid website link.")

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)