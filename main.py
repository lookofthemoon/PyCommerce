from auth import login, registrasi
from admin import tampilkan_menu_admin
from user import tampilkan_menu_user
from utils import menu_awal, bersihkan_layar, bersihkan_layar_dengan_jeda

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
                print("\n❗ Batas Percobaan Login Telah Habis. Program Berhenti.")
                bersihkan_layar_dengan_jeda(1.5)
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
            print("\n✅ Berhasil Keluar dari Program!")
            print("Terima Kasih Telah Menggunakan PyCommerce!")
            break

        else:
            print("\n❗ Opsi Menu yang Dimasukkan Tidak Valid!")
            bersihkan_layar_dengan_jeda(1.5)

if __name__ == "__main__":
    main()