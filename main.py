import math
from data import dataAwal, centroid, k

# Euclidean Distance Multidimensi
def jarak(a, b): # fungsi untuk menghitung data parameter nya a-> data dan b -> centroid berupa array
    # buat nampung hasil nya di buat nol dulu karena belum di jumlah kan 
    total = 0
# ini buat ngelakuin perulangan sebanyak data 
    for i in range(len(a)):
        # baris di bawah berfungsi untuk menghitung selisih dari a dan b lalu mengkuadratkan
        total += (a[i] - b[i]) ** 2
    # kbaris bawah berfungsi untuk menghitung akar kuadrat sesuai rumus
    return math.sqrt(total)


# Hitung centroid dengan rumus mean 
def hitungCentroid(data, cluster, k, centroidLama): # fungsi ini memiliki 4 parameter
    # baris di bawah variable buat nampung centroid baru  
    centroidBaru = []
    # perulangan untuk tiap cluster 
    for i in range(k):
        # variable untuk menampun nilai array kecuali nama lalu mengelompokan nya jika sesuai dengan cluter
        anggota = [data[j][1] for j in range(len(data)) if cluster[j] == i]
       # baris bawah buat nampun kalo si data nya gak cocok sama cluster nya  
        if not anggota:
            centroidBaru.append(centroidLama[i])
            continue
            # baris di bawah ini buat menghitung berapa kolom
        jumlahKolom = len(anggota[0])
        # buat menyimpan centroid dari cluster yang baru di buat
        centroidCluster = []
        # buat melakukan perulangan sebanyak jumlah kolom nya 
        for kolom in range(jumlahKolom):
            #  buat ngitung rata rata tiap kolom lalu bakal di bagi dengan jumlah anggota nya 
            rata = sum(a[kolom] for a in anggota) / len(anggota)
            # buat ngebuletin hasil nya jadi desimal 2 angka 
            centroidCluster.append(round(rata, 2))
# buat naro si centroid cluster nya di centroid baru
        centroidBaru.append(centroidCluster)

    return centroidBaru


# K-means 
def prosesKMeans(data, centroidAwal, iterasi):
    centroidBaru = centroidAwal

    for ulang in range(iterasi):
        print("\n====================")
        print("Iterasi ke-", ulang + 1)
        print("====================")

        cluster = []
        for titik in data:
            daftarJarak = []
            for c in centroidBaru:
                daftarJarak.append(jarak(titik[1], c))
            clusterTerdekat = daftarJarak.index(min(daftarJarak))
            cluster.append(clusterTerdekat)

        print("+----------------+-----------------+-----------+")
        print("| Nama           | Data            | Cluster   |")
        print("+----------------+-----------------+-----------+")

        for i in range(len(data)):
            data[i][2] = cluster[i]
            print(f"| {data[i][0]:<14} | {str(data[i][1]):<15} | Cluster {data[i][2]+1} |")

        print("+----------------+-----------------+-----------+")

        centroidBaru = hitungCentroid(data, cluster, k, centroidBaru)

        print("\n========== CENTROID BARU ==========")
        print("+-----------+----------------------+")
        print("| Centroid  | Nilai                |")
        print("+-----------+----------------------+")
        for i, c in enumerate(centroidBaru):
            print(f"| C{i+1:<8} | {str(c):<20} |")
        print("+-----------+----------------------+")

    return dataAkhir(data, centroidBaru, k), centroidBaru


# ── Fungsi tampilan ───────────────────────────────────────────────────────────
def tampilDataAwal(data):
    print("\n========== DATA BELUM DIOLAH ==========")
    print("+----+-----------------+-----------------+---------+")
    print("| No | Nama            | Data            | Cluster |")
    print("+----+-----------------+-----------------+---------+")
    for no, i in enumerate(data, start=1):
        print(f"| {no:<2} | {i[0]:<15} | {str(i[1]):<15} | {i[2]+1:<7} |")
    print("+----+-----------------+-----------------+---------+")


def tampilCentroid(centroidData):
    print("\n========== CENTROID ==========")
    print("+-----------+----------------------+")
    print("| Centroid  | Nilai                |")
    print("+-----------+----------------------+")
    for i in range(len(centroidData)):
        print(f"| C{i+1:<8} | {str(centroidData[i]):<20} |")
    print("+-----------+----------------------+")


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
        print("+----------------+-----------------+----------------------+")
        print("| Nama           | Data            | Centroid            |")
        print("+----------------+-----------------+----------------------+")
        for data in hasil[i]:
            print(f"| {data[0]:<14} | {str(data[1]):<15} | {str(data[2]):<20} |")
        print("+----------------+-----------------+----------------------+")


# ── Cari Data Anomali dengan Z-Score ─────────────────────────────────────────
def cariAnomali(data, centroidAkhir, k, threshold=2.0):
    if not any(row[2] != 0 for row in data):
        print("\n[!] Jalankan proses K-Means terlebih dahulu.")
        return

    # hitung jarak tiap data ke centroid cluster-nya
    semuaJarak = []
    for row in data:
        d = jarak(row[1], centroidAkhir[row[2]])
        semuaJarak.append(d)

    # hitung mean dan standar deviasi
    mean = sum(semuaJarak) / len(semuaJarak)
    varian = sum((d - mean) ** 2 for d in semuaJarak) / len(semuaJarak)
    std = math.sqrt(varian)

    # hitung z-score tiap data
    anomali = []
    normal = []
    for i, row in enumerate(data):
        z = (semuaJarak[i] - mean) / std if std != 0 else 0
        entry = {
            "nama"    : row[0],
            "nilai"   : row[1],
            "cluster" : row[2] + 1,
            "jarak"   : semuaJarak[i],
            "zscore"  : z
        }
        if abs(z) > threshold:
            anomali.append(entry)
        else:
            normal.append(entry)

    print("\n========== DETEKSI ANOMALI (Z-SCORE) ==========")
    print(f"  Mean jarak  : {mean:.4f}")
    print(f"  Std deviasi : {std:.4f}")
    print(f"  Threshold   : |z| > {threshold}")

    print("\n+----------------+-----------+----------+----------+---------+")
    print("| Nama           | Cluster   | Jarak    | Z-Score  | Status  |")
    print("+----------------+-----------+----------+----------+---------+")
    for i, row in enumerate(data):
        z = (semuaJarak[i] - mean) / std if std != 0 else 0
        status = "ANOMALI" if abs(z) > threshold else "Normal "
        print(f"| {row[0]:<14} | Cluster {row[2]+1} | {semuaJarak[i]:>7.4f} | {z:>8.4f} | {status} |")
    print("+----------------+-----------+----------+----------+---------+")

    if anomali:
        print(f"\n  Ditemukan {len(anomali)} data anomali:")
        for a in anomali:
            print(f"  - {a['nama']} | Cluster {a['cluster']} | z = {a['zscore']:.4f}")
    else:
        print("\n  Tidak ditemukan data anomali.")


# ── Menu utama ────────────────────────────────────────────────────────────────
hasilCluster = []
centroidAkhir = centroid

while True:
    print("\n========== MENU ==========")
    print(f"(k = {k}  |  Rule of Thumb: round(sqrt(n/2)))")
    print("1. Data Belum Diolah")
    print("2. Tampilkan Centroid")
    print("3. Proses K-Means")
    print("4. Data Hasil Clustering")
    print("5. Cari Data Anomali")
    print("6. Keluar")

    try:
        pilih = int(input("Masukkan pilihan : "))
    except ValueError:
        print("Input harus angka")
        continue

    if pilih == 1:
        tampilDataAwal(dataAwal)
    elif pilih == 2:
        tampilCentroid(centroidAkhir)
    elif pilih == 3:
        hasilCluster, centroidAkhir = prosesKMeans(dataAwal, centroid, 5)
    elif pilih == 4:
        if not hasilCluster:
            print("\n[!] Belum ada hasil clustering")
        else:
            tampilDataAkhir(hasilCluster)
    elif pilih == 5:
        cariAnomali(dataAwal, centroidAkhir, k)
    elif pilih == 6:
        print("Program selesai")
        break
    else:
        print("Pilihan tidak tersedia")
