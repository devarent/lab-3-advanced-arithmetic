"""Fungsi inti yang digunakan pada jawaban soal esai Pengujian Unit.

Modul ini sengaja dibuat kecil dan murni (pure function) agar mudah diuji
secara terisolasi. Setiap fungsi memiliki satu tanggung jawab utama.
"""

from __future__ import annotations

BATAS_LULUS = 60
BIAYA_ADMIN_DEFAULT = 5_000
MAKS_SKS = 24


def status_kelulusan(nilai: float) -> str:
    """Menentukan status kelulusan mahasiswa.

    Spesifikasi: mahasiswa dinyatakan Lulus jika nilai akhir minimal 60.

    Args:
        nilai: Nilai akhir mahasiswa pada rentang 0-100.

    Returns:
        "Lulus" atau "Tidak Lulus".

    Raises:
        TypeError: Jika nilai bukan angka.
        ValueError: Jika nilai di luar rentang 0-100.
    """
    if isinstance(nilai, bool) or not isinstance(nilai, (int, float)):
        raise TypeError("nilai harus berupa angka")
    if not 0 <= nilai <= 100:
        raise ValueError("nilai harus berada pada rentang 0-100")

    # Perhatikan operator >=. Operator > akan menimbulkan bug off-by-one
    # pada nilai tepat 60 (lihat demo_bug_operator.py).
    return "Lulus" if nilai >= BATAS_LULUS else "Tidak Lulus"


def hitung_tagihan(
    harga: int,
    biaya_admin: int = BIAYA_ADMIN_DEFAULT,
    persen_diskon: float = 0.0,
) -> int:
    """Menghitung total tagihan mahasiswa.

    Total = harga - diskon + biaya_admin.
    Diskon hanya dihitung dari harga barang, bukan dari biaya administrasi.
    Fitur diskon mahasiswa ditambahkan tanpa mengubah perilaku lama saat
    persen_diskon bernilai 0.

    Args:
        harga: Harga sebelum diskon (rupiah, bilangan bulat >= 0).
        biaya_admin: Biaya administrasi (rupiah, bilangan bulat >= 0).
        persen_diskon: Persentase diskon pada rentang 0-100.

    Returns:
        Total tagihan dalam rupiah (bilangan bulat).

    Raises:
        ValueError: Jika harga/biaya_admin negatif atau persen tidak valid.
    """
    if harga < 0:
        raise ValueError("harga tidak boleh negatif")
    if biaya_admin < 0:
        raise ValueError("biaya_admin tidak boleh negatif")
    if not 0 <= persen_diskon <= 100:
        raise ValueError("persen_diskon harus berada pada rentang 0-100")

    diskon = round(harga * persen_diskon / 100)
    return int(round(harga - diskon + biaya_admin))


def hitung_luas_persegi_panjang(panjang: float, lebar: float) -> float:
    """Menghitung luas persegi panjang (contoh siklus TDD).

    Args:
        panjang: Sisi panjang, harus lebih besar dari 0.
        lebar: Sisi lebar, harus lebih besar dari 0.

    Returns:
        Luas persegi panjang.

    Raises:
        ValueError: Jika panjang atau lebar tidak positif.
    """
    if panjang <= 0 or lebar <= 0:
        raise ValueError("panjang dan lebar harus lebih besar dari 0")
    return float(panjang * lebar)
