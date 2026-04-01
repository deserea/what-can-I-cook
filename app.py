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

    "all purpose flour": "flour",
    "ap flour": "flour",

    "chili powder": "chili flakes"
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
        "ketchup", "barbecue sauce", "salsa", "honey"
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
        if options:
            return f"{name} ({', '.join(options)})"
        return name

    return str(entry)

def skill_rank(level):
    ranks = {"Beginner": 1, "Intermediate": 2, "Advanced": 3}
    return ranks.get(level, 1)

def recipe_matches_filters(recipe, selected_cuisine, selected_meal_type, selected_skill_level, selected_time, vegetarian_only, quick_only, high_protein_only):
    if selected_cuisine != "All" and recipe["cuisine"] != selected_cuisine:
        return False

    if selected_meal_type != "All" and recipe["meal_type"] != selected_meal_type:
        return False

    if selected_skill_level != "All":
        if skill_rank(recipe.get("skill_level", "Beginner")) > skill_rank(selected_skill_level):
            return False

    if vegetarian_only and not recipe["vegetarian"]:
        return False

    if quick_only and not recipe["quick_meal"]:
        return False

    if high_protein_only and not recipe["high_protein"]:
        return False

    time_limit = TIME_FILTERS[selected_time]
    recipe_time = recipe.get("time_minutes", 30)

    if selected_time == "More advanced / longer cook":
        return recipe_time > 60

    if time_limit is not None and recipe_time > time_limit:
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

def flatten_items_for_suggestions(items):
    flattened = []

    for entry in items:
        if isinstance(entry, str):
            flattened.append(normalize_ingredient(entry))
        elif isinstance(entry, dict):
            name = entry.get("name", "")
            if name in {"wrap", "mexican wrap"}:
                flattened.extend(["corn tortilla", "flour tortilla", "lettuce wrap"])
            elif name in {"cheese", "mexican cheese"}:
                flattened.extend(["cheddar", "monterey jack", "cotija", "queso fresco", "pepper jack", "colby jack", "mozzarella"])
            elif name == "melting cheese":
                flattened.extend(["cheddar", "monterey jack", "mozzarella", "pepper jack", "colby jack", "american cheese"])
            elif name == "italian cheese":
                flattened.extend(["parmesan", "pecorino", "asiago", "romano", "mozzarella"])
            elif name == "greek cheese":
                flattened.extend(["feta"])
            else:
                flattened.extend([normalize_ingredient(opt) for opt in entry.get("options", [])])

    return flattened

def get_suggested_add_ons(base_ingredients, filtered_recipes, limit=24):
    scores = {}

    for recipe in filtered_recipes:
        result = score_recipe(base_ingredients, recipe["required"], recipe.get("optional", []))

        if result["required_match_count"] > 0 and result["required_match_percent"] < 100:
            for item in result["missing_required"]:
                scores[item] = scores.get(item, 0) + 3

            for item in flatten_items_for_suggestions(recipe.get("optional", [])):
                normalized = normalize_ingredient(item)
                if normalized not in base_ingredients:
                    scores[normalized] = scores.get(normalized, 0) + 1

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [item for item, _ in ranked[:limit]]

def categorize_suggestions(items):
    categorized = {group: [] for group in INGREDIENT_GROUPS}
    uncategorized = []

    for item in sorted(set(items)):
        placed = False
        normalized = normalize_ingredient(item)

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

def build_matches(user_ingredients, filtered_recipes, servings):
    matches = []

    for recipe in filtered_recipes:
        result = score_recipe(user_ingredients, recipe["required"], recipe.get("optional", []))

        if result["required_match_count"] > 0:
            matches.append({
                "id": recipe.get("id", recipe["name"].lower().replace(" ", "_")),
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
                "skill_level": recipe.get("skill_level", "Beginner"),
                "time_minutes": recipe.get("time_minutes", 30),
                "servings": servings,
                "quick_meal": recipe["quick_meal"],
                "vegetarian": recipe["vegetarian"],
                "high_protein": recipe["high_protein"],
                "questions": recipe.get("questions", []),
                "shopping_tips": recipe.get("shopping_tips", []),
                "chef_upgrade": recipe.get("chef_upgrade", []),
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
    still_needs_more = []

    for name, match in expanded_map.items():
        base_percent = base_map[name]["required_match_percent"] if name in base_map else 0
        expanded_percent = match["required_match_percent"]

        if base_percent == 100:
            can_make_now.append(match)
        elif expanded_percent == 100:
            can_make_with_addons.append(match)
        else:
            still_needs_more.append(match)

    sort_key = lambda x: (x["required_match_percent"], x["required_match_count"], len(x["matched_optional"]))
    return (
        sorted(can_make_now, key=sort_key, reverse=True),
        sorted(can_make_with_addons, key=sort_key, reverse=True),
        sorted(still_needs_more, key=sort_key, reverse=True)
    )

def tags_for_match(match):
    tags = [
        match["cuisine"],
        match["meal_type"],
        match["skill_level"],
        f"{match['time_minutes']} min"
    ]
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
    st.write(f"**Feeds:** about {match['servings']}")
    st.write(f"**Required Match:** {match['required_match_count']}/{match['required_total']} ({match['required_match_percent']}%)")
    st.write(f"**You have:** {', '.join(match['matched_required']) if match['matched_required'] else 'None'}")
    st.write(f"**Still need:** {', '.join(match['missing_required']) if match['missing_required'] else 'Nothing'}")

    if match["matched_optional"]:
        st.write(f"**Flavor boosters you have:** {', '.join(match['matched_optional'])}")

    if match["missing_optional"]:
        st.write(f"**Would be even better with:** {', '.join(match['missing_optional'])}")

    st.divider()

st.title("🍽️ What Can I Cook?")
st.write("A home cooking assistant for American kitchens. Tell it what you have, what you may also have, what you are open to shopping for, and what kind of cooking mood you are in.")

with st.sidebar:
    st.header("Meal Preferences")

    cuisines = sorted(set(recipe["cuisine"] for recipe in recipes))
    meal_types = sorted(set(recipe["meal_type"] for recipe in recipes))

    selected_cuisine = st.selectbox("Cuisine you're feeling", ["All"] + cuisines)
    selected_meal_type = st.selectbox("Meal type", ["All"] + meal_types)
    selected_skill_level = st.selectbox("Cooking level", ["All", "Beginner", "Intermediate", "Advanced"])
    selected_time = st.selectbox(
        "Time commitment",
        ["Any", "Quick meals", "1 hour or less", "2 hours or less", "More advanced / longer cook"]
    )
    servings = st.number_input("How many people should this feed?", min_value=1, max_value=12, value=2, step=1)

    st.header("Extra Filters")
    vegetarian_only = st.checkbox("Vegetarian only")
    quick_only = st.checkbox("Quick meals only")
    high_protein_only = st.checkbox("High protein only")
    strong_matches_only = st.checkbox("Show only strong matches (50%+)", value=False)
    show_chef_upgrades = st.checkbox("Show chef-level upgrade ideas", value=True)

filtered_recipes = [
    recipe for recipe in recipes
    if recipe_matches_filters(
        recipe,
        selected_cuisine,
        selected_meal_type,
        selected_skill_level,
        selected_time,
        vegetarian_only,
        quick_only,
        high_protein_only
    )
]

base_input = st.text_input(
    "What ingredients do you definitely have?",
    placeholder="ground beef, onion, garlic, flour tortillas, monterey jack"
)

maybe_have_input = st.text_input(
    "What other ingredients might you also have?",
    placeholder="lime, cilantro, sour cream, rice, olive oil"
)

willing_to_shop_input = st.text_input(
    "What are you willing to shop for if needed?",
    placeholder="avocado, broth, pasta, yogurt"
)

base_ingredients = [normalize_ingredient(x) for x in base_input.split(",") if x.strip()] if base_input.strip() else []
maybe_have_ingredients = [normalize_ingredient(x) for x in maybe_have_input.split(",") if x.strip()] if maybe_have_input.strip() else []
willing_to_shop = [normalize_ingredient(x) for x in willing_to_shop_input.split(",") if x.strip()] if willing_to_shop_input.strip() else []

current_ingredients = sorted(set(base_ingredients + maybe_have_ingredients))

suggested_add_ons = []
if current_ingredients:
    suggested_add_ons = get_suggested_add_ons(current_ingredients, filtered_recipes)

selected_addons = []
if current_ingredients and suggested_add_ons:
    st.subheader("Pantry or fridge extras you may also have")
    st.write("Select anything you think is probably around. These can unlock better matches and fuller meals.")

    categorized = categorize_suggestions(suggested_add_ons)
    for group, items in categorized.items():
        if items:
            picked = st.multiselect(group, items, key=f"addons_{group}")
            selected_addons.extend(picked)

if st.button("Find Meals"):
    if not current_ingredients:
        st.warning("Please enter at least one ingredient you definitely have.")
    else:
        expanded_ingredients = sorted(set(current_ingredients + [normalize_ingredient(x) for x in selected_addons]))
        shopping_enabled_ingredients = sorted(set(expanded_ingredients + willing_to_shop))

        matches_now = build_matches(expanded_ingredients, filtered_recipes, servings)
        matches_with_shopping = build_matches(shopping_enabled_ingredients, filtered_recipes, servings)

        if strong_matches_only:
            matches_now = [m for m in matches_now if m["required_match_percent"] >= 50]
            matches_with_shopping = [m for m in matches_with_shopping if m["required_match_percent"] >= 50]

        can_make_now, can_make_if_shop, still_missing = split_results(matches_now, matches_with_shopping)

        st.success("Here are your best options.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Can make now", len(can_make_now))
        col2.metric("Can make if you shop", len(can_make_if_shop))
        col3.metric("Still missing more", len(still_missing))

        if can_make_now:
            st.subheader("✅ You can make these now")
            for match in can_make_now:
                display_recipe_card(match)

        if can_make_if_shop:
            st.subheader("🛒 You can make these if you buy the items you said you are open to shopping for")
            for match in can_make_if_shop:
                display_recipe_card(match)

        if still_missing:
            st.subheader("✨ Close matches that still need a few more things")
            for match in still_missing[:10]:
                display_recipe_card(match)

        all_matches = can_make_now + can_make_if_shop + still_missing

        if all_matches:
            st.subheader("🔎 Recipe Detail View")
            selected_name = st.selectbox("Choose a recipe to inspect", [m["name"] for m in all_matches])
            selected_match = next((m for m in all_matches if m["name"] == selected_name), None)

            if selected_match:
                st.markdown(f"## {selected_match['name']}")
                st.write(f"**Tags:** {', '.join(tags_for_match(selected_match))}")
                st.write(f"**Protein:** {selected_match['protein']}")
                st.write(f"**Estimated Time:** {selected_match['time_minutes']} minutes")
                st.write(f"**Skill Level:** {selected_match['skill_level']}")
                st.write(f"**Feeds:** about {selected_match['servings']}")

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

                if selected_match["questions"]:
                    st.markdown("### Helpful Questions")
                    for question in selected_match["questions"]:
                        st.write(f"- {question}")

                focused_shopping = sorted(set(selected_match["missing_required"] + selected_match["missing_optional"]))
                if focused_shopping:
                    st.markdown("### Focused Shopping List")
                    for item in focused_shopping:
                        st.write(f"- {item}")

                if selected_match["shopping_tips"]:
                    st.markdown("### Smart Grocery Add-Ons")
                    for tip in selected_match["shopping_tips"]:
                        st.write(f"- {tip}")

                if selected_match["instructions"]:
                    st.markdown("### Instructions")
                    for i, step in enumerate(selected_match["instructions"], start=1):
                        st.write(f"{i}. {step}")

                if show_chef_upgrades and selected_match["chef_upgrade"]:
                    st.markdown("### Chef-Level Upgrade")
                    for idea in selected_match["chef_upgrade"]:
                        st.write(f"- {idea}")

        master_shopping = set()
        for match in still_missing:
            for item in match["missing_required"]:
                if item not in shopping_enabled_ingredients:
                    master_shopping.add(item)

        if master_shopping:
            st.subheader("📝 Master Shopping List")
            for item in sorted(master_shopping):
                st.write(f"- {item}")
