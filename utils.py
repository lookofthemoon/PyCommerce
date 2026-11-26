from prettytable import PrettyTable, ALL, DOUBLE_BORDER
from datetime import datetime
import pwinput
import time
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
    
def generate_id_transaksi():
    nomor_tertinggi = 0
    for daftar_trx in riwayat_pesanan.values():
        if not isinstance(daftar_trx, list):
            continue
        for pesanan in daftar_trx:
            id_trx = str(pesanan.get("id_transaksi", ""))
            match = re.fullmatch(r"TRX(\d{3})", id_trx)
            if match:
                angka = int(match.group(1))
                if angka > nomor_tertinggi:
                    nomor_tertinggi = angka
    return f"TRX{nomor_tertinggi + 1:03d}"

def generate_id_produk(produk_dict):
    id_terpakai = set()
    for k_id in produk_dict.keys():
        match = re.fullmatch(r"K(\d{3})", str(k_id).strip().upper())
        if match:
            id_terpakai.add(int(match.group(1)))

    for nomor in range(1, 1000):
        if nomor not in id_terpakai:
            return f"K{nomor:03d}"

    return None

def ambil_password(prompt="Masukkan Password Akun : "):
    return pwinput.pwinput(prompt=prompt, mask="*")

def bersihkan_layar():
    os.system("cls" if os.name == "nt" else "clear")

def bersihkan_layar_dengan_jeda(detik=1.5):
    time.sleep(detik)
    bersihkan_layar()

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

EMOJI_PATTERN = re.compile(
    r"["
    r"\U0001F1E6-\U0001F1FF"
    r"\U0001F300-\U0001F5FF"
    r"\U0001F600-\U0001F64F"
    r"\U0001F680-\U0001F6FF"
    r"\U0001F700-\U0001F77F"
    r"\U0001F780-\U0001F7FF"
    r"\U0001F800-\U0001F8FF"
    r"\U0001F900-\U0001F9FF"
    r"\U0001FA00-\U0001FA6F"
    r"\U0001FA70-\U0001FAFF"
    r"\u2600-\u26FF"
    r"\u2700-\u27BF"
    r"\uFE0F"
    r"\u200D"
    r"]",
    re.UNICODE,
)

SIMBOL_ASCII_PATTERN = re.compile(r"[!@#$%^&*()_\-+=\[\]{};:'\",.<>/?\\|~]")

def mengandung_emoji(teks):
    if not isinstance(teks, str):
        return False
    return bool(EMOJI_PATTERN.search(teks))

def validasi_username(username):
    if mengandung_emoji(username):
        return "Username Tidak Boleh Mengandung Emoji!"
    if len(username) < 4:
        return "Username Minimal 4 Karakter."
    if len(username) > 8:
        return "Username Maksimal 8 Karakter."
    if not re.fullmatch(r"[A-Za-z]+", username):
        return "Username Hanya Boleh Menggunakan Huruf (Huruf Kapital atau Huruf Kecil)!"
    return None

def validasi_password(password):
    if mengandung_emoji(password):
        return "Password Tidak Boleh Mengandung Emoji!"
    if len(password) < 4:
        return "Password Minimal 4 Karakter."
    if len(password) > 8:
        return "Password Maksimal 8 Karakter."
    if not re.search(r"[A-Z]", password):
        return "Password Harus Mengandung Minimal 1 Huruf Kapital."
    if not re.search(r"[a-z]", password):
        return "Password Harus Mengandung Minimal 1 Huruf Kecil."
    if not re.search(r"\d", password):
        return "Password Harus Mengandung Minimal 1 Angka."
    if not SIMBOL_ASCII_PATTERN.search(password):
        return "Password Harus Memiliki Minimal 1 Simbol."
    return None

def cetak_ketentuan(judul, daftar_aturan):
    print(f"\n{judul}")
    field_names = ["Ketentuan", "Aturan Input"]
    cetak_tabel(field_names, daftar_aturan)
    
def menu_awal():
    field_names = ["No", "Menu Utama PyCommerce"]
    rows = [
        ["1", "🔐 Login"],
        ["2", "📁 Register Akun Baru"],
        ["3", "🔓 Keluar dari Program"],
    ]
    cetak_tabel(field_names, rows)

def menu_admin(username):
    field_names = ["No", f"Opsi Menu Admin ({username})"]
    rows = [
        ["1", "Lihat Daftar Akun User (Read)"],
        ["2", "Hapus Akun dari Daftar Akun User (Delete)"],
        ["3", "Kelola Pengajuan Isi Saldo User (Update)"],
        ["4", "Pantau Riwayat Transaksi User (Read)"],
        ["5", "Keluar Dari Menu Akses Admin"],
    ]
    cetak_tabel(field_names, rows)

def menu_user(username):
    field_names = ["No", f"Opsi Menu User ({username})"]
    rows = [
        ["1", "Mulai Jual Produk Baru (Create)"],
        ["2", "Kelola Produk Saya (Update)"],
        ["3", "Lihat Katalog & Tambahkan ke Keranjang (Read & Create)"],
        ["4", "Lihat Pesanan Saya (Read)"],
        ["5", "Saldo & Pengajuan Top-Up (Update)"],
        ["6", "Keluar Dari Menu Akses User"],
    ]
    cetak_tabel(field_names, rows)

def menu_saldo_user(username):
    field_names = ["No", f"Menu Saldo ({username})"]
    rows = [
        ["1", "Ajukan Pengisian Saldo"],
        ["2", "Lihat Riwayat Pengajuan Saldo Saya"],
        ["3", "Kembali ke Menu User"],
    ]
    cetak_tabel(field_names, rows)

def menu_katalog_keranjang(username):
    field_names = ["No", f"Menu Keranjang & Checkout ({username})"]
    rows = [
        ["1", "Lihat Keranjang"],
        ["2", "Hapus Produk dari Keranjang"],
        ["3", "Checkout"],
        ["4", "Kembali ke Menu User"],
    ]
    cetak_tabel(field_names, rows)

def menu_kelola_produk_saya(username):
    field_names = ["No", f"Opsi Kelola Produk ({username})"]
    rows = [
        ["1", "Ubah Detail Produk Saya"],
        ["2", "Hapus Produk Saya"],
        ["3", "Kembali ke Menu User"],
    ]
    cetak_tabel(field_names, rows)