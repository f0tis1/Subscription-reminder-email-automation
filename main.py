from datetime import date  # core python module
import pandas as pd  # pip install pandas
from send_email import send_email 
from datetime import datetime, timedelta

# Excel file uploaded at the paragon.ads.company@gmail.com google sheets
# Public GoogleSheets url - not secure!
SHEET_ID = ""  # CHANGE
SHEET_NAME = ""  # CHANGE
URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"


def load_df(url):
    parse_dates = ["Expiration_Date"]
    df = pd.read_csv(url, parse_dates=parse_dates)
    # df = pd.read_csv(url)
    return df

# print(load_df(URL))

def query_data_and_send_emails(df):
    present = date.today()
    email_counter = 0
    for _, row in df.iterrows():
        expiration_date = row['Expiration_Date'].date() # Get the expiration date
        today_date = datetime.now().date() # Get the todays date
        month_reminder = expiration_date - timedelta(days=30) #Set a reminder for a month before (30 days)
        week_reminder = expiration_date - timedelta(days=7) #Set a reminder for a week before (7 days)
        if row["Service_Type"] == "Domain":
            service_cost = f"Κόστος ανανέωσης για 2 έτη: {row['Service_Cost']}"
        else:
            service_cost = f"Κόστος ανανέωσης για 1 έτος: {row['Service_Cost']}"

        #Check for week
        if ( today_date==week_reminder ) and ((row["is_active"] == "yes") or(row["is_active"] == "Yes")):
            send_email(
                subject=f'Υπενθύμιση ανανέωσης πακέτου φιλοξενίας ({row["Service_Type"]}) για {row["Subscription"]}',
                sub_email=row["Sub_Email"],
                subscriber=row["Subscriber"],
                expiration_date=row["Expiration_Date"].strftime("%d/%m/%Y"),  # example: 28/04/2024
                service_type=row["Service_Type"],
                service_plan=row["Service_Plan"],
                service_cost=service_cost,
                subscription=row["Subscription"],
            )
            email_counter += 1
        #Check for month    
        if ( today_date==month_reminder ) and ((row["is_active"] == "yes") or(row["is_active"] == "Yes")):
            send_email(
                subject=f'Υπενθύμιση ανανέωσης πακέτου φιλοξενίας ({row["Service_Type"]}) για {row["Subscription"]}',
                sub_email=row["Sub_Email"],
                subscriber=row["Subscriber"],
                expiration_date=row["Expiration_Date"].strftime("%d/%m/%Y"),  # example: 28/04/2024
                service_type=row["Service_Type"],
                service_plan=row["Service_Plan"],
                service_cost=service_cost,
                subscription=row["Subscription"],
            )
            email_counter += 1
            
    return f"Total Emails Sent: {email_counter}"


# Run Code
df = load_df(URL)
result = query_data_and_send_emails(df)
print(result)
