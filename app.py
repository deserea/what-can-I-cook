import json
import re
import streamlit as st

st.set_page_config(page_title="What Can I Cook?", page_icon="🍽️", layout="wide")

with open("recipes.json", "r", encoding="utf-8") as file:
    loaded = json.load(file)

recipes = loaded["recipes"] if isinstance(loaded, dict) and "recipes" in loaded else loaded

ALIASES = {
    "tomatoes": "tomato",
    "cherry tomatoes": "tomato",
    "roma tomatoes": "tomato",
    "diced tomatoes": "canned tomato",
    "crushed tomatoes": "canned tomato",
    "canned tomatoes": "canned tomato",
    "tomato sauces": "tomato sauce",
    "marinara": "tomato sauce",
    "jarred sauce": "tomato sauce",

    "onions": "onion",
    "yellow onions": "onion",
    "white onions": "onion",
    "red onions": "red onion",
    "green onions": "green onion",
    "scallions": "green onion",

    "garlic cloves": "garlic",
    "minced garlic": "garlic",

    "ground beef": "beef",
    "beef mince": "beef",
    "minced beef": "beef",
    "ground turkey": "turkey",
    "ground chicken": "chicken",
    "ground pork": "pork",

    "chicken breast": "chicken",
    "chicken breasts": "chicken",
    "chicken thigh": "chicken",
    "chicken thighs": "chicken",
    "shredded chicken": "chicken",
    "rotisserie chicken": "chicken",

    "italian sausage": "sausage",
    "hot italian sausage": "sausage",
    "mild italian sausage": "sausage",
    "breakfast sausage": "sausage",

    "salmon fillet": "salmon",
    "salmon filet": "salmon",
    "raw shrimp": "shrimp",
    "frozen shrimp": "shrimp",
    "canned tuna": "tuna",

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

    "oats": "oat",
    "spaghetti": "pasta",
    "penne": "pasta",
    "rigatoni": "pasta",
    "fettuccine": "pasta",
    "linguine": "pasta",
    "macaroni": "pasta",
    "noodles": "noodle",

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
    "ranch": "ranch dressing",
    "ranch dressing": "ranch dressing",

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
    "bagged salad": "lettuce",
    "salad mix": "lettuce",

    "cilantro leaves": "cilantro",
    "flat leaf parsley": "parsley",
    "curly parsley": "parsley",

    "green peas": "peas",
    "frozen peas": "peas",
    "frozen vegetables": "vegetable",
    "mixed vegetables": "vegetable",

    "plain yogurt": "yogurt",
    "greek yogurt": "yogurt",

    "all purpose flour": "flour",
    "ap flour": "flour",

    "chili powder": "chili flakes",
    "taco seasoning": "cumin"
}

INGREDIENT_GROUPS = {
    "Proteins": [
        "chicken", "beef", "pork", "turkey", "sausage", "egg",
        "salmon", "shrimp", "tuna", "tofu"
    ],
    "Vegetables": [
        "onion", "red onion", "green onion", "garlic", "bell pepper", "jalapeno",
        "carrot", "celery", "spinach", "greens", "lettuce", "romaine", "broccoli",
        "cucumber", "tomato", "potato", "sweet potato", "corn", "peas",
        "mushroom", "zucchini", "squash", "avocado"
    ],
    "Fruits": [
        "apple", "banana", "lemon", "lime", "berry", "strawberry", "blueberry"
    ],
    "Grains & Starches": [
        "rice", "pasta", "bread", "corn tortilla", "flour tortilla",
        "lettuce wrap", "potato", "sweet potato", "oat", "quinoa", "noodle"
    ],
    "Dairy & Cheese": [
        "milk", "butter", "yogurt", "sour cream", "cream", "cheddar", "mozzarella",
        "parmesan", "feta", "monterey jack", "pepper jack", "colby jack",
        "swiss", "provolone", "cotija", "queso fresco", "american cheese", "cheese"
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
        "flour", "cornstarch", "sugar", "brown sugar"
    ],
    "Sauces & Condiments": [
        "soy sauce", "vinegar", "hot sauce", "mustard", "mayonnaise",
        "ketchup", "barbecue sauce", "salsa", "honey", "ranch dressing"
    ],
    "Herbs": [
        "cilantro", "parsley", "basil", "dill", "thyme", "rosemary",
        "oregano", "sage", "green onion"
    ],
    "Spices & Seasonings": [
        "salt", "pepper", "black pepper", "garlic powder", "onion powder",
        "paprika", "smoked paprika", "cumin", "coriander", "turmeric",
        "cinnamon", "red pepper flakes", "chili flakes", "italian seasoning", "bay leaf"
    ]
}

WRAP_OPTIONS = {"corn tortilla", "flour tortilla", "lettuce wrap"}
CHEESE_OPTIONS = {
    "cheese", "cheddar", "mozzarella", "parmesan", "feta", "monterey jack",
    "pepper jack", "colby jack", "swiss", "provolone", "cotija",
    "queso fresco", "american cheese"
}
MELTING_CHEESE_OPTIONS = {
    "cheese", "cheddar", "mozzarella", "monterey jack", "pepper jack",
    "colby jack", "provolone", "american cheese"
}
ITALIAN_CHEESE_OPTIONS = {"parmesan", "pecorino", "asiago", "romano", "mozzarella"}
GREEK_CHEESE_OPTIONS = {"feta"}
MEXICAN_CHEESE_OPTIONS = {"cheddar", "monterey jack", "cotija", "queso fresco", "pepper jack", "colby jack", "cheese"}

TIME_FILTERS = {
    "Any": None,
    "Quick meals": 30,
    "1 hour or less": 60,
    "2 hours or less": 120,
    "More advanced / longer cook": 9999
}

def singularize(word):
    word = word.strip().lower()
    if word.endswith("ies") and len(word) > 3:
        return word[:-3] + "y"
    if word.endswith("oes") and len(word) > 3:
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        return word[:-1]
    return word

def normalize_ingredient(text):
    text = str(text).strip().lower()
    text = re.sub(r"[^a-zA-Z0-9\s-]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    if text in ALIASES:
        return ALIASES[text]

    text = singularize(text)

    if text in ALIASES:
        return ALIASES[text]

    return text

def ingredient_matches(user_item, recipe_item):
    user_item = normalize_ingredient(user_item)
    recipe_item = normalize_ingredient(recipe_item)

    if user_item == recipe_item:
        return True

    if recipe_item in {"wrap", "mexican wrap"} and user_item in WRAP_OPTIONS:
        return True

    if recipe_item == "cheese" and user_item in CHEESE_OPTIONS:
        return True

    if recipe_item == "melting cheese" and user_item in MELTING_CHEESE_OPTIONS:
        return True

    if recipe_item == "italian cheese" and user_item in ITALIAN_CHEESE_OPTIONS:
        return True

    if recipe_item == "greek cheese" and user_item in GREEK_CHEESE_OPTIONS:
        return True

    if recipe_item == "mexican cheese" and user_item in MEXICAN_CHEESE_OPTIONS:
        return True

    return user_item in recipe_item or recipe_item in user_item

def entry_matches(entry, user_ingredients):
    if isinstance(entry, str):
        return any(ingredient_matches(user_item, entry) for user_item in user_ingredients)

    if isinstance(entry, dict):
        options = entry.get("options", [])
        return any(
            any(ingredient_matches(user_item, option) for user_item in user_ingredients)
            for option in options
        )

    return False

def matched_label(entry, user_ingredients):
    if isinstance(entry, str):
        return normalize_ingredient(entry)

    if isinstance(entry, dict):
        for option in entry
    