from database import akun_user, keranjang
from utils import cetak_tabel, menu_admin

def tampilkan_menu_admin():
    while True:
        print("\n=== MENU AKSES ADMIN ===")
        menu_admin()
        
        pilihan_admin = input("Silahkan Pilih Opsi Menu (1-3) : ")

        if pilihan_admin == "1":
            if len(akun_user) < 1:
                print("Tidak Ada Akun User yang Berhasil Dideteksi.")
            else:
                print("\nBerikut Adalah Daftar Akun yang Valid dan Aktif Sekarang : ")
                field_names = ["No", "Username Akun User"]
                rows_user = [[idx, user] for idx, (user, _) in enumerate(akun_user.items(), 1)]
                cetak_tabel(field_names, rows_user)
                
        elif pilihan_admin == "2":
            hapus_akun = input("Silahkan Masukkan Nama Akun : ")
            if hapus_akun in akun_user:
                del akun_user[hapus_akun]
                if hapus_akun in keranjang:
                    del keranjang[hapus_akun]
                print(f"✅ Berhasil Menghapus Akun Bernama '{hapus_akun}' dari Daftar Akun User!")
            else:
                print("Nama Akun yang Dimasukkan Tidak Valid/Terdeteksi")
                
        elif pilihan_admin == "3":
            print("✅ Berhasil Keluar dari Menu Akses Admin!")
            break
        else:
            print("Opsi Menu yang Dimasukkan Tidak Valid atau Tidak Terdeteksi!")