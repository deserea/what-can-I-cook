# 🍽️ What Can I Cook?

A simple and interactive Python web app that suggests meal ideas based on the ingredients you already have.

Instead of wondering what to make, just type what’s in your kitchen and get instant recommendations plus a smart shopping list.

---

## 🚀 Live App

👉 https://what-can-i-cook.streamlit.app

---

## ✨ Features

- Enter ingredients you already have  
- Get meal suggestions ranked by best match  
- View match percentages for each recipe  
- See which ingredients you have vs. missing  
- Automatically generates a shopping list  
- Clean, interactive web interface  

---

## 🧠 How it works

1. User enters ingredients (comma-separated)  
2. App compares input against stored recipes (JSON)  
3. Calculates match score and percentage  
4. Displays best matching meals  
5. Builds a shopping list from missing ingredients  

---

## 🛠️ Tech Stack

- Python  
- Streamlit (web app framework)  
- JSON (data storage)  

---

## 💻 Run locally (beginner friendly)

1. Click the green Code button  
2. Select Download ZIP  
3. Unzip the folder  
4. Make sure Python is installed → https://python.org  
5. Open Terminal / Command Prompt in the folder  

Run:

python cook.py

---

## 🌐 Run as a web app locally

Install Streamlit:

pip install streamlit

Run the app:

streamlit run app.py

Then open the browser link provided.

---

## 📂 Project Structure

what-can-i-cook/

├── app.py           # Streamlit web app  
├── cook.py          # Command-line version  
├── recipes.json     # Recipe data  
├── requirements.txt # Dependencies  
└── README.md  

---

## 🔮 Future Improvements

- Add more recipes dynamically  
- Connect to a live recipe API  
- Add dietary filters (vegan, keto, gluten-free)  
- Save favorite meals  
- User accounts / preferences  
- Mobile-friendly UI enhancements  

---

## 👩‍💻 Author

Built by Deserea

Exploring Python, APIs, data, and automation.  
Background in strategy and program leadership, now building technical products.

---

## 💫 Why this project matters

This project demonstrates:

- Working with structured data (JSON)  
- User input handling  
- Algorithmic matching logic  
- Building and deploying a live web app  
- Translating real-world problems into code  

---

✨ Always learning and building.
