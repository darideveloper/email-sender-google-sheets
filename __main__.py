import os
from datetime import datetime
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
images_folder = os.path.join (current_folder, "imgs")

def main (): 
    
    # Connect to email
    email_manager = EmailManager (EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    
    # Get emails from google sheets
    sheets_manager = SheetsManager (GOOGLE_SHEETS, creds_path)
    sheets_manager.set_sheet ("contact form")
    data = sheets_manager.get_data ()
    
    today = datetime.now ().strftime ("%d/%m/%Y")
    
    for row in data:
        
        email = row["email"]
        print (f"Sending email to {email}")
    
        # Submit email
        email_manager.send_email (
            receivers=[email],
            subject=EMAIL_SUBJECT,
            html_path=html_path,
            html_data={
                "email": email,
            },
            imgs_paths = {
                "image1": os.path.join (images_folder, "banner-small.png"),
            }
        )
        
        # Update last update and is new in google sheets
        current_row = data.index (row) + 2
        sheets_manager.write_cell (today, current_row, 2)
        sheets_manager.write_cell ("FALSE", current_row, 3)
        
    pass


if __name__ == "__main__":
    main()