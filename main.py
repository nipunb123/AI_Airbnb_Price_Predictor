import time
import os
from bs4 import BeautifulSoup
import requests
import re
import openpyxl
import threading
import openpyxl
import concurrent.futures

start_time = time.time()

lock = threading.Lock()

def listing_Scrapper(url, money):
    

    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    prettified_html = soup.prettify()

    with lock:
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
        
        worksheet_data += f"{money},"

        return worksheet_data




money_folder = r'YOUR DIRECTORY\money'
href_folder = r'YOUR DIRECTORY\hrefs'


money_list = []
href_list = []
result_list = []


for filename in os.listdir(money_folder):
    file_path = os.path.join(money_folder, filename)
    with open(file_path, 'r') as file:
        money_list.extend([int(line.split('$')[1].replace(',', '').split()[0]) for line in file if line.startswith('$')])

# Read data from href files
for filename in os.listdir(href_folder):
    file_path = os.path.join(href_folder, filename)
    with open(file_path, 'r') as file:
        href_list.extend([line.strip() for line in file])




# Existing code to read money_list and href_list from files

# Function to process listing_Scrapper and update the Excel sheet
def process_listing(index, row, money):
    print("Processing index:", index)
    result = listing_Scrapper(href_list[index], row, money)  # Call listing_Scrapper
    result_elements = result.split(',')  # Split the result by commas
    result_list.append(result_elements)   # Add the split result to the list
    for col, item in enumerate(result_elements, start=1):
        ws.cell(row=row, column=col, value=item)


# Main program
datafile = r"YOUR DIRECTORY\data.xlsx"
wb = openpyxl.load_workbook(datafile)
ws = wb.active

row = 2
index = 0

# Use ThreadPoolExecutor to process listing_Scrapper calls in parallel
with concurrent.futures.ThreadPoolExecutor() as executor:
    
    futures = []
    for money in money_list:
        futures.append(executor.submit(process_listing, index, row, money))
        row += 1
        index += 1

    # Wait for all tasks to complete
    concurrent.futures.wait(futures)

# Save the Excel file after all tasks
wb.save(r"data.xlsx")

print("Process finished --- %s seconds ---" % (time.time() - start_time))
