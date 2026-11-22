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
)

LIST_TIPE = ["Elektronik", "Pakaian", "Kecantikan", "Makanan", "Minuman", "Lainnya"]

def _ambil_saldo(username):
    saldo_user.setdefault(username, 0)
    return saldo_user[username]

def _generate_id_pengajuan():
    nomor_tertinggi = 0
    for item in pengajuan_saldo:
        id_item = str(item.get("id", ""))
        match = re.fullmatch(r"TOP(\d{3})", id_item)
        if match:
            angka = int(match.group(1))
            if angka > nomor_tertinggi:
                nomor_tertinggi = angka
    return f"TOP{nomor_tertinggi + 1:03d}"

def _ajukan_pengisian_saldo(username):
    bersihkan_layar()
    print(f"\n=== AJUKAN PENGISIAN SALDO ({username.upper()}) ===")
    print(f"Saldo Anda saat ini : {format_rupiah(_ambil_saldo(username))}")

    try:
        nominal = int(input("Masukkan nominal pengisian saldo (Rp) : "))
    except ValueError:
        print("❗ Nominal harus berupa angka bulat!")
        bersihkan_layar_dengan_jeda(1.8)
        return

    if nominal <= 0:
        print("❗ Nominal pengisian saldo harus lebih dari Rp 0!")
        bersihkan_layar_dengan_jeda(1.8)
        return

    pengajuan_baru = {
        "id": _generate_id_pengajuan(),
        "username": username,
        "nominal": nominal,
        "status": "Menunggu",
        "tanggal": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
    }
    pengajuan_saldo.append(pengajuan_baru)
    simpan_database()

    print(
        f"✅ Pengajuan pengisian saldo sebesar {format_rupiah(nominal)} "
        f"(ID: {pengajuan_baru['id']}) berhasil dikirim!"
    )
    print("ℹ️ Saldo akan bertambah setelah pengajuan disetujui oleh Admin.")
    bersihkan_layar_dengan_jeda(2.0)

def _lihat_pengajuan_saldo_saya(username):
    bersihkan_layar()
    riwayat_saya = [item for item in pengajuan_saldo if item.get("username") == username]
    if not riwayat_saya:
        print("\nAnda belum pernah mengajukan pengisian saldo.")
        bersihkan_layar_dengan_jeda(1.8)
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
    bersihkan_layar_dengan_jeda(3.5)

def kelola_saldo_user(username):
    while True:
        bersihkan_layar()
        print(f"\n=== SALDO & TOP-UP ({username.upper()}) ===")
        print(f"Saldo Aktif Anda : {format_rupiah(_ambil_saldo(username))}")
        menu_saldo_user(username)

        pilihan = input("Silahkan Pilih Opsi Menu (1-3) : ").strip()
        if pilihan == "1":
            _ajukan_pengisian_saldo(username)
        elif pilihan == "2":
            _lihat_pengajuan_saldo_saya(username)
        elif pilihan == "3":
            bersihkan_layar_dengan_jeda(1.2)
            break
        else:
            print("❗ Opsi Menu yang Dimasukkan Tidak Valid/Terdeteksi")
            bersihkan_layar_dengan_jeda(1.5)

def _input_nama_produk():
    MIN_LEN = 3
    MAX_LEN = 25
    nama_p = input(f"Nama Produk (hanya huruf/spasi, {MIN_LEN}-{MAX_LEN} karakter): ").strip()

    if not (MIN_LEN <= len(nama_p) <= MAX_LEN):
        print(f"❗ Nama produk harus memiliki panjang antara {MIN_LEN} hingga {MAX_LEN} karakter.")
        return None

    if not re.match(r"^[A-Za-z\s]+$", nama_p):
        print("❗ Nama produk hanya boleh mengandung huruf dan spasi (tidak boleh ada angka atau simbol).")
        return None

    return nama_p

def _pilih_tipe_produk():
    print("\n--- PILIH TIPE/KATEGORI PRODUK ---")
    for idx, tipe in enumerate(LIST_TIPE, 1):
        print(f"{idx}. {tipe}")

    while True:
        try:
            pilihan_tipe = int(input(f"Masukkan nomor tipe produk (1-{len(LIST_TIPE)}): "))
            if 1 <= pilihan_tipe <= len(LIST_TIPE):
                tipe_terpilih = LIST_TIPE[pilihan_tipe - 1]
                if tipe_terpilih == "Lainnya":
                    while True:
                        kategori_kustom = input("Masukkan nama kategori produk lainnya (hanya huruf) : ").strip()
                        if not kategori_kustom:
                            print("❗ Kategori produk tidak boleh kosong.")
                            continue
                        if not re.fullmatch(r"[A-Za-z\s]+", kategori_kustom):
                            print("❗ Kategori produk hanya boleh menggunakan huruf dan spasi (tidak boleh angka atau simbol).")
                            continue
                        return kategori_kustom
                return tipe_terpilih
            else:
                print(f"❗ Pilihan tidak valid. Silakan pilih nomor antara 1 hingga {len(LIST_TIPE)}.")
        except ValueError:
            print("❗ Input harus berupa angka. Silakan coba lagi.")

def mulai_jual(username):
    bersihkan_layar()
    print("\n=== TAMBAH PRODUK BARU ===")
    id_baru = generate_id_produk(daftar_produk)
    if not id_baru:
        print("❗ Kapasitas ID produk (K001–K999) sudah penuh!")
        bersihkan_layar_dengan_jeda(1.8)
        return

    print(f"ID Produk Otomatis : {id_baru}")
    print(f"Nama Penjual       : {username}")

    nama_p = _input_nama_produk()
    if nama_p is None:
        print("❗ Proses jual produk dihentikan.")
        bersihkan_layar_dengan_jeda(1.8)
        return

    tipe_p = _pilih_tipe_produk()

    try:
        stok_p = int(input("Jumlah Stok : "))
        harga_p = int(input("Harga Satuan (Rp) : "))
    except ValueError:
        print("❗ Stok dan Harga harus berupa angka!")
        bersihkan_layar_dengan_jeda(1.8)
        return

    if stok_p < 0 or harga_p <= 0:
        print("❗ Stok minimal 0 dan Harga harus lebih dari 0!")
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
    print(f"✅ Berhasil menambahkan produk '{nama_p}' (ID: {id_baru}) oleh penjual '{username}' ke katalog!")
    bersihkan_layar_dengan_jeda(1.8)

def _tampilkan_produk_milik_user(username):
    produk_saya = {
        k_id: p for k_id, p in daftar_produk.items()
        if p.get("Penjual") == username
    }
    if not produk_saya:
        print(f"\nAnda belum memiliki produk yang dijual atas akun '{username}'.")
        return {}

    print(f"\n=== PRODUK MILIK {username.upper()} ===")
    field_names = ["ID", "Nama Produk", "Harga", "Stok", "Tipe", "Deskripsi"]
    rows = [
        [k_id, p["Nama"], format_rupiah(p["Harga"]), p["Stok"], p["Tipe"], p["Deskripsi"]]
        for k_id, p in produk_saya.items()
    ]
    cetak_tabel(field_names, rows)
    return produk_saya

def _ubah_produk_milik_user(username):
    bersihkan_layar()
    produk_saya = _tampilkan_produk_milik_user(username)
    if not produk_saya:
        bersihkan_layar_dengan_jeda(1.5)
        return

    target_id = input("\nMasukkan ID Produk milik Anda yang ingin diubah : ").strip().upper()
    if not target_id:
        return

    if target_id not in daftar_produk:
        print("❗ ID Produk tidak ditemukan di katalog.")
        bersihkan_layar_dengan_jeda(1.8)
        return

    if daftar_produk[target_id].get("Penjual") != username:
        print(
            f"❗ Akses ditolak! Produk '{target_id}' dijual oleh '{daftar_produk[target_id].get('Penjual', '-')}', "
            f"bukan oleh '{username}'."
        )
        bersihkan_layar_dengan_jeda(2.0)
        return

    produk = daftar_produk[target_id]
    print(f"\nMengubah produk '{produk['Nama']}' ({target_id}). Tekan Enter jika tidak ingin mengubah field.")

    nama_baru = input(f"Nama Produk baru [{produk['Nama']}] : ").strip()
    if nama_baru:
        if not (3 <= len(nama_baru) <= 25) or not re.match(r"^[A-Za-z\s]+$", nama_baru):
            print("❗ Nama produk harus 3-25 karakter dan hanya berisi huruf/spasi. Perubahan nama dibatalkan.")
            bersihkan_layar_dengan_jeda(1.8)
        else:
            produk["Nama"] = nama_baru

    ubah_tipe = input(f"Ubah tipe produk [{produk['Tipe']}]? (y/n) : ").strip().lower()
    if ubah_tipe == "y":
        produk["Tipe"] = _pilih_tipe_produk()

    stok_input = input(f"Jumlah Stok baru [{produk['Stok']}] : ").strip()
    if stok_input:
        try:
            stok_baru = int(stok_input)
            if stok_baru < 0:
                print("❗ Stok minimal 0. Perubahan stok dibatalkan.")
                bersihkan_layar_dengan_jeda(1.8)
            else:
                produk["Stok"] = stok_baru
        except ValueError:
            print("❗ Stok harus berupa angka. Perubahan stok dibatalkan.")
            bersihkan_layar_dengan_jeda(1.8)

    harga_input = input(f"Harga Satuan baru [{produk['Harga']}] : ").strip()
    if harga_input:
        try:
            harga_baru = int(harga_input)
            if harga_baru <= 0:
                print("❗ Harga harus lebih dari 0. Perubahan harga dibatalkan.")
                bersihkan_layar_dengan_jeda(1.8)
            else:
                produk["Harga"] = harga_baru
        except ValueError:
            print("❗ Harga harus berupa angka. Perubahan harga dibatalkan.")
            bersihkan_layar_dengan_jeda(1.8)

    desk_input = input(f"Deskripsi baru [{produk['Deskripsi']}] : ").strip()
    if desk_input:
        produk["Deskripsi"] = desk_input

    simpan_database()
    print(f"✅ Perubahan pada produk '{target_id}' berhasil disimpan!")
    bersihkan_layar_dengan_jeda(1.8)

def _hapus_produk_milik_user(username):
    bersihkan_layar()
    produk_saya = _tampilkan_produk_milik_user(username)
    if not produk_saya:
        bersihkan_layar_dengan_jeda(1.5)
        return True

    target_id = input("\nMasukkan ID Produk milik Anda yang ingin dihapus : ").strip().upper()
    if not target_id:
        return False

    if target_id not in daftar_produk:
        print("❗ ID Produk tidak ditemukan di katalog.")
        bersihkan_layar_dengan_jeda(1.8)
        return False

    if daftar_produk[target_id].get("Penjual") != username:
        print(
            f"❗ Akses ditolak! Produk '{target_id}' dijual oleh '{daftar_produk[target_id].get('Penjual', '-')}', "
            f"bukan oleh '{username}'."
        )
        bersihkan_layar_dengan_jeda(2.0)
        return False

    konfirmasi = input(f"Yakin ingin menghapus produk '{daftar_produk[target_id]['Nama']}' ({target_id})? (y/n) : ").strip().lower()
    if konfirmasi == "y":
        del daftar_produk[target_id]
        for cart in keranjang.values():
            cart.pop(target_id, None)
        simpan_database()
        print(f"✅ Produk '{target_id}' berhasil dihapus dari katalog.")
        bersihkan_layar_dengan_jeda(1.8)

        sisa_produk = any(
            p.get("Penjual") == username for p in daftar_produk.values()
        )
        if not sisa_produk:
            print(f"❗ Sudah tidak ada lagi produk yang dijual di akun '{username}'.")
            bersihkan_layar_dengan_jeda(1.8)
            return True
    else:
        print("Penghapusan produk dibatalkan.")
        bersihkan_layar_dengan_jeda(1.5)

    return False

def kelola_produk_saya(username):
    produk_saya = {
        k_id: p for k_id, p in daftar_produk.items()
        if p.get("Penjual") == username
    }

    if not produk_saya:
        print(f"\n❗ Belum ada produk yang dijual di akun '{username}'.")
        bersihkan_layar_dengan_jeda(1.8)
        return

    while True:
        bersihkan_layar()
        print(f"\n=== KELOLA PRODUK SAYA ({username.upper()}) ===")
        _tampilkan_produk_milik_user(username)
        menu_kelola_produk_saya(username)

        pilihan = input("Silahkan Pilih Opsi Menu (1-3) : ").strip()
        if pilihan == "1":
            _ubah_produk_milik_user(username)
        elif pilihan == "2":
            if _hapus_produk_milik_user(username):
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
    print(f"Saldo Anda Saat Ini: {format_rupiah(_ambil_saldo(username))}")
    return True

def checkout_keranjang(username):
    if not keranjang.get(username):
        print("\nKeranjang belanja Anda masih kosong. Tidak ada yang bisa di-checkout.")
        bersihkan_layar_dengan_jeda(1.8)
        return False

    tampilkan_isi_keranjang(username)
    total_belanja = sum(
        daftar_produk[k_id]["Harga"] * jumlah
        for k_id, jumlah in keranjang[username].items()
        if k_id in daftar_produk
    )

    opsi_cart = input("\nIngin melakukan Checkout / Proses Pesanan? (y/n) : ").strip().lower()
    if opsi_cart == "y":
        for k_id, jumlah in keranjang[username].items():
            if k_id not in daftar_produk:
                print(f"❗ Produk dengan ID '{k_id}' sudah tidak tersedia di katalog.")
                bersihkan_layar_dengan_jeda(1.8)
                return False
            if jumlah > daftar_produk[k_id]["Stok"]:
                print(f"❗ Stok produk '{daftar_produk[k_id]['Nama']}' tidak mencukupi untuk checkout.")
                bersihkan_layar_dengan_jeda(1.8)
                return False

        saldo_saat_ini = _ambil_saldo(username)
        if saldo_saat_ini < total_belanja:
            kekurangan = total_belanja - saldo_saat_ini
            print(
                f"\n❌ ERROR: Saldo Anda tidak cukup untuk melakukan checkout!\n"
                f"   Total Belanja : {format_rupiah(total_belanja)}\n"
                f"   Saldo Anda    : {format_rupiah(saldo_saat_ini)}\n"
                f"   Kekurangan    : {format_rupiah(kekurangan)}\n"
                f"   Silakan ajukan pengisian saldo terlebih dahulu dan tunggu persetujuan Admin."
            )
            bersihkan_layar_dengan_jeda(2.5)
            return False

        items_struk = []
        for k_id, jumlah in keranjang[username].items():
            p = daftar_produk[k_id]
            p["Stok"] -= jumlah
            items_struk.append((p["Nama"], p["Harga"], jumlah))

        saldo_user[username] = saldo_saat_ini - total_belanja

        riwayat_pesanan.setdefault(username, [])
        riwayat_pesanan[username].append({
            "Item": keranjang[username].copy(),
            "Total": total_belanja,
        })

        keranjang[username] = {}
        simpan_database()
        print("\n✅ Checkout Berhasil! Saldo telah dipotong, stok diperbarui, dan pesanan sedang diproses.")
        cetak_struk(username, items_struk, total_belanja, saldo=saldo_user[username])
        bersihkan_layar_dengan_jeda(5.0)
        return True
    else:
        print("Checkout dibatalkan.")
        bersihkan_layar_dengan_jeda(1.5)
        return False

def hapus_keranjang(username):
    if not keranjang.get(username):
        print("\nKeranjang belanja Anda masih kosong.")
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

            hapus_id = input("\nMasukkan ID Produk yang ingin dihapus : ").strip().upper()
            if hapus_id in keranjang[username]:
                nama_produk = daftar_produk.get(hapus_id, {}).get("Nama", hapus_id)
                del keranjang[username][hapus_id]
                simpan_database()
                print(f"\n✅ Berhasil menghapus produk '{nama_produk}' (ID: {hapus_id}) dari keranjang!")
                bersihkan_layar_dengan_jeda(1.8)

                if not keranjang[username]:
                    print("Keranjang Anda sekarang sudah kosong.")
                    bersihkan_layar_dengan_jeda(1.5)
                    break
            else:
                print("❗ ID Produk tersebut tidak ditemukan di dalam keranjang belanja Anda.")
                bersihkan_layar_dengan_jeda(1.8)

        elif pilihan_hapus == "2":
            konfirmasi = input("\nApakah Anda yakin ingin mengosongkan SELURUH isi keranjang? (y/n) : ").strip().lower()
            if konfirmasi == "y":
                keranjang[username] = {}
                simpan_database()
                print("\n✅ Berhasil mengosongkan seluruh keranjang belanja!")
                bersihkan_layar_dengan_jeda(1.8)
                break
            else:
                print("Penghapusan keranjang dibatalkan.")
                bersihkan_layar_dengan_jeda(1.5)

        elif pilihan_hapus == "3":
            bersihkan_layar_dengan_jeda(1.2)
            break
        else:
            print("❗ Opsi Menu yang Dimasukkan Tidak Valid/Terdeteksi")
            bersihkan_layar_dengan_jeda(1.5)

def _tambah_produk_ke_keranjang(username):
    while True:
        beli_id = input("\nMasukkan ID Produk yang ingin dibeli (kosongkan lalu Enter untuk ke menu keranjang) : ").strip().upper()
        if not beli_id:
            break

        if beli_id not in daftar_produk:
            print("❗ ID Produk tidak ditemukan di katalog.")
            continue

        try:
            jml = int(input(f"Masukkan jumlah '{daftar_produk[beli_id]['Nama']}' yang ingin dibeli : "))
        except ValueError:
            print("❗ Jumlah harus berupa angka!")
            continue

        if jml <= 0:
            print("❗ Jumlah beli minimal 1.")
            continue
        elif jml > daftar_produk[beli_id]["Stok"]:
            print(f"❗ Stok tidak mencukupi! Sisa stok saat ini: {daftar_produk[beli_id]['Stok']}")
            continue

        keranjang.setdefault(username, {})
        keranjang[username][beli_id] = keranjang[username].get(beli_id, 0) + jml
        simpan_database()
        print(f"✅ Berhasil menambahkan {jml} pcs '{daftar_produk[beli_id]['Nama']}' ke keranjang belanja!")

def _tampilkan_katalog():
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

        print(f"\n=== AKSI KERANJANG & CHECKOUT ({username.upper()}) ===")
        tampilkan_isi_keranjang(username)
        menu_katalog_keranjang(username)

        pilihan_aksi = input("Silahkan Pilih Opsi Menu (1-4) : ").strip()

        if pilihan_aksi == "1":
            # Isi keranjang sudah tampil di atas; loop langsung mengulang
            continue
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
        print("\n❗ Katalog produk masih kosong! Belum ada barang yang tersedia.")
        bersihkan_layar_dengan_jeda(1.8)
        return
    _tampilkan_katalog()
    _tambah_produk_ke_keranjang(username)
    kelola_keranjang_dan_checkout(username, lewati_bersihkan_awal=True)

def lihat_pesanan(username):
    if not riwayat_pesanan.get(username):
        print("\nAnda belum memiliki riwayat pesanan.")
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
        bersihkan_layar_dengan_jeda(4.5)

def tampilkan_menu_user(username):
    while True:
        bersihkan_layar()
        print(f"\n=== MENU AKSES USER ({username}) ===")
        print(f"Saldo Anda : {format_rupiah(_ambil_saldo(username))}")
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