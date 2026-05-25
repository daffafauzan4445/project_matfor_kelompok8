import math
from data import dataAwal, centroidLama, k, centroidAwal

def tampilDataAwal(data):
    print("\n========== DATA BELUM DIOLAH ==========")
    print("+----+-----------------+-----------------+---------+")
    print("| No | Nama            | Data            | Cluster |")
    print("+----+-----------------+-----------------+---------+")

    for no, i in enumerate(data, start=1):
        print(f"| {no:<2} | {i[0]:<15} | {str(i[1]):<15} | {i[2]+1:<7} |")

    print("+----+-----------------+-----------------+---------+")
        
def tampilCentroid(centroid):
    print("\n========== CENTROID ==========")
    print("+-----------+-----------------+")
    print("| Centroid  | Nilai           |")
    print("+-----------+-----------------+")

    for i in range(len(centroid)):
        print(f"| C{i+1:<8} | {str(centroid[i]):<15} |")

    print("+-----------+-----------------+")
        
def jarak(a, b):
    
    if isinstance(b, (int, float)):
        meanA = sum(a) / len(a)
        return abs(meanA - b)
  
    total = 0
    for i in range(len(a)):
        total += (a[i] - b[i]) ** 2
    return math.sqrt(total)

def hitungCentroid(data, cluster, k, centroidLama):

    centroidBaru = []

    for i in range(k):

        anggota = [data[j][1] for j in range(len(data)) if cluster[j] == i]

        if not anggota:
            centroidBaru.append(centroidLama[i])
            continue

        rata = round(sum(sum(a) / len(a) for a in anggota) / len(anggota), 2)

        centroidBaru.append(rata)

    return centroidBaru

def prosesKMeans(data, centroid, iterasi):
    centroidBaru = centroid
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
        print("\nCentroid Baru:")
        
        print("+-----------+-----------------+")
        print("| Centroid  | Nilai           |")
        print("+-----------+-----------------+")

        for i, c in enumerate(centroidBaru):
            print(f"| C{i+1:<8} | {str(c):<15} |")

        print("+-----------+-----------------+")

    return dataAkhir(data, centroidBaru), centroidBaru

def dataAkhir(data, centroidBaru):
    clusterAkhir = [[] for _ in range(k)]

    for i in data:
        clusterAkhir[i[2]].append([
            i[0],
            i[1],
            centroidBaru[i[2]]
        ])
    return clusterAkhir

def tampilDataAkhir(hasil):
    print("\n========== DATA HASIL CLUSTERING ==========")
    for i in range(len(hasil)):
        print("\n====================")
        print("CLUSTER", i+1)
        print("====================")
        
        print("+----------------+-----------------+-----------------+")
        print("| Nama           | Data            | Centroid       |")
        print("+----------------+-----------------+-----------------+")

        for data in hasil[i]:
            print(f"| {data[0]:<14} | {str(data[1]):<15} | {str(data[2]):<15} |")

        print("+----------------+-----------------+-----------------+")


def tampilPositifNegatif(hasil):
    if not hasil or all(len(c) == 0 for c in hasil):
        print("\n[!] Belum ada data hasil clustering. Jalankan proses K-Means terlebih dahulu.")
        return

    print("\n========== DATA PALING POSITIF & NEGATIF (Berdasarkan Rata-Rata) ==========")

    semuaData = []
    for clusterIdx in range(len(hasil)):
        for item in hasil[clusterIdx]:
            nama     = item[0]
            nilaiArr = item[1]
            rataRata = sum(nilaiArr) / len(nilaiArr)
            semuaData.append({
                "nama"    : nama,
                "nilai"   : nilaiArr,
                "rata"    : rataRata,
                "cluster" : clusterIdx + 1
            })

    if not semuaData:
        print("Tidak ada data.")
        return

    semuaData.sort(key=lambda x: x["rata"])

    print("\n======== DATA PALING NEGATIF (Rata-Rata Terendah) ========")
    print("+----------------+-----------------+------------+---------+")
    print("| Nama           | Data            | Rata-rata | Cluster |")
    print("+----------------+-----------------+------------+---------+")
    
    nilaiTerendah = semuaData[0]["rata"]
    for d in semuaData:
        if d["rata"] == nilaiTerendah:
            print(f"| {d['nama']:<14} | {str(d['nilai']):<15} | {d['rata']:<10.2f} | {d['cluster']:<7} |")
        else:
            break

    print("+----------------+-----------------+------------+---------+")

    print("\n  [ Peringkat Bawah - 3 Terendah ]")
    for i, d in enumerate(semuaData[:3]):
        print(f"  {i+1}. {d['nama']:<20} | Rata-Rata: {d['rata']:.2f} | Cluster: {d['cluster']}")

    print("\n======== DATA PALING POSITIF (Rata-Rata Tertinggi) ========")
    print("+----------------+-----------------+------------+---------+")
    print("| Nama           | Data            | Rata-rata | Cluster |")
    print("+----------------+-----------------+------------+---------+")
    
    nilaiTertinggi = semuaData[-1]["rata"]
    for d in reversed(semuaData):
        if d["rata"] == nilaiTertinggi:
            print(f"| {d['nama']:<14} | {str(d['nilai']):<15} | {d['rata']:<10.2f} | {d['cluster']:<7} |")
        else:
            break

    print("\n  [ Peringkat Atas - 3 Tertinggi ]")
    for i, d in enumerate(reversed(semuaData[-3:])):
        print(f"  {i+1}. {d['nama']:<20} | Rata-Rata: {d['rata']:.2f} | Cluster: {d['cluster']}")

    print("\n======= RATA-RATA PER CLUSTER =======")
    print("+-----------+-------------+----------+")
    print("| Cluster   | Rata-rata  | Anggota  |")
    print("+-----------+-------------+----------+")
    for clusterIdx in range(len(hasil)):
        anggotaCluster = [d for d in semuaData if d["cluster"] == clusterIdx + 1]
        if anggotaCluster:
            rataCluster = sum(d["rata"] for d in anggotaCluster) / len(anggotaCluster)
            print(f"| {clusterIdx+1:<9} | {rataCluster:<11.2f} | {len(anggotaCluster):<8} |")

    print("+-----------+-------------+----------+")


def tampilDataPerPertanyaan(data):

    pertanyaan = [
        "Apakah anda setuju organisasi mahasiswa penting di lingkungan kampus untuk menambah pengalaman dalam kerjasama tim?",
        "Apakah anda setuju bahwa organisasi di lingkungan kampus penting untuk menambah relasi?",
        "Apakah anda setuju bahwa mengikuti organisasi dapat membantu meningkatkan prestasi akademik?"
    ]

    labelJawaban = {
        1: "Sangat tidak setuju",
        2: "Tidak setuju",
        3: "Netral",
        4: "Setuju",
        5: "Sangat setuju"
    }

    for kolom in range(len(pertanyaan)):

        print("\n" + "=" * 55)
        print("PERTANYAAN", kolom + 1)
        print(pertanyaan[kolom])
        print("=" * 55)

        for nilai in range(1, 6):

            print(f"\n  [{nilai}] {labelJawaban[nilai]} :")

            print("+----------------------+")
            print("| Nama                 |")
            print("+----------------------+")

            ada = False

            for i in data:

                if i[1][kolom] == nilai:
                    print(f"| {i[0]:<20} |")
                    ada = True

            if not ada:
                print("| Tidak ada            |")

            print("+----------------------+")


# Inisialisasi sebelum menu
hasilCluster = []
centroidAkhir = centroidLama

while True:
    print("\n========== MENU ==========")
    print("1. Data Belum Diolah")
    print("2. Tampilkan Centroid")
    print("3. Proses K-Means")
    print("4. Data Hasil Clustering")
    print("5. Data Per Pertanyaan")
    print("6. Data Paling Positif & Negatif")
    print("7. Keluar")

    pilih = int(input("Masukkan pilihan : "))

    if pilih == 1:
        tampilDataAwal(dataAwal)

    elif pilih == 2:
        tampilCentroid(centroidAkhir)

    elif pilih == 3:
        hasilCluster, centroidAkhir = prosesKMeans(dataAwal, centroidLama, 5)

    elif pilih == 4:
        if not hasilCluster:
            print("\n[!] Belum ada data hasil clustering. Jalankan proses K-Means terlebih dahulu.")
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
