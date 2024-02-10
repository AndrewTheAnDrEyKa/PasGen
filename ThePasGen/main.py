import random
import tkinter as tk
from tkinter import messagebox
from telegram.ext import Updater, CommandHandler, MessageHandler

TOKEN = "6869338202:AAGPTc38jeljdrv5WgtA3wOZWbEofhA_t0k"

def generate_password(length=8):
    characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+"
    password = ''.join(random.choice(characters) for i in range(length))
    return password

def save_password(password):
    with open("passwords.txt", "a") as file:
        file.write(password + "\n")

def generate(update, context):
    length = int(context.args[0]) if len(context.args) > 0 else 8
    password = generate_password(length)
    save_password(password)
    update.message.reply_text(f"Generated password: {password}")

def show_gui():
    def generate_and_display_password():
        length = int(length_entry.get())
        password = generate_password(length)
        password_entry.delete(0, tk.END)
        password_entry.insert(0, password)

    def save_and_display_password():
        password = password_entry.get()
        save_password(password)
        messagebox.showinfo("Saved", "Password saved successfully!")

    root = tk.Tk()
    root.title("Password Generator")

    # Создание элементов интерфейса
    length_label = tk.Label(root, text="Password Length:")
    length_label.grid(row=0, column=0, padx=10, pady=10)

    length_entry = tk.Entry(root)
    length_entry.grid(row=0, column=1, padx=10, pady=10)

    generate_button = tk.Button(root, text="Generate Password", command=generate_and_display_password)
    generate_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    password_label = tk.Label(root, text="Generated Password:")
    password_label.grid(row=2, column=0, padx=10, pady=10)

    password_entry = tk.Entry(root)
    password_entry.grid(row=2, column=1, padx=10, pady=10)

    save_button = tk.Button(root, text="Save Password", command=save_and_display_password)
    save_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

def handle_message(update, context):
    if update.message.text.startswith('/generate'):
        generate(update, context)

if __name__ == "__main__":
    # Запуск GUI
    show_gui()

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("generate", generate))

    dispatcher.add_handler(MessageHandler(None, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()
