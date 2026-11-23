import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, "database.json")

DATA_DEFAULT = {
    "akun_admin": {
        "Admin": "Pyc1#"
    },
    "akun_user": {},
    "saldo_user": {},
    "pengajuan_saldo": [],
    "daftar_produk": {},
    "keranjang": {},
    "riwayat_pesanan": {}
}

def _salin_default():
    return json.loads(json.dumps(DATA_DEFAULT))

def simpan_database():
    payload = {
        "akun_admin": akun_admin,
        "akun_user": akun_user,
        "saldo_user": saldo_user,
        "pengajuan_saldo": pengajuan_saldo,
        "daftar_produk": daftar_produk,
        "keranjang": keranjang,
        "riwayat_pesanan": riwayat_pesanan,
    }
    with open(DB_FILE, "w", encoding="utf-8") as file:
        json.dump(payload, file, indent=2, ensure_ascii=False)

def muat_database():
    if not os.path.exists(DB_FILE):
        data = _salin_default()
        with open(DB_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return data

    try:
        with open(DB_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (json.JSONDecodeError, OSError):
        data = _salin_default()

    default = _salin_default()
    saldo_dimuat = data.get("saldo_user", default["saldo_user"])
    if not isinstance(saldo_dimuat, dict):
        saldo_dimuat = default["saldo_user"]

    for user in data.get("akun_user", {}):
        saldo_dimuat.setdefault(user, 0)

    pengajuan_dimuat = data.get("pengajuan_saldo", default["pengajuan_saldo"])
    if not isinstance(pengajuan_dimuat, list):
        pengajuan_dimuat = []

    return {
        "akun_admin": data.get("akun_admin", default["akun_admin"]),
        "akun_user": data.get("akun_user", default["akun_user"]),
        "saldo_user": saldo_dimuat,
        "pengajuan_saldo": pengajuan_dimuat,
        "daftar_produk": data.get("daftar_produk", default["daftar_produk"]),
        "keranjang": data.get("keranjang", default["keranjang"]),
        "riwayat_pesanan": data.get("riwayat_pesanan", default["riwayat_pesanan"]),
    }

_data = muat_database()
akun_admin = _data["akun_admin"]
akun_user = _data["akun_user"]
saldo_user = _data["saldo_user"]
pengajuan_saldo = _data["pengajuan_saldo"]
daftar_produk = _data["daftar_produk"]
keranjang = _data["keranjang"]
riwayat_pesanan = _data["riwayat_pesanan"]