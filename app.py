import json
import streamlit as st

# Page settings
st.set_page_config(page_title="What Can I Cook?", page_icon="🍽️")

# Load recipes from JSON file
with open("recipes.json", "r", encoding="utf-8") as file:
    recipes = json.load(file)

st.title("🍽️ What Can I Cook?")
st.write("Enter the ingredients you have, separated by commas, and get meal ideas plus a shopping list.")

user_input = st.text_input(
    "Ingredients",
    placeholder="chicken, tortillas, onion"
)

if st.button("Find Meals"):
    if not user_input.strip():
        st.warning("Please enter at least one ingredient.")
    else:
        ingredients = [item.strip().lower() for item in user_input.split(",") if item.strip()]
        matches = []
        shopping_list = set()

        for recipe, needed_ingredients in recipes.items():
            match_count = sum(1 for item in needed_ingredients if item in ingredients)

            if match_count > 0:
                missing = [item for item in needed_ingredients if item not in ingredients]
                match_percent = round((match_count / len(needed_ingredients)) * 100)
                matches.append((recipe, match_count, match_percent, needed_ingredients, missing))

                for item in missing:
                    shopping_list.add(item)

        matches.sort(key=lambda x: x[1], reverse=True)

        if matches:
            st.success("Here are your best meal matches!")

            st.subheader("🍴 Meal Ideas")
            for recipe, match_count, match_percent, needed_ingredients, missing in matches:
                have_items = [i for i in needed_ingredients if i in ingredients]

                st.markdown(f"### {recipe}")
                st.write(f"**Match:** {match_count}/{len(needed_ingredients)} ingredients ({match_percent}%)")
                st.write(f"**You have:** {', '.join(have_items) if have_items else 'None'}")
                st.write(f"**Missing:** {', '.join(missing) if missing else 'Nothing'}")
                st.divider()

            if shopping_list:
                st.subheader("🛒 Shopping List")
                for item in sorted(shopping_list):
                    st.write(f"- {item}")
        else:
            st.warning("No matches found. Try entering more ingredients.")
            Upgrade web app with button, match percentages, and improved shopping list
