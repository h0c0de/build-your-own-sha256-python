"""Irisan 3 — aliran & final: diferensial hashlib.

Pesan contoh 112 karakter FIPS + sejuta 'a';
update berpotongan acak vs sekali jalan; copy()
di tengah aliran; diferensial pada panjang acak
termasuk semua batas blok padding.
"""
import hashlib
import random

import sha256ku as s

PESAN_112 = (b"abcdefghbcdefghicdefghijdefghijk"
             b"efghijklfghijklmghijklmnhijklmno"
             b"ijklmnopjklmnopqklmnopqrlmnopqrs"
             b"mnopqrstnopqrstu")
EMAS_112 = ("cf5b16a778af8380036ce59e7b049237"
            "0b249b11e8f07a51afac45037afee9d1")

if __name__ == "__main__":
    cek = 0
    assert s.sha256(PESAN_112).hexdigest() == EMAS_112
    cek += 1
    # sejuta 'a' (contoh ketiga FIPS) via potongan
    h = s.SHA256()
    sisa = 1_000_000
    while sisa:
        ambil = min(sisa, 65536)
        h.update(b"a" * ambil)
        sisa -= ambil
    assert h.hexdigest() == (
        "cdc76e5c9914fb9281a1c7e284d73e67"
        "f1809a48a497200e046d39ccc7112cd0")
    cek += 1
    # diferensial hashlib: panjang tepi + acak
    acak = random.Random(26)
    panjangs = [0, 1, 2, 3, 54, 55, 56, 57, 63, 64,
                65, 118, 119, 120, 127, 128, 129,
                1000, 4097]
    panjangs += [acak.randrange(0, 300)
                 for _ in range(40)]
    for n in panjangs:
        data = bytes(acak.randrange(256)
                     for _ in range(n))
        assert s.sha256(data).digest() == \
            hashlib.sha256(data).digest(), n
        cek += 1
    # update berpotongan acak == sekali jalan
    data = bytes(acak.randrange(256) for _ in range(500))
    h = s.SHA256()
    i = 0
    while i < len(data):
        langkah = acak.randrange(1, 70)
        h.update(data[i:i + langkah])
        i += langkah
    assert h.digest() == hashlib.sha256(data).digest()
    cek += 1
    # copy() bercabang tanpa saling mengganggu,
    # digest() tidak mengakhiri aliran
    dasar = s.SHA256(b"bersama")
    cabang = dasar.copy()
    dasar.update(b"-satu")
    cabang.update(b"-dua")
    assert dasar.hexdigest() == \
        hashlib.sha256(b"bersama-satu").hexdigest()
    assert cabang.hexdigest() == \
        hashlib.sha256(b"bersama-dua").hexdigest()
    assert dasar.hexdigest() == \
        hashlib.sha256(b"bersama-satu").hexdigest()
    cek += 3
    print("irisan 3: %d pemeriksaan LULUS" % cek)
