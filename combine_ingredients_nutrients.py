import pandas as pd

# Load the CSV files
file1 = '/Users/aruzhan/Desktop/DMS Final Project/raw data sets/fndds_ingredient_nutrient_value.csv'  # Replace with the actual filename
file2 = '/Users/aruzhan/Desktop/DMS Final Project/raw data sets/nutrient.csv'  

df1 = pd.read_csv(file1)
df2 = pd.read_csv(file2)

# Drop unnecessary columns
df1_cleaned = df1[['ingredient code', 'Ingredient description', 'Nutrient code', 'Nutrient value']]
df2_cleaned = df2[['nutrient_nbr', 'name', 'unit_name']]

# Merge the two tables based on the "Nutrient code" and "id"
combined_df = pd.merge(df1_cleaned, df2_cleaned, left_on='Nutrient code', right_on='nutrient_nbr')

# Drop the redundant column 'id' after merging
combined_df = combined_df.drop(columns=['nutrient_nbr'])

# Save the combined DataFrame to a CSV file
combined_df.to_csv('combined_ingredient_nutrient_data.csv', index=False)

print(combined_df.head())
