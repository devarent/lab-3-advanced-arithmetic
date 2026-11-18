"""Unit test untuk src/akademik.py.

Mencakup soal nomor 6 (status kelulusan), nomor 8 (regresi tagihan),
dan nomor 9 (TDD luas persegi panjang).
"""

from __future__ import annotations

import unittest

from src.akademik import (
    hitung_luas_persegi_panjang,
    hitung_tagihan,
    status_kelulusan,
)


class TestStatusKelulusan(unittest.TestCase):
    """Soal 6: batas kelulusan nilai 60."""

    def test_kasus_batas_kelulusan(self) -> None:
        # Tabel test case: di bawah, tepat di bawah, tepat pada, dan di atas batas.
        test_cases = [
            (0, "Tidak Lulus"),    # batas bawah rentang nilai
            (50, "Tidak Lulus"),   # di bawah batas
            (59, "Tidak Lulus"),   # tepat satu poin di bawah batas
            (60, "Lulus"),         # TEPAT PADA BATAS (paling penting)
            (61, "Lulus"),         # tepat satu poin di atas batas
            (80, "Lulus"),         # di atas batas
            (100, "Lulus"),        # batas atas rentang nilai
        ]
        for nilai, expected in test_cases:
            with self.subTest(nilai=nilai):
                self.assertEqual(status_kelulusan(nilai), expected)

    def test_nilai_di_luar_rentang_ditolak(self) -> None:
        for nilai in (-1, 101, -0.5, 100.5):
            with self.subTest(nilai=nilai):
                with self.assertRaises(ValueError):
                    status_kelulusan(nilai)

    def test_tipe_data_bukan_angka_ditolak(self) -> None:
        for nilai in ("60", None, True):
            with self.subTest(nilai=nilai):
                with self.assertRaises(TypeError):
                    status_kelulusan(nilai)  # type: ignore[arg-type]


class TestHitungTagihan(unittest.TestCase):
    """Soal 8: fitur diskon mahasiswa dan regression testing."""

    def test_tc_r1_tagihan_normal_tanpa_diskon_tetap_benar(self) -> None:
        # Regression test: perilaku lama tidak boleh berubah.
        self.assertEqual(hitung_tagihan(100_000, 5_000, 0), 105_000)

    def test_tc_r2_diskon_mahasiswa_10_persen(self) -> None:
        # Fitur baru: 100.000 - 10.000 + 5.000 = 95.000
        self.assertEqual(hitung_tagihan(100_000, 5_000, 10), 95_000)

    def test_tc_r3_biaya_admin_tidak_ikut_didiskon(self) -> None:
        # Diskon 25% hanya dari harga: 200.000 - 50.000 + 5.000 = 155.000
        self.assertEqual(hitung_tagihan(200_000, 5_000, 25), 155_000)

    def test_tc_r4_diskon_100_persen_hanya_bayar_admin(self) -> None:
        self.assertEqual(hitung_tagihan(100_000, 5_000, 100), 5_000)

    def test_tc_r5_input_tidak_valid_ditolak(self) -> None:
        with self.assertRaises(ValueError):
            hitung_tagihan(-1, 5_000, 0)
        with self.assertRaises(ValueError):
            hitung_tagihan(100_000, -1, 0)
        with self.assertRaises(ValueError):
            hitung_tagihan(100_000, 5_000, 101)


class TestHitungLuasPersegiPanjang(unittest.TestCase):
    """Soal 9: contoh siklus Red-Green-Refactor."""

    def test_luas_4_kali_5_adalah_20(self) -> None:
        self.assertEqual(hitung_luas_persegi_panjang(4, 5), 20)

    def test_luas_dengan_bilangan_desimal(self) -> None:
        self.assertAlmostEqual(hitung_luas_persegi_panjang(2.5, 4), 10.0)

    def test_dimensi_tidak_positif_ditolak(self) -> None:
        for panjang, lebar in ((0, 5), (-1, 5), (4, 0), (4, -2)):
            with self.subTest(panjang=panjang, lebar=lebar):
                with self.assertRaises(ValueError):
                    hitung_luas_persegi_panjang(panjang, lebar)


if __name__ == "__main__":
    unittest.main(verbosity=2)
