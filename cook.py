import json

# Load recipes from JSON file
with open("recipes.json", "r", encoding="utf-8") as file:
    recipes = json.load(file)

print("\n🍽️ What Can I Cook? 🍽️\n")

user_input = input("Enter the ingredients you have, separated by commas: ").lower()
ingredients = [item.strip() for item in user_input.split(",")]

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
    print("\nHere are your best matches:\n")

    for recipe, match_count, needed_ingredients, missing in matches:
        print(f"{recipe} ({match_count}/{len(needed_ingredients)} ingredients matched)")
        print(f"You have: {', '.join([i for i in needed_ingredients if i in ingredients])}")
        print(f"Missing: {', '.join(missing)}\n")

    if shopping_list:
        print("🛒 Shopping List:")
        for item in sorted(shopping_list):
            print(f"- {item}")
        print()

else:
    print("\nNo matches found. Try entering more ingredients.\n")
