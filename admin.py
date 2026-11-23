from datetime import datetime
from database import (
    akun_user,
    saldo_user,
    pengajuan_saldo,
    keranjang,
    riwayat_pesanan,
    simpan_database,
    daftar_produk,
)
from utils import (
    cetak_tabel,
    menu_admin,
    bersihkan_layar,
    bersihkan_layar_dengan_jeda,
    format_rupiah,
)

def kumpulkan_semua_transaksi(filter_username=None):
    hasil = []
    if not isinstance(riwayat_pesanan, dict):
        return hasil

    for pembeli, daftar_trx in riwayat_pesanan.items():
        if filter_username and pembeli.lower() != filter_username.lower():
            continue
        if not isinstance(daftar_trx, list):
            continue

        for idx, pesanan in enumerate(daftar_trx, 1):
            items_dict = pesanan.get("Item", {})
            ringkasan_item = []
            if isinstance(items_dict, dict):
                for k_id, jml in items_dict.items():
                    ringkasan_item.append(f"{k_id} (x{jml})")

            hasil.append({
                "id_transaksi": pesanan.get("id_transaksi", f"LEGACY-{idx:03d}"),
                "pembeli": pembeli,
                "waktu": pesanan.get("waktu", "-"),
                "items_str": ", ".join(ringkasan_item) if ringkasan_item else "-",
                "total": pesanan.get("Total", 0),
            })
    return hasil


def tampilkan_tabel_transaksi(daftar_trx, judul):
    bersihkan_layar()
    print(f"\n=== {judul} ===")

    if not daftar_trx:
        print("Belum Ada Data Transaksi yang Sesuai.")
        bersihkan_layar_dengan_jeda(2.0)
        return

    field_names = ["ID Transaksi", "Pembeli", "Waktu", "Item (ID & Jumlah)", "Total"]
    rows = [
        [
            trx["id_transaksi"],
            trx["pembeli"],
            trx["waktu"],
            trx["items_str"],
            format_rupiah(trx["total"]),
        ]
        for trx in daftar_trx
    ]
    cetak_tabel(field_names, rows)

    total_omzet = sum(trx["total"] for trx in daftar_trx)
    print(f"Jumlah Transaksi : {len(daftar_trx)}")
    print(f"Total Nilai      : {format_rupiah(total_omzet)}")

    input("\nTekan Enter untuk kembali...")


def pantau_transaksi_user():
    while True:
        bersihkan_layar()
        print("\n=== PANTAU RIWAYAT TRANSAKSI USER ===")
        cetak_tabel(
            ["No", "Opsi Pemantauan Transaksi"],
            [
                ["1", "Lihat Semua Transaksi Seluruh User"],
                ["2", "Filter Transaksi Berdasarkan Username"],
                ["3", "Kembali ke Menu Admin"],
            ],
        )

        opsi = input("Pilih opsi (1-3) : ").strip()
        if opsi == "1":
            semua_trx = kumpulkan_semua_transaksi()
            tampilkan_tabel_transaksi(semua_trx, "SEMUA TRANSAKSI USER")
        elif opsi == "2":
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
            target_user = input("Masukkan Username User yang Ingin Dipantau : ").strip()
            if not target_user:
                print("❗ Username Tidak Boleh Kosong.")
                bersihkan_layar_dengan_jeda(1.5)
                continue
            trx_user = kumpulkan_semua_transaksi(filter_username=target_user)
            tampilkan_tabel_transaksi(trx_user, f"TRANSAKSI USER: {target_user}")
        elif opsi == "3":
            bersihkan_layar_dengan_jeda(1.2)
            break
        else:
            print("❗ Opsi Pemantauan Tidak Valid!")
            bersihkan_layar_dengan_jeda(1.5)

def kelola_pengajuan_saldo():
    while True:
        bersihkan_layar()
        print("\n=== KELOLA PENGAJUAN ISI SALDO USER ===")

        if not pengajuan_saldo:
            print("Belum Ada Pengajuan Pengisian Saldo dari User.")
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
            print("\nTidak Ada Pengajuan Saldo Berstatus 'Menunggu' yang Perlu Diproses.")
            bersihkan_layar_dengan_jeda(3.0)
            return

        print("\n=== PILIH AKSI PENGAJUAN SALDO ===")
        cetak_tabel(
            ["No", "Opsi Aksi Pengajuan Saldo"],
            [
                ["1", "Terima Pengajuan Saldo"],
                ["2", "Tolak Pengajuan Saldo"],
                ["3", "Kembali ke Menu Admin"],
            ],
        )
        aksi = input("Pilih Aksi (1-3) : ").strip()

        if aksi in ("1", "2"):
            target_id = input("Masukkan ID Pengajuan (contoh: TOP001) : ").strip().upper()
            pengajuan_terpilih = next(
                (item for item in pengajuan_saldo if item.get("id") == target_id),
                None,
            )

            if not pengajuan_terpilih:
                print("❗ ID Pengajuan Tidak Ditemukan.")
                bersihkan_layar_dengan_jeda(1.8)
                continue

            if pengajuan_terpilih.get("status") != "Menunggu":
                print(
                    f"❗ Pengajuan '{target_id}' Sudah Diproses Sebelumnya "
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
                print(f"❗ Akun User '{user_target}' Sudah Tidak Valid/Aktif. Pengajuan Otomatis Ditolak.")
                bersihkan_layar_dengan_jeda(2.0)
                continue

            if aksi == "1":
                saldo_user[user_target] = saldo_user.get(user_target, 0) + nominal
                pengajuan_terpilih["status"] = "Diterima"
                pengajuan_terpilih["waktu_proses"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                simpan_database()
                print(
                    f"✅ Pengajuan '{target_id}' Sebesar {format_rupiah(nominal)} untuk '{user_target}' DITERIMA! "
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
            print(" ❗ Opsi Aksi Tidak Valid!")
            bersihkan_layar_dengan_jeda(1.5)


def tampilkan_menu_admin(username="Admin"):
    while True:
        bersihkan_layar()
        print(f"\n=== MENU AKSES ADMIN ({username}) ===")
        menu_admin(username)

        pilihan_admin = input("Silahkan Pilih Opsi Menu (1-5) : ").strip()

        if pilihan_admin == "1":
            bersihkan_layar()
            if not akun_user:
                print("❗ Tidak Ada Akun User yang Berhasil Dideteksi.")
                bersihkan_layar_dengan_jeda(1.8)
            else:
                print("\nBerikut Adalah Daftar Akun yang Valid dan Aktif Sekarang : ")
                field_names = ["No", "Username Akun User", "Saldo Aktif"]
                rows_user = [
                    [idx, user, format_rupiah(saldo_user.get(user, 0))]
                    for idx, user in enumerate(akun_user.keys(), 1)
                ]
                cetak_tabel(field_names, rows_user)
                input("\nTekan Enter untuk kembali ke Menu Admin...")

        elif pilihan_admin == "2":
            bersihkan_layar()
            if not akun_user:
                print("❗ Tidak Ada Akun User yang Berhasil Dideteksi.")
                bersihkan_layar_dengan_jeda(1.8)
            else:
                print("\nBerikut Adalah Daftar Akun yang Valid dan Aktif Sekarang : ")
                field_names = ["No", "Username Akun User", "Saldo Aktif"]
                rows_user = [
                    [idx, user, format_rupiah(saldo_user.get(user, 0))]
                    for idx, user in enumerate(akun_user.keys(), 1)
                ]
                cetak_tabel(field_names, rows_user)
            hapus_akun = input("Silahkan Masukkan Nama Akun : ").strip()
            if hapus_akun in akun_user:
                del akun_user[hapus_akun]
                saldo_user.pop(hapus_akun, None)
                keranjang.pop(hapus_akun, None)
                riwayat_pesanan.pop(hapus_akun, None)
                pengajuan_saldo[:] = [
                    item for item in pengajuan_saldo if item.get("username") != hapus_akun
                ]
                produk_dihapus = [
                    k_id for k_id, p in daftar_produk.items()
                    if p.get("Penjual") == hapus_akun
                ]
                for k_id in produk_dihapus:
                    del daftar_produk[k_id]
                for cart in keranjang.values():
                    cart.pop(k_id, None)
                simpan_database()
                print(f"✅ Berhasil Menghapus Akun Bernama '{hapus_akun}' dari Daftar Akun User!")
                bersihkan_layar_dengan_jeda(1.8)
            else:
                print("❗ Nama Akun yang Dimasukkan Tidak Valid/Terdeteksi")
                bersihkan_layar_dengan_jeda(1.8)

        elif pilihan_admin == "3":
            kelola_pengajuan_saldo()
            
        elif pilihan_admin == "4":
            pantau_transaksi_user()

        elif pilihan_admin == "5":
            print("✅ Berhasil Keluar dari Menu Akses Admin!")
            bersihkan_layar_dengan_jeda(1.2)
            break
        else:
            print("❗ Opsi Menu yang Dimasukkan Tidak Valid atau Tidak Terdeteksi!")
            bersihkan_layar_dengan_jeda(1.5)