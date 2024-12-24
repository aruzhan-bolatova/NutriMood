# -- coding: utf-8 --
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

    # Ask the user about their dietary preferences
    is_vegetarian = input("Are you vegetarian? (yes/no): ").strip().lower() == "yes"
    is_vegan = input("Are you vegan? (yes/no): ").strip().lower() == "yes"
    is_gluten_free = input("Are you gluten-free? (yes/no): ").strip().lower() == "yes"

    # Create a dictionary for the dietary preferences
    diet_type = {
        "vegetarian": is_vegetarian,
        "vegan": is_vegan,
        "gluten_free": is_gluten_free
    }

    # Ask for dietary restrictions (if any)
    restrictions_input = input("Enter any dietary restrictions (comma separated) or type 'none': ").strip()
    restrictions = restrictions_input if restrictions_input.lower() != 'none' else []

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

        # Insert data into the database
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

# Function to filter recipes and add ingredients to the shopping list
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

        # Fetch breakfast and lunch recipes based on the selected mood goal
        print("Fetching breakfast and lunch recipes...")
        cursor.execute("""
            SELECT * FROM Recipes 
            WHERE mood_tag = %s 
            
        """, (mood_goal,))

        recipes = cursor.fetchall()

        if not recipes:
            print("No recipes found for the given mood goal.")
            return

        # Filter recipes based on preferences
        filtered_recipes = []
        for recipe in recipes:
            try:
                # Parse DietLabels field
                diet_labels = recipe.get('DietLabels')
                if isinstance(diet_labels, str):
                    try:
                        diet_labels = json.loads(diet_labels)  # Parse JSON string
                    except json.JSONDecodeError as e:
                       # print(f"Skipping recipe '{recipe.get('name')}' due to invalid JSON format in DietLabels. Error: {e}")
                        continue
                elif not isinstance(diet_labels, dict):
                   # print(f"Skipping recipe '{recipe.get('name')}' due to unexpected DietLabels type: {type(diet_labels)}")
                    continue

                #print(f"Checking recipe: {recipe['name']} with Diet Labels: {diet_labels}")

                # Calculate partial match percentage
                match_score = sum(
                    1 for key, value in diet_type.items()
                    if key in diet_labels and str(diet_labels[key]).lower() == str(value).lower()
                )
                total_preferences = len(diet_type)
                match_percentage = (match_score / total_preferences) * 100 if total_preferences > 0 else 0

                # Check restrictions
                ingredients = recipe.get('ingredients')
                if isinstance(ingredients, str):
                    try:
                        ingredients = json.loads(ingredients)  # Parse JSON string
                    except json.JSONDecodeError as e:
                       # print(f"Skipping recipe '{recipe.get('name')}' due to invalid JSON format in ingredients. Error: {e}")
                        continue
                elif not isinstance(ingredients, list):
                   # print(f"Skipping recipe '{recipe.get('name')}' due to unexpected ingredients type: {type(ingredients)}")
                    continue

                restricted = any(restriction.lower() in json.dumps(ingredients).lower() for restriction in restrictions)

                if restricted:
                   # print(f"Excluded recipe '{recipe['name']}' due to restriction.")
                    continue

                # Add recipe with match percentage
                filtered_recipes.append((recipe, match_percentage))

            except (TypeError, KeyError) as e:
               # print(f"Skipping recipe due to unexpected data format: {recipe.get('name')}. Error: {e}")
                   continue
        # Sort recipes by match percentage and Spoonacular score
        filtered_recipes.sort(key=lambda x: (x[1], x[0]['spoonacular_score']), reverse=True)

        # Display the top recipes or fallback to the best available recipe
        if filtered_recipes:
            print("\n--- Recommended Recipes ---")
            for recipe, percentage in filtered_recipes[:3]:  # Show top 3 recipes
                print(f"\n### Recipe: {recipe['name']}")
                print(f"- *Recipe ID:* {recipe['recipe_id']}")
                print(f"- *Diet Labels:* {json.dumps(recipe.get('DietLabels', 'N/A'))}")
                print(f"- *Ready In:* {recipe.get('ready_in_minutes', 'N/A')} minutes")
                print(f"- *Summary:* {recipe.get('summary', 'N/A')}")
                print(f"- *Cuisine:* {recipe.get('cuisines', 'N/A')}")
                print(f"- *Dish Type:* {json.dumps(recipe.get('dish_type', 'N/A'))}")
                print(f"- *Instructions:* {recipe.get('instruction_steps', 'N/A')}")
                print(f"- *Caloric Breakdown:* {json.dumps(recipe.get('caloric_breakdown', 'N/A'))}")
        else:
            # Fallback: Show the top recipe regardless of restrictions
            best_recipe = max(recipes, key=lambda r: r.get('spoonacular_score', 0))
            #print("\n recipes matched your preferences. Here's the top recipe available:")
            print(f"\n### Recipe: {best_recipe['name']}")
            print(f"- *Recipe ID:* {best_recipe['recipe_id']}")
            print(f"- *Diet Labels:* {json.dumps(best_recipe.get('DietLabels', 'N/A'))}")
            print(f"- *Ready In:* {best_recipe.get('ready_in_minutes', 'N/A')} minutes")
            print(f"- *Summary:* {best_recipe.get('summary', 'N/A')}")
            print(f"- *Cuisine:* {best_recipe.get('cuisines', 'N/A')}")
            print(f"- *Dish Type:* {json.dumps(best_recipe.get('dish_type', 'N/A'))}")
            print(f"- *Instructions:* {best_recipe.get('instruction_steps', 'N/A')}")
            print(f"- *Caloric Breakdown:* {json.dumps(best_recipe.get('caloric_breakdown', 'N/A'))}")

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        cursor.close()
        conn.close()

# Add this line at the end of the function filter_recipes_by_preferences
print("\nPress Enter to return to the main menu.")
input()  # Waits for the user to press Enter


# Function to view the shopping list
def view_shopping_list(user_id):
    print("\n--- Shopping List ---")

    conn = connect_db()
    if conn is None:
        print("Database connection failed.")
        return

    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT i.name AS ingredient_name, s.quantity
            FROM ShoppingList s
            JOIN Ingredients i ON s.ingredient_id = i.ingredient_id
            WHERE s.user_id = %s
        """, (user_id,))

        shopping_list = cursor.fetchall()

        if not shopping_list:
            print("Your shopping list is empty.")
        else:
            print("\nYour Shopping List:")
            for item in shopping_list:
                print(f"- {item['ingredient_name']}: {item['quantity']}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

# Function to add recipe rating
def add_recipe_rating():
    print("\n--- Add Recipe Rating ---")
    try:
        user_id = int(input("Enter your User ID: "))
        recipe_id = int(input("Enter the Recipe ID: "))
        rating = int(input("Enter your rating for the recipe (1 to 5): "))
        if rating < 1 or rating > 5:
            print("Invalid rating. Please enter a number between 1 and 5.")
            return
        feedback = input("Enter your feedback for the recipe (optional): ")

        conn = connect_db()
        if conn is None:
            print("Database connection failed.")
            return

        cursor = conn.cursor()
        try:
            # Insert rating into RecipeRatings table
            cursor.execute(
                "INSERT INTO RecipeRatings (user_id, recipe_id, rating, feedback) VALUES (%s, %s, %s, %s)",
                (user_id, recipe_id, rating, feedback)
            )
            conn.commit()
            print("Thank you! Your rating and feedback have been saved.")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")
        finally:
            cursor.close()
            conn.close()
    except ValueError:
        print("Invalid input. Please enter valid numeric values for User ID, Recipe ID, and Rating.")
def get_mood_goal_from_user():
    print("\n--- Select Your Mood Goal ---")
    print("1. Boosting Focus and Productivity")
    print("2. Reducing Anxiety")
    print("3. Balanced")
    print("4. Promoting Relaxation and Sleep")

    # Prompt user for input
    choice = input("Please enter the number corresponding to your mood goal: ")

    # Validate input
    if choice == '1':
        return "Boosting Focus and Productivity"
    elif choice == '2':
        return "Reducing Anxiety"
    elif choice == '3':
        return "Balanced"
    elif choice == '4':
        return "Promoting Relaxation and Sleep"
    
    else:
        print("Invalid choice. Please select a number between 1 and 5.")
        return get_mood_goal_from_user()

# Main CLI application
def main():
    while True:
        print("\n--- MoodBite CLI ---")
        print("1. Register New User")
        print("2. Filter Recipes by Preferences")
        print("3. View Shopping List")
        print("4. Add Recipe Rating")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            register_new_user()
        elif choice == '2':
            try:
                user_id = int(input("Enter your User ID: "))
                mood_goal = get_mood_goal_from_user()
                filter_recipes_by_preferences(user_id, mood_goal)
            except ValueError:
                print("Invalid input. Please enter a valid User ID.")
        elif choice == '3':
            try:
                user_id = int(input("Enter your User ID: "))
                view_shopping_list(user_id)
            except ValueError:
                print("Invalid input. Please enter a valid User ID.")
        elif choice == '4':
            add_recipe_rating()
        elif choice == '5':
            print("Exiting MoodBite CLI. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
