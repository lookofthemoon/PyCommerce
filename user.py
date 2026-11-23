import re
from datetime import datetime
from database import (
    daftar_produk,
    keranjang,
    riwayat_pesanan,
    saldo_user,
    pengajuan_saldo,
    simpan_database,
)
from utils import (
    cetak_tabel,
    menu_user,
    menu_saldo_user,
    menu_kelola_produk_saya,
    menu_katalog_keranjang,
    cetak_struk,
    generate_id_produk,
    bersihkan_layar,
    bersihkan_layar_dengan_jeda,
    format_rupiah,
    cetak_ketentuan,
)

LIST_TIPE = ["Elektronik", "Pakaian", "Kecantikan", "Makanan", "Minuman", "Lainnya"]

def generate_id_transaksi():
    nomor_tertinggi = 0
    for daftar_trx in riwayat_pesanan.values():
        if not isinstance(daftar_trx, list):
            continue
        for pesanan in daftar_trx:
            id_trx = str(pesanan.get("id_transaksi", ""))
            match = re.fullmatch(r"TRX(\d{3})", id_trx)
            if match:
                angka = int(match.group(1))
                if angka > nomor_tertinggi:
                    nomor_tertinggi = angka
    return f"TRX{nomor_tertinggi + 1:03d}"

def ambil_saldo(username):
    saldo_user.setdefault(username, 0)
    return saldo_user[username]

def generate_id_pengajuan():
    nomor_tertinggi = 0
    for item in pengajuan_saldo:
        id_item = str(item.get("id", ""))
        match = re.fullmatch(r"TOP(\d{3})", id_item)
        if match:
            angka = int(match.group(1))
            if angka > nomor_tertinggi:
                nomor_tertinggi = angka
    return f"TOP{nomor_tertinggi + 1:03d}"

def ajukan_pengisian_saldo(username):
    bersihkan_layar()
    print(f"\n=== AJUKAN PENGISIAN SALDO ({username.upper()}) ===")
    print(f"Saldo Anda Saat Ini : {format_rupiah(ambil_saldo(username))}")

    try:
        nominal = int(input("Masukkan Nominal Pengisian Saldo (Rp) : "))
    except ValueError:
        print("❗ Nominal Harus Berupa Angka Bulat!")
        bersihkan_layar_dengan_jeda(1.8)
        return

    if nominal <= 0:
        print("❗ Nominal Pengisian Saldo Harus Lebih dari Rp 0!")
        bersihkan_layar_dengan_jeda(1.8)
        return

    pengajuan_baru = {
        "id": generate_id_pengajuan(),
        "username": username,
        "nominal": nominal,
        "status": "Menunggu",
        "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    }
    pengajuan_saldo.append(pengajuan_baru)
    simpan_database()

    print(
        f"✅ Pengajuan Pengisian Saldo Sebesar {format_rupiah(nominal)} "
        f"(ID: {pengajuan_baru['id']}) Berhasil Dikirim!"
    )
    print("ℹ️ Saldo Akan Bertambah Setelah Pengajuan Disetujui oleh Admin.")
    bersihkan_layar_dengan_jeda(4.0)

def lihat_pengajuan_saldo_saya(username):
    bersihkan_layar()
    riwayat_saya = [item for item in pengajuan_saldo if item.get("username") == username]
    if not riwayat_saya:
        print("\nAnda Belum Pernah Mengajukan Pengisian Saldo.")
        bersihkan_layar_dengan_jeda(2.5)
        return

    print(f"\n=== RIWAYAT PENGAJUAN SALDO ({username.upper()}) ===")
    field_names = ["ID", "Nominal", "Status", "Tanggal Ajuan"]
    rows = [
        [
            item.get("id", "-"),
            format_rupiah(item.get("nominal", 0)),
            item.get("status", "-"),
            item.get("tanggal", "-"),
        ]
        for item in riwayat_saya
    ]
    cetak_tabel(field_names, rows)
    input("\nTekan Enter untuk kembali ke Menu User...")

def kelola_saldo_user(username):
    while True:
        bersihkan_layar()
        print(f"\n=== SALDO & TOP-UP ({username.upper()}) ===")
        print(f"Saldo Aktif Anda : {format_rupiah(ambil_saldo(username))}")
        menu_saldo_user(username)

        pilihan = input("Silahkan Pilih Opsi Menu (1-3) : ").strip()
        if pilihan == "1":
            ajukan_pengisian_saldo(username)
        elif pilihan == "2":
            lihat_pengajuan_saldo_saya(username)
        elif pilihan == "3":
            bersihkan_layar_dengan_jeda(1.2)
            break
        else:
            print("❗ Opsi Menu yang Dimasukkan Tidak Valid/Terdeteksi")
            bersihkan_layar_dengan_jeda(1.5)

def input_nama_produk():
    MIN_LEN = 3
    MAX_LEN = 25
    
    cetak_ketentuan(
        "--- KETENTUAN NAMA PRODUK ---",
        [
            ["Panjang Karakter", f"{MIN_LEN} - {MAX_LEN} karakter"],
            ["Jenis Karakter", "Hanya huruf (A-Z / a-z) dan spasi"],
            ["Larangan", "Tidak boleh kosong, angka, atau simbol"],
        ],
    )
    
    nama_p = input(f"Nama Produk (Hanya Huruf/Spasi, {MIN_LEN}-{MAX_LEN} Karakter): ").strip()

    if not (MIN_LEN <= len(nama_p) <= MAX_LEN):
        print(f"❗ Nama Produk Harus Memiliki Panjang Antara {MIN_LEN} hingga {MAX_LEN} Karakter.")
        return None

    if not re.match(r"^[A-Za-z\s]+$", nama_p):
        print("❗ Nama Produk Hanya Boleh Mengandung Huruf dan Spasi (Tidak Boleh Ada Angka atau Simbol).")
        return None

    return nama_p

def pilih_tipe_produk():
    while True:
        bersihkan_layar()
        print("\n=== PILIH TIPE / KATEGORI PRODUK ===")
        rows_tipe = [[str(idx), tipe] for idx, tipe in enumerate(LIST_TIPE, 1)]
        cetak_tabel(["No", "Tipe / Kategori Produk"], rows_tipe)

        try:
            pilihan_tipe = int(input(f"Masukkan Nomor Tipe Produk (1-{len(LIST_TIPE)}) : ").strip())
        except ValueError:
            print("❗ Input Harus Berupa Angka Bulat! Silahkan Pilih dari Tabel Kategori.")
            bersihkan_layar_dengan_jeda(1.8)
            continue

        if not (1 <= pilihan_tipe <= len(LIST_TIPE)):
            print(f"❗ Pilihan Tidak Valid! Masukkan Nomor Antara 1 Hingga {len(LIST_TIPE)}.")
            bersihkan_layar_dengan_jeda(1.8)
            continue

        tipe_terpilih = LIST_TIPE[pilihan_tipe - 1]

        if tipe_terpilih == "Lainnya":
            while True:
                bersihkan_layar()
                print("\n=== KATEGORI PRODUK LAINNYA ===")
                cetak_tabel(
                    ["Ketentuan", "Aturan Input"],
                    [
                        ["Karakter", "Hanya Huruf (A-Z / a-z) dan Spasi"],
                        ["Larangan", "Tidak Boleh Kosong, Angka, atau Simbol"],
                    ],
                )
                kategori_kustom = input(
                    "Masukkan Nama Kategori Produk Lainnya (atau Ketik 'kembali' untuk Pilih Ulang) : "
                ).strip()

                if kategori_kustom.lower() == "kembali":
                    break

                if not kategori_kustom:
                    print("❗ Kategori Produk Tidak Boleh Kosong.")
                    bersihkan_layar_dengan_jeda(1.8)
                    continue

                if not re.fullmatch(r"[A-Za-z\s]+", kategori_kustom):
                    print("❗ Kategori Produk Hanya Boleh Menggunakan Huruf dan Spasi (Tanpa Angka/Simbol).")
                    bersihkan_layar_dengan_jeda(1.8)
                    continue

                return kategori_kustom
            continue

        return tipe_terpilih

def mulai_jual(username):
    bersihkan_layar()
    print("\n=== TAMBAH PRODUK BARU ===")
    id_baru = generate_id_produk(daftar_produk)
    if not id_baru:
        print("❗ Kapasitas ID Produk (K001–K999) Telah Penuh!")
        bersihkan_layar_dengan_jeda(1.8)
        return

    print(f"ID Produk Otomatis : {id_baru}")
    print(f"Nama Penjual       : {username}")

    nama_p = input_nama_produk()
    if nama_p is None:
        print("❗ Proses Jual Produk Dihentikan.")
        bersihkan_layar_dengan_jeda(1.8)
        return

    tipe_p = pilih_tipe_produk()

    cetak_ketentuan(
        "--- KETENTUAN STOK & HARGA ---",
        [
            ["Tipe Data", "Angka Bulat (Integer)"],
            ["Jumlah Stok", "Minimal 0"],
            ["Harga Satuan (Rp)", "Harus Lebih dari Rp 0"],
        ],
    )
    
    try:
        stok_p = int(input("Jumlah Stok : "))
        harga_p = int(input("Harga Satuan (Rp) : "))
    except ValueError:
        print("❗ Stok dan Harga Harus Berupa Angka!")
        bersihkan_layar_dengan_jeda(1.8)
        return

    if stok_p < 0 or harga_p <= 0:
        print("❗ Stok Minimal 0 dan Harga Harus Lebih dari 0!")
        bersihkan_layar_dengan_jeda(1.8)
        return

    desk_p = input("Deskripsi Produk : ").strip() or "-"

    daftar_produk[id_baru] = {
        "Nama": nama_p,
        "Stok": stok_p,
        "Tipe": tipe_p,
        "Harga": harga_p,
        "Penjual": username,
        "Deskripsi": desk_p,
    }
    simpan_database()
    print(f"✅ Berhasil Menambahkan Produk '{nama_p}' (ID: {id_baru}) oleh Penjual '{username}' ke Katalog!")
    bersihkan_layar_dengan_jeda(1.8)

def tampilkan_produk_milik_user(username):
    produk_saya = {
        k_id: p for k_id, p in daftar_produk.items()
        if p.get("Penjual") == username
    }
    if not produk_saya:
        print(f"\n❗ Anda Belum Memiliki Produk yang Dijual atas Akun '{username}'.")
        return {}

    print(f"\n=== PRODUK MILIK {username.upper()} ===")
    field_names = ["ID", "Nama Produk", "Harga", "Stok", "Tipe", "Deskripsi"]
    rows = [
        [k_id, p["Nama"], format_rupiah(p["Harga"]), p["Stok"], p["Tipe"], p["Deskripsi"]]
        for k_id, p in produk_saya.items()
    ]
    cetak_tabel(field_names, rows)
    return produk_saya

def ubah_produk_milik_user(username):
    bersihkan_layar()
    produk_saya = tampilkan_produk_milik_user(username)
    if not produk_saya:
        input("\nTekan Enter untuk kembali ke Menu User...")
        return

    target_id = input("\nMasukkan ID Produk Milik Anda yang Ingin Diubah : ").strip().upper()
    if not target_id:
        return

    if target_id not in daftar_produk:
        print("❗ ID Produk Tidak Ditemukan di Katalog.")
        bersihkan_layar_dengan_jeda(1.8)
        return

    if daftar_produk[target_id].get("Penjual") != username:
        print(
            f"❗ Akses Ditolak! Produk '{target_id}' Dijual oleh '{daftar_produk[target_id].get('Penjual', '-')}', "
            f"Bukan oleh '{username}'."
        )
        bersihkan_layar_dengan_jeda(2.5)
        return

    produk = daftar_produk[target_id]
    print(f"\nMengubah Produk '{produk['Nama']}' ({target_id}). Tekan Enter Jika Tidak Ingin Mengubah Field.")

    nama_baru = input(f"Nama Produk baru [{produk['Nama']}] : ").strip()
    if nama_baru:
        if not (3 <= len(nama_baru) <= 25) or not re.match(r"^[A-Za-z\s]+$", nama_baru):
            print("❗ Nama Produk Harus 3-25 Karakter dan Hanya Berisi Huruf/Spasi. Perubahan Nama Dibatalkan.")
            bersihkan_layar_dengan_jeda(3.0)
        else:
            produk["Nama"] = nama_baru

    ubah_tipe = input(f"Ubah Tipe Produk [{produk['Tipe']}]? (y/n) : ").strip().lower()
    if ubah_tipe == "y":
        produk["Tipe"] = pilih_tipe_produk()

    stok_input = input(f"Jumlah Stok Baru [{produk['Stok']}] : ").strip()
    if stok_input:
        try:
            stok_baru = int(stok_input)
            if stok_baru < 0:
                print("❗ Stok Minimal 0. Perubahan Stok Dibatalkan.")
                bersihkan_layar_dengan_jeda(2.5)
            else:
                produk["Stok"] = stok_baru
        except ValueError:
            print("❗ Stok Harus Berupa Angka. Perubahan Stok Dibatalkan.")
            bersihkan_layar_dengan_jeda(2.5)

    harga_input = input(f"Harga Satuan baru [{produk['Harga']}] : ").strip()
    if harga_input:
        try:
            harga_baru = int(harga_input)
            if harga_baru <= 0:
                print("❗ Harga Harus Lebih dari 0. Perubahan Harga Dibatalkan.")
                bersihkan_layar_dengan_jeda(2.5)
            else:
                produk["Harga"] = harga_baru
        except ValueError:
            print("❗ Harga Harus Berupa Angka. Perubahan Harga Dibatalkan.")
            bersihkan_layar_dengan_jeda(2.5)

    desk_input = input(f"Deskripsi baru [{produk['Deskripsi']}] : ").strip()
    if desk_input:
        produk["Deskripsi"] = desk_input

    simpan_database()
    print(f"✅ Perubahan Pada Produk '{target_id}' Berhasil Disimpan!")
    bersihkan_layar_dengan_jeda(1.8)

def hapus_produk_milik_user(username):
    bersihkan_layar()
    produk_saya = tampilkan_produk_milik_user(username)
    if not produk_saya:
        bersihkan_layar_dengan_jeda(1.5)
        return True

    target_id = input("\nMasukkan ID Produk Milik Anda yang Ingin Dihapus : ").strip().upper()
    if not target_id:
        return False

    if target_id not in daftar_produk:
        print("❗ ID Produk Tidak Ditemukan di Katalog.")
        bersihkan_layar_dengan_jeda(1.8)
        return False

    if daftar_produk[target_id].get("Penjual") != username:
        print(
            f"❗ Akses Ditolak! Produk '{target_id}' Dijual oleh '{daftar_produk[target_id].get('Penjual', '-')}', "
            f"Bukan oleh '{username}'."
        )
        bersihkan_layar_dengan_jeda(3.0)
        return False

    konfirmasi = input(f"Yakin Ingin Menghapus Produk '{daftar_produk[target_id]['Nama']}' ({target_id})? (y/n) : ").strip().lower()
    if konfirmasi == "y":
        del daftar_produk[target_id]
        for cart in keranjang.values():
            cart.pop(target_id, None)
        simpan_database()
        print(f"✅ Produk '{target_id}' Berhasil Dihapus dari Katalog.")
        bersihkan_layar_dengan_jeda(1.8)

        sisa_produk = any(
            p.get("Penjual") == username for p in daftar_produk.values()
        )
        if not sisa_produk:
            print(f"❗ Sudah Tidak Ada Lagi Produk yang Dijual di Akun '{username}'.")
            bersihkan_layar_dengan_jeda(1.8)
            return True
    else:
        print("❗ Penghapusan Produk Dibatalkan.")
        bersihkan_layar_dengan_jeda(1.5)

    return False

def kelola_produk_saya(username):
    produk_saya = {
        k_id: p for k_id, p in daftar_produk.items()
        if p.get("Penjual") == username
    }

    if not produk_saya:
        print(f"\n❗ Belum Ada Produk yang Dijual di Akun '{username}'.")
        bersihkan_layar_dengan_jeda(1.8)
        return

    while True:
        bersihkan_layar()
        print(f"\n=== KELOLA PRODUK SAYA ({username.upper()}) ===")
        tampilkan_produk_milik_user(username)
        menu_kelola_produk_saya(username)

        pilihan = input("Silahkan Pilih Opsi Menu (1-3) : ").strip()
        if pilihan == "1":
            ubah_produk_milik_user(username)
        elif pilihan == "2":
            if hapus_produk_milik_user(username):
                break
        elif pilihan == "3":
            bersihkan_layar_dengan_jeda(1.2)
            break
        else:
            print("❗ Opsi Menu yang Dimasukkan Tidak Valid/Terdeteksi")
            bersihkan_layar_dengan_jeda(1.5)

def tampilkan_isi_keranjang(username):
    if not keranjang.get(username):
        print("\nKeranjang belanja Anda masih kosong.")
        return False

    print(f"\n=== KERANJANG BELANJA MILIK {username.upper()} ===")
    field_names = ["ID Produk", "Nama Produk", "Harga Satuan", "Jumlah", "Subtotal"]
    rows = []
    total_belanja = 0

    for k_id, jumlah in keranjang[username].items():
        if k_id not in daftar_produk:
            continue
        p = daftar_produk[k_id]
        subtotal = p["Harga"] * jumlah
        total_belanja += subtotal
        rows.append([k_id, p["Nama"], format_rupiah(p["Harga"]), jumlah, format_rupiah(subtotal)])

    cetak_tabel(field_names, rows)
    print(f"Total Keseluruhan : {format_rupiah(total_belanja)}")
    print(f"Saldo Anda Saat Ini: {format_rupiah(ambil_saldo(username))}")
    return True

def checkout_keranjang(username):
    if not keranjang.get(username):
        print("\n❗ Keranjang Belanja Anda Masih Kosong. Tidak Ada yang Bisa di-Checkout.")
        bersihkan_layar_dengan_jeda(1.8)
        return False

    tampilkan_isi_keranjang(username)
    total_belanja = sum(
        daftar_produk[k_id]["Harga"] * jumlah
        for k_id, jumlah in keranjang[username].items()
        if k_id in daftar_produk
    )

    opsi_cart = input("\nIngin Melakukan Checkout / Proses Pesanan? (y/n) : ").strip().lower()
    if opsi_cart == "y":
        for k_id, jumlah in keranjang[username].items():
            if k_id not in daftar_produk:
                print(f"❗ Produk dengan ID '{k_id}' Sudah Tidak Tersedia di Katalog.")
                bersihkan_layar_dengan_jeda(1.8)
                return False
            if daftar_produk[k_id].get("Penjual") == username:
                print(
                    f"❗ Checkout Dibatalkan: Produk '{daftar_produk[k_id]['Nama']}' ({k_id}) "
                    f"adalah Produk Milik Anda Sendiri. Hapus Item Tersebut dari Keranjang Terlebih Dahulu."
                )
                bersihkan_layar_dengan_jeda(2.2)
                return False
            if jumlah > daftar_produk[k_id]["Stok"]:
                print(f"❗ Stok Produk '{daftar_produk[k_id]['Nama']}' Tidak Mencukupi untuk Checkout.")
                bersihkan_layar_dengan_jeda(1.8)
                return False

        saldo_saat_ini = ambil_saldo(username)
        if saldo_saat_ini < total_belanja:
            kekurangan = total_belanja - saldo_saat_ini
            print(
                f"\n❌ ERROR: Saldo Anda Tidak Cukup untuk Melakukan Checkout!\n"
                f"   Total Belanja : {format_rupiah(total_belanja)}\n"
                f"   Saldo Anda    : {format_rupiah(saldo_saat_ini)}\n"
                f"   Kekurangan    : {format_rupiah(kekurangan)}\n"
                f"   Silakan Ajukan Pengisian Saldo Terlebih Dahulu dan Tunggu Persetujuan Admin."
            )
            bersihkan_layar_dengan_jeda(2.5)
            return False

        items_struk = []
        for k_id, jumlah in keranjang[username].items():
            p = daftar_produk[k_id]
            p["Stok"] -= jumlah
            items_struk.append((p["Nama"], p["Harga"], jumlah))

        saldo_user[username] = saldo_saat_ini - total_belanja

        id_trx = generate_id_transaksi()
        waktu_trx = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        riwayat_pesanan.setdefault(username, [])
        riwayat_pesanan[username].append({
            "id_transaksi": id_trx,
            "waktu": waktu_trx,
            "Item": keranjang[username].copy(),
            "Total": total_belanja,
        })

        keranjang[username] = {}
        simpan_database()
        print("\n✅ Checkout Berhasil! Saldo Telah Dipotong, Stok Diperbarui, dan Pesanan Sedang Diproses.")
        cetak_struk(username, items_struk, total_belanja, saldo=saldo_user[username])
        input("Tekan Enter untuk Kembali ke Menu User...")
        return True
    else:
        print("❗ Checkout Dibatalkan.")
        bersihkan_layar_dengan_jeda(1.5)
        return False

def hapus_keranjang(username):
    if not keranjang.get(username):
        print("\n❗ Keranjang Belanja Anda Masih Kosong.")
        bersihkan_layar_dengan_jeda(1.8)
        return

    while True:
        bersihkan_layar()
        print(f"\n=== KELOLA PENGHAPUSAN KERANJANG ({username.upper()}) ===")

        field_names_menu = ["No", "Opsi Menu Hapus Keranjang"]
        rows_menu = [
            ["1", "Hapus Produk Tertentu (Berdasarkan ID)"],
            ["2", "Kosongkan Seluruh Keranjang Belanja"],
            ["3", "Kembali ke Menu Keranjang & Checkout"],
        ]
        cetak_tabel(field_names_menu, rows_menu)

        pilihan_hapus = input("Silahkan Pilih Opsi Penghapusan (1-3) : ").strip()

        if pilihan_hapus == "1":
            bersihkan_layar()
            tampilkan_isi_keranjang(username)

            hapus_id = input("\nMasukkan ID Produk yang Ingin Dihapus : ").strip().upper()
            if hapus_id in keranjang[username]:
                nama_produk = daftar_produk.get(hapus_id, {}).get("Nama", hapus_id)
                del keranjang[username][hapus_id]
                simpan_database()
                print(f"\n✅ Berhasil Menghapus Produk '{nama_produk}' (ID: {hapus_id}) dari Keranjang!")
                bersihkan_layar_dengan_jeda(1.8)

                if not keranjang[username]:
                    print("❗ Keranjang Anda Sekarang Sudah Kosong.")
                    bersihkan_layar_dengan_jeda(1.5)
                    break
            else:
                print("❗ ID Produk Tersebut Tidak Ditemukan di Dalam Keranjang Belanja Anda.")
                bersihkan_layar_dengan_jeda(1.8)

        elif pilihan_hapus == "2":
            konfirmasi = input("\nApakah Anda Yakin Ingin Mengosongkan SELURUH Isi Keranjang? (y/n) : ").strip().lower()
            if konfirmasi == "y":
                keranjang[username] = {}
                simpan_database()
                print("\n✅ Berhasil Mengosongkan Seluruh Keranjang Belanja!")
                bersihkan_layar_dengan_jeda(1.8)
                break
            else:
                print("Penghapusan Keranjang Dibatalkan.")
                bersihkan_layar_dengan_jeda(1.5)

        elif pilihan_hapus == "3":
            bersihkan_layar_dengan_jeda(1.2)
            break
        else:
            print("❗ Opsi Menu yang Dimasukkan Tidak Valid/Terdeteksi")
            bersihkan_layar_dengan_jeda(1.5)

def tambah_produk_ke_keranjang(username):
    while True:
        beli_id = input(
            "\nMasukkan ID Produk yang Ingin Dibeli (Atau Enter untuk Lanjut ke Menu Keranjang) : "
        ).strip().upper()
        if not beli_id:
            break

        if beli_id not in daftar_produk:
            print("❗ ID Produk Tidak Ditemukan di Katalog.")
            continue

        produk = daftar_produk[beli_id]
        if produk.get("Penjual") == username:
            print(
                f"❗ Anda Tidak Dapat Memasukkan Produk '{produk['Nama']}' ({beli_id}) "
                f"ke Keranjang Karena Produk Ini Dijual oleh Akun Anda Sendiri."
            )
            continue

        try:
            jml = int(input(f"Masukkan Jumlah '{produk['Nama']}' yang Ingin Dibeli : "))
        except ValueError:
            print("❗ Jumlah Harus Berupa Angka!")
            continue

        if jml <= 0:
            print("❗ Jumlah Beli Minimal 1.")
            continue
        elif jml > produk["Stok"]:
            print(f"❗ Stok Tidak Mencukupi! Sisa Stok Saat Ini: {produk['Stok']}")
            continue

        keranjang.setdefault(username, {})
        keranjang[username][beli_id] = keranjang[username].get(beli_id, 0) + jml
        simpan_database()
        print(f"✅ Berhasil Menambahkan {jml} pcs '{produk['Nama']}' ke Keranjang Belanja!")

def tampilkan_katalog():
    print("\n=== KATALOG PRODUK E-COMMERCE ===")
    field_names = ["ID", "Penjual", "Nama Produk", "Harga", "Stok", "Tipe", "Deskripsi"]
    rows = [
        [
            k_id,
            p.get("Penjual", "-"),
            p["Nama"],
            format_rupiah(p["Harga"]),
            p["Stok"],
            p["Tipe"],
            p["Deskripsi"],
        ]
        for k_id, p in daftar_produk.items()
    ]
    cetak_tabel(field_names, rows)

def kelola_keranjang_dan_checkout(username, lewati_bersihkan_awal=False):
    iterasi_pertama = True
    while True:
        if not (iterasi_pertama and lewati_bersihkan_awal):
            bersihkan_layar()
        iterasi_pertama = False

        print(f"\n=== KERANJANG & CHECKOUT ({username.upper()}) ===")
        menu_katalog_keranjang(username)

        pilihan_aksi = input("Silahkan Pilih Opsi Menu (1-4) : ").strip()

        if pilihan_aksi == "1":
            tampilkan_isi_keranjang(username)
            input("\nSilahkan Tekan Enter untuk Kembali ke Menu Keranjang & Checkout")
        elif pilihan_aksi == "2":
            hapus_keranjang(username)
        elif pilihan_aksi == "3":
            berhasil_checkout = checkout_keranjang(username)
            if berhasil_checkout:
                break
        elif pilihan_aksi == "4":
            bersihkan_layar_dengan_jeda(1.2)
            break
        else:
            print("❗ Opsi Menu yang Dimasukkan Tidak Valid/Terdeteksi")
            bersihkan_layar_dengan_jeda(1.5)

def lihat_katalog_dan_beli(username):
    bersihkan_layar()
    if not daftar_produk:
        print("\n❗ Katalog Produk Masih Kosong! Belum Ada Barang yang Tersedia.")
        bersihkan_layar_dengan_jeda(3.0)
        return
    tampilkan_katalog()
    tambah_produk_ke_keranjang(username)
    kelola_keranjang_dan_checkout(username, lewati_bersihkan_awal=True)

def lihat_pesanan(username):
    if not riwayat_pesanan.get(username):
        print("\n❗ Anda Belum Memiliki Riwayat Pesanan.")
        bersihkan_layar_dengan_jeda(1.8)
    else:
        print(f"\n=== RIWAYAT PESANAN SAYA ({username}) ===")
        field_names = ["ID Produk", "Nama Produk", "Jumlah Beli"]
        for idx, pesanan in enumerate(riwayat_pesanan[username], 1):
            print(f"\nPesanan #{idx} (Total: {format_rupiah(pesanan['Total'])})")
            rows = [
                [k_id, daftar_produk.get(k_id, {}).get("Nama", f"Produk Terhapus ({k_id})"), jml]
                for k_id, jml in pesanan["Item"].items()
            ]
            cetak_tabel(field_names, rows)
        input("Tekan Enter untuk Kembali ke Menu User...")

def tampilkan_menu_user(username):
    while True:
        bersihkan_layar()
        print(f"\n=== MENU AKSES USER ({username}) ===")
        print(f"Saldo Anda : {format_rupiah(ambil_saldo(username))}")
        menu_user(username)

        pilihan_user = input("Silahkan Pilih Opsi Menu (1-6) : ").strip()

        if pilihan_user == "1":
            mulai_jual(username)
        elif pilihan_user == "2":
            kelola_produk_saya(username)
        elif pilihan_user == "3":
            lihat_katalog_dan_beli(username)
        elif pilihan_user == "4":
            lihat_pesanan(username)
        elif pilihan_user == "5":
            kelola_saldo_user(username)
        elif pilihan_user == "6":
            print("✅ Berhasil Keluar dari Menu Akses User!")
            bersihkan_layar_dengan_jeda(1.2)
            break
        else:
            print("❗ Opsi Menu yang Dimasukkan Tidak Valid/Terdeteksi")
            bersihkan_layar_dengan_jeda(1.5)