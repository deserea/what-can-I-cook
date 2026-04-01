import json
import re
import streamlit as st
from collections import defaultdict

# ====================== CONFIG ======================
st.set_page_config(page_title="What Can I Cook?", page_icon="🍽️", layout="wide")

# ====================== LOAD DATA ======================
with open("recipes.json", "r", encoding="utf-8") as file:
    loaded = json.load(file)

recipes = loaded["recipes"] if isinstance(loaded, dict) else loaded

# ====================== OPTIONS ======================
CUISINE_OPTIONS = [
    "All","American","Southern","BBQ","Comfort Food","Italian","French","Spanish",
    "German","Eastern European / Russian","Mediterranean","Greek","Mexican","Tex-Mex",
    "New Mexican","Caribbean","Peruvian / Central & South American","Chinese","Japanese",
    "Thai","Korean","Indian","Filipino","Hawaiian","Pacific Island","Middle Eastern",
    "Ethiopian","African","Kosher","Halal","Native American"
]

MEAL_STYLE_OPTIONS = [
    "All","Comfort Food","Quick & Easy","BBQ & Grilled","One-Pot Meals","Soups & Stews",
    "Salads & Bowls","Sandwiches & Wraps","Rice Dishes","Pasta Dishes","Seafood",
    "Street Food Style","Breakfast/Brunch","Dessert","Snack / Appetizer",
    "Smoothies & Shakes","Hors d'oeuvres"
]

MEAL_GOAL_OPTIONS = [
    "All","Comfort Food","Protein Packed","Low Carb","Keto","GLP-1 Friendly"
]

TIME_FILTERS = {
    "Any": None,
    "Quick (<30 min)": 30,
    "1 hour or less": 60,
    "2 hours or less": 120,
    "Advanced (long cook)": 9999
}

# ====================== SIMPLE NORMALIZER ======================
def normalize(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text

# ====================== MATCHING ======================
def score_recipe(user_ingredients, recipe):
    required = recipe.get("required", [])
    optional = recipe.get("optional", [])

    matched_required = []
    missing_required = []

    for item in required:
        if any(normalize(item) in normalize(u) or normalize(u) in normalize(item) for u in user_ingredients):
            matched_required.append(item)
        else:
            missing_required.append(item)

    matched_optional = []
    for item in optional:
        if any(normalize(item) in normalize(u) or normalize(u) in normalize(item) for u in user_ingredients):
            matched_optional.append(item)

    total = len(required)
    matched = len(matched_required)

    percent = int((matched / total) * 100) if total else 100

    return {
        "percent": percent,
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_optional": matched_optional
    }

# ====================== FILTER ======================
def passes_filters(recipe, cuisine, style, goal, time_limit):
    if cuisine != "All" and recipe.get("cuisine") != cuisine:
        return False
    if style != "All" and recipe.get("meal_style") != style:
        return False
    if goal != "All":
        key = goal.lower().replace(" ", "_").replace("-", "")
        if not recipe.get(key):
            return False
    if time_limit:
        if recipe.get("time_minutes", 9999) > time_limit:
            return False
    return True

# ====================== UI ======================
st.title("🍽️ What Can I Cook?")
st.markdown("Let’s build your meal step-by-step.")

# STEP 1
selected_cuisine = st.selectbox("1️⃣ Cuisine", CUISINE_OPTIONS)

# STEP 2
selected_skill = st.selectbox("2️⃣ Skill Level", ["All","Beginner","Intermediate","Advanced"])

# STEP 3
selected_time = st.selectbox("3️⃣ Time", list(TIME_FILTERS.keys()))

# STEP 4
selected_meal_style = st.selectbox("4️⃣ Meal Style", MEAL_STYLE_OPTIONS)

# STEP 5
selected_meal_goal = st.selectbox("5️⃣ Goal", MEAL_GOAL_OPTIONS)

# STEP 6
user_input = st.text_area(
    "6️⃣ Enter your ingredients (one per line)",
    placeholder="chicken\nrice\ngarlic\nonion",
    height=150
)

user_ingredients = [line.strip() for line in user_input.split("\n") if line.strip()]

# ====================== PROCESS ======================
if user_ingredients:

    filtered = []

    for recipe in recipes:
        if not passes_filters(
            recipe,
            selected_cuisine,
            selected_meal_style,
            selected_meal_goal,
            TIME_FILTERS[selected_time]
        ):
            continue

        score = score_recipe(user_ingredients, recipe)

        if score["percent"] > 0:
            filtered.append((recipe, score))

    filtered.sort(key=lambda x: x[1]["percent"], reverse=True)

    st.subheader(f"Results ({len(filtered)})")

    if filtered:

        for recipe, score in filtered[:15]:

            with st.expander(f"{recipe['name']} — {score['percent']}% match"):

                st.write(f"**Cuisine:** {recipe.get('cuisine')}")
                st.write(f"**Time:** {recipe.get('time_minutes')} min")
                st.write(f"**Skill:** {recipe.get('skill_level')}")

                if score["matched_required"]:
                    st.success("You have: " + ", ".join(score["matched_required"]))

                if score["missing_required"]:
                    st.error("Missing: " + ", ".join(score["missing_required"]))

                if score["matched_optional"]:
                    st.info("Optional: " + ", ".join(score["matched_optional"]))

                st.subheader("Ingredients (with measurements)")
                for ing in recipe.get("ingredients_full", []):
                    st.write(f"- {ing}")

                st.subheader("Instructions")
                for step in recipe.get("instructions", []):
                    st.write(f"- {step}")

                if recipe.get("chef_upgrade"):
                    st.subheader("Chef Upgrade")
                    for tip in recipe["chef_upgrade"]:
                        st.write(f"- {tip}")

    else:
        st.warning("No matches found. Try adding more ingredients.")

else:
    st.info("👈 Enter ingredients to begin")

st.caption("Built to reduce food waste and spark cooking creativity 🍳")