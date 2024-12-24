# -*- coding: utf-8 -*-
"""
Created on Sun Dec 22 20:45:21 2024

@author: 91838
"""

from flask import Flask, request, jsonify, render_template
import json
import mysql.connector

app = Flask(__name__)

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


# Route to register a new user
@app.route('/register', methods=['POST'])
def register_new_user():
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        age = data.get('age')
        gender = data.get('gender')
        height = data.get('height')
        weight = data.get('weight')
        activity_level = data.get('activity_level')
        diet_type = data.get('diet_type', {})
        restrictions = data.get('restrictions', [])

        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor()
        # Insert into Users table
        cursor.execute(
            "INSERT INTO Users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, password)
        )
        user_id = cursor.lastrowid

        # Insert into UserProfiles table
        cursor.execute(
            "INSERT INTO UserProfiles (user_id, age, gender, height, weight, activity_level) "
            "VALUES (%s, %s, %s, %s, %s, %s)",
            (user_id, age, gender, height, weight, activity_level)
        )

        # Insert into DietaryPreferences table
        cursor.execute(
            "INSERT INTO DietaryPreferences (user_id, diet_type, restrictions) VALUES (%s, %s, %s)",
            (user_id, json.dumps(diet_type), json.dumps(restrictions))
        )

        conn.commit()
        return jsonify({"message": "User registered successfully", "user_id": user_id}), 201
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()


# Route to filter recipes based on preferences
@app.route('/filter_recipes', methods=['POST'])
def filter_recipes_by_preferences():
    try:
        data = request.json
        user_id = data.get('user_id')
        mood_goal = data.get('mood_goal')

        conn = connect_db()
        if conn is None:
            return jsonify({"error": "Database connection failed"}), 500

        cursor = conn.cursor(dictionary=True)

        # Fetch user preferences
        cursor.execute("SELECT diet_type, restrictions FROM DietaryPreferences WHERE user_id = %s", (user_id,))
        user_preferences = cursor.fetchone()

        if not user_preferences:
            diet_type = {}
            restrictions = []
        else:
            diet_type = json.loads(user_preferences['diet_type']) if user_preferences['diet_type'] else {}
            restrictions = json.loads(user_preferences['restrictions']) if user_preferences['restrictions'] else []

        # Fetch recipes for the given mood goal
        cursor.execute("SELECT * FROM Recipes WHERE mood_tag = %s", (mood_goal,))
        recipes = cursor.fetchall()

        filtered_recipes = []
        for recipe in recipes:
            try:
                # Parse JSON fields
                diet_labels = json.loads(recipe['DietLabels']) if isinstance(recipe['DietLabels'], str) else {}
                ingredients = json.loads(recipe['ingredients']) if isinstance(recipe['ingredients'], str) else []

                # Apply dietary preferences and restrictions filters
                if diet_type:
                    if not all(diet_labels.get(key, False) == val for key, val in diet_type.items()):
                        continue

                if restrictions:
                    if any(restriction.lower() in ingredient.lower() for restriction in restrictions for ingredient in ingredients):
                        continue

                # Add the recipe to the filtered list if it passes all checks
                filtered_recipes.append(recipe)

            except json.JSONDecodeError:
                continue

        # Sort recipes by Spoonacular score
        filtered_recipes.sort(key=lambda x: x['spoonacular_score'], reverse=True)

        if filtered_recipes:
            selected_recipe = filtered_recipes[0]
            return jsonify({
                "message": "Recipe found",
                "recipe": {
                    "name": selected_recipe['name'],
                    "summary": selected_recipe['summary'],
                    "link": selected_recipe['recipe_link'],
                    "spoonacular_score": selected_recipe['spoonacular_score']
                }
            }), 200
        else:
            return jsonify({"message": "No recipes found matching your preferences"}), 404
    except mysql.connector.Error as err:
        return jsonify({"error": str(err)}), 500
    finally:
        if conn:
            cursor.close()
            conn.close()


# Main function to run the app
if __name__ == '__main__':
    app.run(debug=True)
