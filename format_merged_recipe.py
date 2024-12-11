import pandas as pd

# Load the data (replace 'merged_file.csv' with your merged CSV file)
data = pd.read_csv("merged_recipe_data.csv")

# Strip leading/trailing spaces from all string columns
data = data.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Replace multiline strings in 'Recipe Ingredients' and 'Recipe' with single-line strings
data['Recipe Ingredients'] = data['Recipe Ingredients'].str.replace(r"\s{2,}", " ", regex=True)
data['Recipe'] = data['Recipe'].str.replace(r"\s{2,}", " ", regex=True)

# Drop any rows where all values are missing (optional, if you have incomplete data)
data.dropna(how="all", inplace=True)

# Ensure 'Recipe_Id' is sequential and numeric (reassign if necessary)
if 'Recipe_Id' in data.columns:
    data['Recipe_Id'] = range(1, len(data) + 1)

# Save the cleaned and formatted data back to CSV
data.to_csv("formatted_recipes.csv", index=False)