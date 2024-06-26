import feedparser
import json
from dotenv import load_dotenv
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

def fetchRssData():
    # URL of the RSS feed
    rss_url = "https://www.goodreads.com/review/list_rss/70445162?key=qg0XmblgluNyknWOzUaB4y2ApKPhq64rhV6MNScwws7hKg3B&shelf=read"

    # Parse the RSS feed
    feed = feedparser.parse(rss_url)
    print(feed.entries[0])

    # Convert the feed to a JSON object
    json_data = json.dumps(feed.entries, indent=4)
    # Convert the JSON string back to a Python object
    data = json.loads(json_data)

    # Print the JSON output
    print(len(data))

def inititalizeGoogleSheet():
    print("Initializing Google Sheet")

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    SERVICE_ACCOUNT_FILE = 'service-account.json'

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )

    # Build the Sheets API client
    service = build('sheets', 'v4', credentials=credentials)

    # Replace with your spreadsheet ID and range
    spreadsheet_id = os.environ.get("SPREADSHEET_ID")
    print(spreadsheet_id)
    
    range_name = 'Sheet1!A1:ZZ'

    # Read data from the sheet
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id, range=range_name
    ).execute()

    print(result)

if __name__ == "__main__":
    

   #Load environment variables from .env file
    load_dotenv()

    # fetchRssData()
    inititalizeGoogleSheet() 