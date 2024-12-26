import random
import tkinter as tk
from tkinter import messagebox
from sympy import mod_inverse, isprime

# Функция для генерации простого числа заданного размера (в битах)
def generate_prime(bits):
    while True:
        prime_candidate = random.getrandbits(bits)
        if isprime(prime_candidate):
            return prime_candidate

# Генерация ключей для RSA
def generate_rsa_keys(bits=128):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = 65537
    if phi_n % e == 0:
        e = 3
    d = mod_inverse(e, phi_n)
    return (e, n), (d, n)

# Шифрование
def rsa_encrypt(message, public_key):
    e, n = public_key
    message_int = int.from_bytes(message.encode('utf-8'), byteorder='big')
    cipher_int = pow(message_int, e, n)
    return cipher_int

# Дешифрование
def rsa_decrypt(cipher_int, private_key):
    d, n = private_key
    message_int = pow(cipher_int, d, n)
    message_bytes = message_int.to_bytes((message_int.bit_length() + 7) // 8, byteorder='big')
    return message_bytes.decode('utf-8')

# Интерфейс
def encrypt_message():
    message = entry_message.get()
    if not message:
        messagebox.showwarning("Ошибка", "Введите сообщение!")
        return
    cipher_text = rsa_encrypt(message, public_key)
    entry_cipher.delete(0, tk.END)
    entry_cipher.insert(0, str(cipher_text))

def decrypt_message():
    cipher_text = entry_cipher.get()
    if not cipher_text:
        messagebox.showwarning("Ошибка", "Введите зашифрованное сообщение!")
        return
    try:
        decrypted_message = rsa_decrypt(int(cipher_text), private_key)
        entry_decrypted.delete(0, tk.END)
        entry_decrypted.insert(0, decrypted_message)
    except Exception as e:
        messagebox.showerror("Ошибка", "Невозможно расшифровать сообщение!")

# Генерация ключей RSA
public_key, private_key = generate_rsa_keys()

# Окно
root = tk.Tk()
root.title("RSA Шифратор/Дешифратор")


root.geometry("600x300")

# Поля для ввода и вывода
font_size = 14
tk.Label(root, text="Введите сообщение для шифрования:", font=("Arial", font_size)).grid(row=0, column=0, padx=10, pady=10)
entry_message = tk.Entry(root, width=60, font=("Arial", font_size))
entry_message.grid(row=0, column=1, padx=10, pady=10)

tk.Label(root, text="Зашифрованное сообщение:", font=("Arial", font_size)).grid(row=1, column=0, padx=10, pady=10)
entry_cipher = tk.Entry(root, width=60, font=("Arial", font_size))
entry_cipher.grid(row=1, column=1, padx=10, pady=10)

tk.Label(root, text="Расшифрованное сообщение:", font=("Arial", font_size)).grid(row=2, column=0, padx=10, pady=10)
entry_decrypted = tk.Entry(root, width=60, font=("Arial", font_size))
entry_decrypted.grid(row=2, column=1, padx=10, pady=10)


btn_encrypt = tk.Button(root, text="Зашифровать", command=encrypt_message, font=("Arial", font_size))
btn_encrypt.grid(row=3, column=0, padx=10, pady=10)

btn_decrypt = tk.Button(root, text="Расшифровать", command=decrypt_message, font=("Arial", font_size))
btn_decrypt.grid(row=3, column=1, padx=10, pady=10)

# Запуск
root.mainloop()
