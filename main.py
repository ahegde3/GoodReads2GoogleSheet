import feedparser
import json
from dotenv import load_dotenv
import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

# Constants
RSS_URL = "https://www.goodreads.com/review/list_rss/70445162?key=qg0XmblgluNyknWOzUaB4y2ApKPhq64rhV6MNScwws7hKg3B&shelf=read"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'service-account.json'
RANGE_NAME = 'Sheet1!A1:ZZ'
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")


def fetch_rss_data():
    """Fetches and parses data from an RSS feed."""

    try:

        # Parse the RSS feed
        feed = feedparser.parse(RSS_URL)

        # Convert the feed to a JSON object
        json_data = json.dumps(feed.entries, indent=4)
        # Convert the JSON string back to a Python object
        data = json.loads(json_data)

        return data
    
    except Exception as e:
        print(f"Error fetching RSS data: {e}")
        return None

def initialize_google_sheet():
    """Initializes a Google Sheets API client and reads data from a specified sheet."""

    print("Initializing Google Sheet")

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'service-account.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    # Build the Sheets API client
    service = build('sheets', 'v4', credentials=credentials)

    return service


def insert_data_into_sheet(sheetService, data):
    """Inserts data into a Google Sheet."""

    print("Inserting data into Google Sheet")

    # Replace with your spreadsheet ID and range
    range_name = 'Sheet1!A1:ZZ'

    # Convert the data to a 2D list
    # Define headers
    headers = ["Title", "Author", "Read At", "Rating"]
    values = [headers]
    for item in data:

        if item['user_read_at'] == "":
            read_at = ""
        else :
            read_at = datetime.datetime.strptime(item['user_read_at'],"%a, %d %b %Y %H:%M:%S %z").strftime('%d/%B/%Y')    
        values.append([item["title"], item['author_name'],read_at ,item['user_rating']])

  

    # Update the Google Sheet
    request = sheetService.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=range_name,
        valueInputOption="RAW", body={"values": values}
    )
    response = request.execute()


if __name__ == "__main__":
    

   #Load environment variables from .env file
    load_dotenv()
    sheetService = initialize_google_sheet() 
    data = fetch_rss_data()

    insert_data_into_sheet(sheetService, data)
