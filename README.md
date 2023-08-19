# AI-Powered Airbnb Price Predictor


Welcome to the AI-Powered Airbnb Price Predictor project! This repository contains code and resources for building and deploying a machine-learning model that predicts Airbnb rental prices. Whether you're a data scientist looking to enhance your prediction skills or someone interested in understanding how AI can assist in real-world scenarios, this project is a great learning opportunity.

## Project Overview

The AI-Powered Airbnb Price Predictor project aims to create a predictive model that estimates the price of Airbnb rentals based on various features such as location, property type, number of bedrooms, and more. This can be valuable for both hosts and guests to get an idea of rental pricing in different areas.

## Getting Started

The repository already includes Airbnb data for a night for two guests on September 20-September 21 2023. If you plan on running this code for your own reasons, remove the CSV file, and the text files holding Href and Money values(href.txt and money.txt). Furthermore, remember that running this code can get you flagged by Airbnb for sending too many requests to the website. You will also have to replace the locations.txt file with your own locations which you wish to use (Make sure spelling is correct). Make sure you also have an existing empty, data.xlsx file. 
Lastly, replace all the paths in the code with your own.

In the model file, I used wandb to export graphs about my model. If you want to do this as well, you will have to make a wandb account and get your api key which you will need in order to set it up. If you done want to use wandb and just make the model, remove everything underneath "wandb.init(project="airbnbProject")", it is also commented in the code.

Run the Files in order of LinkFinder, main, model, and then test. The finalDATA file is simply the CSV version of data.xlsx. Remember you can change the URL in Linkfinder to alter the dates and number of guests.

## Requirements

use the following command to get the required libraries.<pre>pip install -r requirements.txt</pre>
