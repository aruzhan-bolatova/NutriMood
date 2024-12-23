# import requests
# import json
# import os
# import csv
# import time
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
# BASE_URL = "https://api.spoonacular.com/recipes/complexSearch"

# class IngredientManager:
#     def __init__(self, ingredients_csv='Ingredients.csv'):
#         """
#         Initialize IngredientManager with a CSV file to track ingredients.
        
#         Args:
#             ingredients_csv (str): Path to the ingredients CSV file
#         """
#         self.ingredients_csv = ingredients_csv
#         self.ingredients_dict = self.load_existing_ingredients()
    
#     def load_existing_ingredients(self):
#         """
#         Load existing ingredients from CSV file.
        
#         Returns:
#             dict: Dictionary of existing ingredients {ingredient_name: ingredient_id}
#         """
#         ingredients = {}
#         try:
#             with open(self.ingredients_csv, 'r', newline='', encoding='utf-8') as csvfile:
#                 reader = csv.reader(csvfile)
#                 next(reader, None)  # Skip header if exists
#                 for row in reader:
#                     if len(row) >= 2:
#                         ingredients[row[1]] = int(row[0])
#         except FileNotFoundError:
#             # Create file with header if it doesn't exist
#             with open(self.ingredients_csv, 'w', newline='', encoding='utf-8') as csvfile:
#                 writer = csv.writer(csvfile)
#                 writer.writerow(['ingredient_id', 'ingredient_name'])
        
#         return ingredients
    
#     def extract_ingredients(self, recipes):
#         """
#         Extract unique ingredients from recipes.
        
#         Args:
#             recipes (list): List of recipe dictionaries
        
#         Returns:
#             list: List of unique ingredient names
#         """
#         unique_ingredients = set()
        
#         for recipe in recipes:
#             # Check if recipe has nutrition information and ingredients
#             if 'nutrition' in recipe and 'ingredients' in recipe['nutrition']:
#                 for ingredient in recipe['nutrition']['ingredients']:
#                     ingredient_name = ingredient.get('name', '').strip().lower()
#                     if ingredient_name:
#                         unique_ingredients.add(ingredient_name)
        
#         return list(unique_ingredients)
    
#     def update_ingredients_csv(self, new_ingredients):
#         """
#         Update ingredients CSV with new ingredients.
#         Assigns new unique IDs to previously unseen ingredients.
        
#         Args:
#             new_ingredients (list): List of new ingredient names
        
#         Returns:
#             int: Number of new ingredients added
#         """
#         new_ingredient_count = 0
        
#         # Determine the next available ingredient ID
#         max_existing_id = max(self.ingredients_dict.values()) if self.ingredients_dict else 0
        
#         # Open CSV in append mode
#         with open(self.ingredients_csv, 'a', newline='', encoding='utf-8') as csvfile:
#             writer = csv.writer(csvfile)
            
#             # Add new ingredients
#             for ingredient in new_ingredients:
#                 # Check if ingredient already exists (case-insensitive)
#                 if ingredient.lower() not in [existing.lower() for existing in self.ingredients_dict.keys()]:
#                     # Assign new ID
#                     new_id = max_existing_id + 1
#                     max_existing_id = new_id
                    
#                     # Write to CSV
#                     writer.writerow([new_id, ingredient])
                    
#                     # Update in-memory dictionary
#                     self.ingredients_dict[ingredient] = new_id
                    
#                     new_ingredient_count += 1
        
#         print(f"Added {new_ingredient_count} new ingredients to {self.ingredients_csv}")
#         return new_ingredient_count

# def fetch_recipes(diet, ingredient_manager, filename='recipes.json'):
#     """
#     Fetch recipes for a specific diet and update JSON and ingredients CSV.
    
#     Args:
#         diet (str): Diet type to search for
#         ingredient_manager (IngredientManager): Instance to manage ingredients
#         filename (str, optional): File to save/append recipes
#     """
#     # Load existing recipes
#     try:
#         with open(filename, 'r') as f:
#             existing_recipes = json.load(f)
#     except (FileNotFoundError, json.JSONDecodeError):
#         existing_recipes = []
    
#     # Prepare API parameters
#     params = {
#         "apiKey": SPOONACULAR_API_KEY,
#         "diet": diet,
#         "includeIngredients" : "camomile",
#         "addRecipeNutrition": True,
#         "addRecipeInstructions": True,
#         "number": 20
#     }
    
#     try:
#         # Make API request
#         response = requests.get(BASE_URL, params=params)
#         response.raise_for_status()
        
#         if response.status_code == 200:
#             # Parse the response
#             new_recipes = response.json().get('results', [])
            
#             # Track initial counts
#             initial_recipe_count = len(existing_recipes)
            
#             # Append new recipes, avoiding duplicates
#             for recipe in new_recipes:
#                 if not any(existing['id'] == recipe['id'] for existing in existing_recipes):
#                     existing_recipes.append(recipe)
            
#             # Extract and update ingredients
#             new_ingredients = ingredient_manager.extract_ingredients(new_recipes)
#             ingredient_manager.update_ingredients_csv(new_ingredients)
            
#             # Save updated recipe list
#             with open(filename, 'w') as f:
#                 json.dump(existing_recipes, f, indent=2)
            
#             print(f"Added {len(existing_recipes) - initial_recipe_count} new recipes for {diet} diet.")
#             print(f"Total recipes now: {len(existing_recipes)}")
    
#     except requests.exceptions.HTTPError as http_err:
#         print(f"HTTP error occurred for {diet} diet: {http_err}")
#     except Exception as err:
#         print(f"Error occurred for {diet} diet: {err}")
    
#     # Optional: Add a small delay to respect API rate limits
#     time.sleep(1)

# def main():
#     # Initialize ingredient manager
#     ingredient_manager = IngredientManager()
    
#     # List of diets to fetch
#     diets = [
#         "gluten-free", "ketogenic", "vegetarian", 
#         "lacto-vegetarian", "ovo-vegetarian", 
#         "vegan", "pescetarian", "paleo"
#     ]
    
#     # Fetch recipes for each diet
#     for diet in diets:
#         fetch_recipes(diet, ingredient_manager)

# if __name__ == "__main__":
#     main()

import requests
import json
import os
import csv
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
BASE_URL = "https://api.spoonacular.com/recipes/complexSearch"

class IngredientManager:
    def __init__(self, ingredients_csv='Ingredients.csv'):
        """
        Initialize IngredientManager with a CSV file to track ingredients.

        Args:
            ingredients_csv (str): Path to the ingredients CSV file
        """
        self.ingredients_csv = ingredients_csv
        self.ingredients_dict = self.load_existing_ingredients()
    
    def load_existing_ingredients(self):
        """
        Load existing ingredients from CSV file.

        Returns:
            dict: Dictionary of existing ingredients {ingredient_name: ingredient_id}
        """
        ingredients = {}
        try:
            with open(self.ingredients_csv, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)  # Skip header if exists
                for row in reader:
                    if len(row) >= 2:
                        ingredients[row[1]] = int(row[0])
        except FileNotFoundError:
            # Create file with header if it doesn't exist
            with open(self.ingredients_csv, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ingredient_id', 'ingredient_name'])
        
        return ingredients
    
    def extract_ingredients(self, recipes):
        """
        Extract unique ingredients from recipes.

        Args:
            recipes (list): List of recipe dictionaries

        Returns:
            list: List of unique ingredient names
        """
        unique_ingredients = set()

        for recipe in recipes:
            # Check if recipe has nutrition information and ingredients
            if 'nutrition' in recipe and 'ingredients' in recipe['nutrition']:
                for ingredient in recipe['nutrition']['ingredients']:
                    ingredient_name = ingredient.get('name', '').strip().lower()
                    if ingredient_name:
                        unique_ingredients.add(ingredient_name)

        return list(unique_ingredients)
    
    def update_ingredients_csv(self, new_ingredients):
        """
        Update ingredients CSV with new ingredients.
        Assigns new unique IDs to previously unseen ingredients.

        Args:
            new_ingredients (list): List of new ingredient names

        Returns:
            int: Number of new ingredients added
        """
        new_ingredient_count = 0

        # Determine the next available ingredient ID
        max_existing_id = max(self.ingredients_dict.values()) if self.ingredients_dict else 0

        # Open CSV in append mode
        with open(self.ingredients_csv, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Add new ingredients
            for ingredient in new_ingredients:
                # Check if ingredient already exists (case-insensitive)
                if ingredient.lower() not in [existing.lower() for existing in self.ingredients_dict.keys()]:
                    # Assign new ID
                    new_id = max_existing_id + 1
                    max_existing_id = new_id

                    # Write to CSV
                    writer.writerow([new_id, ingredient])

                    # Update in-memory dictionary
                    self.ingredients_dict[ingredient] = new_id

                    new_ingredient_count += 1

        print(f"Added {new_ingredient_count} new ingredients to {self.ingredients_csv}")
        return new_ingredient_count

def fetch_recipes(ingredient_manager, filename='recipes.json'):
    """
    Fetch recipes and update JSON and ingredients CSV.

    Args:
        ingredient_manager (IngredientManager): Instance to manage ingredients
        filename (str, optional): File to save/append recipes
    """
    # Load existing recipes
    try:
        with open(filename, 'r') as f:
            existing_recipes = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_recipes = []

    # Prepare API parameters
    params = {
        "apiKey": SPOONACULAR_API_KEY,
        "includeIngredients": "shrimp",
        "addRecipeNutrition": True,
        "addRecipeInstructions": True,
        "number": 20
    }

    try:
        # Make API request
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        if response.status_code == 200:
            # Parse the response
            new_recipes = response.json().get('results', [])

            # Track initial counts
            initial_recipe_count = len(existing_recipes)

            # Append new recipes, avoiding duplicates
            for recipe in new_recipes:
                if not any(existing['id'] == recipe['id'] for existing in existing_recipes):
                    existing_recipes.append(recipe)

            # Extract and update ingredients
            new_ingredients = ingredient_manager.extract_ingredients(new_recipes)
            ingredient_manager.update_ingredients_csv(new_ingredients)

            # Save updated recipe list
            with open(filename, 'w') as f:
                json.dump(existing_recipes, f, indent=2)

            print(f"Added {len(existing_recipes) - initial_recipe_count} new recipes.")
            print(f"Total recipes now: {len(existing_recipes)}")

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Error occurred: {err}")

    # Optional: Add a small delay to respect API rate limits
    time.sleep(1)

def main():
    # Initialize ingredient manager
    ingredient_manager = IngredientManager()

    # Fetch recipes
    fetch_recipes(ingredient_manager)

if __name__ == "__main__":
    main()
