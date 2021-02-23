import logging 
import betfairlightweight

logging.basicConfig(level=logging.INFO)

certs_path = '/mnt/c/Users/dougl/Desktop/betfairkeys'

# Change these login details to your own
my_username = "DWIH11235813"
my_password = "Ab724pQ!c"
my_app_key = "ewTbZ9NTCKyxtJtK"

trading = betfairlightweight.APIClient(username=my_username, password=my_password, app_key=my_app_key, certs=certs_path)

# login
trading.login()

my_data = trading.historic.get_my_data()
for i in my_data:
    print(i)

collection_options = trading.historic.get_collection_options(
    "Horse Racing", "Basic Plan", 1, 3, 2017, 1, 3, 2017
)

print(collection_options)

basket_size = trading.historic.get_data_size(
    "Horse Racing", "Basic Plan", 1, 3, 2017, 1, 3, 2017
)
print(basket_size)
'''
file_list = trading.historic.get_file_list(
    "Horse Racing",
    "Basic Plan",
    from_day=1,
    from_month=1,
    from_year=2020,
    to_day = 31,
    to_month=1,
    to_year=2020,
    market_types_collection = ["WIN","PLACE"],
    countries_collection = ["GB","IE"],
    file_type_collection=["M"],
)
print(file_list)



for file in file_list:
    print(file)
    download = trading.historic.download_file(file_path = file)
    print(download)
    '''