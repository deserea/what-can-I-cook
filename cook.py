recipes = {
    "Chicken Tacos": ["chicken", "tortillas", "onion", "garlic"],
    "Pasta with Garlic and Olive Oil": ["pasta", "garlic", "olive oil"],
    "Beef Stir-Fry": ["beef", "bell pepper", "onion", "soy sauce"],
    "Breakfast Scramble": ["eggs", "cheese", "onion"],
    "Tomato Grilled Cheese": ["bread", "cheese", "tomato", "butter"],
    "Chicken Orzo Soup": ["chicken", "orzo", "carrot", "celery", "onion"]
}

print("\n🍽️ What Can I Cook? 🍽️\n")

user_input = input("Enter the ingredients you have, separated by commas: ").lower()
ingredients = [item.strip() for item in user_input.split(",")]

matches = []

for recipe, needed_ingredients in recipes.items():
    match_count = sum(1 for item in needed_ingredients if item in ingredients)
    if match_count > 0:
        matches.append((recipe, match_count, needed_ingredients))

matches.sort(key=lambda x: x[1], reverse=True)

if matches:
    print("\nHere are your best matches:\n")
    for recipe, match_count, needed_ingredients in matches:
        print(f"{recipe} ({match_count}/{len(needed_ingredients)} ingredients matched)")
        print(f"Needs: {', '.join(needed_ingredients)}\n")
else:
    print("\nNo matches found. Try entering more ingredients.\n")
