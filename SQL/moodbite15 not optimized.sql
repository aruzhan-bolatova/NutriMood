-- Create Database
CREATE DATABASE moodbite15;
USE moodbite15;

-- Ingredients Table
CREATE TABLE Ingredients (
    ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL -- Ingredient name
);

-- MoodTags Table
CREATE TABLE MoodTags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL, -- Mood tag name (e.g., "Reducing Anxiety", "Boosting Focus")
    description TEXT -- Optional: Description of the mood goal
);

-- Insert predefined mood tags
INSERT INTO MoodTags (name, description) VALUES 
('Reducing Anxiety', 'Foods that help reduce anxiety and stress'),
('Boosting Focus and Productivity', 'Foods that help with mental clarity and focus'),
('Boosting Energy Levels', 'Foods that provide sustained energy'),
('Improving Mood and Well-being', 'Foods that enhance mood and emotional well-being'),
('Promoting Relaxation and Sleep', 'Foods that promote calmness and relaxation'),
('Balanced', 'General mood-neutral foods suitable for everyday use');

-- Recipes Table
CREATE TABLE Recipes (
    recipe_id INT PRIMARY KEY, -- Unique ID for each recipe (no AUTO_INCREMENT)
    name VARCHAR(255) NOT NULL, -- Recipe name
    recipe_link VARCHAR(255), -- Optional: URL for the recipe
    ingredients JSON, -- JSON list of ingredients with quantities
    mood_tag_id INT, -- Reference to MoodTags table
    image_link VARCHAR(255), -- Link to recipe image
    summary TEXT, -- Summary of the recipe
    cuisines VARCHAR(255), -- Cuisines (e.g., Italian, Southern)
    dish_type JSON, -- JSON list of dish types (e.g., lunch, breakfast)
    instruction_steps TEXT, -- Steps for cooking the recipe
    spoonacular_score FLOAT, -- Recipe score
    servings INT, -- Number of servings
    price_per_serving FLOAT, -- Price per serving
    caloric_breakdown JSON, -- Caloric breakdown (percent protein, fat, carbs)
    mood_tag VARCHAR(255), -- MoodTag directly from dataset
    DietLabels JSON, -- JSON field for diet labels (vegetarian, vegan, etc.)
    FOREIGN KEY (mood_tag_id) REFERENCES MoodTags(id) -- Link to MoodTags table
);

-- Users Table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL -- Storing plaintext password
);

-- UserProfiles Table
CREATE TABLE UserProfiles (
    profile_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Links to Users table
    age INT, -- User's age
    gender ENUM('Male', 'Female', 'Other'), -- Gender options
    height INT, -- Height in cm
    weight INT, -- Weight in kg
    activity_level ENUM('Minimal', 'Moderate', 'Very Active'), -- Physical activity level
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- MoodTracking Table
CREATE TABLE MoodTracking (
    mood_entry_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Links to Users table
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Automatically set the timestamp
    mood_tag_id INT, -- Links to MoodTags table
    energy_level INT, -- Energy level (1-10 scale)
    stress_level INT, -- Stress level (1-10 scale)
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (mood_tag_id) REFERENCES MoodTags(id) ON DELETE CASCADE
);

-- DietaryPreferences Table
CREATE TABLE DietaryPreferences (
    preference_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Links to Users table
    diet_type JSON NOT NULL, -- JSON for dietary preferences (e.g., vegetarian, vegan)
    restrictions JSON, -- JSON for allergies or specific restrictions
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);


-- MealPlans Table
CREATE TABLE MealPlans (
    meal_plan_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Links to Users table
    meal_type ENUM('breakfast', 'lunch', 'dinner', 'snack'), -- Meal type
    recipe_id INT NOT NULL, -- Links to Recipes table
    servings INT DEFAULT 1, -- Number of servings
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE
);

-- RecipePreferences Table
CREATE TABLE RecipePreferences (
    preference_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Links to Users table
    recipe_id INT NOT NULL, -- Links to Recipes table
    liked BOOLEAN NOT NULL, -- TRUE for like, FALSE for dislike
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Record when the action occurred
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE
);

-- RecipeRatings Table
CREATE TABLE RecipeRatings (
    rating_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Links to Users table
    recipe_id INT NOT NULL, -- Links to Recipes table
    rating INT CHECK (rating BETWEEN 1 AND 5), -- Rating out of 5
    feedback TEXT, -- Optional user feedback
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
);

-- RecipeAnalytics Table
CREATE TABLE RecipeAnalytics (
    analytics_id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT NOT NULL, -- Links to Recipes table
    views INT DEFAULT 0, -- Number of views
    favorites INT DEFAULT 0, -- Number of times favorited
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
);

-- UserFavorites Table
CREATE TABLE UserFavorites (
    favorite_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Links to Users table
    recipe_id INT NOT NULL, -- Links to Recipes table
    added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When the recipe was favorited
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
);

-- ShoppingList Table
CREATE TABLE ShoppingList (
    shopping_list_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Links to Users table
    ingredient_id INT NOT NULL, -- Links to Ingredients table
    quantity VARCHAR(255) NOT NULL, -- Quantity needed
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
);

-- Nutrition Table
CREATE TABLE Nutrition (
    recipe_id INT PRIMARY KEY, -- Links to Recipes table
    calories FLOAT,
    fat FLOAT,
    protein FLOAT,
    carbs FLOAT,
    fiber FLOAT,
    sugar FLOAT,
    sodium FLOAT,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE
);

-- HealthGoals Table
CREATE TABLE HealthGoals (
    goal_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Links to Users table
    goal_type ENUM('weight_loss', 'muscle_gain', 'maintenance'), -- Type of goal
    target_calories INT, -- Daily calorie target
    target_protein FLOAT, -- Protein target (in grams)
    target_carbs FLOAT, -- Carbs target (in grams)
    target_fat FLOAT, -- Fat target (in grams)
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- RecommendationAnalytics Table
CREATE TABLE RecommendationAnalytics (
    analytics_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    recipe_id INT NOT NULL,
    viewed BOOLEAN DEFAULT FALSE, -- Whether the user viewed the recommendation
    liked BOOLEAN DEFAULT FALSE, -- Whether the user liked it
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id) ON DELETE CASCADE
);

-- NutritionTracking Table
CREATE TABLE NutritionTracking (
    tracking_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    date DATE NOT NULL, -- Date of tracking
    total_calories FLOAT, -- Total calories consumed
    total_protein FLOAT, -- Total protein consumed
    total_carbs FLOAT, -- Total carbs consumed
    total_fat FLOAT, -- Total fat consumed
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

ALTER TABLE Recipes
ADD COLUMN DietLabels JSON AFTER caloric_breakdown;
DESCRIBE Recipes;

