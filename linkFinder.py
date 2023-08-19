
import time
start_time = time.time()
import requests
import base64
from bs4 import BeautifulSoup
import threading
import urllib.parse




def scrape_page(url, index, base64String):
    response = requests.get(url+base64String)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    bob = soup.findAll(class_="l1ovpqvx bn2bl2p dir dir-ltr", href=True)
    money = soup.findAll(class_="_tt122m")

    with lock:
        for i in money:
            moneyList.append(i.get_text())

        if not bob:
            return


        
        for indexx, i in enumerate(bob):
            hrefList.append("https://www.airbnb.com/" + str(i['href']))
            print(f"Thread {index} - {indexx}")
            print("https://www.airbnb.com/" + str(i['href']))
            print("\n")
def get_room_number(url):
    return url.split("/")[-1].split("?")[0]



with open('locations.txt', 'r') as file:
    for line in file:
        # Process each line here
        Location = line.strip()
        encoded_string = urllib.parse.quote(Location)

        #Change the Check-in date and the Check-out date in the code below for different dates. You can also change the number of adults.
        #Also change the start_date= to the first of whatever month the check-in and check-out dates are.
        #The locations are automatically changed/updated
        firsturl = "https://www.airbnb.com/s//homes?tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&flexible_trip_lengths%5B%5D=one_week&monthly_start_date=2023-09-01&monthly_length=3&price_filter_input_type=0&price_filter_num_nights=1&channel=EXPLORE&source=structured_search_input_header&search_type=search_query&query=" + encoded_string + "&date_picker_type=calendar&checkin=2023-09-20&checkout=2023-09-21&adults=1&cursor="
        hrefList = []
        moneyList = []
        lock = threading.Lock()

        # Set the number of threads you want to use
        num_threads = 30

        # Create and start threads
        threads = []
        for i in range(num_threads):
            multipliedNumber = (i*18)
            sample_string = '{"section_offset":3,"items_offset":' + str(multipliedNumber) + ',"version":1}'
            sample_string_bytes = sample_string.encode("ascii")
            
            base64_bytes = base64.b64encode(sample_string_bytes)
            base64_string = base64_bytes.decode("ascii")

            thread = threading.Thread(target=scrape_page, args=(firsturl, i, base64_string))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        print("All threads finished.")

        print(hrefList)

        print(len(hrefList))
        print(len(moneyList))


        seen_room_numbers = set()
        unique_hrefList = []
        unique_secondaryList = []

        for i, href in enumerate(hrefList):
            room_number = get_room_number(href)
            if room_number not in seen_room_numbers:
                unique_hrefList.append(href)
                unique_secondaryList.append(moneyList[i])
                seen_room_numbers.add(room_number)

        print(len(unique_hrefList))
        print(len(unique_secondaryList))

        with open('href.txt', "a") as file:
            # Iterate through the list and write each item to the file
            for item in unique_hrefList:
                file.write(item + "\n")

        with open('money.txt', "a") as file:
            # Iterate through the list and write each item to the file
            for item in unique_secondaryList:
                file.write(item + "\n")

        print(Location + "Finished")
        print("Process finished --- %s seconds ---" % (time.time() - start_time))

