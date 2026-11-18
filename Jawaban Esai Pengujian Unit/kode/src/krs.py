"""Logika aplikasi KRS yang dirancang agar mudah diuji secara terisolasi.

Dependensi eksternal (database mahasiswa, kurikulum, dan penyimpanan KRS)
tidak dipanggil langsung. Semuanya diterima melalui constructor sehingga
dapat diganti dengan stub pada saat unit testing.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Protocol, Sequence

MAKS_SKS = 24


@dataclass(frozen=True)
class Mahasiswa:
    """Data mahasiswa yang dibutuhkan oleh logika KRS."""

    nim: str
    nama: str
    status: str
    mk_lulus: frozenset[str] = frozenset()


@dataclass(frozen=True)
class MataKuliah:
    """Data mata kuliah beserta prasyaratnya."""

    kode: str
    nama: str
    sks: int
    prasyarat: tuple[str, ...] = ()


class RepoMahasiswa(Protocol):
    """Antarmuka repository data mahasiswa (dapat diganti stub)."""

    def cari(self, nim: str) -> Mahasiswa | None:
        ...


class RepoKurikulum(Protocol):
    """Antarmuka repository data mata kuliah (dapat diganti stub)."""

    def cari(self, kode: str) -> MataKuliah | None:
        ...


class PenyimpananKRS(Protocol):
    """Antarmuka penyimpanan KRS, misalnya tabel database."""

    def simpan(self, nim: str, daftar_kode: Sequence[str]) -> str:
        ...


def cek_status_aktif(mahasiswa: Mahasiswa | None) -> bool:
    """Mengembalikan True jika mahasiswa ada dan berstatus aktif."""
    return mahasiswa is not None and mahasiswa.status.strip().lower() == "aktif"


def cek_prasyarat(mahasiswa: Mahasiswa, mata_kuliah: MataKuliah) -> bool:
    """Mengembalikan True jika seluruh prasyarat mata kuliah sudah lulus."""
    return all(kode in mahasiswa.mk_lulus for kode in mata_kuliah.prasyarat)


def hitung_total_sks(daftar_mk: Iterable[MataKuliah]) -> int:
    """Menjumlahkan SKS dari daftar mata kuliah."""
    return sum(mk.sks for mk in daftar_mk)


def validasi_beban_sks(total_sks: int, maks_sks: int = MAKS_SKS) -> None:
    """Memastikan beban SKS berada pada rentang yang diizinkan.

    Raises:
        ValueError: Jika total SKS negatif atau melebihi batas.
    """
    if total_sks < 0:
        raise ValueError("total SKS tidak boleh negatif")
    if total_sks > maks_sks:
        raise ValueError(
            f"Beban {total_sks} SKS melebihi batas maksimum {maks_sks} SKS"
        )


class LayananKRS:
    """Orkestrator pengajuan KRS.

    Args:
        repo_mahasiswa: Sumber data mahasiswa.
        repo_kurikulum: Sumber data mata kuliah.
        penyimpanan: Komponen yang menyimpan KRS.
    """

    def __init__(
        self,
        repo_mahasiswa: RepoMahasiswa,
        repo_kurikulum: RepoKurikulum,
        penyimpanan: PenyimpananKRS,
    ) -> None:
        self.repo_mahasiswa = repo_mahasiswa
        self.repo_kurikulum = repo_kurikulum
        self.penyimpanan = penyimpanan

    def ambil_mata_kuliah(self, daftar_kode: Sequence[str]) -> list[MataKuliah]:
        """Mengambil seluruh data mata kuliah atau gagal jika ada yang tidak ada."""
        hasil: list[MataKuliah] = []
        for kode in daftar_kode:
            mata_kuliah = self.repo_kurikulum.cari(kode)
            if mata_kuliah is None:
                raise LookupError(f"Mata kuliah {kode} tidak ditemukan")
            hasil.append(mata_kuliah)
        return hasil

    def ajukan_krs(self, nim: str, daftar_kode: Sequence[str]) -> str:
        """Memvalidasi dan menyimpan KRS.

        Urutan validasi:
        1. Mahasiswa harus ada dan berstatus aktif.
        2. Tidak boleh ada mata kuliah duplikat.
        3. Seluruh mata kuliah harus ada di kurikulum.
        4. Seluruh prasyarat harus sudah lulus.
        5. Total SKS tidak boleh melebihi batas.

        Returns:
            Identitas KRS yang dihasilkan oleh komponen penyimpanan.

        Raises:
            LookupError: Mahasiswa/mata kuliah tidak ditemukan.
            PermissionError: Status mahasiswa tidak aktif.
            ValueError: Duplikat, prasyarat belum lulus, atau SKS berlebih.
        """
        mahasiswa = self.repo_mahasiswa.cari(nim)
        if mahasiswa is None:
            raise LookupError(f"Mahasiswa {nim} tidak ditemukan")
        if not cek_status_aktif(mahasiswa):
            raise PermissionError("Mahasiswa tidak berstatus aktif")

        if len(set(daftar_kode)) != len(daftar_kode):
            raise ValueError("Daftar mata kuliah mengandung duplikat")

        daftar_mk = self.ambil_mata_kuliah(daftar_kode)
        for mata_kuliah in daftar_mk:
            if not cek_prasyarat(mahasiswa, mata_kuliah):
                raise ValueError(
                    f"Prasyarat mata kuliah {mata_kuliah.kode} belum dipenuhi"
                )

        total_sks = hitung_total_sks(daftar_mk)
        validasi_beban_sks(total_sks)
        return self.penyimpanan.simpan(nim, tuple(daftar_kode))
