from database import akun_admin, akun_user, saldo_user, simpan_database
from utils import (
    ambil_password,
    input_batal,
    Batal,
    validasi_username,
    validasi_password,
    bersihkan_layar_dengan_jeda,
)


def login():
    print("\n=== SILAHKAN LOGIN ===")
    for percobaan in range(3):
        try:
            username = input("Masukkan Username Akun : ").strip()
            password = ambil_password("Masukkan Password Akun : ")
        except Batal:
            print("Login dibatalkan.")
            bersihkan_layar_dengan_jeda(1.5)
            return None, None, False

        if password.strip().lower() == "batal":
            print("Login dibatalkan.")
            bersihkan_layar_dengan_jeda(1.5)
            return None, None, False

        if username in akun_admin and akun_admin[username] == password:
            print("\nLogin berhasil!")
            print("Nama akun :", username)
            print("Role      : Admin")
            bersihkan_layar_dengan_jeda(1.5)
            return username, "admin", False

        elif username in akun_user and akun_user[username] == password:
            print("\nLogin berhasil!")
            print("Nama akun :", username)
            print("Role      : User")
            bersihkan_layar_dengan_jeda(1.5)
            return username, "user", False

        else:
            print("\n❌ Username atau Password yang Anda Masukkan Salah!")
            print("Sisa percobaan login :", 2 - percobaan)
            if percobaan < 2:
                bersihkan_layar_dengan_jeda(1.8)

    print("\n❌ Anda gagal login sebanyak 3 kali. Program dihentikan.")
    bersihkan_layar_dengan_jeda(1.8)
    return None, None, True


def registrasi():
    print("\n=== REGISTRASI AKUN USER BARU ===")
    print("Ketentuan Username : 4-8 karakter, hanya huruf (A-Z / a-z)")
    print("Ketentuan Password : 4-8 karakter, wajib ada huruf besar, huruf kecil, angka, dan simbol")

    try:
        user_baru = input_batal("Masukkan Username Baru : ").strip()
    except Batal:
        print("Registrasi dibatalkan.")
        bersihkan_layar_dengan_jeda(1.5)
        return

    pesan_user = validasi_username(user_baru)
    if pesan_user:
        print("❌", pesan_user)
        bersihkan_layar_dengan_jeda(1.8)
        return

    if user_baru in akun_user or user_baru in akun_admin:
        print("❌ Username tersebut sudah terdaftar!")
        bersihkan_layar_dengan_jeda(1.8)
        return

    pass_baru = ambil_password("Masukkan Password Baru : ")
    pesan_pass = validasi_password(pass_baru)

    if pesan_pass:
        print("❌", pesan_pass)
        bersihkan_layar_dengan_jeda(1.8)
        return

    akun_user[user_baru] = pass_baru
    saldo_user[user_baru] = 0
    simpan_database()
    print(f"✅ Akun user '{user_baru}' berhasil didaftarkan! Silakan login.")
    bersihkan_layar_dengan_jeda(1.8)