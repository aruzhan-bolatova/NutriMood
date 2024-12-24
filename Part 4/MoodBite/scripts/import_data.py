import os
import sys

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.data_importer import DataImporter

def ensure_directories_exist():
    """Create necessary directories if they don't exist"""
    directories = [
        'data',
        'data/csv',
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def main():
    # Create necessary directories
    ensure_directories_exist()
    
    # Get absolute path for database
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    db_path = os.path.join(current_dir, 'data', 'moodbite.db')
    
    # Initialize importer with absolute path
    importer = DataImporter(db_path)
    
    # Define CSV paths
    csv_dir = os.path.join('data', 'csv')
    recipes_path = os.path.join(csv_dir, 'recipe_details.csv')
    ingredients_path = os.path.join(csv_dir, 'Ingredients.csv')
    nutrition_path = os.path.join(csv_dir, 'nutrition_details.csv')
    mood_tags_path = os.path.join(csv_dir, 'mood_tags.csv')
    
    # Import data
    print("Importing mood tags...")
    importer.import_generic('MoodTags', mood_tags_path)
    
    print("Importing ingredients...")
    importer.import_ingredients('../data/csv/Ingredients.csv')
    
    print("Importing recipes...")
    importer.import_recipes('../data/csv/recipe_details.csv')
    
    print("Importing nutrition data...")
    importer.import_nutrition('../data/csv/nutrition_details.csv')
    
    # Import emotional goals and related data
    print("Importing emotional goals...")
    importer.import_emotional_goals('../data/csv/EmotionalGoals.csv')

    print("Importing nutrients...")
    importer.import_nutrients('../data/csv/Nutrients.csv')

    print("Importing goal-nutrient relationships...")
    importer.import_goal_nutrients('../data/csv/GoalNutrients.csv')

    print("Importing nutrient-ingredient relationships...")
    importer.import_nutrient_ingredients('../data/csv/NutrientIngredients.csv')

    # Close connection
    importer.close()
    print("Data import completed!")

if __name__ == "__main__":
    main()