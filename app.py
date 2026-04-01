import json
import re
from collections import defaultdict
import streamlit as st

st.set_page_config(page_title="What Can I Cook?", page_icon="🍽️", layout="wide")

# ====================== SMART STARTER FLOW ======================

st.title("🍽️ What Can I Cook?")
st.markdown("Let’s build your meal step-by-step.")

# Step 1 — Cuisine
st.subheader("1️⃣ What cuisine are you feeling?")
selected_cuisine = st.selectbox(
    "Choose cuisine",
    CUISINE_OPTIONS
)

# Step 2 — Skill Level
st.subheader("2️⃣ Your cooking level")
selected_skill = st.selectbox(
    "Choose skill level",
    ["Beginner", "Intermediate", "Advanced"]
)

# Step 3 — Time
st.subheader("3️⃣ How much time do you have?")
selected_time = st.selectbox(
    "Select time",
    list(TIME_FILTERS.keys())
)

# Step 4 — Meal Style
st.subheader("4️⃣ What type of meal?")
selected_meal_style = st.selectbox(
    "Meal style",
    MEAL_STYLE_OPTIONS
)

# Step 5 — Goal
st.subheader("5️⃣ Any goals?")
selected_meal_goal = st.selectbox(
    "Meal goal",
    MEAL_GOAL_OPTIONS
)

# Step 6 — Ingredients
st.subheader("6️⃣ What ingredients do you have?")
user_input = st.text_area(
    "Enter ingredients (one per line)",
    placeholder="chicken\nrice\ngarlic\nonion",
    height=150
)

# Process ingredients
user_ingredients = [line.strip() for line in user_input.split("\n") if line.strip()]

# ======================
# LOAD RECIPES
# ======================
with open("recipes.json", "r", encoding="utf-8") as file:
    loaded = json.load(file)

recipes = loaded["recipes"] if isinstance(loaded, dict) and "recipes" in loaded else loaded

# ======================
# OPTIONS
# ======================
CUISINE_OPTIONS = [
    "All",
    "American",
    "Southern",
    "BBQ",
    "Comfort Food",
    "Italian",
    "French",
    "Spanish",
    "German",
    "Eastern European / Russian",
    "Mediterranean",
    "Greek",
    "Mexican",
    "Tex-Mex",
    "New Mexican",
    "Caribbean",
    "Peruvian / Central & South American",
    "Chinese",
    "Japanese",
    "Thai",
    "Korean",
    "Indian",
    "Filipino",
    "Hawaiian",
    "Pacific Island",
    "Middle Eastern",
    "Ethiopian",
    "African",
    "Kosher",
    "Halal",
    "Native American"
]

MEAL_STYLE_OPTIONS = [
    "All",
    "Comfort Food",
    "Quick & Easy",
    "BBQ & Grilled",
    "One-Pot Meals",
    "Soups & Stews",
    "Salads & Bowls",
    "Sandwiches & Wraps",
    "Rice Dishes",
    "Pasta Dishes",
    "Seafood",
    "Street Food Style",
    "Breakfast/Brunch",
    "Dessert",
    "Snack / Appetizer",
    "Smoothies & Shakes",
    "Hors d'oeuvres"
]

MEAL_GOAL_OPTIONS = [
    "All",
    "Comfort Food",
    "Protein Packed",
    "Low Carb",
    "Keto",
    "GLP-1 Friendly"
]

ACCESS_LEVELS = [
    "Everyday Grocery",
    "Better Grocery / Specialty Section",
    "International Market / Specialty Shop",
    "Farmers Market / Butcher / Fishmonger"
]

TIME_FILTERS = {
    "Any": None,
    "Quick meals (< 30 min)": 30,
    "1 hour or less": 60,
    "2 hours or less": 120,
    "More advanced / longer cook": 9999
}

# ======================
# INGREDIENT NORMALIZATION / ALIASES
# ======================
ALIASES = {
    # tomatoes
    "tomatoes": "tomato",
    "cherry tomatoes": "tomato",
    "roma tomatoes": "tomato",
    "diced tomatoes": "canned tomato",
    "crushed tomatoes": "canned tomato",
    "canned tomatoes": "canned tomato",
    "tomato sauces": "tomato sauce",
    "marinara": "tomato sauce",
    "jarred sauce": "tomato sauce",
    "tomato paste cans": "tomato paste",

    # onions / aromatics
    "onions": "onion",
    "yellow onions": "onion",
    "white onions": "onion",
    "red onions": "red onion",
    "green onions": "green onion",
    "scallions": "green onion",
    "shallots": "shallot",
    "leeks": "leek",
    "garlic cloves": "garlic",
    "minced garlic": "garlic",

    # meats / proteins
    "ground beef": "beef",
    "beef mince": "beef",
    "minced beef": "beef",
    "ground turkey": "turkey",
    "ground chicken": "chicken",
    "ground pork": "pork",
    "ground venison": "venison",
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
    "bratwurst": "sausage",
    "turkey slices": "deli turkey",
    "deli turkey slices": "deli turkey",
    "ham slices": "deli ham",
    "deli ham slices": "deli ham",
    "roast beef slices": "roast beef",
    "pepperoni slices": "pepperoni",
    "salami slices": "salami",
    "prosciutto slices": "prosciutto",
    "capocollo": "capicola",
    "corned beef brisket": "corned beef",
    "pork chops": "pork chop",
    "pork loins": "pork loin",
    "baby back rib": "baby back ribs",
    "spare rib": "spare ribs",
    "short ribs": "short rib",

    # seafood
    "salmon fillet": "salmon",
    "salmon filet": "salmon",
    "raw shrimp": "shrimp",
    "frozen shrimp": "shrimp",
    "canned tuna": "tuna",
    "mahi-mahi": "mahi mahi",
    "sea bass": "sea bass",

    # peppers / chiles
    "bell peppers": "bell pepper",
    "green pepper": "bell pepper",
    "red pepper": "bell pepper",
    "yellow pepper": "bell pepper",
    "orange pepper": "bell pepper",
    "peppers": "bell pepper",
    "jalapenos": "jalapeno",
    "poblanos": "poblano",
    "anaheim peppers": "anaheim chile",
    "ancho chiles": "ancho chile",
    "guajillo chiles": "guajillo chile",
    "arbol chiles": "arbol chile",
    "serranos": "serrano",
    "habaneros": "habanero",
    "calabrian chiles": "calabrian chile",
    "calabrian chili": "calabrian chile",
    "hatch green chiles": "hatch green chile",
    "hatch chile": "hatch green chile",
    "hatch chili": "hatch green chile",
    "hatch red chiles": "hatch red chile",
    "hatch red chile powder": "hatch red chile powder",
    "hatch chile powder": "hatch red chile powder",

    # produce
    "potatoes": "potato",
    "russet potatoes": "potato",
    "yukon gold potatoes": "potato",
    "red potatoes": "potato",
    "sweet potatoes": "sweet potato",
    "eggs": "egg",
    "limes": "lime",
    "lemons": "lemon",
    "mushrooms": "mushroom",
    "zucchinis": "zucchini",
    "carrots": "carrot",
    "celery stalks": "celery",
    "avocados": "avocado",
    "artichokes": "artichoke",
    "cucumbers": "cucumber",
    "brussels sprouts": "brussels sprouts",
    "microgreens": "micro greens",
    "micro-greens": "micro greens",

    # fruits
    "strawberries": "strawberry",
    "blueberries": "blueberry",
    "raspberries": "raspberry",
    "berries": "berry",
    "pineapples": "pineapple",
    "mangoes": "mango",
    "peaches": "peach",
    "pears": "pear",
    "grapes": "grape",
    "kiwis": "kiwi",
    "papayas": "papaya",
    "raisins": "raisin",

    # tortillas / breads / crackers
    "tortillas": "tortilla",
    "corn tortillas": "corn tortilla",
    "flour tortillas": "flour tortilla",
    "lettuce wraps": "lettuce wrap",
    "burger buns": "bread",
    "hot dog buns": "bread",
    "sandwich buns": "bread",
    "french baguette": "french bread",
    "crackers": "cracker",

    # beans / legumes
    "beans": "bean",
    "dried beans": "bean",
    "black beans": "black bean",
    "kidney beans": "kidney bean",
    "white beans": "white bean",
    "pinto beans": "pinto bean",
    "cannellini beans": "cannellini bean",
    "navy beans": "navy bean",
    "garbanzo beans": "chickpea",
    "chickpeas": "chickpea",
    "lentils": "lentil",
    "split peas": "split pea",
    "soy beans": "soybean",
    "soybeans": "soybean",
    "soy beans frozen": "edamame",

    # grains / noodles / starches
    "oats": "oat",
    "spaghetti": "pasta",
    "penne": "pasta",
    "rigatoni": "pasta",
    "fettuccine": "pasta",
    "linguine": "pasta",
    "macaroni": "pasta",
    "orzo pasta": "orzo",
    "egg noodles": "egg noodle",
    "rice noodles": "rice noodle",
    "udon noodles": "udon",
    "rice papers": "rice paper",
    "brown rice": "rice",
    "white rice": "rice",
    "jasmine rice": "rice",
    "basmati rice": "rice",
    "wild rice": "rice",

    # cheese / dairy
    "mozzarella cheese": "mozzarella",
    "cheddar cheese": "cheddar",
    "parmesan cheese": "parmesan",
    "feta cheese": "feta",
    "goat cheese": "goat cheese",
    "monterey jack cheese": "monterey jack",
    "pepper jack cheese": "pepper jack",
    "colby jack cheese": "colby jack",
    "cotija cheese": "cotija",
    "queso fresco cheese": "queso fresco",
    "american cheese": "american cheese",
    "american cheese slices": "american cheese",
    "swiss cheese": "swiss",
    "provolone cheese": "provolone",
    "ricotta cheese": "ricotta",
    "cream cheese block": "cream cheese",
    "halloumi cheese": "halloumi",
    "muenster cheese": "muenster",
    "havarti cheese": "havarti",
    "manchengo": "manchego",
    "machego": "manchego",
    "shredded cheese": "cheese",
    "whole milk": "milk",
    "2 milk": "milk",
    "2% milk": "milk",
    "heavy whipping cream": "heavy cream",
    "whipping cream": "heavy cream",
    "plain yogurt": "yogurt",
    "greek yogurt": "yogurt",
    "whipped topping": "whipped cream",

    # oils / sauces / condiments
    "vegetable oil": "oil",
    "canola oil": "oil",
    "avocado oil": "oil",
    "sesame oil toasted": "sesame oil",
    "soy": "soy sauce",
    "tamari": "soy sauce",
    "bbq sauce": "barbecue sauce",
    "buffalo sauce": "hot sauce",
    "ranch": "ranch dressing",
    "ranch dressing": "ranch dressing",
    "shoyu sauce": "shoyu",
    "shoyu soy sauce": "shoyu",
    "saizon": "sazon",
    "sazón": "sazon",
    "huli huli sauce": "huli huli",
    "fish sauce": "fish sauce",
    "oyster sauce": "oyster sauce",
    "rice vinegar": "rice vinegar",
    "red wine vinegar": "red wine vinegar",
    "apple cider vinegar": "apple cider vinegar",
    "balsamic vinegar": "balsamic vinegar",
    "cooking wine": "white wine",

    # broths / stocks
    "chicken broth": "broth",
    "beef broth": "broth",
    "vegetable broth": "broth",
    "stock": "broth",
    "chicken stock": "broth",
    "beef stock": "broth",
    "vegetable stock": "broth",

    # greens / herbs
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

    # frozen
    "green peas": "peas",
    "frozen peas": "peas",
    "frozen mixed vegetables": "frozen vegetables",
    "mixed vegetables": "frozen vegetables",
    "frozen berries": "frozen berry",
    "frozen fruit": "frozen fruit",
    "hash browns": "hash brown",

    # baking / pantry
    "all purpose flour": "flour",
    "ap flour": "flour",
    "corn starch": "cornstarch",
    "almonds": "almond",
    "peanuts": "peanut",
    "macadamia nuts": "macadamia nut",
    "sesame seeds": "sesame seed",
    "chili powder": "chili flakes",
    "taco seasoning": "cumin",
    "zaatar": "zaatar",
    "sumac": "sumac",
    "berbere": "berbere",
    "gochujang": "gochujang",
    "harissa": "harissa",
    "miso paste": "miso",

    # equipment aliases
    "foil": "foil",
    "aluminum foil": "foil",
    "parchment": "parchment paper",
    "sheet tray": "sheet pan",
    "frying pan": "skillet",
    "cast iron": "cast iron pan"
}

INGREDIENT_GROUPS = {
    "Proteins": [
        "chicken", "turkey", "duck",
        "beef", "steak", "ribeye", "sirloin", "brisket", "short rib",
        "pork", "pork chop", "pork loin", "pork shoulder", "pork belly",
        "ribs", "baby back ribs", "spare ribs", "ham", "bacon", "sausage",
        "lamb", "venison", "bison", "veal",
        "salmon", "shrimp", "tuna", "cod", "tilapia", "halibut", "mahi mahi",
        "snapper", "trout", "catfish", "sea bass", "sardine", "anchovy",
        "crab", "lobster", "scallop", "clam", "mussel", "oyster",
        "egg", "tofu", "tempeh", "seitan", "black bean", "chickpea", "lentil", "edamame",
        "deli turkey", "deli ham", "roast beef", "salami", "pepperoni",
        "prosciutto", "capicola", "pastrami", "corned beef"
    ],
    "Vegetables": [
        "onion", "red onion", "green onion", "shallot", "leek", "garlic",
        "bell pepper", "jalapeno", "serrano", "habanero", "poblano",
        "anaheim chile", "ancho chile", "guajillo chile", "arbol chile",
        "hatch green chile", "hatch red chile",
        "carrot", "celery", "broccoli", "cauliflower", "cabbage", "red cabbage",
        "spinach", "kale", "romaine", "lettuce", "greens", "arugula", "micro greens",
        "cucumber", "zucchini", "yellow squash", "eggplant", "mushroom",
        "potato", "sweet potato", "corn", "peas", "green bean", "asparagus",
        "brussels sprouts", "tomato", "canned tomato", "tomato paste", "tomato sauce",
        "beet", "radish", "turnip", "parsnip", "okra", "artichoke", "avocado"
    ],
    "Fruits": [
        "apple", "banana", "orange", "lemon", "lime", "grape",
        "strawberry", "blueberry", "raspberry", "blackberry", "berry",
        "pineapple", "mango", "peach", "pear", "plum", "cherry",
        "watermelon", "cantaloupe", "kiwi", "papaya", "pomegranate",
        "coconut", "raisin", "frozen fruit", "frozen berry"
    ],
    "Grains & Starches": [
        "rice", "quinoa", "farro", "barley", "couscous", "pasta",
        "orzo", "ramen", "rice noodle", "egg noodle", "udon", "bread",
        "french bread", "corn tortilla", "flour tortilla", "lettuce wrap",
        "pita", "naan", "rice paper", "potato", "sweet potato",
        "oat", "polenta", "grits", "cracker", "panko", "breadcrumbs"
    ],
    "Dairy & Cheese": [
        "milk", "almond milk", "oat milk", "butter", "cream", "heavy cream",
        "sour cream", "cream cheese", "cottage cheese", "ricotta", "yogurt", "whipped cream",
        "cheddar", "mozzarella", "parmesan", "pecorino", "asiago",
        "monterey jack", "pepper jack", "colby jack", "swiss", "provolone",
        "american cheese", "feta", "goat cheese", "brie", "blue cheese",
        "gouda", "havarti", "cotija", "queso fresco", "halloumi", "muenster", "manchego", "cheese"
    ],
    "Oils & Fats": [
        "olive oil", "oil", "vegetable oil", "canola oil", "avocado oil",
        "sesame oil", "coconut oil", "butter", "ghee", "duck fat", "lard"
    ],
    "Legumes & Beans": [
        "bean", "black bean", "pinto bean", "kidney bean", "white bean",
        "navy bean", "cannellini bean", "chickpea", "lentil", "split pea",
        "soybean", "edamame", "black-eyed pea"
    ],
    "Dry Goods & Baking": [
        "broth", "stock", "flour", "almond flour", "cornstarch", "panko", "breadcrumbs",
        "sugar", "brown sugar", "powdered sugar", "honey", "maple syrup",
        "agave", "corn syrup", "molasses", "cocoa powder", "vanilla",
        "baking powder", "baking soda", "yeast", "graham cracker",
        "marshmallow", "chocolate chip", "dark chocolate"
    ],
    "Sauces & Condiments": [
        "ketchup", "mustard", "dijon mustard", "mayonnaise", "ranch dressing",
        "barbecue sauce", "hot sauce", "salsa", "soy sauce", "shoyu",
        "teriyaki sauce", "hoisin", "fish sauce", "oyster sauce",
        "vinegar", "apple cider vinegar", "red wine vinegar", "balsamic vinegar", "rice vinegar",
        "worcestershire", "caesar dressing", "honey mustard", "tahini",
        "peanut butter", "pickle", "relish", "jam", "harissa", "gochujang", "miso", "huli huli"
    ],
    "Herbs": [
        "parsley", "cilantro", "basil", "dill", "mint", "thyme",
        "rosemary", "oregano", "sage", "chive", "green onion"
    ],
    "Spices & Seasonings": [
        "salt", "black pepper", "garlic powder", "onion powder",
        "paprika", "smoked paprika", "cumin", "coriander", "turmeric",
        "cinnamon", "nutmeg", "ginger", "red pepper flakes", "chili flakes",
        "cayenne", "italian seasoning", "bay leaf", "curry powder",
        "five spice", "zaatar", "sumac", "berbere", "saffron", "sazon",
        "hatch red chile powder", "calabrian chile"
    ],
    "Nuts & Seeds": [
        "almond", "walnut", "pecan", "cashew", "peanut", "pistachio",
        "pine nut", "sesame seed", "sunflower seed", "pumpkin seed",
        "chia seed", "flax seed", "macadamia nut"
    ],
    "Frozen Items": [
        "frozen vegetables", "frozen peas", "frozen broccoli", "frozen spinach",
        "frozen corn", "frozen fruit", "frozen berry", "frozen shrimp",
        "frozen salmon", "frozen chicken", "frozen fries", "hash brown"
    ],
    "Alcohol & Cooking Wine": [
        "red wine", "white wine", "beer", "sherry", "mirin",
        "bourbon", "rum", "vodka", "brandy"
    ]
}

KITCHEN_RESOURCES = {
    "Cookware & Bakeware": [
        "sheet pan", "baking dish", "skillet", "cast iron pan",
        "nonstick pan", "pot", "dutch oven", "saucepan", "stock pot", "wok"
    ],
    "Tools": [
        "blender", "food processor", "hand mixer", "stand mixer",
        "whisk", "strainer", "grater", "peeler", "tongs"
    ],
    "Kitchen Supplies": [
        "foil", "parchment paper", "plastic wrap", "zip bag"
    ]
}

WRAP_OPTIONS = {"corn tortilla", "flour tortilla", "lettuce wrap"}

CHEESE_OPTIONS = {
    "cheese", "cheddar", "mozzarella", "parmesan", "feta", "monterey jack",
    "pepper jack", "colby jack", "swiss", "provolone", "cotija",
    "queso fresco", "american cheese", "goat cheese", "ricotta",
    "halloumi", "muenster", "havarti", "manchego"
}

MELTING_CHEESE_OPTIONS = {
    "cheese", "cheddar", "mozzarella", "monterey jack", "pepper jack",
    "colby jack", "provolone", "american cheese", "swiss", "havarti",
    "gouda", "muenster"
}

ITALIAN_CHEESE_OPTIONS = {"parmesan", "pecorino", "asiago", "romano", "mozzarella", "ricotta"}
MEXICAN_CHEESE_OPTIONS = {"cheddar", "monterey jack", "cotija", "queso fresco", "pepper jack", "colby jack", "cheese"}
GREEK_CHEESE_OPTIONS = {"feta", "halloumi"}

NON_FOOD_ITEMS = set()
for group_items in KITCHEN_RESOURCES.values():
    NON_FOOD_ITEMS.update(group_items)

# ======================
# HELPERS
# ======================
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
    text = re.sub(r"[^a-zA-Z0-9\s&/\-'.]", "", text)
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
    if recipe_item == "wrap" and user_item in WRAP_OPTIONS:
        return True
    if recipe_item == "cheese" and user_item in CHEESE_OPTIONS:
        return True
    if recipe_item == "melting cheese" and user_item in MELTING_CHEESE_OPTIONS:
        return True
    if recipe_item == "italian cheese" and user_item in ITALIAN_CHEESE_OPTIONS:
        return True
    if recipe_item == "mexican cheese" and user_item in MEXICAN_CHEESE_OPTIONS:
        return True
    if recipe_item == "greek cheese" and user_item in GREEK_CHEESE_OPTIONS:
        return True

    return user_item in recipe_item or recipe_item in user_item

def entry_matches(entry, user_ingredients):
    if isinstance(entry, str):
        return any(ingredient_matches(user_item, entry) for user_item in user_ingredients)

    if isinstance(entry, dict):
        return any(
            any(ingredient_matches(user_item, opt) for user_item in user_ingredients)
            for opt in entry.get("options", [])
        )

    return False

def matched_label(entry, user_ingredients):
    if isinstance(entry, str):
        return normalize_ingredient(entry)

    if isinstance(entry, dict):
        for option in entry.get("options", []):
            for user_item in user_ingredients:
                if ingredient_matches(user_item, option):
                    return normalize_ingredient(option)
        return entry.get("name", "ingredient")

    return str(entry)

def missing_label(entry):
    if isinstance(entry, str):
        return normalize_ingredient(entry)

    if isinstance(entry, dict):
        name = entry.get("name", "ingredient")
        options = entry.get("options", [])
        return f"{name} ({', '.join(options)})" if options else name

    return str(entry)

def skill_rank(level):
    ranks = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
    return ranks.get(level, 1)

def recipe_matches_goal(recipe, selected_meal_goal):
    if selected_meal_goal == "All":
        return True

    goal_map = {
        "Comfort Food": "comfort_food",
        "Protein Packed": "protein_packed",
        "Low Carb": "low_carb",
        "Keto": "keto",
        "GLP-1 Friendly": "glp1_friendly"
    }
    return bool(recipe.get(goal_map.get(selected_meal_goal), False))

def recipe_matches_filters(
    recipe,
    selected_cuisine,
    selected_meal_style,
    selected_skill_level,
    selected_time,
    selected_access_level
):
    if selected_cuisine != "All" and recipe.get("cuisine") != selected_cuisine:
        return False

    if selected_meal_style != "All" and recipe.get("meal_style") != selected_meal_style:
        return False

    if selected_skill_level != "All":
        if skill_rank(recipe.get("skill_level", "Beginner")) > skill_rank(selected_skill_level):
            return False

    time_limit = TIME_FILTERS[selected_time]
    recipe_time = recipe.get("time_minutes", 9999)

    if selected_time == "More advanced / longer cook":
        return recipe_time > 60
    if time_limit is not None and recipe_time > time_limit:
        return False

    if selected_access_level != "All":
        access_levels = recipe.get("ingredient_access", ["Everyday Grocery"])
        if selected_access_level not in access_levels:
            return False

    return True

def score_recipe(user_ingredients, required_ingredients, optional_ingredients):
    matched_required = []
    missing_required = []

    for entry in required_ingredients:
        if entry_matches(entry, user_ingredients):
            matched_required.append(matched_label(entry, user_ingredients))
        else:
            missing_required.append(missing_label(entry))

    matched_optional = []
    missing_optional = []

    for entry in optional_ingredients:
        if entry_matches(entry, user_ingredients):
            matched_optional.append(matched_label(entry, user_ingredients))
        else:
            missing_optional.append(missing_label(entry))

    required_total = len(required_ingredients)
    required_match_count = len(matched_required)
    required_match_percent = round((required_match_count / required_total) * 100) if required_total else 100

    return {
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_optional": matched_optional,
        "missing_optional": missing_optional,
        "required_match_count": required_match_count,
        "required_total": required_total,
        "required_match_percent": required_match_percent
    }

def flatten_items_for_suggestions(items):
    flattened = []

    for entry in items:
        if isinstance(entry, str):
            flattened.append(normalize_ingredient(entry))
        elif isinstance(entry, dict):
            name = entry.get("name", "")
            if name == "wrap":
                flattened.extend(["corn tortilla", "flour tortilla", "lettuce wrap"])
            elif name == "melting cheese":
                flattened.extend(["cheddar", "mozzarella", "monterey jack", "pepper jack", "colby jack", "american cheese"])
            elif name == "italian cheese":
                flattened.extend(["parmesan", "mozzarella", "ricotta", "pecorino", "asiago"])
            elif name == "mexican cheese":
                flattened.extend(["cheddar", "cotija", "queso fresco", "monterey jack", "pepper jack"])
            elif name == "greek cheese":
                flattened.extend(["feta", "halloumi"])
            else:
                flattened.extend([normalize_ingredient(opt) for opt in entry.get("options", [])])

    return flattened

def get_suggested_add_ons(user_ingredients, filtered_recipes, limit=20):
    scores = defaultdict(int)

    for recipe in filtered_recipes:
        result = score_recipe(user_ingredients, recipe.get("required", []), recipe.get("optional", []))

        for item in result["missing_required"] + result["missing_optional"]:
            clean_item = normalize_ingredient(item.split(" (")[0])
            if clean_item not in NON_FOOD_ITEMS:
                scores[clean_item] += 1

    suggestions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [item for item, _ in suggestions[:limit]]

def categorize_suggestions(items):
    categorized = {group: [] for group in INGREDIENT_GROUPS}
    uncategorized = []

    for item in sorted(set(items)):
        normalized = normalize_ingredient(item)
        placed = False

        for group, group_items in INGREDIENT_GROUPS.items():
            if normalized in group_items:
                categorized[group].append(normalized)
                placed = True
                break

        if not placed:
            uncategorized.append(normalized)

    if uncategorized:
        categorized["Other"] = sorted(set(uncategorized))

    for group in categorized:
        categorized[group] = sorted(set(categorized[group]))

    return categorized

def build_goal_tags(recipe):
    tags = []
    if recipe.get("comfort_food"):
        tags.append("Comfort Food")
    if recipe.get("protein_packed"):
        tags.append("Protein Packed")
    if recipe.get("low_carb"):
        tags.append("Low Carb")
    if recipe.get("keto"):
        tags.append("Keto")
    if recipe.get("glp1_friendly"):
        tags.append("GLP-1 Friendly")
    return tags

# ======================
# STREAMLIT UI
# ======================
st.title("🍽️ What Can I Cook?")
st.markdown("Tell me what you have and I’ll find the best recipes you can make right now.")

with st.sidebar:
    st.header("Filters")

    user_input = st.text_area(
        "What ingredients do you have? (one per line)",
        placeholder="chicken breast\ngarlic\nrice\nbell pepper\nbroth",
        height=220
    )

    col1, col2 = st.columns(2)
    with col1:
        selected_cuisine = st.selectbox("Cuisine", CUISINE_OPTIONS)
        selected_meal_style = st.selectbox("Meal Style", MEAL_STYLE_OPTIONS)
        selected_meal_goal = st.selectbox("Meal Goal", MEAL_GOAL_OPTIONS)

    with col2:
        selected_skill = st.selectbox("Your Skill Level", ["All", "Beginner", "Intermediate", "Advanced"])
        selected_time = st.selectbox("Time Available", list(TIME_FILTERS.keys()))
        selected_access = st.selectbox("Grocery Access Level", ["All"] + ACCESS_LEVELS)

    quick_only = st.checkbox("Only Quick Meals", value=False)
    high_protein_only = st.checkbox("High Protein Only", value=False)
    strong_matches_only = st.checkbox("Only 50%+ Matches", value=False)

user_ingredients = [normalize_ingredient(line.strip()) for line in user_input.strip().split("\n") if line.strip()]

filtered_recipes = []
for recipe in recipes:
    if not recipe_matches_filters(
        recipe,
        selected_cuisine,
        selected_meal_style,
        selected_skill,
        selected_time,
        selected_access
    ):
        continue

    if quick_only and not recipe.get("quick_meal", False):
        continue

    if high_protein_only and not recipe.get("high_protein", False):
        continue

    if selected_meal_goal != "All" and not recipe_matches_goal(recipe, selected_meal_goal):
        continue

    score_data = score_recipe(
        user_ingredients,
        recipe.get("required", []),
        recipe.get("optional", [])
    )

    if strong_matches_only and score_data["required_match_percent"] < 50:
        continue

    filtered_recipes.append({
        **recipe,
        "match_score": score_data["required_match_percent"],
        "score_data": score_data
    })

filtered_recipes.sort(
    key=lambda x: (
        x["match_score"],
        x["score_data"]["required_match_count"],
        len(x["score_data"]["matched_optional"])
    ),
    reverse=True
)

if not user_ingredients:
    st.info("👈 Enter ingredients in the sidebar to get started.")
else:
    st.subheader(f"Found {len(filtered_recipes)} matching recipes")

    if filtered_recipes:
        for i, recipe in enumerate(filtered_recipes[:15]):
            with st.expander(f"🥘 {recipe['name']} — {recipe['match_score']}% match", expanded=(i == 0)):
                col_a, col_b = st.columns([3, 1])

                with col_a:
                    st.write(
                        f"**Cuisine:** {recipe.get('cuisine', 'Unknown')} | "
                        f"**Time:** {recipe.get('time_minutes', '?')} min | "
                        f"**Skill:** {recipe.get('skill_level', 'Beginner')}"
                    )

                    st.write(
                        f"**Meal Style:** {recipe.get('meal_style', 'Unknown')} | "
                        f"**Meal Type:** {recipe.get('meal_type', 'Unknown')}"
                    )

                    goal_tags = build_goal_tags(recipe)
                    if goal_tags:
                        st.write(f"**Goals:** {', '.join(goal_tags)}")

                    if recipe.get("ingredient_access"):
                        st.write(f"**Access:** {', '.join(recipe.get('ingredient_access', []))}")

                    if recipe.get("equipment"):
                        st.write(f"**Equipment:** {', '.join(recipe.get('equipment', []))}")

                    if recipe.get("description"):
                        st.write(recipe["description"])

                with col_b:
                    st.metric("Match", f"{recipe['match_score']}%")

                sd = recipe["score_data"]

                if sd["matched_required"]:
                    st.success("✅ You have: " + ", ".join(sd["matched_required"]))

                if sd["missing_required"]:
                    st.error("❌ Missing: " + ", ".join(sd["missing_required"]))

                if sd["matched_optional"]:
                    st.info("🌟 Optional you have: " + ", ".join(sd["matched_optional"]))

                if sd["missing_optional"]:
                    st.write("➕ Optional extras: " + ", ".join(sd["missing_optional"]))

                if recipe.get("questions"):
                    st.subheader("Helpful Questions")
                    for question in recipe["questions"]:
                        st.write(f"• {question}")

                st.subheader("Instructions")
                for step in recipe.get("instructions", ["No instructions provided."]):
                    st.write(f"• {step}")

                if recipe.get("shopping_tips"):
                    st.subheader("Shopping Tips")
                    for tip in recipe["shopping_tips"]:
                        st.write(f"• {tip}")

                if recipe.get("chef_upgrade"):
                    st.subheader("Chef Upgrade")
                    for item in recipe["chef_upgrade"]:
                        st.write(f"• {item}")

                if recipe.get("advanced_shortcuts"):
                    st.subheader("Easy Advanced Shortcut")
                    for item in recipe["advanced_shortcuts"]:
                        st.write(f"• {item}")

                if recipe.get("advanced_homemade"):
                    st.subheader("Advanced Homemade Option")
                    for item in recipe["advanced_homemade"]:
                        st.write(f"• {item}")

        st.subheader("🛒 Suggested Add-ons to Buy")
        suggestions = get_suggested_add_ons(user_ingredients, filtered_recipes)

        if suggestions:
            cols = st.columns(4)
            for idx, item in enumerate(suggestions[:12]):
                with cols[idx % 4]:
                    st.button(item, key=f"sugg_{idx}", use_container_width=True)
        else:
            st.write("You're all set. No additional ingredients needed.")

    else:
        st.warning("No recipes match your current filters and ingredients. Try broadening your filters or adding more ingredients.")

st.caption("What Can I Cook? — Built to reduce food waste and spark joy in the kitchen.")