import sqlite3
import json
from datetime import datetime
import os

class MoodBiteDB:
    def __init__(self, db_file):
        """Initialize database connection"""
        self.db_file = db_file
        self.conn = None
        
    def connect(self):
        """Create a database connection"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
            
            self.conn = sqlite3.connect(self.db_file)
            self.conn.row_factory = sqlite3.Row  # This enables column access by name
            print(f"Connected to database: {self.db_file}")
            
            # Enable foreign key support
            self.conn.execute("PRAGMA foreign_keys = ON")
            return True
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")
            return False

    def init_db(self):
        """Initialize the database with schema"""
        try:
            with open('schema.sql', 'r') as sql_file:
                self.conn.executescript(sql_file.read())
            self.conn.commit()
            print("Database initialized successfully")
            return True
        except sqlite3.Error as e:
            print(f"Error initializing database: {e}")
            return False

    def create_user(self, username, email, password):
        """Create a new user"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Users (username, email, password)
                VALUES (?, ?, ?)
            """, (username, email, password))
            self.conn.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error creating user: {e}")
            return None

    def create_tables(self):
        """
        Create the Nutrition and Recipes tables if they don't already exist.
        """
        try:
            cursor = self.conn.cursor()
            # Create the Recipes table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Recipes (
                    recipe_id INTEGER PRIMARY KEY,
                    recipe_name TEXT NOT NULL,
                    description TEXT,
                    instructions TEXT
                );
            """)
            
            # Create the Nutrition table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Nutrition (
                    recipe_id INTEGER PRIMARY KEY,
                    calories REAL,
                    fat REAL,
                    protein REAL,
                    carbs REAL,
                    fiber REAL,
                    sugar REAL,
                    sodium REAL,
                    caffein REAL,
                    magnesium REAL,
                    calcium REAL,
                    copper REAL,
                    zinc REAL,
                    iron REAL,
                    vitamin_a REAL, 
                    vitamin_b_one REAL,
                    vitamin_b_two REAL,
                    vitamin_b_three REAL,
                    vitamin_b_five REAL,
                    vitamin_b_six REAL,
                    vitamin_b_twelve REAL,
                    vitamin_c REAL,
                    vitamin_d REAL,
                    vitamin_e REAL,
                    vitamin_k REAL,
                    selenium REAL,
                    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE
                );
            """)
            
            self.conn.commit()
            print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")
            self.conn.rollback()


    def add_recipe(self, recipe_data):
        """Add a new recipe"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Recipes (
                    recipe_id, name, recipe_link, ingredients, mood_tag_id,
                    image_link, summary, cuisines, dish_type, instruction_steps,
                    spoonacular_score, servings, price_per_serving,
                    caloric_breakdown, mood_tag, DietLabels
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                recipe_data['recipe_id'],
                recipe_data['name'],
                recipe_data.get('recipe_link'),
                json.dumps(recipe_data.get('ingredients', {})),
                recipe_data.get('mood_tag_id'),
                recipe_data.get('image_link'),
                recipe_data.get('summary'),
                recipe_data.get('cuisines'),
                json.dumps(recipe_data.get('dish_type', [])),
                recipe_data.get('instruction_steps'),
                recipe_data.get('spoonacular_score'),
                recipe_data.get('servings'),
                recipe_data.get('price_per_serving'),
                json.dumps(recipe_data.get('caloric_breakdown', {})),
                recipe_data.get('mood_tag'),
                json.dumps(recipe_data.get('DietLabels', []))
            ))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding recipe: {e}")
            return False

    def get_recipes_by_mood(self, mood_tag_id):
        """Get recipes by mood tag"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT r.*, m.name as mood_name 
                FROM Recipes r
                JOIN MoodTags m ON r.mood_tag_id = m.id
                WHERE m.id = ?
            """, (mood_tag_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching recipes: {e}")
            return []

    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()