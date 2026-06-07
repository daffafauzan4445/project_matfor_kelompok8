import math

dataAwal = [
    ["Nama 1",   [4,4,4], 0],
    ["Nama 2",   [3,4,4], 0],
    ["Nama 3",   [3,3,4], 0],
    ["Nama 4",   [4,2,3], 0],
    ["Nama 5",   [5,4,5], 0],
    ["Nama 6",   [4,5,4], 0],
    ["Nama 7",   [4,3,3], 0],
    ["Nama 8",   [3,4,3], 0],
    ["Nama 9",   [5,2,4], 0],
    ["Nama 10",  [4,3,3], 0],
    ["Nama 11",  [3,4,3], 0],
    ["Nama 12",  [3,4,4], 0],
    ["Nama 13",  [5,2,2], 0],
    ["Nama 14",  [4,3,3], 0],
    ["Nama 15",  [5,5,5], 0],
    ["Nama 16",  [5,5,3], 0],
    ["Nama 17",  [4,4,3], 0],
    ["Nama 18",  [4,4,3], 0],
    ["Nama 19",  [4,4,4], 0],
    ["Nama 20",  [3,4,5], 0],
    ["Nama 21",  [4,4,4], 0],
    ["Nama 22",  [4,4,4], 0],
    ["Nama 23",  [4,4,4], 0],
    ["Nama 24",  [3,4,3], 0],
    ["Nama 25",  [4,4,4], 0],
    ["Nama 26",  [1,1,5], 0],
    ["Nama 27",  [3,3,3], 0],
    ["Nama 28",  [4,4,4], 0],
    ["Nama 29",  [3,4,3], 0],
    ["Nama 30",  [4,4,4], 0],
    ["Nama 31",  [4,5,3], 0],
    ["Nama 32",  [3,4,3], 0],
    ["Nama 33",  [5,5,3], 0],
]


def minmax(data):
    # ambil jumlah kolom dari data pertama
    jumlahKolom = len(data[0][1])

    # cek tiap kolom apakah range nya > 1, kalau iya perlu normalisasi
    perluNormalisasi = False
    for kolom in range(jumlahKolom):
        nilaiKolom = [row[1][kolom] for row in data]
        if max(nilaiKolom) - min(nilaiKolom) > 1:
            perluNormalisasi = True
            break

    # kalau tidak perlu normalisasi kembalikan data apa adanya
    if not perluNormalisasi:
        print(">> Data tidak perlu dinormalisasi")
        return data

    print(">> Data perlu dinormalisasi, menerapkan MinMax...")

    # hitung nilai min dan max tiap kolom
    minKolom = [min(row[1][k] for row in data) for k in range(jumlahKolom)]
    maxKolom = [max(row[1][k] for row in data) for k in range(jumlahKolom)]

    # terapkan rumus MinMax: x' = (x - min) / (max - min)
    # hasilkan data baru agar data asli tidak berubah
    dataNormal = []
    for row in data:
        nilaiNormal = []
        for k in range(jumlahKolom):
            selisih = maxKolom[k] - minKolom[k]
            # kalau max == min (semua nilai sama) hasil normalisasi = 0
            normal = (row[1][k] - minKolom[k]) / selisih if selisih != 0 else 0
            nilaiNormal.append(round(normal, 4))
        dataNormal.append([row[0], nilaiNormal, row[2]])

    return dataNormal



def ruleOfThumb(data):
    # hitung jumlah data
    n = len(data)
    # terapkan rumus: k = round(sqrt(n/2))
    return round(math.sqrt(n / 2))


# ── Tahap 3: buat centroid awal dengan metode First K Unique ──────────────────
def buatCentroid(data, k):
    # list untuk menampung centroid terpilih
    centroids = []
    # list pencatat nilai yang sudah dipilih agar tidak ada centroid kembar
    seen = []

    for row in data:
        # kalau nilai belum pernah muncul, jadikan centroid
        if row[1] not in seen:
            seen.append(row[1])
            # list() untuk menyalin nilai agar tidak terikat ke objek asli
            centroids.append(list(row[1]))
        # hentikan kalau sudah dapat k centroid
        if len(centroids) == k:
            break

    return centroids


# tahap 1: normalisasi kalau perlu
dataSiap = minmax(dataAwal)

# tahap 2: tentukan k
k = ruleOfThumb(dataSiap)

# tahap 3: buat centroid awal
centroid = buatCentroid(dataSiap, k)
