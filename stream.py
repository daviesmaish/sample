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

    def update_user(self, username, **kwargs):
        user = self.users.get(username)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            self.save_users("users.json")
            return True
        return False

    def save_users(self, filename):
        with open(filename, 'w') as out_file:
            json.dump({username: user.__dict__ for username, user in self.users.items()}, out_file)

    def load_users(self, filename):
        try:
            with open(filename, 'r') as in_file:
                users_data = json.load(in_file)
                if isinstance(users_data, dict):
                    for username, data in users_data.items():
                        self.users[username] = User(**data)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            pass

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

def place_order(user, user_manager):
    st.subheader("Place an Order")
    selected_foods = st.multiselect(
        "Select foods to order:",
        FOOD_ITEMS,
        format_func=lambda x: f"{x['name']} - ${x['price']}"
    )
    
    # Styling for buttons
    if st.button("Confirm Order", key="confirm_order", help="Confirm your selected food items"):
        total_cost = sum(item["price"] for item in selected_foods)
        if total_cost > user.budget:
            st.warning(f"Order exceeds your budget by ${total_cost - user.budget:.2f}.")
        else:
            st.success(f"Order placed successfully! Total cost: ${total_cost:.2f}.")
            user.food_choices.extend([item["name"] for item in selected_foods])
            user_manager.save_users("users.json")

def main():
    # CSS styling
    st.markdown("""
        <style>
            .main {
                background-color: #f8f9fa;
                padding: 20px;
                border-radius: 10px;
            }
            h1, h2, h3 {
                color: #343a40;
            }
            .stButton {
                background-color: #007bff;
                color: black;
                border-radius: 5px;
                font-size: 16px;  /* Increase font size */
                padding: 10px;    /* Add padding */
            }
            .stButton:hover {
                background-color: #0056b3;
            }
            .stMultiselect {
                margin-bottom: 20px;
            }
            .welcome {
                text-align: center;
                margin-bottom: 30px;
            }
            .intro {
                font-size: 1.1em;
                line-height: 1.5;
            }
            .benefits {
                margin-top: 20px;
                padding: 10px;
                background-color: #e9ecef;
                border-radius: 5px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.title("Health Challenge Food Recommendations")
    user_manager = UserManager()

    menu = ["Home", "Register", "Login"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        st.write("<div class='welcome'><h2>Welcome to Your Health Companion!</h2></div>", unsafe_allow_html=True)
        
        st.write("<div class='intro'>"
                 "Are you looking to improve your health through better food choices? "
                 "Our application provides personalized food recommendations tailored to your specific health conditions. "
                 "Whether you're managing diabetes, high blood pressure, or simply looking to eat healthier, we have you covered!"
                 "</div>", unsafe_allow_html=True)

        st.write("<div class='benefits'>"
                 "<h3>Why Choose Us?</h3>"
                 "<ul>"
                 "<li><strong>Personalized Recommendations:</strong> Get food suggestions based on your health needs.</li>"
                 "<li><strong>Easy to Use:</strong> Simple interface to register and start receiving advice.</li>"
                 "<li><strong>Stay Within Budget:</strong> Plan your meals without exceeding your budget.</li>"
                 "<li><strong>Track Your Progress:</strong> Log your meals and see how you’re doing over time.</li>"
                 "</ul>"
                 "</div>", unsafe_allow_html=True)

        st.write("<div class='intro'>"
                 "To get started, please register or log in to access tailored food recommendations and order your meals directly."
                 "</div>", unsafe_allow_html=True)

    elif choice == "Register":
        st.subheader("Register")
        username = st.text_input("Username")
        budget = st.number_input("Budget ($)", min_value=0.0, format="%.2f")
        age = st.number_input("Age", min_value=0)
        weight = st.number_input("Weight (kg)", min_value=0.0)
        height = st.number_input("Height (cm)", min_value=0.0)
        health_condition = st.selectbox("Health Condition", list(HEALTH_CHALLENGES.keys()))

        if st.button("Register"):
            if user_manager.register_user(username, budget, age, weight, height, health_condition):
                st.success("Registration successful!")
            else:
                st.error("Username already exists.")

    elif choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        current_user = user_manager.login_user(username)

        if current_user:
            st.success(f"Welcome back, {current_user.username}!")
            display_user_profile(current_user)

            st.subheader("Update Profile")
            updated_budget = st.number_input("Update Budget ($)", value=current_user.budget, format="%.2f")
            updated_weight = st.number_input("Update Weight (kg)", value=current_user.weight)
            updated_height = st.number_input("Update Height (cm)", value=current_user.height)
            updated_health_condition = st.selectbox("Update Health Condition", list(HEALTH_CHALLENGES.keys()), index=list(HEALTH_CHALLENGES.keys()).index(current_user.health_condition))

            # Styling for the update button
            if st.button("Update Profile", key="update_profile"):
                if user_manager.update_user(
                    username,
                    budget=updated_budget,
                    weight=updated_weight,
                    height=updated_height,
                    health_condition=updated_health_condition
                ):
                    st.success("Profile updated successfully!")
                else:
                    st.error("Error updating profile.")

            display_recommended_foods(current_user.health_condition)
            place_order(current_user, user_manager)
        else:
            st.error("User not found.")

if __name__ == "__main__":
    main()
