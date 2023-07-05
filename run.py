
import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    while True:
        print("pls enter sales data from the last market")
        print("Data should be six numbers, separated by commas")
        print("Example: 10,20,30,40,50")
        data_str = input("enter your data here:")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data


def validate_data(values):
    """
    converts all string values into integers. 
    Raises ValueError if strings cannot be converted
    into int, or if there aren't exactly 6values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f'Exactly 6 value required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'invalid data:{e}, please try again. \n')
        return False
    
    return True


def update_sales_worksheet(data):
    """
    update sales worksheet, add new row with the list data provided
    """
    print("updating sales worksheet.......")
    sales_worksheet=SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("sales worksheet updated successfully")

def update_surplus_worksheet(data):
    """
    update sales worksheet, add new row with the list data provided
    """
    print("updating surplus worksheet.......")
    surplus_worksheet=SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("surplus worksheet updated successfully")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("calculating surplus data.....")
    stock=SHEET.worksheet("stock").get_all_values()
    pprint(stock)
    stock_row=stock[-1]
    pprint(stock_row)
    print(f'stock row:{stock_row}')
    print(f'sales row:{sales_row}')

    surplus_data=[]
    for stock,sales in zip(stock_row,sales_row):
        surplus=int(stock)-sales
        surplus_data.append(surplus)
    
    return surplus_data
      

def main():
    """
    run all program functions
    """
    data=get_sales()
    sales_data=[int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data= calculate_surplus_data(sales_data)
    print(new_surplus_data)
    update_sales_worksheet(new_surplus_data)

print("welcome to love sandwiches data automation")
main()
