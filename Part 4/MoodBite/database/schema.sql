-- SQLite schema for MoodBite application

-- Enable foreign key support
PRAGMA foreign_keys = ON;

-- MoodTags Table
CREATE TABLE IF NOT EXISTS MoodTags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT
);

-- Insert predefined mood tags
INSERT INTO MoodTags (name, description) VALUES 
    ('Reducing Anxiety', 'Foods that help reduce anxiety and stress'),
    ('Boosting Focus and Productivity', 'Foods that help with mental clarity and focus'),
    ('Boosting Energy Levels', 'Foods that provide sustained energy'),
    ('Improving Mood and Well-being', 'Foods that enhance mood and emotional well-being'),
    ('Promoting Relaxation and Sleep', 'Foods that promote calmness and relaxation'),
    ('Balanced', 'General mood-neutral foods suitable for everyday use');

-- Ingredients Table
CREATE TABLE IF NOT EXISTS Ingredients (
    ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Recipes Table
CREATE TABLE IF NOT EXISTS Recipes (
    recipe_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    recipe_link TEXT,
    ingredients TEXT, -- JSON stored as TEXT
    mood_tag_id INTEGER,
    image_link TEXT,
    summary TEXT,
    cuisines TEXT,
    dish_type TEXT, -- JSON stored as TEXT
    instruction_steps TEXT,
    spoonacular_score REAL,
    servings INTEGER,
    price_per_serving REAL,
    caloric_breakdown TEXT, -- JSON stored as TEXT
    mood_tag TEXT,
    DietLabels TEXT, -- JSON stored as TEXT
    FOREIGN KEY (mood_tag_id) REFERENCES MoodTags(id)
);

-- Users Table
CREATE TABLE IF NOT EXISTS Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

-- UserProfiles Table
CREATE TABLE IF NOT EXISTS UserProfiles (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    age INTEGER,
    gender TEXT CHECK (gender IN ('Male', 'Female', 'Other')),
    height INTEGER,
    weight INTEGER,
    activity_level TEXT CHECK (activity_level IN ('Minimal', 'Moderate', 'Very Active')),
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- Add these tables after the existing tables in schema.sql

-- EmotionalGoals Table
CREATE TABLE IF NOT EXISTS EmotionalGoals (
    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    emotional_goal TEXT NOT NULL
);

-- Nutrients Table
CREATE TABLE IF NOT EXISTS Nutrients (
    nutrient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    nutrient TEXT NOT NULL,
    recommended_amount TEXT
);

-- GoalNutrients Table
CREATE TABLE IF NOT EXISTS GoalNutrients (
    goal_id INTEGER NOT NULL,
    nutrient_id INTEGER NOT NULL,
    FOREIGN KEY (goal_id) REFERENCES EmotionalGoals(goal_id),
    FOREIGN KEY (nutrient_id) REFERENCES Nutrients(nutrient_id),
    PRIMARY KEY (goal_id, nutrient_id)
);

-- NutrientIngredients Table
CREATE TABLE IF NOT EXISTS NutrientIngredients (
    nutrient_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    FOREIGN KEY (nutrient_id) REFERENCES Nutrients(nutrient_id),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id),
    PRIMARY KEY (nutrient_id, ingredient_id)
);

-- MoodTracking Table
CREATE TABLE IF NOT EXISTS MoodTracking (
    mood_entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mood_tag_id INTEGER,
    energy_level INTEGER,
    stress_level INTEGER,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (mood_tag_id) REFERENCES MoodTags(id) ON DELETE CASCADE
);

-- DietaryPreferences Table
CREATE TABLE IF NOT EXISTS DietaryPreferences (
    preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    diet_type TEXT NOT NULL, -- JSON stored as TEXT
    restrictions TEXT, -- JSON stored as TEXT
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- MealPlans Table
CREATE TABLE IF NOT EXISTS MealPlans (
    meal_plan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    meal_type TEXT CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack')),
    recipe_id INTEGER NOT NULL,
    servings INTEGER DEFAULT 1,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE
);

-- RecipePreferences Table
CREATE TABLE IF NOT EXISTS RecipePreferences (
    preference_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    liked INTEGER NOT NULL CHECK (liked IN (0, 1)), -- Boolean as INTEGER
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE
);

-- RecipeRatings Table
CREATE TABLE IF NOT EXISTS RecipeRatings (
    rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    rating INTEGER CHECK (rating BETWEEN 1 AND 5),
    feedback TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
);

-- RecipeAnalytics Table
CREATE TABLE IF NOT EXISTS RecipeAnalytics (
    analytics_id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    views INTEGER DEFAULT 0,
    favorites INTEGER DEFAULT 0,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
);

-- UserFavorites Table
CREATE TABLE IF NOT EXISTS UserFavorites (
    favorite_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
);

-- ShoppingList Table
CREATE TABLE IF NOT EXISTS ShoppingList (
    shopping_list_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
);

-- Nutrition Table
CREATE TABLE IF NOT EXISTS Nutrition (
    recipe_id INTEGER PRIMARY KEY,
    calories REAL,
    fat REAL,
    protein REAL,
    cholesterol REAL,
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
    vitamin_kk REAL,
    selenium REAL,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE
);

-- HealthGoals Table
CREATE TABLE IF NOT EXISTS HealthGoals (
    goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    goal_type TEXT CHECK (goal_type IN ('weight_loss', 'muscle_gain', 'maintenance')),
    target_calories INTEGER,
    target_protein REAL,
    target_carbs REAL,
    target_fat REAL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- RecommendationAnalytics Table
CREATE TABLE IF NOT EXISTS RecommendationAnalytics (
    analytics_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    recipe_id INTEGER NOT NULL,
    viewed INTEGER DEFAULT 0 CHECK (viewed IN (0, 1)), -- Boolean as INTEGER
    liked INTEGER DEFAULT 0 CHECK (liked IN (0, 1)), -- Boolean as INTEGER
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE
);

-- NutritionTracking Table
CREATE TABLE IF NOT EXISTS NutritionTracking (
    tracking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date DATE NOT NULL,
    total_calories REAL,
    total_protein REAL,
    total_carbs REAL,
    total_fat REAL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);