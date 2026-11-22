# from prettytable import PrettyTable, ALL, DOUBLE_BORDER
# from datetime import datetime
# import pwinput
# import os
# import re


# def cetak_tabel(field_names, data_rows):
#     table = PrettyTable()
#     table.field_names = field_names
#     table.align = "l"
#     table.padding_width = 2
#     table.set_style(DOUBLE_BORDER)
#     table.hrules = ALL
#     for row in data_rows:
#         table.add_row(row)
#     print(table)

# def ambil_password(prompt="Masukkan Password Akun : "):
#     return pwinput.pwinput(prompt=prompt, mask="*")

# def bersihkan_layar():
#     os.system('cls' if os.name == 'nt' else 'clear')


# def format_rupiah(angka):
#     return "Rp {:,}".format(angka).replace(",", ".")

# def cetak_struk(username, items, total, saldo=None):
#     print("\n" + "=" * 40)
#     print("STRUK PEMBELIAN PYCOMMERCE")
#     print("=" * 40)
#     print(f"Tanggal : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
#     print(f"pembeli : {username}")
#     print("-" * 40)
#     for nama, harga, jumlah in items:
#         print(nama)
#         print(f"   {jumlah} x {format_rupiah(harga)} = {format_rupiah(harga * jumlah)}")

#     print("-" * 40)
#     print(f"Total Pembayaran : {format_rupiah(total)}")
#     if saldo is not None:
#         print(f"Sisa Saldo : {format_rupiah(saldo)}")
#         print("=" * 40)
#         print("Terimah kasih telah berbelanja!".center(40))

        
# class Batal(Exception):
#     pass

# def input_batal(promt):
#     data = input(promt)

#     if data.lower() == "batal":
#         raise Batal

#     return data

# def validasi_password(password):
#     if len(password) < 4:
#         return "Password minimal 4 karekter."

#     if len(password) > 8:
#         return "Password maksimal 8 karakter."

#     if not re.search(r"[A-Z]", password):
#         return "Password Harus Mengandung Minimal 1 Huruf Kapital."

#     if not re.search(r"[a-z]", password):
#         return "Password Harus Mengandung Minimal 1 Huruf Kecil."

#     if not re.search(r"\d", password):
#         return "Password Harus Mengandung Minimal 1 Angka."

#     if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
#         return "Password Harus Memiliki Minimal 1 Simbol"
    
#     return "Password Valid."

# def menu_awal():
#     field_names = ["No", "Menu Utama PyCommerce"]
    
#     rows = [
#         ["1", "🔐 Login"],
#         ["2", "📁 Register Akun Baru"],
#         ["3", "🔓 Keluar dari Program"]
#     ]
#     cetak_tabel(field_names, rows)

# def menu_admin(username):
#     field_names = ["No", f"Opsi Menu Admin ({username})"]
#     rows = [
#         ["1", "Lihat Daftar Akun User"],
#         ["2", "Hapus Akun dari Daftar Akun User"],
#         ["3", "Keluar Dari Menu Akses Admin"]
#     ]
#     cetak_tabel(field_names, rows)

# def menu_user(username):
#     field_names = ["No", f"Opsi Menu User ({username})"]
#     rows = [
#         ["1", "Mulai Jual Produk Baru"],
#         ["2", "Lihat Katalog & Tambahkan Produk ke Keranjang"],
#         ["3", "Lihat Keranjang & Checkout"],
#         ["4", "Hapus Produk dari Keranjang"],
#         ["5", "Lihat Pesanan Saya"],
#         ["6", "Keluar Dari Menu Akses User"]
#     ]
#     cetak_tabel(field_names, rows)

from prettytable import PrettyTable, ALL, DOUBLE_BORDER
from datetime import datetime
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


def generate_id_produk(produk_dict):
    nomor_tertinggi = 0
    for k_id in produk_dict.keys():
        match = re.fullmatch(r"K(\d{3})", str(k_id))
        if match:
            angka = int(match.group(1))
            if angka > nomor_tertinggi:
                nomor_tertinggi = angka

    nomor_berikutnya = nomor_tertinggi + 1
    if nomor_berikutnya > 999:
        return None

    return f"K{nomor_berikutnya:03d}"


def ambil_password(prompt="Masukkan Password Akun : "):
    return pwinput.pwinput(prompt=prompt, mask="*")

def bersihkan_layar(jeda=False):
    if jeda:
        input()
    os.system("cls" if os.name == "nt" else "clear")

def format_rupiah(angka):
    return "Rp {:,}".format(angka).replace(",", ".")

def cetak_struk(username, items, total, saldo=None):
    print("\n" + "=" * 40)
    print("STRUK PEMBELIAN PYCOMMERCE")
    print("=" * 40)
    print(f"Tanggal : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    print(f"Pembeli : {username}")
    print("-" * 40)
    for nama, harga, jumlah in items:
        print(nama)
        print(f"   {jumlah} x {format_rupiah(harga)} = {format_rupiah(harga * jumlah)}")

    print("-" * 40)
    print(f"Total Pembayaran : {format_rupiah(total)}")
    if saldo is not None:
        print(f"Sisa Saldo       : {format_rupiah(saldo)}")
    print("=" * 40)
    print("Terima kasih telah berbelanja!".center(40))

class Batal(Exception):
    pass

def input_batal(prompt):
    data = input(prompt)
    if data.strip().lower() == "batal":
        raise Batal
    return data


def validasi_username(username):
    if len(username) < 4:
        return "Username minimal 4 karakter."
    if len(username) > 8:
        return "Username maksimal 8 karakter."
    if not re.fullmatch(r"[A-Za-z]+", username):
        return "Username hanya boleh menggunakan huruf (huruf kapital atau huruf kecil)."
    return None

def validasi_password(password):
    if len(password) < 4:
        return "Password minimal 4 karakter."
    if len(password) > 8:
        return "Password maksimal 8 karakter."
    if not re.search(r"[A-Z]", password):
        return "Password harus mengandung minimal 1 huruf kapital."
    if not re.search(r"[a-z]", password):
        return "Password harus mengandung minimal 1 huruf kecil."
    if not re.search(r"\d", password):
        return "Password harus mengandung minimal 1 angka."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password harus memiliki minimal 1 simbol."
    return None

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
        ["2", "Lihat Katalog & Tambahkan ke Keranjang"],
        ["3", "Lihat Pesanan Saya"],
        ["4", "Keluar Dari Menu Akses User"]
    ]
    cetak_tabel(field_names, rows)


def menu_katalog_keranjang(username):
    field_names = ["No", f"Menu Keranjang & Checkout ({username})"]
    rows = [
        ["1", "Lihat Keranjang"],
        ["2", "Hapus Produk dari Keranjang"],
        ["3", "Checkout"],
        ["4", "Kembali ke Menu User"]
    ]
    cetak_tabel(field_names, rows)
    
def menu_user(username):
    field_names = ["No", f"Opsi Menu User ({username})"]
    rows = [
        ["1", "Mulai Jual Produk Baru"],
        ["2", "Kelola Produk Saya"],
        ["3", "Lihat Katalog & Tambahkan ke Keranjang"],
        ["4", "Lihat Pesanan Saya"],
        ["5", "Keluar Dari Menu Akses User"]
    ]
    cetak_tabel(field_names, rows)

def menu_kelola_produk_saya(username):
    field_names = ["No", f"Opsi Kelola Produk ({username})"]
    rows = [
        ["1", "Ubah Detail Produk Saya"],
        ["2", "Hapus Produk Saya"],
        ["3", "Kembali ke Menu User"]
    ]
    cetak_tabel(field_names, rows)