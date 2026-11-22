from database import akun_admin, akun_user, simpan_database
from utils import (
    ambil_password,
    input_batal,
    Batal,
    validasi_username,
    validasi_password,
)

def login():
    print("\n=== SILAHKAN LOGIN ===")
    for percobaan in range(3):
        try:
            username = input("Masukkan Username Akun : ").strip()
            password = ambil_password("Masukkan Password Akun : ")
        except Batal:
            print("Login dibatalkan.")
            return None, None, False

        if password.strip().lower() == "batal":
            print("Login dibatalkan.")
            return None, None, False

        if username in akun_admin and akun_admin[username] == password:
            print("\nLogin berhasil!")
            print("Nama akun :", username)
            print("Role      : Admin")
            return username, "admin", False

        elif username in akun_user and akun_user[username] == password:
            print("\nLogin berhasil!")
            print("Nama akun :", username)
            print("Role      : User")
            return username, "user", False

        else:
            print("\n❌ Username atau Password yang Anda Masukkan Salah!")
            print("Sisa percobaan login :", 2 - percobaan)

    print("\n❌ Anda gagal login sebanyak 3 kali. Program dihentikan.")
    return None, None, True

def registrasi():
    print("\n=== REGISTRASI AKUN USER BARU ===")
    print("Ketentuan Username : 4-8 karakter, hanya huruf (A-Z / a-z)")
    print("Ketentuan Password : 4-8 karakter, wajib ada huruf besar, huruf kecil, angka, dan simbol")

    try:
        user_baru = input_batal("Masukkan Username Baru : ").strip()
    except Batal:
        print("Registrasi dibatalkan.")
        return

    pesan_user = validasi_username(user_baru)
    if pesan_user:
        print("❌", pesan_user)
        return

    if user_baru in akun_user or user_baru in akun_admin:
        print("❌ Username tersebut sudah terdaftar!")
        return

    pass_baru = ambil_password("Masukkan Password Baru : ")
    pesan_pass = validasi_password(pass_baru)

    if pesan_pass:
        print("❌", pesan_pass)
        return

    akun_user[user_baru] = pass_baru
    simpan_database()
    print(f"✅ Akun user '{user_baru}' berhasil didaftarkan! Silakan login.")
