import re
from database import daftar_produk, keranjang, riwayat_pesanan
from utils import cetak_tabel, menu_user

def mulai_jual():
    print("\n=== TAMBAH PRODUK BARU ===")
    id_baru = input("Masukkan ID Produk (Contoh: K005) : ").strip()
    if id_baru in daftar_produk:
        print("❗ ID Produk sudah terdaftar! Gunakan ID lain.")
        return

    MIN_LEN = 3
    MAX_LEN = 15

    while True:
        nama_p = input(f"Nama Produk (hanya huruf, {MIN_LEN}-{MAX_LEN} karakter): ").strip()

        if not (MIN_LEN <= len(nama_p) <= MAX_LEN):
            print (f"❗ Nama produk harus memiliki panjang antara {MIN_LEN} hingga {MAX_LEN} karakter.")
            continue

        if not re.match("^[A-Za-z\\s]+$", nama_p):
            print("❗Nama produk hanya boleh mengandung huruf dan spasi (tidak boleh ada angka atau simbol).")
            continue

        break

    while True:
        nama_penjual = input("Nama Penjual : ").strip()
        if not nama_penjual:
            print("❗ Nama penjual tidak boleh kosong. Silakan masukkan nama penjual.")
            continue
        break

    list_tipe = ["Elektronik", "Pakaian", "Kecantikan", "Makanan", "Minuman", "Lainnya"]

    print("\n--- PILIH TIPE/KATEGORI PRODUK ---")
    for idx, tipe in enumerate(list_tipe, 1):
        print(f"{idx}. {tipe}")

    while True:
        try:
            pilihan_tipe = int(input("Masukkan nomor tipe produk (1-6): "))
            if 1 <= pilihan_tipe <= len(list_tipe):
                tipe_p = list_tipe[pilihan_tipe - 1]
                break
            else:
                print("❗ Pilihan tidak valid. Silakan pilih nomor antara 1 hingga 6.")
        except ValueError:
            print("❗ Input harus berupa angka. Silakan coba lagi.")

    try:
        stok_p = int(input("Jumlah Stok : "))
        harga_p = int(input("Harga Satuan (Rp) : "))
    except ValueError:
        print("❗ Stok dan Harga harus berupa angka!")
        return
        
    desk_p = input("Deskripsi Produk : ").strip()
    
    daftar_produk[id_baru] = {
        "Nama": nama_p,
        "Stok": stok_p,
        "Tipe": tipe_p,
        "Harga": harga_p,
        "Deskripsi": desk_p
    }
    print(f"✅ Berhasil menambahkan produk '{nama_p}' dengan tipe '{tipe_p}' ke katalog!")

def lihat_katalog_dan_beli(username):
    print("\n=== KATALOG PRODUK E-COMMERCE ===")
    field_names = ["ID", "Nama Produk", "Harga", "Stok", "Tipe", "Penjual", "Deskripsi"]
    rows = []
    for k_id, p in daftar_produk.items():

        penjual = p.get("Penjual", "-")
        rows.append([k_id, p["Nama"], f"Rp{p['Harga']:,}", p["Stok"], p["Tipe"], penjual, p["Deskripsi"]])
    
    cetak_tabel(field_names, rows)
    
    beli_id = input("\nMasukkan ID Produk yang ingin dimasukkan ke keranjang (atau ketik 'batal'): ").strip()
    if beli_id.lower() == 'batal':
        return
        
    if beli_id in daftar_produk:
        try:
            jml = int(input(f"Masukkan jumlah '{daftar_produk[beli_id]['Nama']}' yang ingin dibeli: "))
        except ValueError:
            print("❗ Jumlah harus berupa angka!")
            return
            
        if jml <= 0:
            print("❗ Jumlah beli minimal 1.")
        elif jml > daftar_produk[beli_id]["Stok"]:
            print(f"❗ Stok tidak mencukupi! Sisa stok saat ini: {daftar_produk[beli_id]['Stok']}")
        else:
            if username not in keranjang:
                keranjang[username] = {}
                
            if beli_id in keranjang[username]:
                keranjang[username][beli_id] += jml
            else:
                keranjang[username][beli_id] = jml
                
            print(f"✅ Berhasil menambahkan {jml} pcs '{daftar_produk[beli_id]['Nama']}' ke keranjang belanja!")
    else:
        print("❗ ID Produk tidak ditemukan di katalog.")

def lihat_dan_checkout_keranjang(username):
    if username not in keranjang or not keranjang[username]:
        print("\nKeranjang belanja Anda masih kosong.")
        return
        
    print(f"\n=== KERANJANG BELANJA MILIK {username.upper()} ===")
    field_names = ["ID Produk", "Nama Produk", "Harga Satuan", "Jumlah", "Subtotal"]
    rows = []
    total_belanja = 0
    
    for k_id, jumlah in keranjang[username].items():
        p = daftar_produk[k_id]
        subtotal = p["Harga"] * jumlah
        total_belanja += subtotal
        rows.append([k_id, p["Nama"], f"Rp{p['Harga']:,}", jumlah, f"Rp{subtotal:,}"])
        
    cetak_tabel(field_names, rows)
    print(f"Total Keseluruhan : Rp{total_belanja:,}")
    
    opsi_cart = input("\nIngin melakukan Checkout / Proses Pesanan? (y/n) : ")
    if opsi_cart.lower() == 'y':
        for k_id, jumlah in keranjang[username].items():
            daftar_produk[k_id]["Stok"] -= jumlah
            
        if username not in riwayat_pesanan:
            riwayat_pesanan[username] = []
            
        riwayat_pesanan[username].append({
            "Item": keranjang[username].copy(),
            "Total": total_belanja
        })
        
        keranjang[username] = {}
        print("\n✅ Checkout Berhasil! Stok produk telah diperbarui (dikurangi), dan pesanan sedang diproses.")
    else:
        print("Checkout dibatalkan.")

def lihat_pesanan(username):
    if username not in riwayat_pesanan or not riwayat_pesanan[username]:
        print("\nAnda belum memiliki riwayat pesanan.")
    else:
        print(f"\n=== RIWAYAT PESANAN SAYA ({username}) ===")
        field_names = ["ID Produk", "Nama Produk", "Jumlah Beli"]
        for idx, pesanan in enumerate(riwayat_pesanan[username], 1):
            print(f"\nPesanan #{idx} (Total: Rp{pesanan['Total']:,})")
            rows = [[k_id, daftar_produk[k_id]["Nama"], jml] for k_id, jml in pesanan["Item"].items()]
            cetak_tabel(field_names, rows)
            
def hapus_keranjang(username):
    if username not in keranjang or not keranjang[username]:
        print("\nKeranjang belanja Anda masih kosong.")
        return
        
    while True:
        print(f"\n=== KELOLA PENGHAPUSAN KERANJANG ({username.upper()}) ===")
        
        field_names_menu = ["No", "Opsi Menu Hapus Keranjang"]
        rows_menu = [
            ["1", "Hapus Produk Tertentu (Berdasarkan ID)"],
            ["2", "Kosongkan Seluruh Keranjang Belanja"],
            ["3", "Kembali ke Menu Utama User"]
        ]
        cetak_tabel(field_names_menu, rows_menu)
        
        pilihan_hapus = input("Silahkan Pilih Opsi Penghapusan (1-3) : ").strip()
        
        if pilihan_hapus == "1":
            print(f"\n=== ISI KERANJANG BELANJA ===")
            field_names_cart = ["ID Produk", "Nama Produk", "Harga Satuan", "Jumlah", "Subtotal"]
            rows_cart = []
            
            for k_id, jumlah in keranjang[username].items():
                p = daftar_produk[k_id]
                subtotal = p["Harga"] * jumlah
                rows_cart.append([k_id, p["Nama"], f"Rp{p['Harga']:,}", jumlah, f"Rp{subtotal:,}"])
                
            cetak_tabel(field_names_cart, rows_cart)
            
            hapus_id = input("\nMasukkan ID Produk yang ingin dihapus (atau ketik 'batal'): ").strip()
            if hapus_id.lower() == 'batal':
                continue
                
            if hapus_id in keranjang[username]:
                nama_produk = daftar_produk[hapus_id]["Nama"]
                del keranjang[username][hapus_id]
                print(f"\n✅ Berhasil menghapus produk '{nama_produk}' (ID: {hapus_id}) dari keranjang!")
                
                if not keranjang[username]:
                    print("Keranjang Anda sekarang sudah kosong.")
                    break
            else:
                print("❗ ID Produk tersebut tidak ditemukan di dalam keranjang belanja Anda.")
                
        elif pilihan_hapus == "2":
            konfirmasi = input("\nApakah Anda yakin ingin mengosongkan SELURUH isi keranjang? (y/n) : ").strip()
            if konfirmasi.lower() == 'y':
                keranjang[username] = {}
                print("\n✅ Berhasil mengosongkan seluruh keranjang belanja!")
                break
            else:
                print("Penghapusan keranjang dibatalkan.")
                
        elif pilihan_hapus == "3":
            break
        else:
            print("❗ Opsi Menu yang Dimasukkan Tidak Valid/Terdeteksi")

def tampilkan_menu_user(username):
    while True:
        print(f"\n=== MENU AKSES USER ({username}) ===")
        menu_user(username)
        
        pilihan_user = input("Silahkan Pilih Opsi Menu (1-6) : ")
        
        if pilihan_user == "1":
            mulai_jual()
        elif pilihan_user == "2":
            lihat_katalog_dan_beli(username)
        elif pilihan_user == "3":
            lihat_dan_checkout_keranjang(username)
        elif pilihan_user == "4":
            hapus_keranjang(username)
        elif pilihan_user == "5":
            lihat_pesanan(username)
        elif pilihan_user == "6":
            print("✅ Berhasil Keluar dari Menu Akses User!")
            break
        else:
            print("❗ Opsi Menu yang Dimasukkan Tidak Valid/Terdeteksi")