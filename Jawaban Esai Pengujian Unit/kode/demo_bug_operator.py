"""Demonstrasi bug off-by-one pada soal nomor 6d.

Fungsi di bawah ini sengaja menggunakan operator > (seharusnya >=).
Jalankan dengan:
    python demo_bug_operator.py
"""

from src.akademik import status_kelulusan


def status_kelulusan_salah(nilai: float) -> str:
    """Versi yang mengandung bug: nilai tepat 60 dianggap tidak lulus."""
    return "Lulus" if nilai > 60 else "Tidak Lulus"


def main() -> None:
    print("nilai | implementasi benar (>=) | implementasi salah (>)")
    print("-" * 58)
    for nilai in (59, 60, 61):
        benar = status_kelulusan(nilai)
        salah = status_kelulusan_salah(nilai)
        penanda = "  <-- BUG" if benar != salah else ""
        print(f"{nilai:>5} | {benar:>22} | {salah:>22}{penanda}")

    print()
    print("Test case batas nilai 60 akan GAGAL pada implementasi yang salah,")
    print("sedangkan test case 50, 59, 61, dan 80 tetap lulus. Inilah sebabnya")
    print("pengujian kondisi batas wajib dilakukan.")


if __name__ == "__main__":
    main()
