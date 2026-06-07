import math
from data import dataAwal, dataSiap, k, centroid
import matplotlib.pyplot as plt    # library untuk menampilkan bar chrat


# ── Euclidean Distance ────────────────────────────────────────────────────────
def euclidean(a, b):
    # hitung selisih kuadrat tiap dimensi lalu jumlahkan
    total = 0
    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2
    # akar kuadrat dari total selisih kuadrat
    return math.sqrt(total)


# ── Hitung centroid baru dengan mean ─────────────────────────────────────────
def hitungCentroid(data, cluster, k, centroidLama):
    centroidBaru = []
    for i in range(k):
        # kumpulkan semua anggota cluster i
        anggota = [data[j][1] for j in range(len(data)) if cluster[j] == i]
        # kalau cluster kosong pakai centroid lama
        if not anggota:
            centroidBaru.append(centroidLama[i])
            continue
        # hitung mean tiap kolom
        jumlahKolom = len(anggota[0])
        centroidCluster = []
        for kolom in range(jumlahKolom):
            rata = sum(a[kolom] for a in anggota) / len(anggota)
            centroidCluster.append(round(rata, 4))
        centroidBaru.append(centroidCluster)
    return centroidBaru


# ── K-Means ───────────────────────────────────────────────────────────────────
def prosesKMeans(data, centroidAwal, iterasi):
    centroidBaru = centroidAwal

    for ulang in range(iterasi):
        print("\n====================")
        print("Iterasi ke-", ulang + 1)
        print("====================")

        cluster = []
        for titik in data:
            # hitung jarak ke semua centroid menggunakan euclidean
            daftarJarak = [euclidean(titik[1], c) for c in centroidBaru]
            # ambil index centroid dengan jarak terkecil sebagai cluster
            cluster.append(daftarJarak.index(min(daftarJarak)))

        print("+----------------+-----------------------+-----------+")
        print("| Nama           | Data                  | Cluster   |")
        print("+----------------+-----------------------+-----------+")
        for i in range(len(data)):
            data[i][2] = cluster[i]
            print(f"| {data[i][0]:<14} | {str(data[i][1]):<21} | Cluster {data[i][2]+1} |")
        print("+----------------+-----------------------+-----------+")

        # update centroid baru menggunakan mean
        centroidLama = centroidBaru.copy()
        centroidBaru = hitungCentroid(data, cluster, k, centroidBaru)

        print("\n========== CENTROID BARU ==========")
        print("+-----------+---------------------------+")
        print("| Centroid  | Nilai                     |")
        print("+-----------+---------------------------+")
        for i, c in enumerate(centroidBaru):
            print(f"| C{i+1:<8} | {str(c):<25} |")
        print("+-----------+---------------------------+")

    return dataAkhir(data, centroidBaru, k), centroidBaru


# ── Cari Data Anomali ────────────────────────────────────────────────
def cariAnomali(data, centroidAkhir, k):
    if not any(row[2] != 0 for row in data):
        print("\n[!] Jalankan proses K-Means terlebih dahulu.")
        return

    # hitung jarak tiap data ke centroid cluster-nya
    semuaJarak = [euclidean(row[1], centroidAkhir[row[2]]) for row in data]

    # hitung Q1, Q3, IQR
    terurut = sorted(semuaJarak)
    n       = len(terurut)
    q1      = terurut[n // 4]
    q3      = terurut[(3 * n) // 4]
    iqr     = q3 - q1
    batasBawah = q1 - 1.5 * iqr
    batasAtas  = q3 + 1.5 * iqr

    print("\n========== DETEKSI ANOMALI (IQR) ==========")
    print(f"  Q1          : {q1:.4f}")
    print(f"  Q3          : {q3:.4f}")
    print(f"  IQR         : {iqr:.4f}")
    print(f"  Batas bawah : {batasBawah:.4f}  (Q1 - 1.5 x IQR)")
    print(f"  Batas atas  : {batasAtas:.4f}  (Q3 + 1.5 x IQR)")

    print("\n+----------------+-----------+----------+---------+")
    print("| Nama           | Cluster   | Jarak    | Status  |")
    print("+----------------+-----------+----------+---------+")

    anomali = []
    for i, row in enumerate(data):
        d      = semuaJarak[i]
        status = "ANOMALI" if d < batasBawah or d > batasAtas else "Normal "
        if status == "ANOMALI":
            anomali.append((row[0], row[2]+1, d))
        print(f"| {row[0]:<14} | Cluster {row[2]+1} | {d:>7.4f} | {status} |")

    print("+----------------+-----------+----------+---------+")

    if anomali:
        print(f"\n  Ditemukan {len(anomali)} data anomali:")
        for a in anomali:
            print(f"  - {a[0]} | Cluster {a[1]} | jarak = {a[2]:.4f}")
    else:
        print("\n  Tidak ditemukan data anomali.")
        

# ── Fungsi tampilan ───────────────────────────────────────────────────────────
def tampilDataAwal(data):
    print("\n========== DATA BELUM DIOLAH ==========")
    print("+----+-----------------+-----------------+---------+")
    print("| No | Nama            | Data            | Cluster |")
    print("+----+-----------------+-----------------+---------+")
    for no, i in enumerate(data, start=1):
        print(f"| {no:<2} | {i[0]:<15} | {str(i[1]):<15} | {i[2]+1:<7} |")
    print("+----+-----------------+-----------------+---------+")


def tampilDataSiap(data):
    print("\n========== DATA SETELAH NORMALISASI ==========")
    print("+----+-----------------+-----------------------------+---------+")
    print("| No | Nama            | Data (MinMax)               | Cluster |")
    print("+----+-----------------+-----------------------------+---------+")
    for no, i in enumerate(data, start=1):
        print(f"| {no:<2} | {i[0]:<15} | {str(i[1]):<27} | {i[2]+1:<7} |")
    print("+----+-----------------+-----------------------------+---------+")


def tampilCentroid(centroidData):
    print("\n========== CENTROID ==========")
    print("+-----------+---------------------------+")
    print("| Centroid  | Nilai                     |")
    print("+-----------+---------------------------+")
    for i in range(len(centroidData)):
        print(f"| C{i+1:<8} | {str(centroidData[i]):<25} |")
    print("+-----------+---------------------------+")


def dataAkhir(data, centroidBaru, k):
    clusterAkhir = [[] for _ in range(k)]
    for i in data:
        clusterAkhir[i[2]].append([i[0], i[1], centroidBaru[i[2]]])
    return clusterAkhir


def tampilDataAkhir(hasil):
    print("\n========== DATA HASIL CLUSTERING ==========")
    for i in range(len(hasil)):
        print("\n====================")
        print("CLUSTER", i+1)
        print("====================")
        print("+----------------+-----------------------------+-----------------------------+")
        print("| Nama           | Data                        | Centroid                    |")
        print("+----------------+-----------------------------+-----------------------------+")
        for data in hasil[i]:
            print(f"| {data[0]:<14} | {str(data[1]):<27} | {str(data[2]):<27} |")
        print("+----------------+-----------------------------+-----------------------------+")
        

# ── Visualisasi Hasil Clustering ────────────────────────────────────────────────
def visualisasiCluster(hasil):

    jumlah = []

    for cluster in hasil:
        jumlah.append(len(cluster))

    label = []

    for i in range(len(jumlah)):
        label.append(f"Cluster {i+1}")

    plt.bar(label, jumlah)
    plt.grid(axis='y')
    plt.title("Jumlah Anggota Tiap Cluster")
    plt.xlabel("Cluster")
    plt.ylabel("Jumlah Mahasiswa")

    plt.show()
    
    
# ── Evaluasi Model dengan Silhouette Score ───────────────────────────────────
def silhouetteScore(data, centroidAkhir):
    totalScore = 0

    for row in data:

        # cluster data saat ini
        clusterSaatIni = row[2]

        # a = jarak ke centroid cluster sendiri
        a = euclidean(
            row[1],
            centroidAkhir[clusterSaatIni]
        )

        # b = jarak terdekat ke centroid cluster lain
        b = float("inf")

        for i in range(len(centroidAkhir)):

            if i != clusterSaatIni:

                jarakClusterLain = euclidean(
                    row[1],
                    centroidAkhir[i]
                )

                if jarakClusterLain < b:
                    b = jarakClusterLain

        # hitung silhouette score data
        if max(a, b) == 0:
            s = 0
        else:
            s = (b - a) / max(a, b)

        totalScore += s

    scoreAkhir = totalScore / len(data)

    print("\n========== EVALUASI MODEL ==========")
    print(f"Silhouette Score = {scoreAkhir:.4f}")

    if scoreAkhir >= 0.71:
        kualitas = "Sangat Baik"
    elif scoreAkhir >= 0.51:
        kualitas = "Baik"
    elif scoreAkhir >= 0.26:
        kualitas = "Cukup"
    else:
        kualitas = "Kurang"

    print(f"Kualitas Cluster : {kualitas}")

    return scoreAkhir


# ── Menu utama ────────────────────────────────────────────────────────────────
hasilCluster  = []
centroidAkhir = centroid

while True:
    print("\n========== MENU ==========")
    print(f"(k = {k}  |  Rule of Thumb: round(sqrt(n/2)))")
    print("1. Data Asli")
    print("2. Data Setelah Normalisasi")
    print("3. Tampilkan Centroid")
    print("4. Proses K-Means")
    print("5. Data Hasil Clustering")
    print("6. Visualisasi Hasil Clustering")
    print("7. Evaluasi Model")
    print("8. Cari Data Anomali")
    print("0. Keluar")

    try:
        pilih = int(input("Masukkan pilihan : "))
    except ValueError:
        print("Input harus angka")
        continue

    if pilih == 1:
        tampilDataAwal(dataAwal)
    elif pilih == 2:
        tampilDataSiap(dataSiap)
    elif pilih == 3:
        tampilCentroid(centroidAkhir)
    elif pilih == 4:
        hasilCluster, centroidAkhir = prosesKMeans(dataSiap, centroid, 5)
    elif pilih == 5:
        if not hasilCluster:
            print("\n[!] Belum ada hasil clustering")
        else:
            tampilDataAkhir(hasilCluster)
    elif pilih == 6:
        if not hasilCluster:
            print("\n[!] Belum ada hasil clustering")
        else:
            visualisasiCluster(hasilCluster)
    elif pilih == 7:
        if not hasilCluster:
            print("\n[!] Jalankan proses K-Means terlebih dahulu.")
        else:
            silhouetteScore(dataSiap, centroidAkhir)
    elif pilih == 8:
        cariAnomali(dataSiap, centroidAkhir, k)
    elif pilih == 0:
        print("Program selesai")
        break
    else:
        print("Pilihan tidak tersedia")
