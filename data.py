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


def ruleOfThumb():
    n = len(dataAwal)
    return round(math.sqrt(n / 2))


def buatCentroid(k):
    centroids = []
    seen = []
    for row in dataAwal:
        if row[1] not in seen:
            seen.append(row[1])
            centroids.append(list(row[1]))
        if len(centroids) == k:
            break
    return centroids


k = ruleOfThumb()
centroid = buatCentroid(k)
