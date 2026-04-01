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
    "vegetable broth": "broth",
    "spring mix": "lettuce",
    "greens": "lettuce"
}

PANTRY_STAPLES = {
    "salt", "pepper", "oil", "olive oil", "butter", "water",
    "garlic powder", "onion powder", "paprika", "smoked paprika",
    "cumin", "oregano", "basil", "thyme", "rosemary",
    "red pepper flakes", "chili flakes", "cayenne",
    "soy sauce", "vinegar", "broth"
}

INGREDIENT_GROUPS = {
    "Pantry Staples": [
        "olive oil", "butter", "broth", "soy sauce", "vinegar", "salt", "pepper"
    ],
    "Seasonings": [
        "garlic powder", "onion powder", "paprika", "smoked paprika",
        "cumin", "oregano", "basil", "thyme", "rosemary",
        "red pepper flakes", "chili flakes", "cayenne", "cinnamon"
    ],
    "Grains & Starches": [
        "pasta", "rice", "quinoa", "oat", "tortilla", "bread", "potato", "sweet potato", "orzo"
    ],
    "Dairy & Eggs": [
        "milk", "cheddar", "mozzarella", "parmesan", "yogurt", "egg", "feta"
    ],
    "Vegetables": [
        "bell pepper", "carrot", "celery", "spinach", "mushroom", "zucchini",
        "cucumber", "broccoli", "avocado", "lettuce", "corn", "cabbage", "romaine"
    ],
    "Beans & Canned Goods": [
        "black bean", "white bean", "kidney bean", "chickpea", "lentil", "tomato sauce"
    ],
    "Fruit & Brighteners": [
        "lemon", "lime", "apple", "banana", "blueberry", "strawberry"
    ]
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
        if found:
            matched_items.append(recipe_item)
        else:
            missing_items.append(recipe_item)

    match_count = len(matched_items)
    total_count = len(normalized_recipe)
    match_percent = round((match_count / total_count) * 100) if total_count else 0

    return matched_items, missing_items, match_count, total_count, match_percent

def categorize_suggested_items(items):
    categorized = {group: [] for group in INGREDIENT_GROUPS}
    uncategorized = []

    for item in sorted(items):
        placed = False
        for group, group_items in INGREDIENT_GROUPS.items():
            if item in group_items:
                categorized[group].append(item)
                placed = True
                break
        if not placed:
            uncategorized.append(item)

    if uncategorized:
        categorized["Other"] = uncategorized

    return categorized

def get_suggested_add_ons(base_ingredients, filtered_recipes, limit=18):
    suggestion_scores = {}

    for recipe in filtered_recipes:
        matched_items, missing_items, match_count, total_count, match_percent = score_recipe(
            base_ingredients, recipe["ingredients"]
        )

        # near-match recipes are most useful for prompting pantry extras
        if match_count > 0 and match_percent < 100:
            for item in missing_items:
                item = normalize_ingredient(item)
                suggestion_scores[item] = suggestion_scores.get(item, 0) + 1

    # rank by how often they help unlock recipes
    ranked = sorted(suggestion_scores.items(), key=lambda x: x[1], reverse=True)
    return [item for item, score in ranked[:limit]]

def build_matches(user_ingredients, filtered_recipes):
    matches = []

    for recipe in filtered_recipes:
        matched_items, missing_items, match_count, total_count, match_percent = score_recipe(
            user_ingredients, recipe["ingredients"]
        )

        if match_count > 0:
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

    matches.sort(key=lambda x: (x["match_percent"], x["match_count"]), reverse=True)
    return matches

def split_results(base_matches, expanded_matches):
    base_map = {m["name"]: m for m in base_matches}
    expanded_map = {m["name"]: m for m in expanded_matches}

    can_make_now = []
    can_make_with_addons = []
    still_needs_shopping = []

    for name, match in expanded_map.items():
        base_percent = base_map[name]["match_percent"] if name in base_map else 0
        expanded_percent = match["match_percent"]

        if base_percent == 100:
            can_make_now.append(match)
        elif expanded_percent == 100:
            can_make_with_addons.append(match)
        else:
            still_needs_shopping.append(match)

    can_make_now.sort(key=lambda x: (x["match_percent"], x["match_count"]), reverse=True)
    can_make_with_addons.sort(key=lambda x: (x["match_percent"], x["match_count"]), reverse=True)
    still_needs_shopping.sort(key=lambda x: (x["match_percent"], x["match_count"]), reverse=True)

    return can_make_now, can_make_with_addons, still_needs_shopping

def display_recipe_card(match):
    tags = [match["cuisine"], match["meal_type"]]
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

st.title("🍽️ What Can I Cook? v3")
st.write("Start with what you definitely have, then let the app help you uncover pantry extras that can turn simple ingredients into better meals.")

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

filtered_recipes = [
    recipe for recipe in recipes
    if recipe_matches_filters(
        recipe,
        selected_cuisine,
        selected_meal_type,
        vegetarian_only,
        quick_only,
        high_protein_only
    )
]

base_input = st.text_input(
    "Ingredients you definitely have",
    placeholder="ground beef, tomatoes, onion, garlic"
)

base_ingredients = []
if base_input.strip():
    raw_base = [item.strip() for item in base_input.split(",") if item.strip()]
    base_ingredients = [normalize_ingredient(item) for item in raw_base]

suggested_add_ons = []
if base_ingredients:
    suggested_add_ons = get_suggested_add_ons(base_ingredients, filtered_recipes)

if base_ingredients and suggested_add_ons:
    st.subheader("🧠 You may also have some of these pantry or fridge extras")
    st.write("Select anything you think you probably have. These can unlock more complete or tastier dishes.")

    categorized_suggestions = categorize_suggested_items(suggested_add_ons)
    selected_addons = []

    for group, items in categorized_suggestions.items():
        if items:
            selected = st.multiselect(group, items, key=f"addons_{group}")
            selected_addons.extend(selected)
else:
    selected_addons = []

if st.button("Find Meals"):
    if not base_ingredients:
        st.warning("Please enter at least one ingredient you definitely have.")
    else:
        expanded_ingredients = sorted(set(base_ingredients + [normalize_ingredient(i) for i in selected_addons]))

        base_matches = build_matches(base_ingredients, filtered_recipes)
        expanded_matches = build_matches(expanded_ingredients, filtered_recipes)

        if strong_matches_only:
            base_matches = [m for m in base_matches if m["match_percent"] >= 50]
            expanded_matches = [m for m in expanded_matches if m["match_percent"] >= 50]

        can_make_now, can_make_with_addons, still_needs_shopping = split_results(base_matches, expanded_matches)

        st.success("Here are your meal options.")

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Recipes you can make now", len(can_make_now))
        with col2:
            st.metric("Recipes unlocked with pantry add-ons", len(can_make_with_addons))

        if can_make_now:
            st.subheader("✅ You can make these now")
            for match in can_make_now:
                display_recipe_card(match)

        if can_make_with_addons:
            st.subheader("✨ You can make these if you also have the selected pantry extras")
            for match in can_make_with_addons:
                display_recipe_card(match)

        if still_needs_shopping:
            st.subheader("🛒 These still need a few things")
            for match in still_needs_shopping[:10]:
                display_recipe_card(match)

        shopping_list = set()
        for match in still_needs_shopping:
            for item in match["missing"]:
                if item not in PANTRY_STAPLES and item not in expanded_ingredients:
                    shopping_list.add(item)

        if shopping_list:
            st.subheader("📝 Shopping List")
            for item in sorted(shopping_list):
                st.write(f"- {item}")
