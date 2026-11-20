
import os
from auth import login, registrasi
from admin import tampilkan_menu_admin
from user import tampilkan_menu_user
from utils import menu_awal

def main():
    while True:
        os.system("cls" if os.name == "nt" else "clear")

        print("Selamat Datang di PyCommerce : Sistem E-Commerce")
        print("Silahkan Login Terlebih Dahulu!")
        print("================================================")

        menu_awal()
        pilihan_awal = input("Silahkan Pilih Opsi Menu (1-3) : ")

        if pilihan_awal == "1":
            username, role = login()

            if username is not None and role is not None:
                print(f"\nAkun Aktif : {username}")
                print(f"Role       : {role.title()}")

                if role == "admin":
                    tampilkan_menu_admin()
                elif role == "user":
                    tampilkan_menu_user(username)

            input("\nTekan Enter untuk kembali ke menu awal...")

        elif pilihan_awal == "2":
            registrasi()
            input("\nTekan Enter untuk kembali ke menu awal...")

        elif pilihan_awal == "3":
            print("\nBerhasil Keluar dari Program!")
            print("Terima kasih telah menggunakan PyCommerce!")
            break

        else:
            print("\nOpsi Menu yang Dimasukkan Tidak Valid!")
            input("Tekan Enter untuk mengulang kembali...")

if __name__ == "__main__":
    main()

print("\nProgram Telah Berhenti Berjalan. Terima Kasih!")