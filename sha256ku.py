"""SHA-256 menurut FIPS 180-4.

Konstanta K dan nilai awal H(0) tidak disalin dari
tabel: keduanya diturunkan dari definisinya di
standar — 32 bit pertama bagian pecahan akar
pangkat tiga (K) dan akar kuadrat (H(0)) bilangan
prima pertama — dengan aritmetika integer eksak.
"""

from math import isqrt

_MASK = 0xFFFFFFFF


def _prima(jumlah):
    hasil = []
    calon = 2
    while len(hasil) < jumlah:
        if all(calon % p for p in hasil if p * p <= calon):
            hasil.append(calon)
        calon += 1
    return hasil


def _akar3_int(n):
    """Akar pangkat tiga integer (floor) via Newton."""
    if n == 0:
        return 0
    x = 1 << ((n.bit_length() + 2) // 3)
    while True:
        y = (2 * x + n // (x * x)) // 3
        if y >= x:
            break
        x = y
    while (x + 1) ** 3 <= n:
        x += 1
    while x ** 3 > n:
        x -= 1
    return x


def _turunkan_konstanta():
    prima = _prima(64)
    # K[t]: frac(cbrt(p)) * 2^32
    #      = cbrt_int(p * 2^96) - cbrt_int(p) * 2^32
    k = []
    for p in prima:
        utuh = _akar3_int(p << 96)
        k.append((utuh - (_akar3_int(p) << 32)) & _MASK)
    # H(0)[i]: frac(sqrt(p)) * 2^32, cara yang sama
    h = []
    for p in prima[:8]:
        utuh = isqrt(p << 64)
        h.append((utuh - (isqrt(p) << 32)) & _MASK)
    return k, h


K, _H0 = _turunkan_konstanta()


def _rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & _MASK


def _ch(x, y, z):
    return (x & y) ^ (~x & z)


def _maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)


def _sigma0(x):
    return _rotr(x, 2) ^ _rotr(x, 13) ^ _rotr(x, 22)


def _sigma1(x):
    return _rotr(x, 6) ^ _rotr(x, 11) ^ _rotr(x, 25)


def _s0(x):
    return _rotr(x, 7) ^ _rotr(x, 18) ^ (x >> 3)


def _s1(x):
    return _rotr(x, 17) ^ _rotr(x, 19) ^ (x >> 10)


class SHA256:
    """Hash beraliran: update() berpotongan bebas,
    digest()/hexdigest() tidak mengakhiri aliran
    (bekerja pada salinan keadaan)."""

    def __init__(self, data=b""):
        self._h = list(_H0)
        self._buf = bytearray()
        self._panjang = 0  # total byte yang masuk
        if data:
            self.update(data)

    def copy(self):
        lain = SHA256()
        lain._h = list(self._h)
        lain._buf = bytearray(self._buf)
        lain._panjang = self._panjang
        return lain

    def update(self, data):
        if not isinstance(data, (bytes, bytearray,
                                  memoryview)):
            raise TypeError("data harus bytes-like")
        data = bytes(data)
        self._panjang += len(data)
        self._buf += data
        while len(self._buf) >= 64:
            self._kompres(self._buf[:64])
            del self._buf[:64]
        return self

    def _kompres(self, blok):
        w = [int.from_bytes(blok[i * 4:i * 4 + 4],
                            "big") for i in range(16)]
        for t in range(16, 64):
            w.append((w[t - 16] + _s0(w[t - 15])
                      + w[t - 7] + _s1(w[t - 2]))
                     & _MASK)
        a, b, c, d, e, f, g, h = self._h
        for t in range(64):
            t1 = (h + _sigma1(e) + _ch(e, f, g)
                  + K[t] + w[t]) & _MASK
            t2 = (_sigma0(a) + _maj(a, b, c)) & _MASK
            h, g, f, e, d, c, b, a = \
                g, f, e, (d + t1) & _MASK, c, b, a, \
                (t1 + t2) & _MASK
        self._h = [(x + y) & _MASK for x, y in
                   zip(self._h, (a, b, c, d, e, f, g, h))]

    def digest(self):
        salinan = self.copy()
        # padding FIPS 180-4 §5.1.1: bit '1', nol,
        # lalu panjang bit pesan sebagai 64 bit BE
        panjang_bit = self._panjang * 8
        salinan.update(b"\x80")
        while len(salinan._buf) != 56:
            salinan.update(b"\x00")
        salinan._buf += panjang_bit.to_bytes(8, "big")
        salinan._kompres(salinan._buf[:64])
        salinan._buf.clear()
        return b"".join(x.to_bytes(4, "big")
                        for x in salinan._h)

    def hexdigest(self):
        return self.digest().hex()


def sha256(data=b""):
    """Sekali jalan: kembalikan objek SHA256 yang
    sudah terisi `data` (pola hashlib)."""
    return SHA256(data)
