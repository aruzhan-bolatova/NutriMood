import json
import csv
import os
import re

def clean_text(text):
    """
    Clean text to remove problematic characters and ensure CSV compatibility
    """
    if text is None:
        return 'NULL'
    
    # Convert to string and remove newlines, replace quotes
    text_str = str(text)
    text_str = text_str.replace('\n', ' ').replace('\r', ' ')
    text_str = text_str.replace('"', "'")
    
    return text_str

def safe_json_dumps(data):
    """
    Safely convert data to JSON string, handling None and complex objects
    """
    if data is None:
        return 'NULL'
    
    try:
        return json.dumps(data)
    except (TypeError, ValueError):
        # If JSON dump fails, try to convert to string
        return str(data)


def process_recipes(json_data):
    # Prepare directories
    os.makedirs('output', exist_ok=True)

    # Prepare recipe details CSV
    recipe_details_file = 'output/recipe_details.csv'
    nutrition_details_file = 'output/nutrition_details.csv'

    # Define nutrition columns in the specified order
    nutrition_columns = [
        'Recipe ID', 'Calories', 'Fat', 'Trans Fat', 'Saturated Fat', 
        'Mono Unsaturated Fat', 'Poly Unsaturated Fat', 'Protein', 
        'Cholesterol', 'Carbohydrates', 'Net Carbohydrates', 'Alcohol', 
        'Fiber', 'Sugar', 'Sodium', 'Caffein', 'Manganese', 'Potassium', 
        'Magnesium', 'Calcium', 'Copper', 'Zinc', 'Phosphorus', 'Fluoride', 
        'Choline', 'Iron', 'Vitamin A', 'Vitamin B1', 'Vitamin B2', 
        'Vitamin B3', 'Vitamin B5', 'Vitamin B6', 'Vitamin B12', 
        'Vitamin C', 'Vitamin D', 'Vitamin E', 'Vitamin K', 'Folate', 
        'Folic Acid', 'Iodine', 'Selenium'
    ]

    # Open CSV files and write headers
    with open(recipe_details_file, 'w', newline='', encoding='utf-8') as recipe_csv, \
         open(nutrition_details_file, 'w', newline='', encoding='utf-8') as nutrition_csv:
        
        # Recipe details CSV writer
        recipe_writer = csv.writer(recipe_csv)
        recipe_writer.writerow([
            'ID', 'Title', 'Diet Labels', 'Ready in Minutes',
            'Price per Serving', 'Servings', 'Image', 'Summary', 
            'Cuisines', 'Dish Type', 'Instruction Steps', 
            'Spoonacular Score', 'Spoonacular ID', 
            'Spoonacular Source URL', 'Ingredients', 
            'Caloric Breakdown'
        ])

        # Nutrition details CSV writer
        nutrition_writer = csv.writer(nutrition_csv)
        nutrition_writer.writerow(nutrition_columns)

        # Process each recipe
        for idx, recipe in enumerate(json_data, 1):
            # Prepare diet labels with NULL for missing values
            diet_labels = {
                'vegetarian': recipe.get('vegetarian', 'NULL'),
                'vegan': recipe.get('vegan', 'NULL'),
                'glutenFree': recipe.get('glutenFree', 'NULL'),
                'dairyFree': recipe.get('dairyFree', 'NULL'),
            }

            # Add additional diet labels from 'diets' list
            if recipe.get('diets'):
                for diet in recipe['diets']:
                    # Convert diet to a 'camelCase' key if needed
                    diet_key = diet.replace(' ', '')
                    if diet_key == 'glutenfree':
                        diet_key = 'glutenFree'
                    elif diet_key == 'dairyfree':
                        diet_key = 'dairyFree'
                    
                    diet_labels[diet_key] = True

            # Prepare ingredients with NULL handling
            ingredients = []
            if recipe.get('nutrition', {}).get('ingredients'):
                ingredients = [
                    {
                        'id': ing.get('id', 'NULL'),
                        'name': clean_text(ing.get('name', 'NULL')),
                        'amount': ing.get('amount', 'NULL'),
                        'unit': ing.get('unit', 'NULL')
                    } for ing in recipe['nutrition']['ingredients']
                ]
            
            # Prepare instruction steps with NULL handling
            instruction_steps = []
            if recipe.get('analyzedInstructions'):
                for instruction in recipe['analyzedInstructions']:
                    for step in instruction.get('steps', []):
                        instruction_steps.append(clean_text(step.get('step', 'NULL')))
                
                # Join the steps into a plain text format, removing extra formatting
                instruction_steps = ". ".join(instruction_steps)

            # Prepare cuisines and dish types
            cuisines = ','.join(recipe.get('cuisines', ['NULL']))
            # Prepare dish type JSON
            dish_type_json = {
                "lunch/dinner": False,
                "breakfast": False,
                "snack": False
            }

            # Categorize dish types
            if recipe.get('dishTypes'):
                dish_types = [dt.lower() for dt in recipe['dishTypes']]
                
                # Check for lunch/dinner categories
                if any(dt in ['lunch', 'side dish', 'dinner', 'soup', 'salad'] for dt in dish_types):
                    dish_type_json["lunch/dinner"] = True
                
                # Check for breakfast categories
                if any(dt in ['breakfast', 'brunch', 'morning meal'] for dt in dish_types):
                    dish_type_json["breakfast"] = True
                
                # Check for snack categories
                if any(dt in ['beverages', 'drink', 'snack', 'dessert'] for dt in dish_types):
                    dish_type_json["snack"] = True

            # Write recipe details
            recipe_writer.writerow([
                idx,
                clean_text(recipe.get('title', 'NULL')),
                safe_json_dumps(diet_labels),
                recipe.get('readyInMinutes', 'NULL'),
                recipe.get('pricePerServing', 'NULL'),
                recipe.get('servings', 'NULL'),
                clean_text(recipe.get('image', 'NULL')),
                clean_text(recipe.get('summary', 'NULL')),
                clean_text(cuisines),
                safe_json_dumps(dish_type_json),
                clean_text(instruction_steps),
                recipe.get('spoonacularScore', 'NULL'),
                recipe.get('id', 'NULL'),
                clean_text(recipe.get('spoonacularSourceUrl', 'NULL')),
                safe_json_dumps(ingredients),
                safe_json_dumps(recipe.get('nutrition', {}).get('caloricBreakdown', 'NULL'))
            ])

            # Prepare nutrition details with NULL for missing values
            # Create a dict for easy lookup of nutrition values, defaulting to 'NULL'
            def get_nutrient_value(name):
                for nutrient in recipe.get('nutrition', {}).get('nutrients', []):
                    if nutrient['name'] == name:
                        return nutrient.get('amount', 'NULL')
                return 'NULL'

            # Map nutrition values to the specified columns
            nutrition_values = [
                idx,  # Recipe ID
                get_nutrient_value('Calories'),
                get_nutrient_value('Fat'),
                get_nutrient_value('Trans Fat'),
                get_nutrient_value('Saturated Fat'),
                get_nutrient_value('Mono Unsaturated Fat'),
                get_nutrient_value('Poly Unsaturated Fat'),
                get_nutrient_value('Protein'),
                get_nutrient_value('Cholesterol'),
                get_nutrient_value('Carbohydrates'),
                get_nutrient_value('Net Carbohydrates'),
                get_nutrient_value('Alcohol'),
                get_nutrient_value('Fiber'),
                get_nutrient_value('Sugar'),
                get_nutrient_value('Sodium'),
                get_nutrient_value('Caffeine'),
                get_nutrient_value('Manganese'),
                get_nutrient_value('Potassium'),
                get_nutrient_value('Magnesium'),
                get_nutrient_value('Calcium'),
                get_nutrient_value('Copper'),
                get_nutrient_value('Zinc'),
                get_nutrient_value('Phosphorus'),
                get_nutrient_value('Fluoride'),
                get_nutrient_value('Choline'),
                get_nutrient_value('Iron'),
                get_nutrient_value('Vitamin A'),
                get_nutrient_value('Vitamin B1'),
                get_nutrient_value('Vitamin B2'),
                get_nutrient_value('Vitamin B3'),
                get_nutrient_value('Vitamin B5'),
                get_nutrient_value('Vitamin B6'),
                get_nutrient_value('Vitamin B12'),
                get_nutrient_value('Vitamin C'),
                get_nutrient_value('Vitamin D'),
                get_nutrient_value('Vitamin E'),
                get_nutrient_value('Vitamin K'),
                get_nutrient_value('Folate'),
                get_nutrient_value('Folic Acid'),
                get_nutrient_value('Iodine'),
                get_nutrient_value('Selenium')
            ]

            # Write nutrition details
            nutrition_writer.writerow(nutrition_values)

    print(f"CSV files have been created in the 'output' directory:")
    print(f"1. {recipe_details_file}")
    print(f"2. {nutrition_details_file}")

# Main execution
def main():
    try:
        # Load JSON data
        with open('recipes.json', 'r', encoding='utf-8') as f:
            recipes_data = json.load(f)

        # Process recipes
        process_recipes(recipes_data)
    
    except FileNotFoundError:
        print("Error: 'recipes.json' file not found. Please ensure the file exists in the current directory.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in 'recipes.json'. Please check the file contents.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()