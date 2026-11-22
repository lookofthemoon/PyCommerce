from database import akun_user, keranjang, riwayat_pesanan, simpan_database
from utils import cetak_tabel, menu_admin, bersihkan_layar

def tampilkan_menu_admin(username="Admin"):
    while True:
        bersihkan_layar()
        print(f"\n=== MENU AKSES ADMIN ({username}) ===")
        menu_admin(username)

        pilihan_admin = input("Silahkan Pilih Opsi Menu (1-3) : ").strip()

        if pilihan_admin == "1":
            bersihkan_layar()
            if not akun_user:
                print("Tidak Ada Akun User yang Berhasil Dideteksi.")
            else:
                print("\nBerikut Adalah Daftar Akun yang Valid dan Aktif Sekarang : ")
                field_names = ["No", "Username Akun User"]
                rows_user = [[idx, user] for idx, user in enumerate(akun_user.keys(), 1)]
                cetak_tabel(field_names, rows_user)

        elif pilihan_admin == "2":
            bersihkan_layar()
            hapus_akun = input("Silahkan Masukkan Nama Akun : ").strip()
            if hapus_akun in akun_user:
                del akun_user[hapus_akun]
                keranjang.pop(hapus_akun, None)
                riwayat_pesanan.pop(hapus_akun, None)
                simpan_database()
                print(f"✅ Berhasil Menghapus Akun Bernama '{hapus_akun}' dari Daftar Akun User!")
            else:
                print("❌ Nama Akun yang Dimasukkan Tidak Valid/Terdeteksi")

        elif pilihan_admin == "3":
            bersihkan_layar()
            print("✅ Berhasil Keluar dari Menu Akses Admin!")
            break
        else:
            print("❌ Opsi Menu yang Dimasukkan Tidak Valid atau Tidak Terdeteksi!")