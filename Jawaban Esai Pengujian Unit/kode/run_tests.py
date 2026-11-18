"""Test harness sederhana untuk seluruh unit test pada folder kode.

Contoh peran test harness (soal nomor 10):
- Menemukan dan menjalankan seluruh test case secara otomatis.
- Menyediakan lingkungan eksekusi yang konsisten.
- Mencatat hasil dan waktu eksekusi.
- Menghasilkan laporan ringkas serta exit code untuk CI.

Jalankan dari folder kode:
    python run_tests.py
"""

from __future__ import annotations

import io
import pathlib
import sys
import time
import unittest


ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def main() -> int:
    loader = unittest.TestLoader()
    suite = loader.discover(str(ROOT / "tests"), top_level_dir=str(ROOT))

    buffer = io.StringIO()
    runner = unittest.TextTestRunner(stream=buffer, verbosity=2)

    mulai = time.perf_counter()
    hasil = runner.run(suite)
    durasi = time.perf_counter() - mulai

    jumlah_test = hasil.testsRun
    jumlah_gagal = len(hasil.failures)
    jumlah_error = len(hasil.errors)
    jumlah_skip = len(hasil.skipped)
    jumlah_lulus = jumlah_test - jumlah_gagal - jumlah_error - jumlah_skip

    laporan = [
        "=" * 62,
        "LAPORAN PENGUJIAN UNIT - APLIKASI AKADEMIK DAN KRS",
        "=" * 62,
        f"Waktu eksekusi      : {durasi:.3f} detik",
        f"Jumlah test case    : {jumlah_test}",
        f"Lulus               : {jumlah_lulus}",
        f"Gagal (failure)     : {jumlah_gagal}",
        f"Error               : {jumlah_error}",
        f"Dilewati (skipped)  : {jumlah_skip}",
        f"Status akhir        : {'LULUS' if hasil.wasSuccessful() else 'GAGAL'}",
        "=" * 62,
        "",
        "DETAIL EKSEKUSI",
        "-" * 62,
        buffer.getvalue(),
    ]
    teks = "\n".join(laporan)

    print(teks)
    (ROOT / "laporan_pengujian.txt").write_text(teks, encoding="utf-8")

    return 0 if hasil.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
