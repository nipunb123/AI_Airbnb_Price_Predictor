import joblib
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

def listing_Scrapper(url):
    

    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    prettified_html = soup.prettify()


    desired_amenities = [
        "Essentials",
        "Air conditioning",
        "Cleaning products",
        "Cooking basics",
        "Dryer",
        "Heating",
        "Hot tub",
        "Kitchen",
        "Pool",
        "Washer",
        "Wifi",
        "Bathtub",
        "TV",
        "Dishwasher",
        "Stove",
        "Beach access",
        "Lake access",
        "Waterfront",
        "BBQ grill",
        "Fire pit",
        "Free parking on premise",
        "Sauna",
        "Breakfast",
        "Bay view",
        "Beach view",
        "Canal view",
        "City skyline view",
        "Courtyard view",
        "Desert view",
        "Garden view",
        "Golf course view",
        "Harbor view",
        "Lake view",
        "Marina view",
        "Mountain view",
        "Ocean view",
        "Park view",
        "Pool view",
        "Resort view",
        "River view",
        "Sea view",
        "Valley view",
        "Vineyard view",
        "Fireplace"
    ]
    worksheet_data = ""






    #########################################################
    #bs4 Setup
    




    info_line = None
    for line in prettified_html.splitlines():
        if '"IS_DEV":false,"HYPERLOOP_ENV"' in line:
            info_line = line
            break

    if not info_line:
        print("Line not found?")






    ###########################################################################
    amenitiesPattern = r'__typename":"Amenity"(.*?)"title":"(.*?)"'
    amenity_matches = re.findall(amenitiesPattern, info_line)
    finalAmenities = []

    for match in amenity_matches:
        _, title = match
        last_phrase = title.split('"title":"')[-1].strip('",')
        finalAmenities.append(last_phrase)

    finalAmenities = list(dict.fromkeys(finalAmenities))

    #print(str(len(finalAmenities)) + " amenities found and added")
    ############################################################################





    ############################################################################
    try:
        starRatingPattern = r'"starRating":(\d+(?:\.\d+)?)'
        starRating_matches = re.findall(starRatingPattern, info_line)

        Rating = starRating_matches[0]
    except:
        Rating = 0
    #print("Overall Rating: " + str(Rating))
    worksheet_data += f"{Rating},"

    ############################################################################




    ############################################################################
    try:
        pattern = r'"title":"Entire (.*?)"'
        matches = re.findall(pattern, info_line)

        houseType = matches[0]

        if "hosted" in houseType:
            first_word = houseType.split("hosted")[0]
        else:
            first_word = houseType

    except:
        first_word="Room"
    #print("House Type: " + str(first_word))
    worksheet_data += f"{first_word},"

    ############################################################################




    ##########################################################################
    try:
        reviewCountPattern = r'"reviewCount":(\d+)'
        reviewCount_matches = re.findall(reviewCountPattern, info_line)

        reviewCount = reviewCount_matches[0]
    except:
        reviewCount = 0
    #print("Number of Reviews: " + str(reviewCount))
    worksheet_data += f"{reviewCount},"

    ############################################################################




    ############################################################################

    bed_pattern = r'"__typename":"BasicListItem","title":"([\d.]+) beds"'
    bed_matches = re.findall(bed_pattern, info_line)

    try:
        numBeds = bed_matches[0]
        #print("Number of beds: " + str(numBeds))
    except:
        numBeds = 1
    worksheet_data += f"{numBeds},"

        
    ############################################################################




    ############################################################################

    try:
        bath_pattern = r'"__typename":"BasicListItem","title":"([\d.]+) (private |shared )?bath(s?)"'
                        #"__typename":"BasicListItem","title":"1 bath"
        bath_matches = re.findall(bath_pattern, info_line)


        numBaths = bath_matches[0][0]
        #print(numBaths)

    except:
        numBaths=0

    worksheet_data += f"{numBaths},"

    ############################################################################





    ############################################################################

    bedroom_pattern = r'"__typename":"BasicListItem","title":"([\d.]+) bedrooms"'
    bedroom_matches = re.findall(bedroom_pattern, info_line)
    try:
        numbedrooms = bedroom_matches[0]
        #print("Number of bedroom: " + str(numbedrooms))
    except:
        #print("ROOM ERROR")
        numbedrooms=1
    worksheet_data += f"{numbedrooms},"

    ############################################################################


    ###########################################################################

    guest_pattern = r'"__typename":"BasicListItem","title":".*?(\d+|\d+\+?) guests( maximum)?"'
    guest_matches = re.findall(guest_pattern, info_line)

    numguests = guest_matches[0][0]
    #print("Number of guests: " + str(numguests))
    worksheet_data += f"{numguests},"

    ############################################################################





    ########################################################################
    if '{"__typename":"BasicListItem","title":"Superhost"' in info_line:
        Superhost = True
    else:
        Superhost=False

    #print("Superhost: " + str(Superhost))
    worksheet_data += f"{Superhost},"

    #########################################################################




    #########################################################################

    if '[{"__typename":"BasicListItem","accessibilityLabel":null,"title":"New"' in info_line:
        NewListing = True
    else:
        NewListing = False

    #print("New Listing: " + str(NewListing))
    worksheet_data += f"{NewListing},"

    #########################################################################


    #########################################################################
    location_pattern = r'"lat":(-?\d+\.\d+),"lng":(-?\d+\.\d+)'
    match = re.search(location_pattern, info_line)

    if match:
        latitude = match.group(1)
        longitude = match.group(2)
        #print("Latitude:", latitude)
        #print("Longitude:", longitude)
    else:
        print("Pattern not found.")

    worksheet_data += f"{latitude},"

    worksheet_data += f"{longitude},"
    #########################################################################

    #########################################################################
    categories = ["Cleanliness", "Accuracy", "Communication", "Location", "Check_in", "Value"]
    Cleanliness = 0
    Accuracy = 0
    Communication = 0
    Location = 0
    Check_in = 0
    Value = 0


    starRatingPattern = r'"localizedRating":"(\d+(?:\.\d+)*)"'
    starRating_matches = re.findall(starRatingPattern, info_line)


    #for i in starRating_matches:
        #print(i)
    #########################################################################



    #########################################################################
    rating_dict = {}

    for category, rating in zip(categories, starRating_matches):
        rating_dict[category] = rating

    try:
        #print("Cleanliness:", rating_dict["Cleanliness"])
        #print("Accuracy:", rating_dict["Accuracy"])
        #print("Communication:", rating_dict["Communication"])
        #print("Location:", rating_dict["Location"])
        #print("Check_in:", rating_dict["Check_in"])
        #print("Value:", rating_dict["Value"])
        worksheet_data += f'{rating_dict["Cleanliness"]},'
        worksheet_data += f'{rating_dict["Accuracy"]},'
        worksheet_data += f'{rating_dict["Communication"]},'
        worksheet_data += f'{rating_dict["Location"]},'
        worksheet_data += f'{rating_dict["Check_in"]},'
        worksheet_data += f'{rating_dict["Value"]},'
    except:
        #print(Cleanliness,Accuracy,Communication,Location,Check_in,Value)
        worksheet_data += f'{0},'
        worksheet_data += f'{0},'
        worksheet_data += f'{0},'
        worksheet_data += f'{0},'
        worksheet_data += f'{0},'
        worksheet_data += f'{0},'
    #########################################################################



    #########################################################################
    amenity_dict = {desired_amenity: False for desired_amenity in desired_amenities}

    for desired_amenity in desired_amenities:
        for amenity in finalAmenities:
            if desired_amenity.lower() in amenity.lower():
                amenity_dict[desired_amenity] = True
                break  # Break the loop if a match is found

    # Print the dictionary
    #for desired_amenity, has_amenity in amenity_dict.items():
        #print(f"{desired_amenity}: {has_amenity}")

    for desired_amenity, has_amenity in amenity_dict.items():
        worksheet_data += f"{has_amenity},"
    #########################################################################

    

    return worksheet_data

url = "ENTER THE URL YOU WANT TO PREDICT THE PRICE FOR HERE"



outputString = listing_Scrapper(url)



# Load the trained model
loaded_model = joblib.load('airbnbModel.joblib')

# Get the list of features used by the model
model_features = loaded_model.get_booster().feature_names

value_list = outputString.split(',')
houseType = value_list.pop(1)
print(houseType)

feature_names = ['Overall Rating', 'Number of Reviews', 'Number of beds', 'Number of Bath', 'Number of bedroom', 'Number of guests', 'Superhost', 'New Listing', 'Latitude', 'Longitude', 'Cleanliness', 'Accuracy', 'Communication', 'Location', 'Check_in', 'Value', 'Essentials', 'Air conditioning', 'Cleaning products', 'Cooking basics', 'Dryer', 'Heating', 'Hot tub', 'Kitchen', 'Pool', 'Washer', 'Wifi', 'Bathtub', 'TV', 'Dishwasher', 'Stove', 'Beach access', 'Lake access', 'Waterfront', 'BBQ grill', 'Fire pit', 'Free parking on premise', 'Sauna', 'Breakfast', 'Bay view', 'Beach view', 'Canal view', 'City skyline view', 'Courtyard view', 'Desert view', 'Garden view', 'Golf course view', 'Harbor view', 'Lake view', 'Marina view', 'Mountain view', 'Ocean view', 'Park view', 'Pool view', 'Resort view', 'River view', 'Sea view', 'Valley view', 'Vineyard view', 'Fireplace', 'House Type_Room', 'House Type_bungalow', 'House Type_cabin', 'House Type_chalet', 'House Type_condo', 'House Type_cottage', 'House Type_guest suite', 'House Type_guesthouse', 'House Type_home', 'House Type_loft', 'House Type_place', 'House Type_rental unit', 'House Type_serviced apartment', 'House Type_townhouse', 'House Type_vacation home', 'House Type_villa']

new_data_dict = {}

# Your existing code...

# Iterate through the feature names and corresponding values
for feature in feature_names:
    if value_list:
        value = value_list.pop(0)
    else:
        value = 0  # Default value is 0
        
    # Check if the feature value is a number (can be converted to float)
    try:
        value = float(value)
    except ValueError:
        # If the value is not a number, treat it as a string and cast it to boolean
        value = value.lower() == 'true'
        
    new_data_dict[feature] = [value]


for feature in feature_names:
    # Use regex to check if the feature starts with "House Type_" followed by "house"
    if re.match(rf'^House Type_{(houseType)}', feature):
        new_data_dict[feature] = [1]



# Convert the dictionary to a DataFrame
new_data = pd.DataFrame(new_data_dict)

# Ensure the order of columns in new_data matches the order during training

# Make predictions using the loaded model
predictions = loaded_model.predict(new_data)

print("The estimated price of your Airbnb is: $" + str(predictions[0]))
