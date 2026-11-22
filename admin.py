from datetime import datetime
from database import (
    akun_user,
    saldo_user,
    pengajuan_saldo,
    keranjang,
    riwayat_pesanan,
    simpan_database,
)
from utils import (
    cetak_tabel,
    menu_admin,
    bersihkan_layar,
    bersihkan_layar_dengan_jeda,
    format_rupiah,
)

def _kelola_pengajuan_saldo():
    while True:
        bersihkan_layar()
        print("\n=== KELOLA PENGAJUAN ISI SALDO USER ===")

        if not pengajuan_saldo:
            print("Belum ada pengajuan pengisian saldo dari user.")
            bersihkan_layar_dengan_jeda(1.8)
            return

        field_names = ["ID", "Username", "Nominal", "Status", "Tanggal Ajuan"]
        rows = [
            [
                item.get("id", "-"),
                item.get("username", "-"),
                format_rupiah(item.get("nominal", 0)),
                item.get("status", "-"),
                item.get("tanggal", "-"),
            ]
            for item in pengajuan_saldo
        ]
        cetak_tabel(field_names, rows)

        menunggu = [item for item in pengajuan_saldo if item.get("status") == "Menunggu"]
        if not menunggu:
            print("\nTidak ada pengajuan saldo berstatus 'Menunggu' yang perlu diproses.")
            bersihkan_layar_dengan_jeda(1.8)
            return

        print("\n1. Terima Pengajuan Saldo")
        print("2. Tolak Pengajuan Saldo")
        print("3. Kembali ke Menu Admin")
        aksi = input("Pilih aksi (1-3) : ").strip()

        if aksi in ("1", "2"):
            target_id = input("Masukkan ID Pengajuan (contoh: TOP001) : ").strip().upper()
            pengajuan_terpilih = next(
                (item for item in pengajuan_saldo if item.get("id") == target_id),
                None,
            )

            if not pengajuan_terpilih:
                print("❌ ID Pengajuan tidak ditemukan.")
                bersihkan_layar_dengan_jeda(1.8)
                continue

            if pengajuan_terpilih.get("status") != "Menunggu":
                print(
                    f"❌ Pengajuan '{target_id}' sudah diproses sebelumnya "
                    f"({pengajuan_terpilih.get('status')})."
                )
                bersihkan_layar_dengan_jeda(1.8)
                continue

            user_target = pengajuan_terpilih["username"]
            nominal = pengajuan_terpilih["nominal"]

            if user_target not in akun_user:
                pengajuan_terpilih["status"] = "Ditolak"
                pengajuan_terpilih["waktu_proses"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                simpan_database()
                print(f"❌ Akun user '{user_target}' sudah tidak ada. Pengajuan otomatis ditolak.")
                bersihkan_layar_dengan_jeda(2.0)
                continue

            if aksi == "1":
                saldo_user[user_target] = saldo_user.get(user_target, 0) + nominal
                pengajuan_terpilih["status"] = "Diterima"
                pengajuan_terpilih["waktu_proses"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                simpan_database()
                print(
                    f"✅ Pengajuan '{target_id}' sebesar {format_rupiah(nominal)} untuk '{user_target}' DITERIMA! "
                    f"Saldo baru: {format_rupiah(saldo_user[user_target])}."
                )
            else:
                pengajuan_terpilih["status"] = "Ditolak"
                pengajuan_terpilih["waktu_proses"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                simpan_database()
                print(
                    f"✅ Pengajuan '{target_id}' sebesar {format_rupiah(nominal)} untuk '{user_target}' DITOLAK."
                )
            bersihkan_layar_dengan_jeda(2.0)

        elif aksi == "3":
            bersihkan_layar_dengan_jeda(1.2)
            break
        else:
            print("❌ Opsi aksi tidak valid!")
            bersihkan_layar_dengan_jeda(1.5)


def tampilkan_menu_admin(username="Admin"):
    while True:
        bersihkan_layar()
        print(f"\n=== MENU AKSES ADMIN ({username}) ===")
        menu_admin(username)

        pilihan_admin = input("Silahkan Pilih Opsi Menu (1-4) : ").strip()

        if pilihan_admin == "1":
            bersihkan_layar()
            if not akun_user:
                print("Tidak Ada Akun User yang Berhasil Dideteksi.")
                bersihkan_layar_dengan_jeda(1.8)
            else:
                print("\nBerikut Adalah Daftar Akun yang Valid dan Aktif Sekarang : ")
                field_names = ["No", "Username Akun User", "Saldo Aktif"]
                rows_user = [
                    [idx, user, format_rupiah(saldo_user.get(user, 0))]
                    for idx, user in enumerate(akun_user.keys(), 1)
                ]
                cetak_tabel(field_names, rows_user)
                bersihkan_layar_dengan_jeda(2.5)

        elif pilihan_admin == "2":
            hapus_akun = input("Silahkan Masukkan Nama Akun : ").strip()
            if hapus_akun in akun_user:
                del akun_user[hapus_akun]
                saldo_user.pop(hapus_akun, None)
                keranjang.pop(hapus_akun, None)
                riwayat_pesanan.pop(hapus_akun, None)
                pengajuan_saldo[:] = [
                    item for item in pengajuan_saldo if item.get("username") != hapus_akun
                ]
                simpan_database()
                print(f"✅ Berhasil Menghapus Akun Bernama '{hapus_akun}' dari Daftar Akun User!")
                bersihkan_layar_dengan_jeda(1.8)
            else:
                print("❌ Nama Akun yang Dimasukkan Tidak Valid/Terdeteksi")
                bersihkan_layar_dengan_jeda(1.8)

        elif pilihan_admin == "3":
            _kelola_pengajuan_saldo()

        elif pilihan_admin == "4":
            print("✅ Berhasil Keluar dari Menu Akses Admin!")
            bersihkan_layar_dengan_jeda(1.2)
            break
        else:
            print("❌ Opsi Menu yang Dimasukkan Tidak Valid atau Tidak Terdeteksi!")
            bersihkan_layar_dengan_jeda(1.5)