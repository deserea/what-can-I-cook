import json
import re

def singularize(word):
    word = word.strip().lower()
    if word.endswith("ies") and len(word) > 3:
        return word[:-3] + "y"
    if word.endswith("oes") and len(word) > 3:
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        return word[:-1]
    return word

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
    "tomato paste cans": "tomato paste",

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

    "salmon fillet": "salmon",
    "salmon filet": "salmon",
    "raw shrimp": "shrimp",
    "frozen shrimp": "shrimp",
    "canned tuna": "tuna",
    "mahi-mahi": "mahi mahi",
    "sea bass": "sea bass",

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

    "burger buns": "bread",
    "hot dog buns": "bread",
    "sandwich buns": "bread",
    "french baguette": "french bread",
    "crackers": "cracker",

    "limes": "lime",
    "lemons": "lemon",

    "beans": "bean",
    "black beans": "black bean",
    "kidney beans": "kidney bean",
    "white beans": "white bean",
    "pinto beans": "pinto bean",
    "cannellini beans": "cannellini bean",
    "garbanzo beans": "chickpea",
    "chickpeas": "chickpea",
    "lentils": "lentil",
    "split peas": "split pea",
    "soy beans": "soybean",
    "soybeans": "soybean",
    "soy beans frozen": "edamame",

    "mushrooms": "mushroom",
    "zucchinis": "zucchini",
    "carrots": "carrot",
    "celery stalks": "celery",
    "avocados": "avocado",
    "artichokes": "artichoke",
    "cucumbers": "cucumber",

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

    "brown rice": "rice",
    "white rice": "rice",
    "jasmine rice": "rice",
    "basmati rice": "rice",
    "wild rice": "rice",

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
    "2% milk": "milk",
    "heavy whipping cream": "heavy cream",
    "whipping cream": "heavy cream",
    "plain yogurt": "yogurt",
    "greek yogurt": "yogurt",

    "vegetable oil": "oil",
    "canola oil": "oil",
    "avocado oil": "oil",
    "sesame oil toasted": "sesame oil",

    "soy": "soy sauce",
    "tamari": "soy sauce",
    "bbq sauce": "barbecue sauce",
    "buffalo sauce": "hot sauce",
    "ranch": "ranch dressing",
    "shoyu sauce": "shoyu",
    "saizon": "sazon",
    "sazón": "sazon",

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
    "frozen mixed vegetables": "frozen vegetables",
    "frozen berries": "frozen berry",
    "frozen fruit": "frozen fruit",
    "hash browns": "hash brown",

    "all purpose flour": "flour",
    "ap flour": "flour",
    "corn starch": "cornstarch",
    "almonds": "almond",
    "peanuts": "peanut",
    "macadamia nuts": "macadamia nut",
    "sesame seeds": "sesame seed"
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
            any(ingredient_matches(user_item, option) for user_item in user_ingredients)
            for option in entry.get("options", [])
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
        "required_total": required_total,
        "required_match_count": required_match_count,
        "required_match_percent": required_match_percent
    }

def goal_tags(recipe):
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

def display_recipe_detail(recipe, score_data):
    print(f"\n🍴 {recipe['name']}")
    print(f"Cuisine: {recipe.get('cuisine', 'Unknown')}")
    print(f"Meal Style: {recipe.get('meal_style', 'Unknown')}")
    print(f"Meal Type: {recipe.get('meal_type', 'Unknown')}")
    print(f"Time: {recipe.get('time_minutes', '?')} min")
    print(f"Skill Level: {recipe.get('skill_level', 'Beginner')}")

    tags = goal_tags(recipe)
    if tags:
        print(f"Goals: {', '.join(tags)}")

    print(f"\nMatch: {score_data['required_match_count']}/{score_data['required_total']} required ingredients ({score_data['required_match_percent']}%)")

    if score_data["matched_required"]:
        print("✅ You have:")
        for item in score_data["matched_required"]:
            print(f"- {item}")

    if score_data["missing_required"]:
        print("❌ Missing:")
        for item in score_data["missing_required"]:
            print(f"- {item}")

    if score_data["matched_optional"]:
        print("🌟 Optional you have:")
        for item in score_data["matched_optional"]:
            print(f"- {item}")

    if score_data["missing_optional"]:
        print("➕ Optional extras:")
        for item in score_data["missing_optional"]:
            print(f"- {item}")

    if recipe.get("equipment"):
        print("🔧 Equipment:")
        for item in recipe["equipment"]:
            print(f"- {item}")

    if recipe.get("questions"):
        print("\nHelpful Questions:")
        for item in recipe["questions"]:
            print(f"- {item}")

    print("\nInstructions:")
    for i, step in enumerate(recipe.get("instructions", []), start=1):
        print(f"{i}. {step}")

    if recipe.get("shopping_tips"):
        print("\nShopping Tips:")
        for item in recipe["shopping_tips"]:
            print(f"- {item}")

    if recipe.get("chef_upgrade"):
        print("\nChef Upgrade:")
        for item in recipe["chef_upgrade"]:
            print(f"- {item}")

    if recipe.get("advanced_shortcuts"):
        print("\nEasy Advanced Shortcut:")
        for item in recipe["advanced_shortcuts"]:
            print(f"- {item}")

    if recipe.get("advanced_homemade"):
        print("\nAdvanced Homemade Option:")
        for item in recipe["advanced_homemade"]:
            print(f"- {item}")

print("\n🍽️ What Can I Cook? 🍽️\n")

user_input = input("Enter the ingredients you have, separated by commas: ").lower().strip()
user_ingredients = [normalize_ingredient(item.strip()) for item in user_input.split(",") if item.strip()]

if not user_ingredients:
    print("\nNo ingredients entered.\n")
    raise SystemExit

matches = []

for recipe in recipes:
    score_data = score_recipe(
        user_ingredients,
        recipe.get("required", []),
        recipe.get("optional", [])
    )

    if score_data["required_match_count"] > 0:
        matches.append((recipe, score_data))

matches.sort(
    key=lambda x: (
        x[1]["required_match_percent"],
        x[1]["required_match_count"],
        len(x[1]["matched_optional"])
    ),
    reverse=True
)

if matches:
    print("\nHere are your best matches:\n")

    for i, (recipe, score_data) in enumerate(matches[:15], 1):
        print(
            f"{i}. {recipe['name']} "
            f"({score_data['required_match_count']}/{score_data['required_total']} required matched, "
            f"{score_data['required_match_percent']}%)"
        )

    choice = input("\nSelect a recipe number to see details (or press Enter to skip): ").strip()

    if choice.isdigit():
        index = int(choice) - 1

        if 0 <= index < len(matches[:15]):
            recipe, score_data = matches[index]
            display_recipe_detail(recipe, score_data)
        else:
            print("\nInvalid selection.\n")

else:
    print("\nNo matches found. Try entering more ingredients.\n")