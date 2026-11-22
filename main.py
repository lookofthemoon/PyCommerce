from auth import login, registrasi
from admin import tampilkan_menu_admin
from user import tampilkan_menu_user
from utils import menu_awal, bersihkan_layar

def main():
    while True:
        bersihkan_layar()

        print("Selamat Datang di PyCommerce : Sistem E-Commerce")
        print("Silahkan Login Terlebih Dahulu!")
        print("================================================")

        menu_awal()
        pilihan_awal = input("Silahkan Pilih Opsi Menu (1-3) : ").strip()

        if pilihan_awal == "1":
            bersihkan_layar()
            username, role, gagal_login = login()

            if gagal_login:
                print("\nBatas percobaan login telah habis. Program berhenti.")
                break

            if username is not None and role is not None:
                if role == "admin":
                    tampilkan_menu_admin(username)
                elif role == "user":
                    tampilkan_menu_user(username)

        elif pilihan_awal == "2":
            bersihkan_layar()
            registrasi()

        elif pilihan_awal == "3":
            bersihkan_layar()
            print("\nBerhasil Keluar dari Program!")
            print("Terima kasih telah menggunakan PyCommerce!")
            break

        else:
            print("\nOpsi Menu yang Dimasukkan Tidak Valid!")

if __name__ == "__main__":
    main()