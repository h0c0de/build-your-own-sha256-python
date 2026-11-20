# Build Your Own — SHA-256

Implementasi **SHA-256** dalam Python murni,
dibangun langsung dari spesifikasinya,
**FIPS 180-4** — pola yang sama dengan build 20
(AES dari FIPS-197): standar federal yang terbuka
sebagai panduan, contoh di dalamnya sebagai
jangkar, dan implementasi pustaka standar
(`hashlib`) sebagai wasit diferensial.

Satu keputusan yang membedakan build ini:
**konstantanya tidak disalin dari tabel mana
pun.** FIPS 180-4 mendefinisikan K sebagai 32 bit
pertama bagian pecahan akar pangkat tiga dari 64
bilangan prima pertama, dan H(0) hal yang sama
dari akar kuadrat 8 prima pertama — jadi keduanya
diturunkan di sini dengan aritmetika integer
eksak (akar pangkat tiga Newton, `math.isqrt`),
dan hasilnya dicocokkan ke nilai tercetak standar
di kedua ujung tabel: `K[0] = 428a2f98`,
`K[63] = c67178f2`, `H(0)[0] = 6a09e667`.

## Isi

| Berkas | Isi |
| --- | --- |
| `sha256ku.py` | Hash-nya: penurunan konstanta, fungsi kompresi 64 putaran, padding, API beraliran mirip hashlib |
| `uji_irisan1.py` … `uji_irisan3.py` | Konstanta & padding; contoh resmi FIPS; diferensial `hashlib` + aliran |

## Memakai

```python
from sha256ku import sha256, SHA256

assert sha256(b"abc").hexdigest() == (
    "ba7816bf8f01cfea414140de5dae2223"
    "b00361a396177a9cb410ff61f20015ad")

h = SHA256()
h.update(b"ber")
h.update(b"potongan")
salinan = h.copy()          # bercabang aman
print(h.hexdigest())        # tidak mengakhiri aliran
```

## Bukti

- Tiga contoh resmi FIPS 180-4 persis: string
  kosong, `abc`, pesan 56 karakter (dua blok),
  ditambah pesan 112 karakter dan sejuta `a`.
- Diferensial `hashlib`: 0 beda pada semua
  panjang tepi padding (54/55/56/57, 63/64/65,
  118/119/120, 127/128/129) + 40 panjang acak.
- Update berpotongan acak (1–69 byte) selalu sama
  dengan sekali jalan; `copy()` bercabang tanpa
  saling mengganggu.

## Di luar lingkup

Keluarga SHA-512/224/384, SHA-1, HMAC — build ini
hanya SHA-256, dan tujuannya kejelasan yang
terbukti benar, bukan kecepatan.

## Lisensi

Kode: MIT. FIPS 180-4 adalah standar pemerintah
AS (domain publik).
