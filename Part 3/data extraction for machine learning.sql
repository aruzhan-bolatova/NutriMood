#Downloads data to create Machine learing model 

SELECT recipe_id, 
       COUNT(CASE WHEN liked = TRUE THEN 1 END) AS total_likes,
       COUNT(CASE WHEN liked = FALSE THEN 1 END) AS total_dislikes
FROM RecipePreferences
GROUP BY recipe_id;

SELECT recipe_id, 
       COUNT(CASE WHEN viewed = TRUE THEN 1 END) AS total_views,
       COUNT(CASE WHEN liked = TRUE THEN 1 END) AS total_recommendation_likes
FROM RecommendationAnalytics
GROUP BY recipe_id;

SELECT recipe_id, views, favorites, spoonacular_score 
FROM RecipeAnalytics;




SELECT ra.recipe_id, ra.views, ra.favorites, r.spoonacular_score
FROM RecipeAnalytics ra
JOIN Recipes r ON ra.recipe_id = r.recipe_id;



