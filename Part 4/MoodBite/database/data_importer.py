import pandas as pd
import sqlite3
import json
from datetime import datetime

class DataImporter:
    def __init__(self, db_path):
        """Initialize database connection"""
        self.conn = sqlite3.connect(db_path)
        
    def import_recipes(self, csv_path):
        """Import recipes from CSV file"""
        try:
            # Read CSV file
            df = pd.read_csv(csv_path)
            cursor = self.conn.cursor()
            
            # Convert specific columns to JSON strings
            json_columns = ['ingredients', 'dish_type', 'caloric_breakdown', 'DietLabels']
            for col in json_columns:
                if col in df.columns:
                    df[col] = df[col].apply(lambda x: json.dumps(eval(x)) if pd.notna(x) else None)
            
            # Insert data row by row
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT OR REPLACE INTO Recipes (
                        recipe_id, name, recipe_link, ingredients, mood_tag_id,
                        image_link, summary, cuisines, dish_type, instruction_steps,
                        spoonacular_score, servings, price_per_serving,
                        caloric_breakdown, mood_tag, DietLabels
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row.get('recipe_id'),
                    row.get('name'),
                    row.get('recipe_link'),
                    row.get('ingredients'),
                    row.get('mood_tag_id'),
                    row.get('image_link'),
                    row.get('summary'),
                    row.get('cuisines'),
                    row.get('dish_type'),
                    row.get('instruction_steps'),
                    row.get('spoonacular_score'),
                    row.get('servings'),
                    row.get('price_per_serving'),
                    row.get('caloric_breakdown'),
                    row.get('mood_tag'),
                    row.get('DietLabels')
                ))
            
            self.conn.commit()
            print(f"Successfully imported {len(df)} recipes")
            return True
            
        except Exception as e:
            print(f"Error importing recipes: {e}")
            self.conn.rollback()
            return False

    def import_ingredients(self, csv_path):
        """Import ingredients from CSV file"""
        try:
            df = pd.read_csv(csv_path)
            cursor = self.conn.cursor()
            
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT OR REPLACE INTO Ingredients (name)
                    VALUES (?)
                """, (row['ingredient'],))
            
            self.conn.commit()
            print(f"Successfully imported {len(df)} ingredients")
            return True
            
        except Exception as e:
            print(f"Error importing ingredients: {e}")
            self.conn.rollback()
            return False

    def import_nutrition(self, csv_path):
        """
        Import nutrition data from a CSV file into the Nutrition table.
        """
        try:
            # Read the CSV file into a pandas DataFrame
            df = pd.read_csv(csv_path)
            cursor = self.conn.cursor()
            
            # Loop through the DataFrame rows and insert them into the Nutrition table
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT OR REPLACE INTO Nutrition (
                        recipe_id, calories, fat, protein, carbs,
                        fiber, sugar, sodium, caffein, magnesium, calcium, copper,
                        zinc, iron, vitamin_a, vitamin_b_one, vitamin_b_two, vitamin_b_three, vitamin_b_five, vitamin_b_six, vitamin_b_twelve, vitamin_c, vitamin_d,
                        vitamin_e, vitamin_k, selenium
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row['Recipe ID'],         # Ensure CSV column names match
                    row.get('Calories', None),
                    row.get('Fat', None),
                    row.get('Protein', None),
                    row.get('Carbohydrates', None),
                    row.get('Fiber', None),
                    row.get('Sugar', None),
                    row.get('Sodium', None),
                    row.get('Caffein', None),
                    row.get('Magnesium', None),
                    row.get('Calcium', None),
                    row.get('Copper', None),
                    row.get('Zinc', None),
                    row.get('Iron', None),
                    row.get('Vitamin A', None),
                    row.get('Vitamin B1', None),
                    row.get('Vitamin B2', None),
                    row.get('Vitamin B3', None),
                    row.get('Vitamin B5', None),
                    row.get('Vitamin B6', None),
                    row.get('Vitamin B12', None),
                    row.get('Vitamin C', None),
                    row.get('Vitamin D', None),
                    row.get('Vitamin E', None),
                    row.get('Vitamin K', None),
                    row.get('Selenium', None)
                ))
            
            # Commit changes
            self.conn.commit()
            print(f"Successfully imported {len(df)} nutrition records")
            return True

        except Exception as e:
            print(f"Error importing nutrition data: {e}")
            self.conn.rollback()
            return False

    def import_generic(self, table_name, csv_path, mapping=None):
        """
        Import data into any table using column mapping
        mapping: dict of CSV column names to database column names
        """
        try:
            df = pd.read_csv(csv_path)
            
            # Apply column mapping if provided
            if mapping:
                df = df.rename(columns=mapping)
            
            # Get column names from DataFrame
            columns = df.columns.tolist()
            placeholders = ','.join(['?' for _ in columns])
            
            cursor = self.conn.cursor()
            for _, row in df.iterrows():
                query = f"""
                    INSERT OR REPLACE INTO {table_name}
                    ({','.join(columns)})
                    VALUES ({placeholders})
                """
                cursor.execute(query, tuple(row))
            
            self.conn.commit()
            print(f"Successfully imported {len(df)} records into {table_name}")
            return True
            
        except Exception as e:
            print(f"Error importing data into {table_name}: {e}")
            self.conn.rollback()
            return False
        
    def import_emotional_goals(self, csv_path):
        """Import emotional goals from CSV file"""
        try:
            df = pd.read_csv(csv_path)
            cursor = self.conn.cursor()
            
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT OR REPLACE INTO EmotionalGoals (emotional_goal)
                    VALUES (?)
                """, (row['emotional_goal'],))
            
            self.conn.commit()
            print(f"Successfully imported {len(df)} emotional goals")
            return True
            
        except Exception as e:
            print(f"Error importing emotional goals: {e}")
            self.conn.rollback()
            return False

    def import_nutrients(self, csv_path):
        """Import nutrients from CSV file"""
        try:
            df = pd.read_csv(csv_path)
            cursor = self.conn.cursor()
            
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT OR REPLACE INTO Nutrients (nutrient, recommended_amount)
                    VALUES (?, ?)
                """, (row['nutrient'], row.get('recommended_amount')))
            
            self.conn.commit()
            print(f"Successfully imported {len(df)} nutrients")
            return True
            
        except Exception as e:
            print(f"Error importing nutrients: {e}")
            self.conn.rollback()
            return False

    def import_goal_nutrients(self, csv_path):
        """Import goal-nutrient relationships from CSV file"""
        try:
            df = pd.read_csv(csv_path)
            cursor = self.conn.cursor()
            
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT OR REPLACE INTO GoalNutrients (goal_id, nutrient_id)
                    VALUES (?, ?)
                """, (row['goal_id'], row['nutrient_id']))
            
            self.conn.commit()
            print(f"Successfully imported {len(df)} goal-nutrient relationships")
            return True
            
        except Exception as e:
            print(f"Error importing goal-nutrient relationships: {e}")
            self.conn.rollback()
            return False

    def import_nutrient_ingredients(self, csv_path):
        """Import nutrient-ingredient relationships from CSV file"""
        try:
            df = pd.read_csv(csv_path)
            cursor = self.conn.cursor()
            
            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT OR REPLACE INTO NutrientIngredients (nutrient_id, ingredient_id)
                    VALUES (?, ?)
                """, (row['nutrient_id'], row['ingredient_id']))
            
            self.conn.commit()
            print(f"Successfully imported {len(df)} nutrient-ingredient relationships")
            return True
            
        except Exception as e:
            print(f"Error importing nutrient-ingredient relationships: {e}")
            self.conn.rollback()
            return False

    def close(self):
        """Close the database connection"""
        self.conn.close()