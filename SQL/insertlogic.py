import pandas as pd
import mysql.connector
import json

# MySQL connection details
conn = mysql.connector.connect(
    user='root',  # Replace with your MySQL username
    password='Arya@1234',  # Replace with your MySQL password
    host='127.0.0.1',  # Localhost (or the IP address of your MySQL server)
    database='moodbite1520'  # Replace with your database name
)
cursor = conn.cursor()

# Load the CSV file
csv_file_path = 'Recipe.csv'  # Path to the uploaded CSV file
recipes_df = pd.read_csv(csv_file_path)

# Insert data into Recipes table
for _, row in recipes_df.iterrows():
    insert_query = """
    INSERT INTO Recipes (
        recipe_id, name, recipe_link, ingredients, mood_tag_id, image_link,
        summary, cuisines, dish_type, instruction_steps, spoonacular_score,
        servings, price_per_serving, caloric_breakdown, mood_tag, DietLabels
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Extract values from the CSV row and handle NULLs and JSON formatting
    values = (
        int(row['ID']),
        row['Title'],
        row['Spoonacular Source URL'] if pd.notnull(row['Spoonacular Source URL']) else None,
        json.dumps(row['Ingredients']) if pd.notnull(row['Ingredients']) else None,
        None,  # Replace with actual mood_tag_id logic if applicable
        row['Image'] if pd.notnull(row['Image']) else None,
        row['Summary'] if pd.notnull(row['Summary']) else None,
        row['Cuisines'] if pd.notnull(row['Cuisines']) else None,
        json.dumps(row['Dish Type']) if pd.notnull(row['Dish Type']) else None,
        row['Instruction Steps'] if pd.notnull(row['Instruction Steps']) else None,
        float(row['Spoonacular Score']) if pd.notnull(row['Spoonacular Score']) else None,
        int(row['Servings']) if pd.notnull(row['Servings']) else None,
        float(row['Price per Serving']) if pd.notnull(row['Price per Serving']) else None,
        json.dumps(row['Caloric Breakdown']) if pd.notnull(row['Caloric Breakdown']) else None,
        row['MoodTag'] if pd.notnull(row['MoodTag']) else None,
        json.dumps(row['Diet Labels']) if pd.notnull(row['Diet Labels']) else None
    )

    try:
        cursor.execute(insert_query, values)
    except Exception as e:
        print(f"Error inserting row {row['ID']}: {e}")

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully into the Recipes table.")
#%%
import pandas as pd
import mysql.connector
import json

# MySQL connection details
conn = mysql.connector.connect(
    user='root',  # Replace with your MySQL username
    password='Arya@1234',  # Replace with your MySQL password
    host='127.0.0.1',  # Localhost (or the IP address of your MySQL server)
    database='moodbite1520'  # Replace with your database name
)
cursor = conn.cursor()

# Load the Ingredients CSV file
ingredients_csv_file_path = 'Ingredients.csv'  # Path to the uploaded CSV file
ingredients_df = pd.read_csv(ingredients_csv_file_path)

# Insert data into Ingredients table
for _, row in ingredients_df.iterrows():
    insert_query = """
    INSERT INTO Ingredients (
        name
    ) VALUES (%s)
    """

    # Extract values from the CSV row
    values = (
        row['ingredient'],  # Replace 'ingredient' with the actual column name in the CSV
    )

    try:
        cursor.execute(insert_query, values)
    except Exception as e:
        print(f"Error inserting ingredient: {e}")

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully into the Ingredients table.")
#%%
import pandas as pd
import mysql.connector
import json

# MySQL connection details
conn = mysql.connector.connect(
    user='root',  # Replace with your MySQL username
    password='Arya@1234',  # Replace with your MySQL password
    host='127.0.0.1',  # Localhost (or the IP address of your MySQL server)
    database='moodbite1520'  # Replace with your database name
)
cursor = conn.cursor()

# Load the Nutrition CSV file
nutrition_csv_file_path = 'nutrition_details.csv'  # Path to the uploaded CSV file
nutrition_df = pd.read_csv(nutrition_csv_file_path)

# Insert data into Nutrition table
for _, row in nutrition_df.iterrows():
    insert_query = """
    INSERT INTO Nutrition (
        recipe_id, calories, fat, protein, carbs, fiber, sugar, sodium
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    # Extract values from the CSV row
    values = (
        int(row['recipe_id']),
        float(row['calories']) if pd.notnull(row['calories']) else None,
        float(row['fat']) if pd.notnull(row['fat']) else None,
        float(row['protein']) if pd.notnull(row['protein']) else None,
        float(row['carbs']) if pd.notnull(row['carbs']) else None,
        float(row['fiber']) if pd.notnull(row['fiber']) else None,
        float(row['sugar']) if pd.notnull(row['sugar']) else None,
        float(row['sodium']) if pd.notnull(row['sodium']) else None
    )

    try:
        cursor.execute(insert_query, values)
    except Exception as e:
        print(f"Error inserting recipe_id {row['recipe_id']}: {e}")

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully into the Nutrition table.")
#%%

import pandas as pd
import mysql.connector

# MySQL connection details
conn = mysql.connector.connect(
    user='root',  # Replace with your MySQL username
    password='Arya@1234',  # Replace with your MySQL password
    host='127.0.0.1',  # Localhost (or the IP address of your MySQL server)
    database='moodbite1520'  # Replace with your database name
)
cursor = conn.cursor()

# Load the Nutrition CSV file
nutrition_csv_file_path = 'nutrition_details.csv'  # Update with your CSV file path
nutrition_df = pd.read_csv(nutrition_csv_file_path)

# Insert data into Nutrition table
for _, row in nutrition_df.iterrows():
    insert_query = """
    INSERT INTO Nutrition (
        recipe_id, calories, fat, protein, carbs, fiber, sugar, sodium
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    # Extract and handle NULL values
    values = (
        int(row['Recipe ID']),
        float(row['Calories']) if pd.notnull(row['Calories']) else None,
        float(row['Fat']) if pd.notnull(row['Fat']) else None,
        float(row['Protein']) if pd.notnull(row['Protein']) else None,
        float(row['Carbohydrates']) if pd.notnull(row['Carbohydrates']) else None,
        float(row['Fiber']) if pd.notnull(row['Fiber']) else None,
        float(row['Sugar']) if pd.notnull(row['Sugar']) else None,
        float(row['Sodium']) if pd.notnull(row['Sodium']) else None
    )

    try:
        cursor.execute(insert_query, values)
    except Exception as e:
        print(f"Error inserting recipe_id {row['Recipe ID']}: {e}")

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully into the Nutrition table.")
#%%
import pandas as pd
import mysql.connector

# MySQL connection details
conn = mysql.connector.connect(
    user='root',  # Replace with your MySQL username
    password='Arya@1234',  # Replace with your MySQL password
    host='127.0.0.1',  # Localhost (or the IP address of your MySQL server)
    database='moodbite1520'  # Replace with your database name
)
cursor = conn.cursor()

# Insert data into MoodTags table
insert_queries = [
    "INSERT INTO MoodTags (name, description) VALUES ('Reducing Anxiety', 'Foods that help reduce anxiety and stress');",
    "INSERT INTO MoodTags (name, description) VALUES ('Boosting Focus and Productivity', 'Foods that help with mental clarity and focus');",
    "INSERT INTO MoodTags (name, description) VALUES ('Boosting Energy Levels', 'Foods that provide sustained energy');",
    "INSERT INTO MoodTags (name, description) VALUES ('Improving Mood and Well-being', 'Foods that enhance mood and emotional well-being');",
    "INSERT INTO MoodTags (name, description) VALUES ('Promoting Relaxation and Sleep', 'Foods that promote calmness and relaxation');",
    "INSERT INTO MoodTags (name, description) VALUES ('Balanced', 'General mood-neutral foods suitable for everyday use');"
]

for query in insert_queries:
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"Error executing query: {query}\nError: {e}")

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data inserted successfully into the MoodTags table.")

#%%

import mysql.connector
from faker import Faker
import random
import json

# Initialize Faker
fake = Faker()

# MySQL connection details
conn = mysql.connector.connect(
    user='root',  # Replace with your MySQL username
    password='Arya@1234',  # Replace with your MySQL password
    host='127.0.0.1',  # Localhost (or the IP address of your MySQL server)
    database='moodbite1520'  # Replace with your database name
)
cursor = conn.cursor()

# Step 1: Delete existing data
try:
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("DELETE FROM UserProfiles;")
    cursor.execute("DELETE FROM DietaryPreferences;")
    cursor.execute("DELETE FROM Users;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
    conn.commit()
    print("Existing data deleted successfully.")
except Exception as e:
    print(f"Error during data deletion: {e}")

# Step 2: Insert new users
for _ in range(50):
    name = fake.name()
    username = name.lower().replace(" ", ".")
    email = fake.email()
    password = '123'  # Common password for all users

    user_insert_query = f"""
    INSERT INTO Users (username, email, password)
    VALUES ('{username}', '{email}', '{password}');
    """

    try:
        cursor.execute(user_insert_query)
    except Exception as e:
        print(f"Error inserting user: {e}")

# Fetch the newly inserted user IDs
cursor.execute("SELECT user_id FROM Users;")
user_ids = [row[0] for row in cursor.fetchall()]

# Step 3: Insert new profiles
genders = ['Male', 'Female', 'Other']
activity_levels = ['Minimal', 'Moderate', 'Very Active']
dietary_preferences = [
    {"vegetarian": True, "vegan": False},
    {"vegetarian": False, "vegan": True},
    {"vegetarian": False, "vegan": False},
    {"vegetarian": True, "vegan": True}
]
restrictions = [
    ["nuts"],
    ["shellfish"],
    ["dairy"],
    [],  # No restrictions
    ["gluten", "soy"]
]

for user_id in user_ids:
    age = random.randint(18, 60)
    gender = random.choice(genders)
    height = random.randint(150, 200)  # Height in cm
    weight = random.randint(50, 100)  # Weight in kg

    # Correlate activity level with age and weight
    if age < 30:
        activity_level = random.choices(['Moderate', 'Very Active'], weights=[1, 2])[0]
    elif age < 50:
        activity_level = random.choices(['Minimal', 'Moderate'], weights=[1, 2])[0]
    else:
        activity_level = 'Minimal'

    # Insert into UserProfiles
    user_profile_insert_query = f"""
    INSERT INTO UserProfiles (user_id, age, gender, height, weight, activity_level)
    VALUES ({user_id}, {age}, '{gender}', {height}, {weight}, '{activity_level}');
    """

    try:
        cursor.execute(user_profile_insert_query)
    except Exception as e:
        print(f"Error inserting user profile for user_id {user_id}: {e}")

    # Insert dietary preferences
    diet_type = random.choice(dietary_preferences)
    user_restrictions = random.choice(restrictions)

    dietary_insert_query = f"""
    INSERT INTO DietaryPreferences (user_id, diet_type, restrictions)
    VALUES ({user_id}, '{json.dumps(diet_type)}', '{json.dumps(user_restrictions)}');
    """

    try:
        cursor.execute(dietary_insert_query)
    except Exception as e:
        print(f"Error inserting dietary preferences for user_id {user_id}: {e}")

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("New data inserted successfully into Users, UserProfiles, and DietaryPreferences tables.")
#%%
import mysql.connector
import random

# MySQL connection details
conn = mysql.connector.connect(
    user='root',  # Replace with your MySQL username
    password='Arya@1234',  # Replace with your MySQL password
    host='127.0.0.1',  # Localhost (or the IP address of your MySQL server)
    database='moodbite1520'  # Replace with your database name
)
cursor = conn.cursor()

# Step 1: Fetch all user_ids and recipe_ids
cursor.execute("SELECT user_id FROM Users;")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT recipe_id FROM Recipes;")
recipe_ids = [row[0] for row in cursor.fetchall()]

# Step 2: Generate RecipePreferences data
# Simulate likes/dislikes for each user on random recipes
recipe_preferences_queries = []

for user_id in user_ids:
    # Each user will swipe on a random number of recipes (e.g., 10–30)
    swipes = random.randint(10, 30)
    swiped_recipes = random.sample(recipe_ids, min(swipes, len(recipe_ids)))  # Randomly choose recipes
    for recipe_id in swiped_recipes:
        liked = random.choice([True, False])  # Randomly decide like/dislike
        recipe_preferences_queries.append(
            f"INSERT INTO RecipePreferences (user_id, recipe_id, liked) VALUES ({user_id}, {recipe_id}, {liked});"
        )

# Step 3: Insert RecipePreferences data into the database
for query in recipe_preferences_queries:
    try:
        cursor.execute(query)
    except Exception as e:
        print(f"Error executing query: {query}\nError: {e}")

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("RecipePreferences table populated successfully!")

#%%


import mysql.connector
import random

# MySQL connection details
conn = mysql.connector.connect(
    user='root',
    password='Arya@1234',
    host='127.0.0.1',
    database='moodbite1520'
)
cursor = conn.cursor()

# Fetch user_ids and recipe_ids
cursor.execute("SELECT user_id FROM Users;")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT recipe_id FROM Recipes;")
recipe_ids = [row[0] for row in cursor.fetchall()]

# Generate recommendations and user interactions
for user_id in user_ids:
    recommended_recipes = random.sample(recipe_ids, random.randint(5, 15))  # Recommend 5-15 recipes per user
    for recipe_id in recommended_recipes:
        viewed = random.choice([True, False])
        liked = random.choice([True, False]) if viewed else False  # Can only like if viewed
        cursor.execute("""
            INSERT INTO RecommendationAnalytics (user_id, recipe_id, viewed, liked)
            VALUES (%s, %s, %s, %s)
        """, (user_id, recipe_id, viewed, liked))

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("RecommendationAnalytics table populated.")

#%%

# Reconnect to the database
conn = mysql.connector.connect(
    user='root',
    password='Arya@1234',
    host='127.0.0.1',
    database='moodbite1520'
)
cursor = conn.cursor()

# Fetch and update analytics for each recipe
cursor.execute("SELECT recipe_id FROM Recipes;")
recipe_ids = [row[0] for row in cursor.fetchall()]

for recipe_id in recipe_ids:
    # Count views and likes from RecommendationAnalytics
    cursor.execute("""
        SELECT COUNT(*) AS views, SUM(liked) AS favorites
        FROM RecommendationAnalytics
        WHERE recipe_id = %s
    """, (recipe_id,))
    result = cursor.fetchone()
    views, favorites = result

    # Insert or update RecipeAnalytics
    cursor.execute("""
        INSERT INTO RecipeAnalytics (recipe_id, views, favorites)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE views = VALUES(views), favorites = VALUES(favorites)
    """, (recipe_id, views, favorites))

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("RecipeAnalytics table updated.")

#%%
# Reconnect to the database
conn = mysql.connector.connect(
    user='root',
    password='Arya@1234',
    host='127.0.0.1',
    database='moodbite1520'
)
cursor = conn.cursor()

# Fetch user interactions from RecommendationAnalytics
cursor.execute("""
    SELECT user_id, recipe_id
    FROM RecommendationAnalytics
    WHERE viewed = TRUE
""")
interactions = cursor.fetchall()

# Generate ratings and feedback
for user_id, recipe_id in interactions:
    rating = random.randint(1, 5)  # Random rating between 1 and 5
    feedback = f"This is feedback for recipe {recipe_id} by user {user_id}."
    cursor.execute("""
        INSERT INTO RecipeRatings (user_id, recipe_id, rating, feedback)
        VALUES (%s, %s, %s, %s)
    """, (user_id, recipe_id, rating, feedback))

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("RecipeRatings table populated.")

#%%

import mysql.connector
import random

# MySQL connection
conn = mysql.connector.connect(
    user='root',  # Replace with your MySQL username
    password='Arya@1234',  # Replace with your MySQL password
    host='127.0.0.1',  # Localhost
    database='moodbite1520'  # Replace with your database name
)
cursor = conn.cursor()

# Fetch all user_ids and recipe_ids
cursor.execute("SELECT user_id FROM Users;")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT recipe_id FROM Recipes;")
recipe_ids = [row[0] for row in cursor.fetchall()]

# Generate random favorites
favorites_queries = []
for user_id in user_ids:
    # Each user favorites 5-10 random recipes
    favorite_recipes = random.sample(recipe_ids, random.randint(5, 10))
    for recipe_id in favorite_recipes:
        favorites_queries.append((user_id, recipe_id))

# Insert into UserFavorites table
try:
    query = "INSERT INTO UserFavorites (user_id, recipe_id) VALUES (%s, %s)"
    cursor.executemany(query, favorites_queries)
    conn.commit()
    print(f"{cursor.rowcount} rows inserted into UserFavorites table.")
except Exception as e:
    print(f"Error: {e}")
finally:
    cursor.close()
    conn.close()

