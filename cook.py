import json

# Load recipes
with open("recipes.json", "r", encoding="utf-8") as file:
    recipes = json.load(file)

print("\n🍽️ What Can I Cook? 🍽️\n")

user_input = input("Enter the ingredients you have, separated by commas: ").lower()
ingredients = [item.strip() for item in user_input.split(",")]

matches = []

for recipe, needed_ingredients in recipes.items():
    match_count = sum(1 for item in needed_ingredients if item in ingredients)

    if match_count > 0:
        missing = [item for item in needed_ingredients if item not in ingredients]
        matches.append((recipe, match_count, needed_ingredients, missing))

matches.sort(key=lambda x: x[1], reverse=True)

if matches:
    print("\nHere are your best matches:\n")

    for i, (recipe, match_count, needed_ingredients, missing) in enumerate(matches, 1):
        print(f"{i}. {recipe} ({match_count}/{len(needed_ingredients)} ingredients matched)")

    # 👇 NEW PART
    choice = input("\nSelect a recipe number to see details (or press Enter to skip): ")

    if choice.isdigit():
        index = int(choice) - 1

        if 0 <= index < len(matches):
            recipe, match_count, needed_ingredients, missing = matches[index]

            print(f"\n🍴 {recipe}")
            print(f"You have: {', '.join([i for i in needed_ingredients if i in ingredients])}")
            print(f"Missing: {', '.join(missing)}\n")

            if missing:
                print("🛒 Shopping List:")
                for item in missing:
                    print(f"- {item}")
                print()
        else:
            print("\nInvalid selection.\n")

else:
    print("\nNo matches found. Try entering more ingredients.\n")
