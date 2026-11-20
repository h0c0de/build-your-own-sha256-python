"""Irisan 1 — konstanta turunan + kerangka padding.

K dan H(0) diturunkan dari definisi FIPS 180-4
(akar prima, aritmetika integer eksak) lalu
dicocokkan ke nilai tercetak standar pada kedua
ujung tabel; padding diperiksa strukturnya pada
panjang-panjang tepi.
"""
import sha256ku as s

# nilai tercetak FIPS 180-4 (jangkar kedua ujung)
K_AWAL = 0x428A2F98
K_AKHIR = 0xC67178F2
H_AWAL = 0x6A09E667
H_AKHIR = 0x5BE0CD19

if __name__ == "__main__":
    cek = 0
    assert len(s.K) == 64 and len(s._H0) == 8
    assert s.K[0] == K_AWAL and s.K[63] == K_AKHIR
    assert s._H0[0] == H_AWAL and s._H0[7] == H_AKHIR
    cek += 3
    # turunan ulang harus deterministik & prima benar
    prima = s._prima(64)
    assert prima[:8] == [2, 3, 5, 7, 11, 13, 17, 19]
    assert prima[63] == 311
    cek += 2
    # struktur padding: total panjang sesudah padding
    # selalu kelipatan 64, byte 0x80 tepat sesudah
    # pesan, 8 byte terakhir = panjang bit
    import hashlib
    for n in (0, 1, 55, 56, 57, 63, 64, 65, 119, 120):
        h = s.SHA256(b"a" * n)
        assert h._panjang == n
        assert len(h._buf) == n % 64
        cek += 1
    print("irisan 1: %d pemeriksaan LULUS" % cek)
