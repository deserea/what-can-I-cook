import json
import streamlit as st

# Load recipes from JSON file
with open("recipes.json", "r", encoding="utf-8") as file:
    recipes = json.load(file)

st.title("🍽️ What Can I Cook?")
st.write("Enter the ingredients you have, separated by commas, and get meal ideas plus a shopping list.")

user_input = st.text_input("Ingredients", placeholder="chicken, tortillas, onion")

if user_input:
    ingredients = [item.strip().lower() for item in user_input.split(",")]
    matches = []
    shopping_list = set()

    for recipe, needed_ingredients in recipes.items():
        match_count = sum(1 for item in needed_ingredients if item in ingredients)

        if match_count > 0:
            missing = [item for item in needed_ingredients if item not in ingredients]
            matches.append((recipe, match_count, needed_ingredients, missing))

            for item in missing:
                shopping_list.add(item)

    matches.sort(key=lambda x: x[1], reverse=True)

    if matches:
        st.subheader("Best Matches")

        for recipe, match_count, needed_ingredients, missing in matches:
            st.markdown(f"### {recipe} ({match_count}/{len(needed_ingredients)} matched)")
            have_items = [i for i in needed_ingredients if i in ingredients]
            st.write("**You have:**", ", ".join(have_items) if have_items else "None")
            st.write("**Missing:**", ", ".join(missing) if missing else "Nothing")

        if shopping_list:
            st.subheader("🛒 Shopping List")
            for item in sorted(shopping_list):
                st.write(f"- {item}")
    else:
        st.warning("No matches found. Try entering more ingredients.")
