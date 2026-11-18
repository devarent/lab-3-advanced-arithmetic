# Jawaban Esai — Pengujian Unit dan Penjaminan Mutu Perangkat Lunak

Folder ini berisi jawaban lengkap Latihan Soal Bab 3 (Pengujian Unit), dalam
bentuk dokumen dan kode program yang dapat dijalankan.

## Isi Folder

| File / Folder | Keterangan |
|---|---|
| `Jawaban_Latihan_Essai_Pengujian_Unit.docx` | Dokumen jawaban lengkap (dapat diedit) |
| `Jawaban_Latihan_Essai_Pengujian_Unit.pdf` | Versi PDF siap cetak/kumpul |
| `kode/src/akademik.py` | Fungsi kelulusan, tagihan + diskon, luas persegi panjang |
| `kode/src/krs.py` | Logika KRS dengan dependency injection (siap distub) |
| `kode/tests/test_akademik.py` | Unit test soal 6, 8, dan 9 |
| `kode/tests/test_krs.py` | Unit test soal 11 dengan stub |
| `kode/run_tests.py` | Test harness: menjalankan semua tes + laporan |
| `kode/demo_bug_operator.py` | Demonstrasi bug `>` vs `>=` (soal 6d) |
| `kode/laporan_pengujian.txt` | Laporan hasil eksekusi test harness |

## Cara Menjalankan

Prasyarat: Python 3.10 atau lebih baru (tidak perlu instal library tambahan).

```bash
cd kode

# Menjalankan seluruh unit test + menghasilkan laporan
python run_tests.py

# Menjalankan salah satu file test secara langsung
python -m unittest tests.test_akademik -v
python -m unittest tests.test_krs -v

# Demonstrasi bug operator >
python demo_bug_operator.py
```

Contoh keluaran test harness:

```text
==============================================================
LAPORAN PENGUJIAN UNIT - APLIKASI AKADEMIK DAN KRS
==============================================================
Waktu eksekusi      : 0.033 detik
Jumlah test case    : 23
Lulus               : 23
Gagal (failure)     : 0
Error               : 0
Dilewati (skipped)  : 0
Status akhir        : LULUS
==============================================================
```

## Pemetaan Kode ke Soal

| Soal | Kode | Test |
|---|---|---|
| 6 — Status kelulusan | `src/akademik.py` → `status_kelulusan()` | `TestStatusKelulusan` |
| 7 — Stub API bank | pola stub di `tests/test_krs.py` (kelas `*Stub`) | `TestAjukanKRS` |
| 8 — Diskon & regresi | `src/akademik.py` → `hitung_tagihan()` | `TestHitungTagihan` |
| 9 — TDD luas | `src/akademik.py` → `hitung_luas_persegi_panjang()` | `TestHitungLuasPersegiPanjang` |
| 10 — Test harness | `run_tests.py` | seluruh suite |
| 11 — KRS + stub | `src/krs.py` | `tests/test_krs.py` |

## Catatan

- Semua test menggunakan `unittest` dari pustaka standar Python sehingga tidak
  bergantung pada paket eksternal.
- Stub dibuat manual (tanpa `unittest.mock`) agar mekanisme penggantian
  dependensi terlihat jelas untuk keperluan pembelajaran.
- Nama, NIM, dan keterangan pada halaman sampul dokumen dapat diubah sesuai
  kebutuhan sebelum dikumpulkan.
