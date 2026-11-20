from prettytable import PrettyTable, ALL, DOUBLE_BORDER
import pwinput
import os
import re


def cetak_tabel(field_names, data_rows):
    table = PrettyTable()
    table.field_names = field_names
    table.align = "l"
    table.padding_width = 2
    table.set_style(DOUBLE_BORDER)
    table.hrules = ALL
    for row in data_rows:
        table.add_row(row)
    print(table)

def ambil_password(prompt="Masukkan Password Akun : "):
    return pwinput.pwinput(prompt=prompt, mask="*")

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

class Batal(Exception):
    pass

def input_batal(promt):
    data = input(promt)

    if data.lower() == "batal":
        raise Batal

    return data

def validasi_password(password):
    if len(password) < 4:
        return "Password minimal 4 karekter."

    if len(password) > 8:
        return "Password maksimal 8 karakter."

    if not re.search(r"[A-Z]", password):
        return "Password Harus Mengandung Minimal 1 Huruf Kapital."

    if not re.search(r"[a-z]", password):
        return "Password Harus Mengandung Minimal 1 Huruf Kecil."

    if not re.search(r"\d", password):
        return "Password Harus Mengandung Minimal 1 Angka."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password Harus Memiliki Minimal 1 Simbol"
    
    return "Password Valid Terima Kasih Banyak."

def menu_awal():
    field_names = ["No", "Menu Utama PyCommerce"]
    
    rows = [
        ["1", "🔐 Login"],
        ["2", "📁 Register Akun Baru"],
        ["3", "🔓 Keluar dari Program"]
    ]
    cetak_tabel(field_names, rows)

def menu_admin(username):
    field_names = ["No", f"Opsi Menu Admin ({username})"]
    rows = [
        ["1", "Lihat Daftar Akun User"],
        ["2", "Hapus Akun dari Daftar Akun User"],
        ["3", "Keluar Dari Menu Akses Admin"]
    ]
    cetak_tabel(field_names, rows)

def menu_user(username):
    field_names = ["No", f"Opsi Menu User ({username})"]
    rows = [
        ["1", "Mulai Jual Produk Baru"],
        ["2", "Lihat Katalog & Tambahkan Produk ke Keranjang"],
        ["3", "Lihat Keranjang & Checkout"],
        ["4", "Hapus Produk dari Keranjang"],
        ["5", "Lihat Pesanan Saya"],
        ["6", "Keluar Dari Menu Akses User"]
    ]
    cetak_tabel(field_names, rows)