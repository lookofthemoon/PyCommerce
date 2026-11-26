from database import akun_admin, akun_user, saldo_user, simpan_database
from utils import (
    ambil_password,
    input_batal,
    Batal,
    validasi_username,
    validasi_password,
    bersihkan_layar_dengan_jeda,
    cetak_ketentuan,
    bersihkan_layar,
)

def login():
    print("\n=== SILAHKAN LOGIN ===")
    for percobaan in range(3):
        try:
            username = input("Masukkan Username Akun : ").strip()
            password = ambil_password("Masukkan Password Akun : ")
        except Batal:
            print("❗ Login Dibatalkan.")
            bersihkan_layar_dengan_jeda(1.5)
            return None, None, False

        if password.strip().lower() == "batal":
            print("❗ Login Dibatalkan.")
            bersihkan_layar_dengan_jeda(1.5)
            return None, None, False

        if username in akun_admin and akun_admin[username] == password:
            print("\n✅ Login Berhasil!")
            print("Nama akun :", username)
            print("Role      : Admin")
            bersihkan_layar_dengan_jeda(1.5)
            return username, "admin", False

        elif username in akun_user and akun_user[username] == password:
            print("\n✅ Login Berhasil!")
            print("Nama akun :", username)
            print("Role      : User")
            bersihkan_layar_dengan_jeda(1.5)
            return username, "user", False

        else:
            print("\n❗ Username atau Password yang Anda Masukkan Salah!")
            print("Sisa Percobaan Login :", 2 - percobaan)
            if percobaan < 2:
                bersihkan_layar_dengan_jeda(1.8)

    print("\n❗ Anda Gagal Login Sebanyak 3 Kali. Program Dihentikan.")
    bersihkan_layar_dengan_jeda(1.8)
    return None, None, True


def registrasi():
    while True:
        bersihkan_layar()
        print("\n=== REGISTRASI AKUN USER BARU ===")
        print("(Ketik 'batal' untuk kembali ke Menu Utama)")
        cetak_ketentuan(
            "--- KETENTUAN USERNAME ---",
            [
                ["Panjang Karakter", "4 - 8 Karakter"],
                ["Jenis Karakter", "Hanya Huruf (A-Z / a-z)"],
                ["Larangan Emoji", "Tidak Boleh Mengandung Emoji"],
            ],
        )
        cetak_ketentuan(
            "--- KETENTUAN PASSWORD ---",
            [
                ["Panjang Karakter", "4 - 8 Karakter"],
                ["Huruf Kapital", "Wajib Minimal 1 Huruf Besar (A-Z)"],
                ["Huruf Kecil", "Wajib Minimal 1 Huruf Kecil (a-z)"],
                ["Angka", "Wajib Minimal 1 Angka (0-9)"],
                ["Simbol", "Wajib Minimal 1 Simbol (Contoh: !@#$%^&*)"],
                ["Larangan Emoji", "Tidak Boleh Mengandung Emoji"],
            ],
        )

        try:
            user_baru = input_batal("Masukkan Username Baru : ").strip()
        except Batal:
            print("❗ Registrasi Dibatalkan.")
            bersihkan_layar_dengan_jeda(1.5)
            return

        pesan_user = validasi_username(user_baru)
        if pesan_user:
            print("❗", pesan_user)
            bersihkan_layar_dengan_jeda(1.8)
            continue

        if user_baru in akun_user or user_baru in akun_admin:
            print("❗ Username Tersebut Sudah Terdaftar!")
            bersihkan_layar_dengan_jeda(1.8)
            continue

        try:
            pass_baru = ambil_password("Masukkan Password Baru : ")
        except Batal:
            print("❗ Registrasi Dibatalkan.")
            bersihkan_layar_dengan_jeda(1.5)
            return

        if pass_baru.strip().lower() == "batal":
            print("❗ Registrasi Dibatalkan.")
            bersihkan_layar_dengan_jeda(1.5)
            return

        pesan_pass = validasi_password(pass_baru)
        if pesan_pass:
            print("❗", pesan_pass)
            bersihkan_layar_dengan_jeda(1.8)
            continue

        akun_user[user_baru] = pass_baru
        saldo_user[user_baru] = 0
        simpan_database()
        print(f"✅ Akun user '{user_baru}' Berhasil Didaftarkan! Silahkan Login.")
        bersihkan_layar_dengan_jeda(1.8)
        return