import json
import re
import streamlit as st

st.set_page_config(page_title="What Can I Cook?", page_icon="🍽️")

with open("recipes.json", "r", encoding="utf-8") as file:
    recipes = json.load(file)

# Ingredient aliases for common variations
ALIASES = {
    "tomatoes": "tomato",
    "cherry tomatoes": "tomato",
    "roma tomatoes": "tomato",
    "onions": "onion",
    "red onions": "onion",
    "yellow onions": "onion",
    "garlic cloves": "garlic",
    "cloves garlic": "garlic",
    "ground beef": "beef",
    "minced beef": "beef",
    "beef mince": "beef",
    "italian sausage": "sausage",
    "hot italian sausage": "sausage",
    "mild italian sausage": "sausage",
    "chicken breast": "chicken",
    "chicken breasts": "chicken",
    "chicken thighs": "chicken",
    "bell peppers": "bell pepper",
    "peppers": "bell pepper",
    "eggs": "egg",
    "tortillas": "tortilla"
}

def singularize(word):
    word = word.strip().lower()

    if word in ALIASES:
        return ALIASES[word]

    # basic plural handling
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

    return singularize(text)

def ingredient_matches(user_item, recipe_item):
    user_item = normalize_ingredient(user_item)
    recipe_item = normalize_ingredient(recipe_item)

    if user_item == recipe_item:
        return True

    # partial match either direction
    if user_item in recipe_item or recipe_item in user_item:
        return True

    return False

st.title("🍽️ What Can I Cook?")
st.write("Enter any ingredients you have, singular or plural, and get meal ideas plus a smart shopping list.")

user_input = st.text_input(
    "Ingredients",
    placeholder="ground beef, tomatoes, onions, garlic, pasta"
)

if st.button("Find Meals"):
    if not user_input.strip():
        st.warning("Please enter at least one ingredient.")
    else:
        raw_ingredients = [item.strip() for item in user_input.split(",") if item.strip()]
        user_ingredients = [normalize_ingredient(item) for item in raw_ingredients]

        matches = []
        shopping_list = set()

        for recipe_name, recipe_ingredients in recipes.items():
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

            if match_count > 0:
                match_percent = round((match_count / len(normalized_recipe)) * 100)

                matches.append({
                    "recipe": recipe_name,
                    "match_count": match_count,
                    "match_percent": match_percent,
                    "have": matched_items,
                    "missing": missing_items,
                    "total": len(normalized_recipe)
                })

                for item in missing_items:
                    shopping_list.add(item)

        matches.sort(key=lambda x: (x["match_percent"], x["match_count"]), reverse=True)

        if matches:
            st.success("Here are your best meal matches!")

            st.subheader("🍴 Meal Ideas")
            for match in matches:
                st.markdown(f"### {match['recipe']}")
                st.write(f"**Match:** {match['match_count']}/{match['total']} ingredients ({match['match_percent']}%)")
                st.write(f"**You have:** {', '.join(match['have']) if match['have'] else 'None'}")
                st.write(f"**Missing:** {', '.join(match['missing']) if match['missing'] else 'Nothing'}")
                st.divider()

            if shopping_list:
                st.subheader("🛒 Shopping List")
                for item in sorted(shopping_list):
                    st.write(f"- {item}")
        else:
            st.warning("No matches found. Try entering different ingredients.")
