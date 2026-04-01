import json
import re
import streamlit as st

st.set_page_config(page_title="What Can I Cook?", page_icon="🍽️", layout="wide")

with open("recipes.json", "r", encoding="utf-8") as file:
    recipes = json.load(file)

ALIASES = {
    "tomatoes": "tomato",
    "cherry tomatoes": "tomato",
    "roma tomatoes": "tomato",
    "onions": "onion",
    "red onions": "red onion",
    "yellow onions": "onion",
    "green onions": "green onion",
    "scallions": "green onion",
    "garlic cloves": "garlic",
    "ground beef": "beef",
    "minced beef": "beef",
    "beef mince": "beef",
    "ground turkey": "turkey",
    "ground chicken": "chicken",
    "italian sausage": "sausage",
    "hot italian sausage": "sausage",
    "mild italian sausage": "sausage",
    "chicken breast": "chicken",
    "chicken breasts": "chicken",
    "chicken thigh": "chicken",
    "chicken thighs": "chicken",
    "bell peppers": "bell pepper",
    "peppers": "bell pepper",
    "jalapenos": "jalapeno",
    "potatoes": "potato",
    "sweet potatoes": "sweet potato",
    "eggs": "egg",
    "tortillas": "tortilla",
    "limes": "lime",
    "lemons": "lemon",
    "beans": "bean",
    "black beans": "black bean",
    "kidney beans": "kidney bean",
    "white beans": "white bean",
    "chickpeas": "chickpea",
    "garbanzo beans": "chickpea",
    "lentils": "lentil",
    "mushrooms": "mushroom",
    "zucchinis": "zucchini",
    "carrots": "carrot",
    "celery stalks": "celery",
    "avocados": "avocado",
    "strawberries": "strawberry",
    "blueberries": "blueberry",
    "raspberries": "raspberry",
    "oats": "oat",
    "spaghetti": "pasta",
    "penne": "pasta",
    "rigatoni": "pasta",
    "fettuccine": "pasta",
    "brown rice": "rice",
    "white rice": "rice",
    "flour tortillas": "tortilla",
    "corn tortillas": "tortilla",
    "mozzarella cheese": "mozzarella",
    "cheddar cheese": "cheddar",
    "parmesan cheese": "parmesan",
    "vegetable oil": "oil",
    "avocado oil": "oil",
    "soy": "soy sauce",
    "tamari": "soy sauce",
    "chicken broth": "broth",
    "beef broth": "broth",
    "vegetable broth": "broth"
}

PANTRY_STAPLES = {
    "salt", "pepper", "oil", "olive oil", "butter", "water",
    "garlic powder", "onion powder", "paprika", "smoked paprika",
    "cumin", "oregano", "basil", "thyme", "rosemary",
    "red pepper flakes", "chili flakes", "cayenne",
    "soy sauce", "vinegar", "broth"
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
    text = text.strip().lower()
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

    if user_item in recipe_item or recipe_item in user_item:
        return True

    return False

def recipe_matches_filters(recipe, selected_cuisine, selected_meal_type, vegetarian_only, quick_only, high_protein_only):
    if selected_cuisine != "All" and recipe["cuisine"] != selected_cuisine:
        return False
    if selected_meal_type != "All" and recipe["meal_type"] != selected_meal_type:
        return False
    if vegetarian_only and not recipe["vegetarian"]:
        return False
    if quick_only and not recipe["quick_meal"]:
        return False
    if high_protein_only and not recipe["high_protein"]:
        return False
    return True

def score_recipe(user_ingredients, recipe_ingredients):
    normalized_recipe = [normalize_ingredient(item) for item in recipe_ingredients]
    matched_items = []
    missing_items = []

    for recipe_item in normalized_recipe:
        found = any(ingredient_matches(user_item, recipe_item) for user_item in user_ingredients)
        if found or recipe_item in PANTRY_STAPLES:
            matched_items.append(recipe_item)
        else:
            missing_items.append(recipe_item)

    match_count = len(matched_items)
    total_count = len(normalized_recipe)
    match_percent = round((match_count / total_count) * 100) if total_count else 0

    return matched_items, missing_items, match_count, total_count, match_percent

st.title("🍽️ What Can I Cook?")
st.write("Turn the ingredients you already have into smarter meal ideas, match scores, and a shopping list.")

with st.sidebar:
    st.header("Filters")
    cuisines = sorted(set(recipe["cuisine"] for recipe in recipes))
    meal_types = sorted(set(recipe["meal_type"] for recipe in recipes))

    selected_cuisine = st.selectbox("Cuisine", ["All"] + cuisines)
    selected_meal_type = st.selectbox("Meal Type", ["All"] + meal_types)
    vegetarian_only = st.checkbox("Vegetarian only")
    quick_only = st.checkbox("Quick meals only")
    high_protein_only = st.checkbox("High protein only")
    strong_matches_only = st.checkbox("Show only strong matches (50%+)", value=False)

user_input = st.text_input(
    "Ingredients",
    placeholder="ground beef, tomatoes, onion, garlic, pasta, spinach"
)

if st.button("Find Meals"):
    if not user_input.strip():
        st.warning("Please enter at least one ingredient.")
    else:
        raw_ingredients = [item.strip() for item in user_input.split(",") if item.strip()]
        user_ingredients = [normalize_ingredient(item) for item in raw_ingredients]

        matches = []
        shopping_list = set()

        for recipe in recipes:
            if not recipe_matches_filters(
                recipe,
                selected_cuisine,
                selected_meal_type,
                vegetarian_only,
                quick_only,
                high_protein_only
            ):
                continue

            matched_items, missing_items, match_count, total_count, match_percent = score_recipe(
                user_ingredients,
                recipe["ingredients"]
            )

            if match_count > 0:
                if not strong_matches_only or match_percent >= 50:
                    matches.append({
                        "name": recipe["name"],
                        "match_count": match_count,
                        "total": total_count,
                        "match_percent": match_percent,
                        "have": matched_items,
                        "missing": missing_items,
                        "cuisine": recipe["cuisine"],
                        "meal_type": recipe["meal_type"],
                        "protein": recipe["protein"],
                        "quick_meal": recipe["quick_meal"],
                        "vegetarian": recipe["vegetarian"],
                        "high_protein": recipe["high_protein"]
                    })

                for item in missing_items:
                    if item not in PANTRY_STAPLES:
                        shopping_list.add(item)

        matches.sort(key=lambda x: (x["match_percent"], x["match_count"]), reverse=True)

        if matches:
            st.success("Here are your best meal matches!")

            st.subheader("🍴 Meal Ideas")
            for match in matches:
                tags = []
                tags.append(match["cuisine"])
                tags.append(match["meal_type"])
                if match["vegetarian"]:
                    tags.append("Vegetarian")
                if match["quick_meal"]:
                    tags.append("Quick")
                if match["high_protein"]:
                    tags.append("High Protein")

                st.markdown(f"### {match['name']}")
                st.write(f"**Tags:** {', '.join(tags)}")
                st.write(f"**Protein:** {match['protein']}")
                st.write(f"**Match:** {match['match_count']}/{match['total']} ingredients ({match['match_percent']}%)")
                st.write(f"**You have:** {', '.join(match['have']) if match['have'] else 'None'}")
                st.write(f"**Missing:** {', '.join(match['missing']) if match['missing'] else 'Nothing'}")
                st.divider()

            if shopping_list:
                st.subheader("🛒 Shopping List")
                for item in sorted(shopping_list):
                    st.write(f"- {item}")
        else:
            st.warning("No matches found. Try different ingredients or loosen the filters.")
