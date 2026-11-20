# CATATAN — Build 26: SHA-256

Satu halaman per irisan: konsep inti + temuan.
Panduan: FIPS 180-4. Wasit: contoh resmi di dalam
standar itu sendiri + diferensial `hashlib`.

## Irisan 1 — Konstanta turunan + padding (15)

**Konsep.** SHA-256 tidak punya satu pun angka
ajaib yang bebas: K adalah bit pecahan akar
pangkat tiga 64 prima pertama, H(0) bit pecahan
akar kuadrat 8 prima pertama ("nothing up my
sleeve numbers"). Padding: bit `1`, bit `0`
sampai panjang ≡ 56 (mod 64), lalu panjang bit
pesan sebagai bilangan 64-bit big-endian.

**Temuan.** Penurunan konstantanya murni soal
skala integer: frac(∛p)·2³² = ∛(p·2⁹⁶) − ∛p·2³²,
semua dalam integer eksak — akar pangkat tiga
Newton berlantai (floor) yang dikoreksi di kedua
arah pada akhir iterasi, karena Newton integer
bisa berhenti satu di atas atau di bawah. Kedua
ujung tabel cocok dengan cetakan standar
(428a2f98…c67178f2; 6a09e667…5be0cd19) sebelum
satu blok pun dihash — bukti emas pra-kode build
ini. Panjang tepi padding yang berbahaya tetap
yang klasik: 55 byte muat satu blok, 56 byte
memaksa blok kedua.

## Irisan 2 — Fungsi kompresi (3)

**Konsep.** Setiap blok 512 bit diperluas ke
jadwal 64 kata (σ0/σ1 memutar kata-kata awal),
lalu 64 putaran mengocok delapan variabel kerja
dengan Ch (pemilih per bit), Maj (voting per
bit), dan dua fungsi Σ berbasis ROTR. Semua
operasi modulo 2³²; pergeseran adalah ROTR dan
SHR yang berbeda — menukar keduanya adalah bug
klasik yang hanya tertangkap contoh resmi.

**Temuan.** Tiga contoh FIPS lolos pada jalan
pertama, termasuk pesan 56 karakter yang
padding-nya tumpah ke blok kedua — irisan 1 dan 2
saling mengunci: padding yang salah akan
menggeser blok kedua dan contoh ini gagal.

## Irisan 3 — Aliran & final (65)

**Konsep.** API beraliran meniru kontrak hashlib:
`update()` menerima potongan berapa pun dan
mengompresi setiap 64 byte penuh; `digest()`
bekerja pada *salinan* keadaan sehingga tidak
mengakhiri aliran; `copy()` memungkinkan
percabangan hash dari awalan yang sama.

**Temuan.** Dua jebakan aliran yang dijaga uji:
(1) penghitung panjang harus dibaca *sebelum*
padding ditambahkan lewat jalur update yang sama
— kalau tidak, byte padding ikut terhitung
sebagai pesan; (2) `digest()` yang memutasi
keadaan akan merusak update berikutnya, jadi ia
wajib menyalin dulu. Diferensial melawan hashlib
hijau di semua panjang tepi + acak, dan sejuta
`a` yang dialirkan per 64 KiB menghasilkan digest
contoh ketiga FIPS persis. Build paling tenang
di seri ini — standar yang preskriptif penuh
memang meninggalkan sedikit ruang untuk tafsir,
berbeda jauh dengan TOML (build 24) yang separuh
susahnya adalah hukum namespace.
