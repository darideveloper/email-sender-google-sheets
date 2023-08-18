import os
from dotenv import load_dotenv
from email_manager.sender import EmailManager
from spreadsheets.google_sheets import SheetsManager

load_dotenv ()
EMAIL_HOST_USER = os.getenv ("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv ("EMAIL_HOST_PASSWORD")
EMAIL_SUBJECT = os.getenv ("EMAIL_SUBJECT")
GOOGLE_SHEETS = os.getenv ("GOOGLE_SHEETS")

current_folder = os.path.dirname (__file__)
creds_path = os.path.join (current_folder, "credentials.json")
html_path = os.path.join (current_folder, "template.html")

def main (): 
    
    # Connect to email
    email_manager = EmailManager (EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    
    # Get emails from google sheets
    sheets_manager = SheetsManager (GOOGLE_SHEETS, creds_path)
    sheets_manager.set_sheet ("contact form")
    data = sheets_manager.get_data ()
    
    for row in data:
    
        # Submit email
        email_manager.send_email (
            receivers=[row["email"]],
            subject=EMAIL_SUBJECT,
            html_path=html_path
        )
        
        # Update date in google sheets
        print ()
        
        # Update status in google sheets
        
    pass


if __name__ == "__main__":
    main()