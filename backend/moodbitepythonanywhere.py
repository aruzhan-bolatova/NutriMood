# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 01:07:53 2024

@author: 91838
"""
import json
import mysql.connector

# Database connection setup
def connect_db():
    try:
        conn = mysql.connector.connect(
            user='root',  # Replace with your MySQL username
            password='Arya@1234',  # Replace with your MySQL password
            host='127.0.0.1',  # Localhost or IP address of your MySQL server
            database='moodbite1520'  # Your database name
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Function to register a new user
def register_new_user():
    print("\n--- Register New User ---")
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = input("Enter password: ")
    age = input("Enter age: ")
    gender = input("Enter gender (Male/Female/Other): ")
    height = input("Enter height (in cm): ")
    weight = input("Enter weight (in kg): ")
    activity_level = input("Enter activity level (Minimal/Moderate/Very Active): ")

    # Get dietary preferences and restrictions
    diet_type_input = input("Enter dietary preferences as JSON (e.g., {'vegetarian': true, 'vegan': false}) or type 'skip': ")
    restrictions_input = input("Enter restrictions as a comma-separated list or type 'skip': ")

    try:
        diet_type = json.loads(diet_type_input.replace("'", '"')) if diet_type_input.strip().lower() != 'skip' else {}
        restrictions = [r.strip() for r in restrictions_input.split(',')] if restrictions_input.strip().lower() != 'skip' else []
    except json.JSONDecodeError:
        print("Invalid JSON format. Please try again.")
        return

    conn = connect_db()
    if conn is None:
        print("Database connection failed.")
        return

    cursor = conn.cursor()
    try:
        # Insert user details into Users table
        cursor.execute("INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        user_id = cursor.lastrowid  # Fetch the last inserted user ID

        # Insert user profile details
        cursor.execute(
            "INSERT INTO UserProfiles (user_id, age, gender, height, weight, activity_level) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, age, gender, height, weight, activity_level)
        )

        # Insert dietary preferences
        cursor.execute(
            "INSERT INTO DietaryPreferences (user_id, diet_type, restrictions) VALUES (%s, %s, %s)",
            (user_id, json.dumps(diet_type), json.dumps(restrictions))
        )

        conn.commit()
        print(f"User registered successfully with ID: {user_id}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def filter_recipes_by_preferences(user_id, mood_goal):
    print("\n--- Filtering Recipes Based on Preferences ---")

    conn = connect_db()
    if conn is None:
        print("Database connection failed.")
        return

    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch user preferences
        print("Fetching user preferences...")
        cursor.execute("SELECT diet_type, restrictions FROM DietaryPreferences WHERE user_id = %s", (user_id,))
        user_preferences = cursor.fetchone()

        if not user_preferences:
            print("No dietary preferences found for this user. Showing all recipes.")
            diet_type = {}
            restrictions = []
        else:
            # Parse diet_type and restrictions
            diet_type = json.loads(user_preferences['diet_type']) if user_preferences['diet_type'] else {}
            restrictions = json.loads(user_preferences['restrictions']) if user_preferences['restrictions'] else []

        print(f"Diet Type: {diet_type}")
        print(f"Restrictions: {restrictions}")

        # Fetch recipes for the given mood goal
        print("Fetching recipes...")
        cursor.execute("SELECT * FROM Recipes WHERE mood_tag = %s", (mood_goal,))
        recipes = cursor.fetchall()

        if not recipes:
            print("No recipes found for the given mood goal.")
            return

        # Filter recipes based on preferences
        filtered_recipes = []
        for recipe in recipes:
            try:
                # Parse JSON fields
                diet_labels = json.loads(recipe['DietLabels']) if isinstance(recipe['DietLabels'], str) else {}

                print(f"Checking recipe: {recipe['name']} with Diet Labels: {diet_labels}")

                # Calculate a matching percentage
                match_score = sum(1 for key, value in diet_type.items() if key in diet_labels and diet_labels[key] == value)
                total_preferences = len(diet_type)
                match_percentage = (match_score / total_preferences) * 100 if total_preferences > 0 else 0

                # Check restrictions
                restricted = any(restriction.lower() in recipe['ingredients'].lower() for restriction in restrictions)

                if restricted:
                    print(f"Excluded due to restriction: {recipe['name']}")
                    continue

                # Add recipe with its match percentage
                filtered_recipes.append((recipe, match_percentage))

            except json.JSONDecodeError as e:
                print(f"Skipping recipe due to invalid JSON format: {recipe['name']}. Error: {e}")

        # Sort recipes by match percentage and Spoonacular score
        filtered_recipes.sort(key=lambda x: (x[1], x[0]['spoonacular_score']), reverse=True)

        # Display the top recipe(s)
        if filtered_recipes:
            print("\n--- Recommended Recipes ---")
            for recipe, percentage in filtered_recipes[:3]:  # Show top 3 recipes
                print(f"\nName: {recipe['name']}")
                print(f"Match Percentage: {percentage:.2f}%")
                print(f"Summary: {recipe['summary']}")
                print(f"Link: {recipe['recipe_link']}")
                print(f"Spoonacular Score: {recipe['spoonacular_score']}")
        else:
            print("No recipes found matching your preferences.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
        
# Main CLI application
def main():
    while True:
        print("\n--- MoodBite CLI ---")
        print("1. Register New User")
        print("2. Filter Recipes by Preferences")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register_new_user()
        elif choice == '2':
            try:
                user_id = int(input("Enter your User ID: "))
                mood_goal = input("Enter your mood goal (e.g., Boosting Energy Levels): ")
                filter_recipes_by_preferences(user_id, mood_goal)
            except ValueError:
                print("Invalid input. Please enter a valid User ID.")
        elif choice == '3':
            print("Exiting MoodBite CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()