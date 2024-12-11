import pandas as pd

# Load the first CSV file (food_data_final.csv)
food_data_final = pd.read_csv("food_data_final.csv")

# Load the second CSV file 
second_table = pd.read_csv("updated_recipes_with_moods.csv")

# Clean column names
food_data_final.columns = food_data_final.columns.str.strip()
second_table.columns = second_table.columns.str.strip() 

food_data_final['Dish'] = food_data_final['Dish'].str.strip().str.lower()
second_table['Dish'] = second_table['Dish'].str.strip().str.lower()

# Merge the tables on the 'Dish' column and drop redundant/duplicating columns
merged_data = pd.merge(
    food_data_final,
    second_table[['Dish', 'Mood_Tag']],  # Only keep necessary columns from the second table
    on="Dish",
    how="inner"  # Perform an inner join
)

# Save the merged and processed table to a new CSV file
merged_data.to_csv("merged_recipe_data.csv", index=False)

print(merged_data.head())
