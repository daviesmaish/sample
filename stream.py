import streamlit as st
import json

# Constants
HEALTH_CHALLENGES = {
    "diabetes": ["whole grains", "leafy greens", "berries", "nuts", "fish"],
    "high blood pressure": ["bananas", "beets", "oats", "fatty fish", "garlic"],
    "weight loss": ["fruits", "vegetables", "lean proteins", "legumes", "whole grains"],
    "high cholesterol": ["oats", "avocados", "fatty fish", "walnuts", "olive oil"],
    "digestive issues": ["yogurt", "fiber-rich foods", "bananas", "whole grains", "fermented foods"],
    "low energy": ["nuts", "whole grains", "fruits", "lean meats", "dark chocolate"],
    "skin health": ["avocados", "blueberries", "salmon", "sweet potatoes", "olive oil"],
    "immune support": ["citrus fruits", "garlic", "spinach", "yogurt", "almonds"],
    "bone health": ["dairy products", "leafy greens", "salmon", "fortified foods", "nuts"],
    "heart health": ["berries", "oats", "dark chocolate", "olive oil", "fatty fish"],
    "stress relief": ["dark chocolate", "green tea", "berries", "nuts", "oats"],
    "inflammation": ["leafy greens", "berries", "fatty fish", "turmeric", "olive oil"],
    "mood improvement": ["bananas", "berries", "oats", "dark chocolate", "nuts"],
    "hydration": ["cucumbers", "watermelon", "celery", "orange", "strawberries"],
    "hair health": ["nuts", "salmon", "eggs", "berries", "avocados"]
}

FOOD_ITEMS = [
    {"name": "Oatmeal", "price": 2.5, "category": "Breakfast", "recipe": "Mix oats with water or milk, cook until soft."},
    {"name": "Banana", "price": 0.5, "category": "Fruit", "recipe": "Peel and eat."},
    {"name": "Salmon", "price": 6.0, "category": "Protein", "recipe": "Grill or bake with seasoning."},
    {"name": "Spinach", "price": 1.5, "category": "Vegetable", "recipe": "Sauté with garlic."},
    {"name": "Almonds", "price": 3.0, "category": "Snacks", "recipe": "Eat raw or roasted."},
    {"name": "Yogurt", "price": 1.0, "category": "Dairy", "recipe": "Enjoy plain or with fruits."},
    {"name": "Garlic", "price": 0.3, "category": "Herb", "recipe": "Chop and add to dishes."},
    {"name": "Beets", "price": 1.2, "category": "Vegetable", "recipe": "Roast or boil."},
    {"name": "Berries", "price": 3.5, "category": "Fruit", "recipe": "Eat fresh or add to smoothies."},
    {"name": "Whole Grains", "price": 2.0, "category": "Grain", "recipe": "Use in bread or cereals."},
]

class User:
    def __init__(self, username, budget, age, weight, height, health_condition, food_choices=None, meals_logged=None):
        self.username = username
        self.budget = budget
        self.age = age
        self.weight = weight
        self.height = height
        self.health_condition = health_condition
        self.food_choices = food_choices if food_choices is not None else []
        self.meals_logged = meals_logged if meals_logged is not None else []

class UserManager:
    def __init__(self):
        self.users = {}
        self.load_users("users.json")

    def register_user(self, username, budget, age, weight, height, health_condition):
        if username in self.users:
            return False
        self.users[username] = User(username, budget, age, weight, height, health_condition)
        self.save_users("users.json")
        return True

    def login_user(self, username):
        return self.users.get(username)

    def save_users(self, filename):
        with open(filename, 'w') as out_file:
            json.dump({username: user.__dict__ for username, user in self.users.items()}, out_file)

    def load_users(self, filename):
        try:
            with open(filename, 'r') as in_file:
                users_data = json.load(in_file)
                if isinstance(users_data, dict):  # Check if it's a dictionary
                    for username, data in users_data.items():
                        if all(key in data for key in ["username", "budget", "age", "weight", "height", "health_condition"]):
                            self.users[username] = User(**data)
                        else:
                            st.error(f"Missing data for user: {username}")
                else:
                    st.error("User data is not in the expected format. Please check the JSON file.")
        except FileNotFoundError:
            st.error("User data file not found.")
        except json.JSONDecodeError:
            st.error("Error reading user data. Please check the JSON format.")

def display_user_profile(user):
    st.subheader("Your Profile")
    st.write(f"**Username:** {user.username}")
    st.write(f"**Budget:** ${user.budget:.2f}")
    st.write(f"**Age:** {user.age}")
    st.write(f"**Weight:** {user.weight} kg")
    st.write(f"**Height:** {user.height} cm")
    st.write(f"**Health Condition:** {user.health_condition}")

def display_recommended_foods(health_condition):
    st.write(f"### Foods recommended for {health_condition}:")
    recommended_foods = HEALTH_CHALLENGES.get(health_condition, [])
    available_foods = [food for food in FOOD_ITEMS if food["name"].lower() in map(str.lower, recommended_foods)]
    
    if available_foods:
        for food in available_foods:
            st.write(f"- **{food['name']}** - **${food['price']}** ({food['category']})")
            st.write(f"  - **Recipe:** {food['recipe']}")
    else:
        st.write("No foods available for this health condition.")

def main():
    # Custom CSS
    st.markdown("""
        <style>
            body {
                background-color: #f0f4f8;
                font-family: 'Arial', sans-serif;
            }
            .header {
                text-align: center;
                color: #2c3e50;
            }
            .section-title {
                color: #2980b9;
            }
            .stButton>button {
                background-color: #2980b9;
                color: white;
            }
            .stButton>button:hover {
                background-color: #3498db;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Health Challenge Food Recommendations", anchor="header")
    user_manager = UserManager()

    menu = ["Home", "Register", "Login"]
    choice = st.sidebar.selectbox("Select an option", menu)

    if choice == "Home":
        st.subheader("Welcome to the Health Challenge Food Recommendations App!")
        st.write("Get personalized food recommendations based on your health challenges.")
        st.write("### Tips for a Healthy Lifestyle:")
        st.write("1. Stay hydrated by drinking plenty of water.")
        st.write("2. Incorporate a variety of fruits and vegetables into your diet.")
        st.write("3. Exercise regularly to maintain a healthy weight.")
        st.write("4. Get enough sleep to support overall health.")

    elif choice == "Register":
        st.subheader("Register New User")
        username = st.text_input("Username")
        budget = st.number_input("Budget ($)", min_value=0.0, format="%.2f")
        age = st.number_input("Age", min_value=0)
        weight = st.number_input("Weight (kg)", min_value=0.0)
        height = st.number_input("Height (cm)", min_value=0.0)
        health_condition = st.selectbox("Health Condition", list(HEALTH_CHALLENGES.keys()))

        if st.button("Register"):
            if user_manager.register_user(username, budget, age, weight, height, health_condition):
                st.success("User registered successfully!")
            else:
                st.error("Username already exists.")

    elif choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        current_user = user_manager.login_user(username)

        if current_user:
            st.success(f"Logged in as **{current_user.username}**")
            display_user_profile(current_user)  # Display user profile
            health_condition = st.selectbox("Select a health challenge to solve", list(HEALTH_CHALLENGES.keys()))
            if st.button("Get Food Recommendations"):
                display_recommended_foods(health_condition)
        else:
            st.error("User not found.")

if __name__ == "__main__":
    main()