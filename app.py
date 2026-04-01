import json
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
    "minced beef": "beef",
    "beef mince": "beef",
    "ground turkey": "turkey",
    "ground chicken": "chicken",
    "ground pork": "pork",

    "italian sausage": "sausage",
    "hot italian sausage": "sausage",
    "mild italian sausage": "sausage",
    "breakfast sausage": "sausage",

    "chicken breast": "chicken",
    "chicken breasts": "chicken",
    "chicken thigh": "chicken",
    "chicken thighs": "chicken",
    "shredded chicken": "chicken",

    "bell peppers": "bell pepper",
    "green pepper": "bell pepper",
    "yellow pepper": "bell pepper",
    "orange pepper": "bell pepper",
    "peppers": "bell pepper",
    "jalapenos": "jalapeno",

    "potatoes": "potato",
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
    "pinto beans": "bean",
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

    "brown rice": "rice",
    "white rice": "rice",
    "wild rice": "rice",

    "mozzarella cheese": "mozzarella",
    "cheddar cheese": "cheddar",
    "parmesan cheese": "parmesan",
    "feta cheese": "feta",
    "jack cheese": "monterey jack",
    "monterey jack cheese": "monterey jack",
    "pepper jack cheese": "pepper jack",
    "cotija cheese": "cotija",
    "queso fresco cheese": "queso fresco",
    "shredded cheese": "cheese",
    "mexican blend cheese": "cheese",
    "italian blend cheese": "cheese",
    "cheese blend": "cheese",

    "vegetable oil": "oil",
    "avocado oil": "oil",
    "canola oil": "oil",

    "soy": "soy sauce",
    "tamari": "soy sauce",

    "chicken broth": "broth",
    "beef broth": "broth",
    "vegetable broth": "broth",
    "stock": "broth",
    "chicken stock": "broth",
    "beef stock": "broth",
    "vegetable stock": "broth",

    "spring mix": "lettuce",
    "mixed greens": "lettuce",
    "greens": "lettuce",
    "romaine lettuce": "romaine",

    "cilantro leaves": "cilantro",
    "flat leaf parsley": "parsley",
    "curly parsley": "parsley",

    "green peas": "peas",
    "frozen peas": "peas",

    "seaweed sheets": "seaweed",
    "nori": "seaweed",

    "walnuts": "walnut",
    "olives": "olive",
    "pickles": "pickle",

    "plain yogurt": "yogurt",
    "greek yogurt": "yogurt",

    "chili powder": "chili flakes"
}

INGREDIENT_GROUPS = {
    "Pantry Staples": [
        "olive oil", "oil", "butter", "broth", "soy sauce", "vinegar",
        "salt", "pepper", "black pepper"
    ],
    "Seasonings": [
        "garlic powder", "onion powder", "paprika", "smoked paprika",
        "cumin", "oregano", "basil", "thyme", "rosemary",
        "red pepper flakes", "chili flakes", "cayenne", "cinnamon"
    ],
    "Grains & Starches": [
        "pasta", "rice", "quinoa", "oat", "corn tortilla", "flour tortilla",
        "lettuce wrap", "bread", "potato", "sweet potato", "orzo"
    ],
    "Dairy & Eggs": [
        "milk", "cheddar", "mozzarella", "parmesan", "yogurt", "egg", "feta",
        "cream", "sour cream", "monterey jack", "pepper jack", "cotija",
        "queso fresco", "cheese"
    ],
    "Vegetables": [
        "bell pepper", "carrot", "celery", "spinach", "mushroom", "zucchini",
        "cucumber", "broccoli", "avocado", "lettuce", "corn", "cabbage",
        "romaine", "onion", "red onion"
    ],
    "Beans & Canned Goods": [
        "black bean", "white bean", "kidney bean", "chickpea", "lentil",
        "tomato sauce", "tuna"
    ],
    "Fruit & Brighteners": [
        "lemon", "lime", "apple", "banana", "blueberry", "strawberry", "berry"
    ],
    "Fresh Extras": [
        "cilantro", "parsley", "basil", "dill", "ginger", "green onion",
        "pickle", "olive"
    ]
}

CHEESE_OPTIONS = {
    "cheese",
    "cheddar",
    "mozzarella",
    "parmesan",
    "feta",
    "monterey jack",
    "pepper jack",
    "cotija",
    "queso fresco"
}

MELTING_CHEESE_OPTIONS = {
    "cheese",
    "cheddar",
    "mozzarella",
    "monterey jack",
    "pepper jack"
}

MEXICAN_WRAP_OPTIONS = {
    "corn tortilla",
    "flour tortilla",
    "lettuce wrap"
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

    if recipe_item == "wrap" and user_item in MEXICAN_WRAP_OPTIONS:
        return True

    if recipe_item == "cheese" and user_item in CHEESE_OPTIONS:
        return True

    if recipe_item == "melting cheese" and user_item in MELTING_CHEESE_OPTIONS:
        return True

    if user_item in recipe_item or recipe_item in user_item:
        return True

    return False

def get_entry_label(entry):
    if isinstance(entry, str):
        return normalize_ingredient(entry)

    if isinstance(entry, dict):
        return entry.get("name", "ingredient")

    return str(entry)

def entry_matches_user_ingredients(entry, user_ingredients):
    if isinstance(entry, str):
        normalized_entry = normalize_ingredient(entry)
        return any(ingredient_matches(user_item, normalized_entry) for user_item in user_ingredients)

    if isinstance(entry, dict):
        options = entry.get("options", [])
        return any(
            any(ingredient_matches(user_item, option) for user_item in user_ingredients)
            for option in options
        )

    return False

def get_best_matched_option(entry, user_ingredients):
    if isinstance(entry, str):
        normalized_entry = normalize_ingredient(entry)
        for user_item in user_ingredients:
            if ingredient_matches(user_item, normalized_entry):
                return normalized_entry
        return normalized_entry

    if isinstance(entry, dict):
        options = entry.get("options", [])
        for option in options:
            for user_item in user_ingredients:
                if ingredient_matches(user_item, option):
                    return normalize_ingredient(option)
        return entry.get("name", "ingredient")

    return str(entry)

def get_missing_label(entry):
    if isinstance(entry, str):
        return normalize_ingredient(entry)

    if isinstance(entry, dict):
        name = entry.get("name", "ingredient")
        options = entry.get("options", [])
        if options:
            return f"{name} ({', '.join(options)})"
        return name

    return str(entry)

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

def score_recipe(user_ingredients, required_ingredients, optional_ingredients):
    matched_required = []
    missing_required = []

    for entry in required_ingredients:
        if entry_matches_user_ingredients(entry, user_ingredients):
            matched_required.append(get_best_matched_option(entry, user_ingredients))
        else:
            missing_required.append(get_missing_label(entry))

    matched_optional = []
    missing_optional = []

    for entry in optional_ingredients:
        if entry_matches_user_ingredients(entry, user_ingredients):
            matched_optional.append(get_best_matched_option(entry, user_ingredients))
        else:
            missing_optional.append(get_missing_label(entry))

    required_total = len(required_ingredients)
    required_match_count = len(matched_required)
    required_match_percent = round((required_match_count / required_total) * 100) if required_total else 0

    return {
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_optional": matched_optional,
        "missing_optional": missing_optional,
        "required_total": required_total,
        "required_match_count": required_match_count,
        "required_match_percent": required_match_percent
    }

def categorize_suggested_items(items):
    categorized = {group: [] for group in INGREDIENT_GROUPS}
    uncategorized = []

    for item in sorted(items):
        normalized_item = normalize_ingredient(item)
        placed = False

        for group, group_items in INGREDIENT_GROUPS.items():
            if normalized_item in group_items:
                categorized[group].append(normalized_item)
                placed = True
                break

        if not placed:
            uncategorized.append(normalized_item)

    if uncategorized:
        categorized["Other"] = sorted(list(set(uncategorized)))

    for group in list(categorized.keys()):
        categorized[group] = sorted(list(set(categorized[group])))

    return categorized

def flatten_recipe_items_for_suggestions(items):
    flattened = []

    for entry in items:
        if isinstance(entry, str):
            flattened.append(normalize_ingredient(entry))
        elif isinstance(entry, dict):
            name = entry.get("name", "")
            options = entry.get("options", [])

            if name == "wrap":
                flattened.extend(["corn tortilla", "flour tortilla", "lettuce wrap"])
            elif name == "cheese":
                flattened.extend(["cheddar", "monterey jack", "cotija", "queso fresco", "mozzarella", "feta"])
            elif name == "melting cheese":
                flattened.extend(["cheddar", "monterey jack", "mozzarella", "pepper jack"])
            else:
                flattened.extend([normalize_ingredient(opt) for opt in options])

    return flattened

def get_suggested_add_ons(base_ingredients, filtered_recipes, limit=20):
    suggestion_scores = {}

    for recipe in filtered_recipes:
        result = score_recipe(base_ingredients, recipe["required"], recipe.get("optional", []))

        if result["required_match_count"] > 0 and result["required_match_percent"] < 100:
            for item in result["missing_required"]:
                suggestion_scores[item] = suggestion_scores.get(item, 0) + 3

            optional_items = flatten_recipe_items_for_suggestions(recipe.get("optional", []))
            for item in optional_items:
                if item not in base_ingredients:
                    suggestion_scores[item] = suggestion_scores.get(item, 0) + 1

    ranked = sorted(suggestion_scores.items(), key=lambda x: x[1], reverse=True)
    return [item for item, _ in ranked[:limit]]

def build_matches(user_ingredients, filtered_recipes):
    matches = []

    for recipe in filtered_recipes:
        result = score_recipe(user_ingredients, recipe["required"], recipe.get("optional", []))

        if result["required_match_count"] > 0:
            matches.append({
                "name": recipe["name"],
                "required_match_count": result["required_match_count"],
                "required_total": result["required_total"],
                "required_match_percent": result["required_match_percent"],
                "matched_required": result["matched_required"],
                "missing_required": result["missing_required"],
                "matched_optional": result["matched_optional"],
                "missing_optional": result["missing_optional"],
                "cuisine": recipe["cuisine"],
                "meal_type": recipe["meal_type"],
                "protein": recipe["protein"],
                "quick_meal": recipe["quick_meal"],
                "vegetarian": recipe["vegetarian"],
                "high_protein": recipe["high_protein"],
                "instructions": recipe.get("instructions", [])
            })

    matches.sort(
        key=lambda x: (
            x["required_match_percent"],
            x["required_match_count"],
            len(x["matched_optional"])
        ),
        reverse=True
    )

    return matches

def split_results(base_matches, expanded_matches):
    base_map = {m["name"]: m for m in base_matches}
    expanded_map = {m["name"]: m for m in expanded_matches}

    can_make_now = []
    can_make_with_addons = []
    still_needs_shopping = []

    for name, match in expanded_map.items():
        base_percent = base_map[name]["required_match_percent"] if name in base_map else 0
        expanded_percent = match["required_match_percent"]

        if base_percent == 100:
            can_make_now.append(match)
        elif expanded_percent == 100:
            can_make_with_addons.append(match)
        else:
            still_needs_shopping.append(match)

    sort_key = lambda x: (
        x["required_match_percent"],
        x["required_match_count"],
        len(x["matched_optional"])
    )

    return (
        sorted(can_make_now, key=sort_key, reverse=True),
        sorted(can_make_with_addons, key=sort_key, reverse=True),
        sorted(still_needs_shopping, key=sort_key, reverse=True)
    )

def tags_for_match(match):
    tags = [match["cuisine"], match["meal_type"]]
    if match["vegetarian"]:
        tags.append("Vegetarian")
    if match["quick_meal"]:
        tags.append("Quick")
    if match["high_protein"]:
        tags.append("High Protein")
    return tags

def display_recipe_card(match):
    st.markdown(f"### {match['name']}")
    st.write(f"**Tags:** {', '.join(tags_for_match(match))}")
    st.write(f"**Protein:** {match['protein']}")
    st.write(
        f"**Required Match:** {match['required_match_count']}/{match['required_total']} "
        f"ingredients ({match['required_match_percent']}%)"
    )
    st.write(f"**You have:** {', '.join(match['matched_required']) if match['matched_required'] else 'None'}")
    st.write(f"**Still need:** {', '.join(match['missing_required']) if match['missing_required'] else 'Nothing'}")

    if match["matched_optional"]:
        st.write(f"**Flavor boosters you have:** {', '.join(match['matched_optional'])}")

    if match["missing_optional"]:
        st.write(f"**Would be even better with:** {', '.join(match['missing_optional'])}")

    st.divider()

st.title("🍽️ What Can I Cook? v7")
st.write("Start with what you definitely have, then let the app uncover pantry extras, substitutions, and flexible recipe matches.")

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
    placeholder="ground beef, tomato, onion, garlic, corn tortillas, monterey jack"
)

base_ingredients = []
if base_input.strip():
    raw_base = [item.strip() for item in base_input.split(",") if item.strip()]
    base_ingredients = [normalize_ingredient(item) for item in raw_base]

suggested_add_ons = []
if base_ingredients:
    suggested_add_ons = get_suggested_add_ons(base_ingredients, filtered_recipes)

selected_addons = []
if base_ingredients and suggested_add_ons:
    st.subheader("🧠 You may also have some of these pantry or fridge extras")
    st.write("Select anything you think you probably have. These can unlock more complete meals and better flavor.")

    categorized_suggestions = categorize_suggested_items(suggested_add_ons)
    for group, items in categorized_suggestions.items():
        if items:
            selected = st.multiselect(group, items, key=f"addons_{group}")
            selected_addons.extend(selected)

if st.button("Find Meals"):
    if not base_ingredients:
        st.warning("Please enter at least one ingredient you definitely have.")
    else:
        expanded_ingredients = sorted(set(base_ingredients + [normalize_ingredient(i) for i in selected_addons]))

        base_matches = build_matches(base_ingredients, filtered_recipes)
        expanded_matches = build_matches(expanded_ingredients, filtered_recipes)

        if strong_matches_only:
            base_matches = [m for m in base_matches if m["required_match_percent"] >= 50]
            expanded_matches = [m for m in expanded_matches if m["required_match_percent"] >= 50]

        can_make_now, can_make_with_addons, still_needs_shopping = split_results(base_matches, expanded_matches)

        st.success("Here are your best meal options.")

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

        all_detail_matches = can_make_now + can_make_with_addons + still_needs_shopping

        if all_detail_matches:
            st.subheader("🔎 Recipe Detail View")
            recipe_names = [m["name"] for m in all_detail_matches]
            selected_recipe_name = st.selectbox("Choose a recipe to inspect", recipe_names)

            selected_match = next((m for m in all_detail_matches if m["name"] == selected_recipe_name), None)

            if selected_match:
                st.markdown(f"## {selected_match['name']}")
                st.write(f"**Tags:** {', '.join(tags_for_match(selected_match))}")
                st.write(f"**Protein:** {selected_match['protein']}")

                col_a, col_b = st.columns(2)

                with col_a:
                    st.markdown("### Required Ingredients")
                    for item in selected_match["matched_required"]:
                        st.write(f"✅ {item}")
                    for item in selected_match["missing_required"]:
                        st.write(f"⬜ {item}")

                with col_b:
                    st.markdown("### Optional Flavor Boosters")
                    if selected_match["matched_optional"]:
                        for item in selected_match["matched_optional"]:
                            st.write(f"✨ {item}")
                    if selected_match["missing_optional"]:
                        for item in selected_match["missing_optional"]:
                            st.write(f"➕ {item}")
                    if not selected_match["matched_optional"] and not selected_match["missing_optional"]:
                        st.write("No optional boosters listed.")

                focused_shopping = sorted(set(selected_match["missing_required"] + selected_match["missing_optional"]))
                if focused_shopping:
                    st.markdown("### Focused Shopping List")
                    for item in focused_shopping:
                        st.write(f"- {item}")

                if selected_match["instructions"]:
                    st.markdown("### Quick Directions")
                    for i, step in enumerate(selected_match["instructions"], start=1):
                        st.write(f"{i}. {step}")

        shopping_list = set()
        for match in still_needs_shopping:
            for item in match["missing_required"]:
                if item not in expanded_ingredients:
                    shopping_list.add(item)

        if shopping_list:
            st.subheader("📝 Shopping List")
            for item in sorted(shopping_list):
                st.write(f"- {item}")
