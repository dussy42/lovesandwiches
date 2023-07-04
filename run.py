import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

sales = SHEET.worksheet('sales')

data = sales.get_all_values()

print(data)

def get_sales():
    """
    Get sales figures input from the user
    """
    data_str=input("enter your data here:")
   
    sales_data=data_str.split(",")
    validate_data(sales_data)


def validate_data(values):
    """
    converts all string values into integers. 
    Raises ValueError if strings cannot be converted
    into int, or if there aren't exactly 6values.
    """
    try:
        if len(values) !=6:
            raise ValueError(
                f'Exactly 6 value required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'invalid data:{e}, please try again. \n')
get_sales()