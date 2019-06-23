import struct
import numpy as np
import matplotlib.pyplot as plt
from random import randint
from shapely.geometry import Point, Polygon, LineString


class Point(object):
    def __init__(self, x, y, klas=None):
        self.X = x
        self.Y = y
        self.Klas = klas if klas is not None else ''

    def __str__(self):
        return "Tocka(%s,%s,%s)" % (self.X, self.Y, self.Klas)


def preberiBin(izDatoteke, vDatoteko):
    arrTock = np.array((()))
    with open(izDatoteke, "r") as file:
        data = np.fromfile(file, dtype=np.float32)
    reshaped = np.size(data) / 2
    data = np.reshape(data, (int(reshaped), 2))
    for i in range(len(data)):
        p = Point(data[i][0], data[i][1])
        arrTock = np.append(arrTock, p)
    return arrTock

# 1.Klasificiramo vsako oglišče vi glede na njegovega predhodnika vp (= vi-1)
# in naslednika vn (= vi+1). Naletimo lahko na pet tipov oglišč
# - prevoj (INT) - vp ima večjo in vn manjšo vrednost Y (ali obratno)
# kot pa testirano vi
# - lokalni minimum (MIN) - vp in vn imata večjo vrednost Y
# - lokalni maksimum (MAX) - vp in vn imata manjšo vrednost Y
# - vodoravni odsek - kadar ima en sosed (vp ali vn) enako vrednost Y
# (znotraj neke tolerance) kot vi nastopi vodoravni odsek.
# Le tega ločimo na dva tipa:
#    - HMAX, kadar ima drugi sosed manjšo vrednost Y
#    - HMIN, kadar ima drugi sosed večjo vrednost Y
# - izločitev (IGN), kadar imajo vsa tri oglišča isto vrednost Y
# (znotraj neke tolerance) takšno oglišče prezremo pri kasnejšnih korakih


def Klasificiramo(arrTock):
    prevoj = np.array((()))
    min1 = np.array((()))
    max1 = np.array((()))
    hmax = np.array((()))
    hmin = np.array((()))
    for i in range(len(arrTock)):
        # PREVOJ
        # - če smo na zadnji točki v arrayu, je naslednik prva točka v arr.
        if i == (len(arrTock)-1):
            if arrTock[i - 1].Y > arrTock[i].Y and \
                 arrTock[0].Y < arrTock[i].Y or \
                    arrTock[i - 1].Y < arrTock[i].Y and \
                    arrTock[0].Y > arrTock[i].Y:
                # print(arrTock[i - 1])
                # print(arrTock[i])
                # print(arrTock[0])
                arrTock[i].Klas = 'prevoj'
                prevoj = np.append(prevoj, arrTock[i])
        else:
            if arrTock[i - 1].Y > arrTock[i].Y and \
                arrTock[i + 1].Y < arrTock[i].Y \
                    or arrTock[i - 1].Y < arrTock[i].Y and \
                    arrTock[i + 1].Y > arrTock[i].Y:
                # print(arrTock[i - 1])
                # print(arrTock[i])
                # print(arrTock[i + 1])
                arrTock[i].Klas = 'prevoj'
                prevoj = np.append(prevoj, arrTock[i])
        # MIN
        # - če smo na zadnji točki v arrayu, je naslednik prva točka v arr.
        if i == (len(arrTock) - 1):
            if arrTock[i - 1].Y > arrTock[i].Y and \
                    arrTock[0].Y > arrTock[i].Y:
                arrTock[i].Klas = 'min'
                min1 = np.append(min1, arrTock[i])
        else:
            if arrTock[i - 1].Y > arrTock[i].Y and \
                    arrTock[i + 1].Y > arrTock[i].Y:
                arrTock[i].Klas = 'min'
                min1 = np.append(min1, arrTock[i])
        # MAX
        # - če smo na zadnji točki v arrayu, je naslednik prva točka v arr.
        if i == (len(arrTock) - 1):
            if arrTock[i - 1].Y < arrTock[i].Y and \
                    arrTock[0].Y < arrTock[i].Y:
                arrTock[i].Klas = 'max'
                max1 = np.append(max1, arrTock[i])
        else:
            if arrTock[i - 1].Y < arrTock[i].Y and \
                    arrTock[i + 1].Y < arrTock[i].Y:
                arrTock[i].Klas = 'max'
                max1 = np.append(max1, arrTock[i])
        # Vodoravni Odsek
        if i == (len(arrTock) - 1):
            # Predhodnjik
            if np.isclose(arrTock[i - 1].Y, arrTock[i].Y, atol=0.000001):
                if arrTock[0].Y < arrTock[i].Y:
                    arrTock[i].Klas = 'hmax'
                    hmax = np.append(hmax, arrTock[i])
                elif arrTock[0].Y > arrTock[i].Y:
                    arrTock[i].Klas = 'hmin'
                    hmin = np.append(hmin, arrTock[i])
            # Naslednjik
            elif np.isclose(arrTock[0].Y, arrTock[i].Y, atol=0.000001):
                if arrTock[i-1].Y < arrTock[i].Y:
                    arrTock[i].Klas = 'hmax'
                    hmax = np.append(hmax, arrTock[i])
                elif arrTock[i-1].Y > arrTock[i].Y:
                    arrTock[i].Klas = 'hmin'
                    hmin = np.append(hmin, arrTock[i])
        else:
            if np.isclose(arrTock[i - 1].Y, arrTock[i].Y, atol=0.000001):
                if arrTock[i+1].Y < arrTock[i].Y:
                    arrTock[i].Klas = 'hmax'
                    hmax = np.append(hmax, arrTock[i])
                elif arrTock[i+1].Y > arrTock[i].Y:
                    arrTock[i].Klas = 'hmin'
                    hmin = np.append(hmin, arrTock[i])
            # Naslednjik
            elif np.isclose(arrTock[i+1].Y, arrTock[i].Y, atol=0.000001):
                if arrTock[i-1].Y < arrTock[i].Y:
                    arrTock[i].Klas = 'hmax'
                    hmax = np.append(hmax, arrTock[i])
                elif arrTock[i-1].Y > arrTock[i].Y:
                    arrTock[i].Klas = 'hmin'
                    hmin = np.append(hmin, arrTock[i])
    # IGN
    j = None
    for i in range(len(arrTock)):
        if j is not None:
            i = j
        if i == (len(arrTock) - 1):
            if np.isclose(arrTock[i - 1].Y, arrTock[i].Y, atol=0.000001) and \
                 np.isclose(arrTock[0].Y, arrTock[i].Y, atol=0.000001):
                arrTock[i].Klas = 'IGN'
                # index = np.argwhere(arrTock == arrTock[i])
                # print(index)
                # arrTock = np.delete(arrTock, index)
                # j = i
                continue
        else:
            if np.isclose(arrTock[i - 1].Y, arrTock[i].Y, atol=0.000001) and \
                 np.isclose(arrTock[i + 1].Y, arrTock[i].Y, atol=0.000001):
                arrTock[i].Klas = 'IGN'
                # index = np.argwhere(arrTock == arrTock[i])
                # print(index)
                # arrTock = np.delete(arrTock, index)
                # j = i
                continue
        # if j is not None:
            # j += 1
    return arrTock

"""  for point in prevoj:
        print(point)
    print('\n')
    for point in max1:
        print(point)
    print('\n')
    for point in min1:
        print(point)
    print('\n')
    for point in hmax:
        print(point)
    print('\n') """

# 3. Inicializiramo dve preiskovalni premici, zadnjo ter sprednjo.
# 3.1 Inicializacija zadnje premice poteka sledeče:
#  - Iz urejenega seznama S vzamemo eno točko, ter vse točke, ki imajo enako Y
#  vrednost (znotraj neke tolerance)
#  - Te točke sortiramo po X vrednostih
#  - Sedaj napolnimo zadnjo preiskovalno premico po sledečih pravilih,
#  če je tip oglišča:
#    - MAX, dodaj oglišče dvakrat,
#    - HMAX, dodaj oglišče enkrat,
#    - točke ki predstavljajo presečišča vstavimo samo enkrat,
#    - vse ostale tipe oglišč prezremo.


def zadnjaPremica(arrTock):
    tocke = np.array(())
    zadnjaPreiskovalnaPremica = np.array(())
    # randomTocka = randint(0, len(arrTock) - 1)
    # randomTocka = arrTock[randomTocka]
    randomTocka = arrTock[0]
    for i in range(len(arrTock)):
        if np.isclose(arrTock[i].Y, randomTocka.Y, atol=0.001):
            tocke = np.append(tocke, arrTock[i])
    tocke = sorted(tocke, key=lambda point: point.X)
    for tocka in tocke:
        if tocka.Klas != 'IGN':
            if tocka.Klas == 'max':
                zadnjaPreiskovalnaPremica = \
                    np.append(zadnjaPreiskovalnaPremica, tocka)
                zadnjaPreiskovalnaPremica = \
                    np.append(zadnjaPreiskovalnaPremica, tocka)
            elif tocka.Klas == 'hmax' or tocka.Klas == 'prevoj':
                zadnjaPreiskovalnaPremica = \
                    np.append(zadnjaPreiskovalnaPremica, tocka)
    return zadnjaPreiskovalnaPremica


# 3.2 Inicializacija sprednje preiskovalne premice poteka sledeče:
#  - Iz urejenega seznama S vzamemo naslednjo točko,
#  ter isto kot prej vse točke ki imajo enako Y vrednost
# (znotraj neke tolerance)
#  - Dodatno na tej Y vrednosti ustvarimo paralelno premico z osjo X ter
#  poiscemo vsa presecisca s stranicami mnogokotnika
#  - Točke iz seznama in najdena presecisca sortiramo po njunih vrednostih X
#  - Sedaj napolnimo sprednjo preiskovalno premico po sledečih pravilih,
#  če je tip oglišča:
#    - MIN, dodaj oglišče dvakrat v sprednjo preiskovalno premico,
#    - INT ali HMIN, dodaj oglišče enkrat v sprednjo preiskovalno premico,
#    - točke ki predstavljajo presečišča vstavimo samo enkrat,
#    - in vse ostale tipe prezremo.


def sprednjaPremica(arrTock):
    tocke = np.array(())
    sprednjaPreiskovalnaPremica = np.array(())
    randomTocka = arrTock[1]
    for i in range(len(arrTock)):
        if np.isclose(arrTock[i].Y, randomTocka.Y, atol=0.001):
            tocke = np.append(tocke, arrTock[i])
        # Poisci presecisca s polygonom.


# Zadnja in sprednja preiskovalna premica bi sedaj morale imeti isto (sodo)
# stevilo tock! V nasprotnem primeru je nekje prislo do napake


if __name__ == "__main__":
    arrTock = preberiBin('polygon4.bin', 'out.bin')
    arrTock = Klasificiramo(arrTock)
    # Sortiraj tocke glede na X vrednost!
    arrTock = sorted(arrTock, key=lambda point: point.Y)
    zadnjaPreiskovalnaPremica = zadnjaPremica(arrTock)
    for tocka in zadnjaPreiskovalnaPremica:
        print(tocka)
    # for tocka in arrTock:
    #   print(tocka)
    # narisi = arrTock
    # narisi = np.append(narisi, narisi[0])
    # xs = np.array((()))
    # ys = np.array((()))
    # for x in narisi:
    #     xs = np.append(xs, x.X)
    #     ys = np.append(ys, x.Y)
    # plt.figure()
    # plt.plot(xs, ys)
    # plt.show()
    pass
