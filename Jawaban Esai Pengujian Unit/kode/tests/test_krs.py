"""Unit test untuk src/krs.py menggunakan stub (soal 11).

Stub menggantikan database mahasiswa, kurikulum, dan penyimpanan KRS agar
pengujian cepat, deterministik, dan tidak membutuhkan database nyata.
"""

from __future__ import annotations

import unittest

from src.krs import (
    LayananKRS,
    Mahasiswa,
    MataKuliah,
    cek_prasyarat,
    cek_status_aktif,
    hitung_total_sks,
    validasi_beban_sks,
)


class RepoMahasiswaStub:
    """Stub repository mahasiswa: mengembalikan data yang sudah ditentukan."""

    def __init__(self, data: dict[str, Mahasiswa]) -> None:
        self.data = data
        self.dipanggil_dengan: list[str] = []

    def cari(self, nim: str) -> Mahasiswa | None:
        self.dipanggil_dengan.append(nim)
        return self.data.get(nim)


class RepoKurikulumStub:
    """Stub repository kurikulum: mengembalikan mata kuliah dari dictionary."""

    def __init__(self, data: dict[str, MataKuliah]) -> None:
        self.data = data
        self.dipanggil_dengan: list[str] = []

    def cari(self, kode: str) -> MataKuliah | None:
        self.dipanggil_dengan.append(kode)
        return self.data.get(kode)


class PenyimpananStub:
    """Stub penyimpanan KRS yang merekam data yang hendak disimpan."""

    def __init__(self, gagal: bool = False) -> None:
        self.gagal = gagal
        self.tersimpan: list[tuple[str, tuple[str, ...]]] = []

    def simpan(self, nim: str, daftar_kode: tuple[str, ...]) -> str:
        if self.gagal:
            raise RuntimeError("Koneksi database terputus")
        self.tersimpan.append((nim, tuple(daftar_kode)))
        return f"KRS-{nim}"


MAHASISWA_AKTIF = Mahasiswa(
    nim="2023230006",
    nama="Muhammad Arya Fatthurahman",
    status="Aktif",
    mk_lulus=frozenset({"TI101", "TI102"}),
)
MAHASISWA_NONAKTIF = Mahasiswa(
    nim="2023000001", nama="Mahasiswa Cuti", status="Cuti"
)

MK_PEMROGRAMAN = MataKuliah("TI201", "Pemrograman Lanjut", 3, ("TI101",))
MK_BASIS_DATA = MataKuliah("TI202", "Basis Data", 3, ("TI102",))
MK_UMUM = MataKuliah("TI203", "Kewirausahaan", 2)
MK_TANPA_PRASYARAT = MataKuliah("TI204", "Etika Profesi", 2)


def buat_layanan(
    mahasiswa: dict[str, Mahasiswa] | None = None,
    kurikulum: dict[str, MataKuliah] | None = None,
    penyimpanan: PenyimpananStub | None = None,
) -> tuple[LayananKRS, PenyimpananStub]:
    """Membuat LayananKRS dengan dependensi tiruan (dependency injection)."""
    repo_mhs = RepoMahasiswaStub(
        mahasiswa if mahasiswa is not None else {MAHASISWA_AKTIF.nim: MAHASISWA_AKTIF}
    )
    repo_kur = RepoKurikulumStub(
        kurikulum
        if kurikulum is not None
        else {
            "TI201": MK_PEMROGRAMAN,
            "TI202": MK_BASIS_DATA,
            "TI203": MK_UMUM,
            "TI204": MK_TANPA_PRASYARAT,
        }
    )
    penyimpanan = penyimpanan or PenyimpananStub()
    return LayananKRS(repo_mhs, repo_kur, penyimpanan), penyimpanan


class TestFungsiDasarKRS(unittest.TestCase):
    """Pengujian unit-unit kecil KRS."""

    def test_status_aktif(self) -> None:
        self.assertTrue(cek_status_aktif(MAHASISWA_AKTIF))
        self.assertFalse(cek_status_aktif(MAHASISWA_NONAKTIF))
        self.assertFalse(cek_status_aktif(None))

    def test_prasyarat(self) -> None:
        self.assertTrue(cek_prasyarat(MAHASISWA_AKTIF, MK_PEMROGRAMAN))
        self.assertTrue(cek_prasyarat(MAHASISWA_AKTIF, MK_TANPA_PRASYARAT))

        mahasiswa_baru = Mahasiswa("2023000002", "Mahasiswa Baru", "Aktif")
        self.assertFalse(cek_prasyarat(mahasiswa_baru, MK_PEMROGRAMAN))

    def test_hitung_total_sks(self) -> None:
        self.assertEqual(
            hitung_total_sks([MK_PEMROGRAMAN, MK_BASIS_DATA, MK_UMUM]), 8
        )
        self.assertEqual(hitung_total_sks([]), 0)

    def test_batas_beban_sks(self) -> None:
        validasi_beban_sks(0)   # batas bawah, tidak error
        validasi_beban_sks(24)  # tepat pada batas, tidak error

        with self.assertRaises(ValueError):
            validasi_beban_sks(25)

        with self.assertRaises(ValueError):
            validasi_beban_sks(-1)


class TestAjukanKRS(unittest.TestCase):
    """Pengujian orkestrasi pengajuan KRS."""

    def test_krs_valid_disimpan_dengan_payload_benar(self) -> None:
        layanan, penyimpanan = buat_layanan()

        hasil = layanan.ajukan_krs("2023230006", ["TI201", "TI202", "TI203"])

        self.assertEqual(hasil, "KRS-2023230006")
        self.assertEqual(
            penyimpanan.tersimpan,
            [("2023230006", ("TI201", "TI202", "TI203"))],
        )

    def test_mahasiswa_tidak_aktif_ditolak_tanpa_menyimpan(self) -> None:
        layanan, penyimpanan = buat_layanan(
            mahasiswa={MAHASISWA_NONAKTIF.nim: MAHASISWA_NONAKTIF}
        )

        with self.assertRaises(PermissionError):
            layanan.ajukan_krs(MAHASISWA_NONAKTIF.nim, ["TI203"])

        self.assertEqual(penyimpanan.tersimpan, [])

    def test_mahasiswa_tidak_ditemukan(self) -> None:
        layanan, _ = buat_layanan()

        with self.assertRaises(LookupError):
            layanan.ajukan_krs("9999999999", ["TI203"])

    def test_prasyarat_belum_lulus_ditolak(self) -> None:
        mahasiswa_baru = Mahasiswa("2023000002", "Mahasiswa Baru", "Aktif")
        layanan, penyimpanan = buat_layanan(
            mahasiswa={mahasiswa_baru.nim: mahasiswa_baru}
        )

        with self.assertRaises(ValueError):
            layanan.ajukan_krs(mahasiswa_baru.nim, ["TI201"])

        self.assertEqual(penyimpanan.tersimpan, [])

    def test_sks_melebihi_batas_ditolak(self) -> None:
        # Delapan mata kuliah x 3 SKS = 24 SKS (lolos), tambah satu MK = 27 (gagal).
        kurikulum = {
            f"TI30{i}": MataKuliah(f"TI30{i}", f"Mata Kuliah {i}", 3)
            for i in range(9)
        }
        layanan, penyimpanan = buat_layanan(kurikulum=kurikulum)
        daftar = [f"TI30{i}" for i in range(8)]
        layanan.ajukan_krs("2023230006", daftar)  # 24 SKS, harus lolos
        self.assertEqual(len(penyimpanan.tersimpan), 1)

        with self.assertRaises(ValueError):
            layanan.ajukan_krs("2023230006", daftar + ["TI308"])  # 27 SKS

    def test_mata_kuliah_duplikat_ditolak(self) -> None:
        layanan, _ = buat_layanan()

        with self.assertRaises(ValueError):
            layanan.ajukan_krs("2023230006", ["TI203", "TI203"])

    def test_mata_kuliah_tidak_ada_di_kurikulum(self) -> None:
        layanan, _ = buat_layanan()

        with self.assertRaises(LookupError):
            layanan.ajukan_krs("2023230006", ["TI999"])

    def test_kegagalan_database_diteruskan_ke_pemanggil(self) -> None:
        penyimpanan_gagal = PenyimpananStub(gagal=True)
        layanan, _ = buat_layanan(penyimpanan=penyimpanan_gagal)

        with self.assertRaises(RuntimeError):
            layanan.ajukan_krs("2023230006", ["TI203"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
