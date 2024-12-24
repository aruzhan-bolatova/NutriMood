-- Create Database
CREATE DATABASE moodbite1520_test;
USE moodbite1520_test;

-- Ingredients Table
CREATE TABLE Ingredients (
    ingredient_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL -- Ingredient name
);

CREATE INDEX idx_name ON Ingredients(name);

-- MoodTags Table
CREATE TABLE MoodTags (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL, -- Mood tag name (e.g., "Reducing Anxiety", "Boosting Focus")
    description TEXT -- Optional: Description of the mood goal
);

CREATE INDEX idx_moodtag_name ON MoodTags(name);

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

-- Add generated columns for DietLabels JSON
ALTER TABLE Recipes
ADD COLUMN vegetarian BOOLEAN GENERATED ALWAYS AS (JSON_EXTRACT(DietLabels, '$.vegetarian')) STORED,
ADD COLUMN vegan BOOLEAN GENERATED ALWAYS AS (JSON_EXTRACT(DietLabels, '$.vegan')) STORED,
ADD COLUMN gluten_free BOOLEAN GENERATED ALWAYS AS (JSON_EXTRACT(DietLabels, '$.glutenFree')) STORED;

CREATE INDEX idx_vegetarian ON Recipes(vegetarian);
CREATE INDEX idx_vegan ON Recipes(vegan);
CREATE INDEX idx_gluten_free ON Recipes(gluten_free);
CREATE INDEX idx_mood_tag_id ON Recipes(mood_tag_id);
CREATE INDEX idx_cuisines ON Recipes(cuisines);

-- Users Table
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL -- Storing plaintext password
);

CREATE UNIQUE INDEX idx_username ON Users(username);
CREATE UNIQUE INDEX idx_email ON Users(email);

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

CREATE INDEX idx_user_id ON UserProfiles(user_id);

-- MoodTracking Table
CREATE TABLE MoodTracking (
    mood_entry_id INT AUTO_INCREMENT PRIMARY KEY, -- Auto-incremented primary key
    user_id INT NOT NULL, -- Links to Users table
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- Automatically set the timestamp
    mood_tag_id INT NOT NULL, -- Links to MoodTags table
    energy_level INT, -- Energy level (1-10 scale)
    stress_level INT, -- Stress level (1-10 scale)
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (mood_tag_id) REFERENCES MoodTags(id) ON DELETE CASCADE
);

-- Add indexes for improved query performance
CREATE INDEX idx_user_id_mood ON MoodTracking(user_id);
CREATE INDEX idx_mood_tag_id ON MoodTracking(mood_tag_id);

-- DietaryPreferences Table
CREATE TABLE DietaryPreferences (
    preference_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Links to Users table
    diet_type JSON NOT NULL, -- JSON for dietary preferences (e.g., vegetarian, vegan)
    restrictions JSON, -- JSON for allergies or specific restrictions
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

CREATE INDEX idx_user_id_preferences ON DietaryPreferences(user_id);

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

CREATE INDEX idx_user_id_meal ON MealPlans(user_id);
CREATE INDEX idx_recipe_id_meal ON MealPlans(recipe_id);

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

CREATE INDEX idx_user_id_recipe ON RecipePreferences(user_id);
CREATE INDEX idx_recipe_id_preferences ON RecipePreferences(recipe_id);

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

CREATE INDEX idx_user_id_rating ON RecipeRatings(user_id);
CREATE INDEX idx_recipe_id_rating ON RecipeRatings(recipe_id);

-- RecipeAnalytics Table
CREATE TABLE RecipeAnalytics (
    analytics_id INT AUTO_INCREMENT PRIMARY KEY,
    recipe_id INT NOT NULL, -- Links to Recipes table
    views INT DEFAULT 0, -- Number of views
    favorites INT DEFAULT 0, -- Number of times favorited
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
);

CREATE INDEX idx_recipe_id_analytics ON RecipeAnalytics(recipe_id);

-- UserFavorites Table
CREATE TABLE UserFavorites (
    favorite_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Links to Users table
    recipe_id INT NOT NULL, -- Links to Recipes table
    added_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP, -- When the recipe was favorited
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
);

CREATE INDEX idx_user_id_favorites ON UserFavorites(user_id);
CREATE INDEX idx_recipe_id_favorites ON UserFavorites(recipe_id);

-- ShoppingList Table
CREATE TABLE ShoppingList (
    shopping_list_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL, -- Links to Users table
    ingredient_id INT NOT NULL, -- Links to Ingredients table
    quantity VARCHAR(255) NOT NULL, -- Quantity needed
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
);

CREATE INDEX idx_user_id_shopping ON ShoppingList(user_id);
CREATE INDEX idx_ingredient_id_shopping ON ShoppingList(ingredient_id);

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

CREATE INDEX idx_user_id_health ON HealthGoals(user_id);

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

CREATE INDEX idx_user_id_recommendation ON RecommendationAnalytics(user_id);
CREATE INDEX idx_recipe_id_recommendation ON RecommendationAnalytics(recipe_id);

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

CREATE INDEX idx_user_id_tracking ON NutritionTracking(user_id);
CREATE INDEX idx_date_tracking ON NutritionTracking(date);


SELECT * FROM Recipes;
SELECT * FROM Ingredients;
select * FRom Nutrition;
Select * from MoodTags;
Select * from users;

-- Disable foreign key checks to prevent constraint issues during deletion
SET FOREIGN_KEY_CHECKS = 0;
SET SQL_SAFE_UPDATES = 0;

-- Delete data from dependent tables first
DELETE FROM UserProfiles;
DELETE FROM DietaryPreferences;

-- Then delete from the parent table
DELETE FROM Users;

-- Re-enable foreign key checks
SET SQL_SAFE_UPDATES = 1;
Select * from users;

Select * from UserProfiles;

Select * from DietaryPreferences;
Select * from  RecipePreferences;
Select * from  RecommendationAnalytics;
Select * from RecipeAnalytics;
Select * from RecipeRatings;
 Select * from  UserFavorites










