dataAwal = [
    ["acha",            [4,4,4], 0],
    ["Khilda",          [3,4,4], 0],
    ["Kharisa",         [3,3,4], 0],
    ["Nadiana",         [4,2,3], 0],
    ["Faiq",            [5,4,5], 0],
    ["Khansa",          [4,5,4], 0],
    ["ripda",           [4,3,3], 0],
    ["Elbima",          [3,4,3], 0],
    ["Aqsah",           [5,2,4], 0],
    ["Dhafin",          [4,3,3], 0],
    ["Sylvia",          [3,4,3], 0],
    ["Indah",           [3,4,4], 0],
    ["Ridwan",          [5,2,2], 0],
    ["Hasna",           [4,3,3], 0],
    ["Aflah",           [5,5,5], 0],
    ["Fakhira",         [5,5,3], 0],
    ["Arifah",          [4,4,3], 0],
    ["Almaidah",        [4,4,3], 0],
    ["Nazhwa",          [4,4,4], 0],
    ["Lesley",          [2,2,2], 0],
    ["Afit",            [4,4,4], 0],
    ["Zidni",           [4,4,4], 0],
    ["Barra",           [4,4,4], 0],
    ["Elbima2",         [3,4,3], 0],
    ["Yahfasyat",       [4,4,4], 0],
    ["Tuska",           [1,1,5], 0],
    ["Najib",           [3,3,3], 0],
    ["Lucky",           [4,4,4], 0],
    ["Anonim",          [3,4,3], 0],
    ["Adiba",           [4,4,4], 0],
    ["Raditya",         [4,5,3], 0],
    ["RATUW",           [3,4,3], 0],
    ["Daffa",           [5,5,3], 0],
]

k = 3

centroidAwal = [
    [5, 4, 5],
    [3, 3, 3],
    [1, 1, 5],
]


centroidLama = [
    round(sum(c) / len(c), 2)
    for c in centroidAwal
]