import math
from data import dataAwal, centroid, k


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


# Euclidean Distance Multidimensi
def jarak(a, b):
    total = 0

    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2

    return math.sqrt(total)


# Hitung centroid multidimensi
def hitungCentroid(data, cluster, k, centroidLama):
    centroidBaru = []

    for i in range(k):
        anggota = [data[j][1] for j in range(len(data)) if cluster[j] == i
        ]

        if not anggota:
            centroidBaru.append(centroidLama[i])
            continue

        jumlahKolom = len(anggota[0])

        centroidCluster = []

        for kolom in range(jumlahKolom):
            rata = sum(a[kolom] for a in anggota) / len(anggota)
            centroidCluster.append(round(rata, 2))

        centroidBaru.append(centroidCluster)

    return centroidBaru


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


def tampilPositifNegatif(hasil):

    if not hasil or all(len(c) == 0 for c in hasil):
        print("\n[!] Belum ada data hasil clustering.")
        return

    print("\n========== DATA PALING POSITIF & NEGATIF ==========")

    semuaData = []

    for clusterIdx in range(len(hasil)):
        for item in hasil[clusterIdx]:

            nama = item[0]
            nilaiArr = item[1]
            rataRata = sum(nilaiArr) / len(nilaiArr)
            semuaData.append({"nama": nama, "nilai": nilaiArr, "rata": rataRata, "cluster": clusterIdx + 1})

    semuaData.sort(key=lambda x: x["rata"])

    print("\n======= DATA PALING NEGATIF =======")

    for i, d in enumerate(semuaData[:3]):
        print(f"{i+1}. {d['nama']} | Rata-rata: {d['rata']:.2f} | Cluster: {d['cluster']}")

    print("\n======= DATA PALING POSITIF =======")

    for i, d in enumerate(reversed(semuaData[-3:])):
        print(f"{i+1}. {d['nama']} | Rata-rata: {d['rata']:.2f} | Cluster: {d['cluster']}")


def tampilDataPerPertanyaan(data):

    pertanyaan = [
        "Apakah anda setuju organisasi mahasiswa penting di lingkungan kampus untuk menambah pengalaman dalam kerjasama tim?",
        "Apakah anda setuju bahwa organisasi di lingkungan kampus penting untuk menambah relasi?",
        "Apakah anda setuju bahwa mengikuti organisasi dapat membantu meningkatkan prestasi akademik?"
    ]

    labelJawaban = {
        1: "Sangat Tidak Setuju",
        2: "Tidak Setuju",
        3: "Netral",
        4: "Setuju",
        5: "Sangat Setuju"
    }

    for kolom in range(len(pertanyaan)):

        print("\n==================================================")
        print("PERTANYAAN", kolom + 1)
        print(pertanyaan[kolom])
        print("==================================================")

        for nilai in range(1, 6):

            print(f"\n[{nilai}] {labelJawaban[nilai]}")

            ada = False

            for i in data:

                if i[1][kolom] == nilai:
                    print("-", i[0])
                    ada = True

            if not ada:
                print("Tidak ada")


hasilCluster = []
centroidAkhir = centroid


while True:

    print("\n========== MENU ==========")
    print("1. Data Belum Diolah")
    print("2. Tampilkan Centroid")
    print("3. Proses K-Means")
    print("4. Data Hasil Clustering")
    print("5. Data Per Pertanyaan")
    print("6. Data Paling Positif & Negatif")
    print("7. Keluar")

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
        hasilCluster, centroidAkhir = prosesKMeans(
            dataAwal,
            centroid,
            5
        )

    elif pilih == 4:
        if not hasilCluster:
            print("\n[!] Belum ada hasil clustering")

        else:
            tampilDataAkhir(hasilCluster)

    elif pilih == 5:
        tampilDataPerPertanyaan(dataAwal)

    elif pilih == 6:
        tampilPositifNegatif(hasilCluster)

    elif pilih == 7:
        print("Program selesai")
        break

    else:
        print("Pilihan tidak tersedia")
