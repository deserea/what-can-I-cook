import json
import math
import re
import streamlit as st

st.set_page_config(page_title="What Can I Cook?", page_icon="🍽️", layout="wide")

with open("recipes.json", "r", encoding="utf-8") as file:
    loaded_data = json.load(file)

if isinstance(loaded_data, dict) and "recipes" in loaded_data:
    recipes = loaded_data["recipes"]
else:
    recipes = loaded_data

ALIASES = {
    "tomatoes": "tomato",
    "cherry tomatoes": "tomato",
    "roma tomatoes": "tomato",
    "diced tomatoes": "canned tomato",
    "crushed tomatoes": "canned tomato",
    "canned tomatoes": "canned tomato",
    "tomato sauces": "tomato sauce",

    "onions": "onion",
    "yellow onions": "onion",
    "white onions": "onion",
    "red onions": "red onion",
    "green onions": "green onion",
    "scallions": "green onion",

    "garlic cloves": "garlic",
    "cloves garlic": "garlic",
    "minced garlic": "garlic",

    "ground beef": "beef",
    "beef mince": "beef",
    "minced beef": "beef",
    "ground turkey": "turkey",
    "ground chicken": "chicken",
    "ground pork": "pork",
    "ground sausage": "sausage",

    "chicken breast": "chicken",
    "chicken breasts": "chicken",
    "chicken thigh": "chicken",
    "chicken thighs": "chicken",
    "shredded chicken": "chicken",
    "rotisserie chicken": "chicken",

    "turkey breast": "turkey",
    "pork chops": "pork",
    "pork shoulder": "pork",
    "pork loin": "pork",

    "salmon fillet": "salmon",
    "salmon filet": "salmon",
    "frozen shrimp": "shrimp",
    "raw shrimp": "shrimp",
    "canned tuna": "tuna",
    "tuna fish": "tuna",

    "bell peppers": "bell pepper",
    "green pepper": "bell pepper",
    "red pepper": "bell pepper",
    "yellow pepper": "bell pepper",
    "orange pepper": "bell pepper",
    "peppers": "bell pepper",
    "jalapenos": "jalapeno",

    "potatoes": "potato",
    "russet potatoes": "potato",
    "yukon gold potatoes": "potato",
    "red potatoes": "potato",
    "sweet potatoes": "sweet potato",

    "eggs": "egg",

    "tortillas": "tortilla",
    "corn tortillas": "corn tortilla",
    "flour tortillas": "flour tortilla",
    "lettuce wraps": "lettuce wrap",
    "romaine leaves": "lettuce wrap",
    "butter lettuce": "lettuce wrap",

    "limes": "lime",
    "lemons": "lemon",

    "beans": "bean",
    "black beans": "black bean",
    "kidney beans": "kidney bean",
    "white beans": "white bean",
    "pinto beans": "pinto bean",
    "garbanzo beans": "chickpea",
    "chickpeas": "chickpea",
    "lentils": "lentil",

    "mushrooms": "mushroom",
    "zucchinis": "zucchini",
    "carrots": "carrot",
    "celery stalks": "celery",
    "avocados": "avocado",

    "strawberries": "strawberry",
    "blueberries": "blueberry",
    "raspberries": "raspberry",
    "berries": "berry",
    "grapes": "grape",

    "oats": "oat",
    "spaghetti": "pasta",
    "penne": "pasta",
    "rigatoni": "pasta",
    "linguine": "pasta",
    "fettuccine": "pasta",
    "macaroni": "pasta",
    "noodles": "noodle",
    "ramen noodles": "ramen",

    "brown rice": "rice",
    "white rice": "rice",
    "jasmine rice": "rice",
    "basmati rice": "rice",
    "wild rice": "rice",

    "mozzarella cheese": "mozzarella",
    "cheddar cheese": "cheddar",
    "parmesan cheese": "parmesan",
    "feta cheese": "feta",
    "monterey jack cheese": "monterey jack",
    "pepper jack cheese": "pepper jack",
    "colby jack cheese": "colby jack",
    "cotija cheese": "cotija",
    "queso fresco cheese": "queso fresco",
    "american cheese": "american cheese",
    "swiss cheese": "swiss",
    "provolone cheese": "provolone",
    "shredded cheese": "cheese",
    "mexican blend cheese": "cheese",
    "italian blend cheese": "cheese",

    "vegetable oil": "oil",
    "canola oil": "oil",
    "avocado oil": "oil",

    "soy": "soy sauce",
    "tamari": "soy sauce",
    "bbq sauce": "barbecue sauce",
    "buffalo sauce": "hot sauce",

    "chicken broth": "broth",
    "beef broth": "broth",
    "vegetable broth": "broth",
    "stock": "broth",
    "chicken stock": "broth",
    "beef stock": "broth",
    "vegetable stock": "broth",

    "spring mix": "lettuce",
    "mixed greens": "greens",
    "romaine lettuce": "romaine",
    "iceberg lettuce": "lettuce",
    "baby spinach": "spinach",
    "fresh spinach": "spinach",

    "cilantro leaves": "cilantro",
    "flat leaf parsley": "parsley",
    "curly parsley": "parsley",

    "green peas": "peas",
    "frozen peas": "peas",

    "plain yogurt": "yogurt",
    "greek yogurt": "yogurt",
    "half and half": "cream",
    "heavy cream": "cream",

    "all purpose flour": "flour",
    "ap flour": "flour",

    "chili powder": "chili flakes"
}

INGREDIENT_GROUPS = {
    "Proteins": [
        "chicken", "beef", "pork", "turkey", "sausage", "bacon", "ham",
        "egg", "tofu", "salmon", "shrimp", "tuna", "cod", "tilapia"
    ],
    "Vegetables": [
        "onion", "red onion", "green onion", "garlic", "bell pepper", "jalapeno",
        "carrot", "celery", "spinach", "kale", "lettuce", "romaine", "greens",
        "cabbage", "broccoli", "cauliflower", "zucchini", "cucumber", "tomato",
        "potato", "sweet potato", "corn", "peas", "green bean", "asparagus",
        "mushroom", "squash", "avocado"
    ],
    "Fruits": [
        "apple", "banana", "orange", "lemon", "lime", "strawberry",
        "blueberry", "raspberry", "berry", "grape", "pineapple", "peach", "pear"
    ],
    "Grains & Starches": [
        "rice", "pasta", "bread", "corn tortilla", "flour tortilla", "lettuce wrap",
        "potato", "sweet potato", "oat", "quinoa", "orzo", "noodle", "ramen"
    ],
    "Dairy & Cheese": [
        "milk", "butter", "egg", "yogurt", "sour cream", "cream cheese", "cream",
        "cheddar", "mozzarella", "parmesan", "feta", "monterey jack", "pepper jack",
        "colby jack", "swiss", "provolone", "queso fresco", "cotija",
        "american cheese", "cheese"
    ],
    "Oils & Fats": [
        "olive oil", "oil", "butter", "sesame oil"
    ],
    "Legumes & Beans": [
        "bean", "black bean", "kidney bean", "white bean", "pinto bean",
        "chickpea", "lentil"
    ],
    "Dry Goods & Canned": [
        "broth", "tomato sauce", "canned tomato", "tomato paste", "breadcrumbs",
        "flour", "cornstarch", "sugar", "brown sugar", "coconut milk", "tuna"
    ],
    "Sauces & Condiments": [
        "soy sauce", "vinegar", "hot sauce", "mustard", "mayonnaise",
        "ketchup", "barbecue sauce", "ranch", "salsa", "teriyaki sauce",
        "worcestershire", "honey", "maple syrup"
    ],
    "Herbs": [
        "cilantro", "parsley", "basil", "dill", "thyme", "rosemary",
        "oregano", "sage", "mint", "green onion"
    ],
    "Spices & Seasonings": [
        "salt", "pepper", "black pepper", "garlic powder", "onion powder",
        "paprika", "smoked paprika", "cumin", "coriander", "turmeric",
        "cinnamon", "cayenne", "red pepper flakes", "chili flakes",
        "italian seasoning", "bay leaf"
    ]
}

WRAP_OPTIONS = {"corn tortilla", "flour tortilla", "lettuce wrap"}
CHEESE_OPTIONS = {
    "cheese", "cheddar", "mozzarella", "parmesan", "feta", "monterey jack",
    "pepper jack", "colby jack", "swiss", "provolone", "queso fresco",
    "cotija", "american cheese"
}
MELTING_CHEESE_OPTIONS = {
    "cheese", "cheddar", "mozzarella", "monterey jack", "pepper jack",
    "colby jack", "provolone", "american cheese"
}
ITALIAN_CHEESE_OPTIONS = {"parmesan", "pecorino", "asiago", "romano", "mozzarella"}
GREEK_CHEESE_OPTIONS = {"feta"}
MEXICAN_CHEESE_OPTIONS = {"cheddar", "monterey jack", "cotija", "queso fresco", "pepper jack", "colby jack", "cheese"}

TIME_OPTIONS = {
    "Any": None,
    "Quick (under 30 min)": 30,
    "Around 1 hour": 60,
    "2 hours or less": 120,
   