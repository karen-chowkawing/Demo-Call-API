# a script to call weather API and process data
import pandas as pd
import json
import os
from datetime import datetime
from selenium import webdriver
coordinate_file_path = 'YOUR_PATH/*.xlsx'
json_path = 'YOUR_PATH/*.json'

def get_file_name():

    coordinates = pd.read_excel(coordinate_file_path, index_col=0, sheet_name='YOUR_SHEET_NAME')
    print(coordinates.head())

    # Generate file names based on coordinates

    name1_list =[]
    name2_list = []
    name3_list = []
    name4_list = []

    # Loop through each row in the coordinates DataFrame

    for i in range(len(coordinates)):
        str_WTG = str(coordinates['WTG  No '][i])
        str_Lati = str(coordinates['Latitude'][i])
        str_Longi = str(coordinates['Longitude'][i])
        name1 = "wind_"+str_WTG+"_"+str_Lati+"_"+str_Longi+"_day.csv"
        print(name1)
        name1_list.append(name1)
        name2 = "wind_"+str_WTG+"_"+str_Lati+"_"+str_Longi+"_night.csv"
        print(name2)
        name2_list.append(name2)
        name3 = "solar_"+str_WTG+"_"+str_Lati+"_"+str_Longi+"_day.csv"
        print(name3)
        name3_list.append(name3)
        name4 = "solar_"+str_WTG+"_"+str_Lati+"_"+str_Longi+"_night.csv"
        print(name4)
        name4_list.append(name4)

    # Return lists of generated file names

    return [name1_list, name2_list, name3_list, name4_list]


# Get today's date for daily file naming
def get_daily_file_name(today):

    today = datetime.today()
    today.strftime('%Y-%m-%d')
    print(today,type(today))

    return today


# Format the original JSON data into a DataFrame and prepare URLs
def formatting():

    # Load original JSON data
    with open(json_path) as f:
        ori_file = json.load(f)

    # Convert JSON data to DataFrame
    ori_file_df = pd.DataFrame.from_dict(ori_file)
    format0 = ori_file_df["forecasts1Hour"]
    format0['validTimeUtc'] = format0['validTimeUtc'].apply(lambda x : datetime.fromtimestamp(x))

    print(format0.head())

    # Prepare API URLs for wind and solar data
    format0['urlWind']="YOUR_LINK_TO_API"+"hourly/energywind/15day?geocode="+format0['Latitude'].map(str)+","+format0['Longitude'].map(str)+"&format=json&units=e&height=60.5&apiKey=API_KEY"

    format0['urlSolar']="YOUR_LINK_TO_API"+"15minute/energysolar/7day?geocode="+format0['Longitude'].map(str)+","+format0['Longitude'].map(str)+"&format=json&units=e&height=60.5&apiKey=API_KEY"

    # Get file names for saving data
    url_name = get_file_name()
    print(url_name.head())
    format0['urlNameWindDay']=url_name[0]
    format0['urlNameWindNight']=url_name[1]
    format0['urlNameSolarDay']=url_name[2]
    format0['urlNameSolarNight']=url_name[3]

    return format0

# Write data to a file
def write_file(data,name):

    data=data
    with open(os.path.join(path, name), 'w') as fp:
        fp.write(data)

    return

# Call the API and process the data
def call_api():


    format_file = formatting()
    # print(format_file)
    url1_list = format_file['urlWind'].values.tolist()
    url2_list = format_file['urlSolar'].values.tolist()

    driver = webdriver.Firefox()

    for urlWind in url1_list:
        # print("url",url)
        Winddata = driver.get(urlWind)
        json.loads(Winddata)
        write_file(Winddata,format_file['urlNameWindDay'])
        # print(Winddata)

    for urlSolar in url2_list:
        # print("url",url)
        SolarData = driver.get(urlSolar)
        json.loads(SolarData)
        write_file(SolarData,format_file['urlNameSolarDay'])
        # print(SolarData)

    driver.close()




def main():
    get_file_name()
    get_daily_file_name(today)
    formatting()
    write_file(data,name)
    call_api()

main()
