from database import akun_admin, akun_user, simpan_data
from utils import ambil_password, input_batal, Batal, SALDO_AWAL, validasi_password


def login():
    print("")
    print("=== SILAHKAN LOGIN ===")

    # maksimal 3 kali percobaan login
    for percobaan in range(3):
        try:
            username = input("Masukkan Username Akun : ")
            password = ambil_password("Masukkan Password Akun (ketik 'batal' untuk kembali) : ")
        
        # FITUR BATAL
        except Batal:
         print("Login dibatalkan.")
         return None, None

    # CEK ADMIN/USER
    if username in akun_admin and akun_admin[username] == password:
        print("Login berhasil!")
        print("Nama akun :", username)
        print("Role : Admin")
        return username, "admin"
    
    elif username in akun_user and akun_user[username] == password:
        print("Login berhasil!")
        print("Nama akun :", username)
        print("Role : User")
        return username, "user"
    else:
        print("\n❌ Username atau Password yang Anda Masukkan Salah!")
        print("Sisa percobaan login :", 2 - percobaan)

    # JIKA GAGAL 3 KALI
    print(" Anda gagal login sebanyak 3 kali.")
    return None, None


def registrasi():
    print("\n=== REGISTRASI AKUN USER BARU ===")

    try:
        user_baru = input_batal("Masukkan Username Baru : ")

    # FITUR BATAL
    except Batal:
        print("Registrasi dibatalkan.")
        return
    
    if user_baru in akun_user or user_baru in akun_admin:
        print("❌ Username tersebut sudah terdaftar!")
    else:
        pass_baru = ambil_password("Masukkan Password Baru : ")
        # Validasi password
        pesan = validasi_password(pass_baru)

        if pesan:
            print("❌", pesan)
            return

        akun_user[user_baru] = {
            "password": pass_baru,
            "saldo": SALDO_AWAL
        }
    
        simpan_data()
        print(f"✅ Registrasi berhasil! Akun dengan username '{user_baru}' sekarang dapat digunakan untuk login.")