import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
import shap
import numpy as np
import wandb
import plotly.graph_objects as go
import joblib
import os
import matplotlib.pyplot as plt



# Load the CSV file into a pandas DataFrame
data = pd.read_csv('finalDATA.csv')
data['House Type'] = data['House Type'].str.strip()

# Define a custom function to clean numeric values with commas
def clean_numeric_value(value):
    try:
        return float(value.replace(',', ''))
    except:
        return None

# Apply the custom function to the "Number of Reviews" and "Cost" columns
data['Number of Reviews'] = data['Number of Reviews'].apply(clean_numeric_value)
data['Cost'] = data['Cost'].apply(clean_numeric_value)

# Convert categorical text to numerical using one-hot encoding
data = pd.get_dummies(data, columns=['House Type'], drop_first=True)

# Outlier removal using IQR method
Q1 = data['Cost'].quantile(0.25)
Q3 = data['Cost'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
data = data[(data['Cost'] > lower_bound) & (data['Cost'] < upper_bound)]

# Split features and target
X = data.drop(columns=['Cost'])
y = data['Cost']

# Split data into training, validation, and test sets
X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3)
X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5)


# Initialize and train the XGBoost Regressor model
xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1)
xgb_model.fit(X_train, y_train)

# Other evaluation and prediction steps...

# Predict on the validation set
y_val_pred = xgb_model.predict(X_val)

# Calculate RMSE and R2 score on the validation set
val_rmse = mean_squared_error(y_val, y_val_pred, squared=False)
val_r2 = r2_score(y_val, y_val_pred)

# Print the performance metrics
print("Validation RMSE:", val_rmse)
print("Validation R2 Score:", val_r2)



# Save the trained model to a file
model_filename = 'airbnbModel.joblib'
# Check if the file exists
if os.path.exists(model_filename):
    # Delete the file
    os.remove(model_filename)
    joblib.dump(xgb_model, model_filename)
else:
    joblib.dump(xgb_model, model_filename)


#REMOVE EVERYTHING UNDERNEATH THIS LINE IF YOU DON'T WANT TO GRAPH DATA AND JUST SAVE THE MODEL
wandb.init(project="airbnbProject")
# Get feature importances
feature_importances = xgb_model.feature_importances_

# Print feature importances
print("Feature Importances:")
# Get indices that would sort the feature importances in descending order
sorted_indices = sorted(range(len(feature_importances)), key=lambda k: feature_importances[k], reverse=True)

for idx in sorted_indices:
    print(f"{X.columns[idx]}: {feature_importances[idx]*100}")

# Initialize the SHAP explainer
explainer = shap.Explainer(xgb_model)

# Calculate SHAP values for the validation set
shap_values = explainer(X_val)


# Generate the SHAP summary plot as a Matplotlib figure
shap_summary_plot = shap.summary_plot(shap_values, X_val, feature_names=X.columns, show=False)
output_image_path = "shap_summary_plot.png"
plt.savefig(output_image_path, bbox_inches='tight', dpi=300)
# Convert the Matplotlib figure to an image


# Log the image to WandB using wandb.Image
wandb.log({"shap_summary_plot": wandb.Image("shap_summary_plot.png")})



# List of columns to consider
columns_to_analyze = ["Overall Rating", "Number of Reviews", "Latitude", "Longitude", "Cleanliness", "Accuracy", "Communication", "Check_in", "Value", "Location", 'Number of beds','Number of Bath', 'Number of bedroom', 'Number of guests', 'Superhost',
       'New Listing','Essentials','Air conditioning', 'Cleaning products', 'Cooking basics', 'Dryer',
       'Heating', 'Hot tub', 'Kitchen', 'Pool', 'Washer', 'Wifi', 'Bathtub',
       'TV', 'Dishwasher', 'Stove', 'Beach access', 'Lake access',
       'Waterfront', 'BBQ grill', 'Fire pit', 'Free parking on premise',
       'Sauna', 'Breakfast', 'Bay view', 'Beach view', 'Canal view',
       'City skyline view', 'Courtyard view', 'Desert view', 'Garden view',
       'Golf course view', 'Harbor view', 'Lake view', 'Marina view',
       'Mountain view', 'Ocean view', 'Park view', 'Pool view', 'Resort view',
       'River view', 'Sea view', 'Valley view', 'Vineyard view', 'Fireplace',

       'House Type_Room', 'House Type_bungalow', 'House Type_cabin',
       'House Type_chalet', 'House Type_condo', 'House Type_cottage',
       'House Type_guest suite', 'House Type_guesthouse', 'House Type_home',
       'House Type_loft', 'House Type_place', 'House Type_rental unit',
       'House Type_serviced apartment', 'House Type_townhouse',
       'House Type_vacation home', 'House Type_villa']


# Initialize a dictionary to store average SHAP values for each feature and each group
average_shap_values_by_feature = {}

for feature in columns_to_analyze:
    feature_index = X.columns.get_loc(feature)
    
    # Initialize lists to store x-axis values (feature values) and y-axis values (average SHAP values)
    x_values = []
    y_values = []
    
    # Get unique values in the current feature column that exist in the dataset
    unique_feature_values = X_val[feature].unique()

    # If there are more than 10 unique values, split them into 10 groups
    if len(unique_feature_values) > 15:
        sorted_unique_values = np.sort(unique_feature_values)
        unique_values_groups = np.array_split(sorted_unique_values, 15)
        
        # Loop through each group of unique values and calculate average SHAP values
        for group_values in unique_values_groups:
            index_values = np.where(X_val[feature].isin(group_values))[0]
            if len(index_values) > 0:  # Only consider values that exist in the dataset
                shap_values_values = shap_values[index_values, feature_index]
                average_shap_value = np.mean(shap_values_values.values)
                
                # Get the range of values within the group for defining the x-axis range
                value_range = f"{min(group_values)} - {max(group_values)}"
                
                # Append the value range and the average SHAP value to the lists
                x_values.append(value_range)
                y_values.append(average_shap_value)
    else:
        # If there are 10 or fewer unique values, keep them as individual points
        for value in unique_feature_values:
            index_values = np.where(X_val[feature] == value)[0]
            if len(index_values) > 0:  # Only consider values that exist in the dataset
                shap_values_values = shap_values[index_values, feature_index]
                average_shap_value = np.mean(shap_values_values.values)
                
                # Append the value and the average SHAP value to the lists
                x_values.append(value)
                y_values.append(average_shap_value)
    
    # Store the x and y values for the current feature
    average_shap_values_by_feature[feature] = (x_values, y_values)


net_shap_values_by_type = {}

# Initialize lists to store net SHAP values and feature names for non-"House Type" features
net_shap_values = []
net_shap_feature_names = []



# Loop through each House Type category
for feature, (x_values, y_values) in average_shap_values_by_feature.items():



    if feature.startswith("House Type"):
        try:
            # Calculate the net SHAP value by summing up positive and negative values
            net_shap_value = y_values[1] + y_values[0]
        except:
            net_shap_value = y_values[0]
        
        # Store the net SHAP value for the current House Type category
        net_shap_values_by_type[feature] = net_shap_value


    if not feature.startswith("House Type"):
        x_values, y_values = average_shap_values_by_feature[feature]
        if len(x_values) == 2:  # Check if there are only 2 x-values
            try:
                # Calculate the net SHAP value by summing up positive and negative values
                net_shap_value = y_values[1] + y_values[0]
            except:
                net_shap_value = y_values[0]
            
            # Store the net SHAP value and feature name
            net_shap_values.append(net_shap_value)
            net_shap_feature_names.append(feature)

        elif len(x_values) > 2:            
            fig = go.Figure([go.Bar(x=x_values, y=y_values)])
            fig.update_layout(title=f"Average SHAP Values for {feature}",
                            xaxis_title=feature, yaxis_title="Average SHAP Value")
            
            # Log the Plotly figure using wandb.log()
            wandb.log({f"Average_SHAP_{feature}": fig})



# Sort the net SHAP values and House Type categories by the net SHAP values
sorted_house_type_values = sorted(net_shap_values_by_type.items(), key=lambda x: x[1])
sorted_house_type_categories = [item[0] for item in sorted_house_type_values]
sorted_net_shap_values = [item[1] for item in sorted_house_type_values]

# Create a Plotly bar chart for net SHAP values of House Type categories
fig_house_type = go.Figure([go.Bar(x=sorted_house_type_categories, y=sorted_net_shap_values)])
fig_house_type.update_layout(title="Net SHAP Values for House Type Categories",
                             xaxis_title="House Type", yaxis_title="Net SHAP Value")

# Log the Plotly figure using wandb.log()
wandb.log({"Net_SHAP_House_Type": fig_house_type})

# Sort the net SHAP values and feature names by the net SHAP values
sorted_indices = sorted(range(len(net_shap_values)), key=lambda k: net_shap_values[k])
sorted_net_shap_values = [net_shap_values[idx] for idx in sorted_indices]
sorted_net_shap_feature_names = [net_shap_feature_names[idx] for idx in sorted_indices]

# Create a Plotly bar chart for the net SHAP values of features with 2 x-values
fig_features_2_unique_x = go.Figure([go.Bar(x=sorted_net_shap_feature_names, y=sorted_net_shap_values)])
fig_features_2_unique_x.update_layout(title="Net SHAP Values for Features with 2 Unique X-Values",
                                     xaxis_title="Feature", yaxis_title="Net SHAP Value")

# Log the Plotly figure using wandb.log()
wandb.log({"Net_SHAP_Features_2_Unique_X": fig_features_2_unique_x})


wandb.finish()
