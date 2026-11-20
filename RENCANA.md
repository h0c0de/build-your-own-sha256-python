# RENCANA — Build 26: SHA-256

Sumber: **FIPS 180-4** (standar federal AS, domain
publik) — spesifikasinya adalah panduannya, contoh
di dalamnya adalah jangkar emasnya, dan `hashlib`
pustaka standar adalah wasit diferensialnya.
Pola yang sama dengan build 20 (AES dari FIPS-197).

Bukti emas pra-kode: konstanta K dan H(0) TIDAK
disalin dari tabel mana pun — keduanya diturunkan
dari definisinya di FIPS 180-4 §4.2.2/§5.3.3 (bit
pecahan akar pangkat tiga 64 bilangan prima
pertama; akar kuadrat 8 prima pertama) dengan
aritmetika integer eksak, lalu dicocokkan dengan
nilai pertama yang tercetak di standar:
K[0] = 428a2f98, H(0)[0] = 6a09e667.

## Lingkup

MASUK:
- SHA-256 penuh: padding §5.1.1, fungsi putaran
  §4.1.2/§6.2.2 (Ch, Maj, Σ, σ, ROTR/SHR), jadwal
  pesan 64 kata, kompresi 64 putaran.
- API objek beraliran (update berpotongan bebas,
  digest/hexdigest, copy) + fungsi sekali jalan.
- Masukan bytes; panjang pesan hingga batas
  standar 2^64 bit di medan panjang padding.

DILUAR (tercatat):
- Keluarga SHA-512/SHA-224/SHA-384, SHA-1, MD5 —
  build ini hanya SHA-256.
- HMAC/PBKDF2 (dibangun di atas hash, bukan
  bagian dari FIPS 180-4).
- Optimasi kecepatan (tujuan: kejelasan yang
  terbukti benar, bukan benchmark).

## Irisan

- [x] Irisan 1 — Konstanta turunan + padding:
  K/H(0) dari akar prima, kerangka blok 512 bit.
- [x] Irisan 2 — Fungsi kompresi: satu blok
  terverifikasi contoh FIPS ("abc", string kosong).
- [x] Irisan 3 — Aliran & final: update berpotongan,
  copy, diferensial hashlib lintas batas blok
  (55/56/64/65 byte) + contoh panjang standar
  (56 & 112 karakter, sejuta 'a').

## Pagar selesai

- [x] `uji_irisan1.py` … `uji_irisan3.py` hijau;
  diferensial hashlib 0 beda.
- [x] `CATATAN.md` satu halaman per irisan.
- [x] Repo GitHub publik
  `build-your-own-sha256-python` terbit dan
  terverifikasi (SHA blob lokal == remote, halaman
  publik terbaca).
