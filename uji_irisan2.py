"""Irisan 2 — fungsi kompresi: contoh resmi
FIPS 180-4 (string kosong, "abc", dan pesan 56
karakter dua blok dari Appendix standar)."""
import sha256ku as s

CONTOH = [
    (b"",
     "e3b0c44298fc1c149afbf4c8996fb924"
     "27ae41e4649b934ca495991b7852b855"),
    (b"abc",
     "ba7816bf8f01cfea414140de5dae22"
     "23b00361a396177a9cb410ff61f20015ad"),
    (b"abcdbcdecdefdefgefghfghighijhijk"
     b"ijkljklmklmnlmnomnopnopq",
     "248d6a61d20638b8e5c026930c3e6039"
     "a33ce45964ff2167f6ecedd419db06c1"),
]

if __name__ == "__main__":
    cek = 0
    for pesan, harap in CONTOH:
        got = s.sha256(pesan).hexdigest()
        assert got == harap, (pesan[:12], got)
        cek += 1
    print("irisan 2: %d pemeriksaan LULUS" % cek)
