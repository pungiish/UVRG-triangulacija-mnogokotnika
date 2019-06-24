import struct
import numpy as np
import matplotlib.pyplot as plt
from random import randint
import shapely.geometry


class Point(object):
    def __init__(self, x, y, klas=None):
        self.X = x
        self.Y = y
        self.Klas = klas if klas is not None else ''

    def __str__(self):
        return "Tocka(%s,%s,%s)" % (self.X, self.Y, self.Klas)


def sekanjeDaljic(daljica1, daljica2):
    D = (((daljica1[1][0])-(daljica1[0][0]))*((daljica2[1][1])-(daljica2[0][1]))) - \
            (((daljica2[1][0])-(daljica2[0][0]))*((daljica1[1][1])-(daljica1[0][1])))

    A = (((daljica2[1][0])-(daljica2[0][0]))*((daljica1[0][1])-(daljica2[0][1]))) - \
        (((daljica1[0][0])-(daljica2[0][0]))*((daljica2[1][1])-(daljica2[0][1])))

    B = (((daljica1[1][0])-(daljica1[0][0]))*((daljica1[0][1])-(daljica2[0][1]))) - \
        (((daljica1[0][0])-(daljica2[0][0]))*((daljica1[1][1])-(daljica1[0][1])))

    if D != 0:
        Ua = float(A/D)
        Ub = float(B/D)
        if 0 < Ua and Ua < 1 and 0 < Ub and Ub < 1:
            x = float(daljica1[0][0])+Ua*(float(daljica1[1][0])-float(daljica1[0][0]))
            y = float(daljica1[0][1]) + Ua * (float(daljica1[1][1]) - float(daljica1[0][1]))
            print("Sekanje", "Daljici se sekata. Presečišče je na koordinatah " + str(x) + "," + str(y) + ".")
            return Point(x, y)
        else:
            return False
        # elif Ua==1.0 or Ub==-0.0 or Ub==1.0 or Ua==-0.0 or Ub==0.0 or Ua==0.0:
        # x = float(daljica1[0][0])+Ua*(float(daljica1[1][0])-float(daljica1[0][0]))
        # y = float(daljica1[0][1])+Ua*(float(daljica1[1][1])-float(daljica1[0][1]))
        # print("Dotikanje", "Daljici se dotikata, na koordinatah " + str(x) + "," + str(y) + ".")
        # return Point(x, y)
    else:
        return False


def preberiBin(izDatoteke, vDatoteko):
    arrTock = np.array((()))
    with open(izDatoteke, "r") as file:
        data = np.fromfile(file, dtype=np.float32)
    reshaped = np.size(data) / 2
    data = np.reshape(data, (int(reshaped), 2))
    newData = data.tolist()
    for i in range(len(data)):
        p = Point(data[i][0], data[i][1])
        arrTock = np.append(arrTock, p)
    return arrTock, newData

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
            if np.isclose(arrTock[i - 1].Y, arrTock[i].Y, atol=0.0001):
                if arrTock[0].Y < arrTock[i].Y:
                    arrTock[i].Klas = 'hmax'
                    hmax = np.append(hmax, arrTock[i])
                elif arrTock[0].Y > arrTock[i].Y:
                    arrTock[i].Klas = 'hmin'
                    hmin = np.append(hmin, arrTock[i])
            # Naslednjik
            elif np.isclose(arrTock[0].Y, arrTock[i].Y, atol=0.0001):
                if arrTock[i-1].Y < arrTock[i].Y:
                    arrTock[i].Klas = 'hmax'
                    hmax = np.append(hmax, arrTock[i])
                elif arrTock[i-1].Y > arrTock[i].Y:
                    arrTock[i].Klas = 'hmin'
                    hmin = np.append(hmin, arrTock[i])
        else:
            if np.isclose(arrTock[i - 1].Y, arrTock[i].Y, atol=0.0001):
                if arrTock[i+1].Y < arrTock[i].Y:
                    arrTock[i].Klas = 'hmax'
                    hmax = np.append(hmax, arrTock[i])
                elif arrTock[i+1].Y > arrTock[i].Y:
                    arrTock[i].Klas = 'hmin'
                    hmin = np.append(hmin, arrTock[i])
            # Naslednjik
            elif np.isclose(arrTock[i+1].Y, arrTock[i].Y, atol=0.0001):
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
            if np.isclose(arrTock[i - 1].Y, arrTock[i].Y, atol=0.0001) and \
                 np.isclose(arrTock[0].Y, arrTock[i].Y, atol=0.0001):
                arrTock[i].Klas = 'IGN'
                # index = np.argwhere(arrTock == arrTock[i])
                # print(index)
                # arrTock = np.delete(arrTock, index)
                # j = i
                continue
        else:
            if np.isclose(arrTock[i - 1].Y, arrTock[i].Y, atol=0.0001) and \
                 np.isclose(arrTock[i + 1].Y, arrTock[i].Y, atol=0.0001):
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


def zadnjaPremica(arrTockSorted, arrTock):
    arrx = np.array(())
    tocke = np.array(())
    zadnjaPreiskovalnaPremica = np.array(())
    # index = randint(0, len(arrTockSorted) - 1)
    randomTocka = arrTockSorted[0]
    # Če smo vzeli zadnjo točko, index = -1, ker ga potem inkrementiramo, ko kličemo funkcijo sprednjaPremica
    # if index == len(arrTockSorted)-1:
    #    index = -1
    # randomTocka = arrrTockSorted[0]
    # if randomTocka.Klas != 'max' and randomTocka.Klas != 'hmax':
    #    zadnjaPremica(arrTockSorted, arrTock)
    for i in range(len(arrTockSorted)):
        if np.isclose(arrTockSorted[i].Y, randomTocka.Y, atol=0.01):
            tocke = np.append(tocke, arrTockSorted[i])
    tocke = sorted(tocke, key=lambda point: point.X)
    for tocka in tocke:
        if tocka.Klas != 'IGN':
            if tocka.Klas == 'max':
                zadnjaPreiskovalnaPremica = \
                    np.append(zadnjaPreiskovalnaPremica, tocka)
                zadnjaPreiskovalnaPremica = \
                    np.append(zadnjaPreiskovalnaPremica, tocka)
            elif tocka.Klas == 'hmax':
                zadnjaPreiskovalnaPremica = \
                    np.append(zadnjaPreiskovalnaPremica, tocka)
    # Poisci presecisca s stranicami polygona.
    shapely_line = shapely.geometry.LineString([(-2, randomTocka.Y),
        (2, randomTocka.Y)])
    for i in range(len(arrTock)):
        if i != len(arrTock) - 1:
            shapely_line1 = shapely.geometry.LineString([(arrTock[i].X, arrTock[i].Y),
            (arrTock[i + 1].X, arrTock[i + 1].Y)])
            print(shapely_line.coords[0])
            print(shapely_line.coords[1])
            print(shapely_line1.coords[0])
            print(shapely_line1.coords[1])
            print('\n')
            tocka = sekanjeDaljic(shapely_line.coords, shapely_line1.coords)
            if tocka:
                arrx = np.append(arrx, tocka.X)
            """ if shapely_line1.intersects(shapely_line):
                intersection_line = shapely_line1.intersection(shapely_line)
                p = Point(intersection_line.x, intersection_line.y)
                points = np.append(points, p) """
        else:
            shapely_line1 = shapely.geometry.LineString([(arrTock[i].X, arrTock[i].Y),
                (arrTock[0].X, arrTock[0].Y)])
            print(shapely_line.coords[0])
            print(shapely_line.coords[1])
            print(shapely_line1.coords[0])
            print(shapely_line1.coords[1])
            print('\n')
            tocka = sekanjeDaljic(shapely_line.coords, shapely_line1.coords)
            if tocka:
                arrx = np.append(arrx, tocka.X)
            """ if shapely_line1.intersects(shapely_line):
                intersection_line = shapely_line1.intersection(shapely_line)
                p = Point(intersection_line.x, intersection_line.y)
                points = np.append(points, p) """
    # Zbriši duplikate
    arrx = np.unique(arrx)
    K = None
    # preveri, če je so v arrx slučajno točke polygona
    for i in range(len(zadnjaPreiskovalnaPremica)):
        for j in range(len(arrx)):
            if K is not None:
                j = K
            if zadnjaPreiskovalnaPremica[i].X == arrx[j]:
                idx = np.argwhere(zadnjaPreiskovalnaPremica[i].X == arrx[j])
                arrx = np.delete(arrx, idx)
                if j != 0:
                    K = j - 1
                else:
                    K = j
    for x in arrx:
        zadnjaPreiskovalnaPremica = np.append(zadnjaPreiskovalnaPremica, Point(x, randomTocka.Y))
    for point in zadnjaPreiskovalnaPremica:
        print(point)
    sprednjaPreiskovalnaPremica = sprednjaPremica(arrTockSorted, arrTock, 1)
    return zadnjaPreiskovalnaPremica, sprednjaPreiskovalnaPremica


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


def sprednjaPremica(arrTockSorted, arrTock, idx):
    arrx = np.array(())
    points = np.array(())
    tocke = np.array(())
    sprednjaPreiskovalnaPremica = np.array(())
    sprednjaPreiskovalnaPremica1 = np.array(())
    randomTocka = arrTockSorted[idx]
    shapely_line = shapely.geometry.LineString([(-2, randomTocka.Y),
        (2, randomTocka.Y)])
    # shapely_polygon = shapely.geometry.Polygon(data)
    # plt.plot(*shapely_polygon.exterior.xy)
    # plt.show()
    # intersection_line = shapely_polygon.intersection(shapely_line)
    # print(intersection_line)

    # dodaj točke, ki imajo isti y znotraj neke tolerance
    for i in range(len(arrTockSorted)):
        if np.isclose(arrTockSorted[i].Y, randomTocka.Y, atol=0.001):
            sprednjaPreiskovalnaPremica = np.append(sprednjaPreiskovalnaPremica, arrTockSorted[i])
            continue
    # Poisci presecisca s stranicami polygona.
    for i in range(len(arrTock)):
        if i != len(arrTock) - 1:
            shapely_line1 = shapely.geometry.LineString([(arrTock[i].X, arrTock[i].Y),
            (arrTock[i + 1].X, arrTock[i + 1].Y)])
            print(shapely_line.coords[0])
            print(shapely_line.coords[1])
            print(shapely_line1.coords[0])
            print(shapely_line1.coords[1])
            print('\n')
            tocka = sekanjeDaljic(shapely_line.coords, shapely_line1.coords)
            if tocka:
                arrx = np.append(arrx, tocka.X)
            """ if shapely_line1.intersects(shapely_line):
                intersection_line = shapely_line1.intersection(shapely_line)
                p = Point(intersection_line.x, intersection_line.y)
                points = np.append(points, p) """
        else:
            shapely_line1 = shapely.geometry.LineString([(arrTock[i].X, arrTock[i].Y),
                (arrTock[0].X, arrTock[0].Y)])
            print(shapely_line.coords[0])
            print(shapely_line.coords[1])
            print(shapely_line1.coords[0])
            print(shapely_line1.coords[1])
            print('\n')
            tocka = sekanjeDaljic(shapely_line.coords, shapely_line1.coords)
            if tocka:
                arrx = np.append(arrx, tocka.X)
            """ if shapely_line1.intersects(shapely_line):
                intersection_line = shapely_line1.intersection(shapely_line)
                p = Point(intersection_line.x, intersection_line.y)
                points = np.append(points, p) """
    # Zbriši duplikate
    arrx = np.unique(arrx)
    K = None
    # preveri, če je so v arrx slučajno točke polygona
    for i in range(len(sprednjaPreiskovalnaPremica)):
        for j in range(len(arrx)):
            if K is not None:
                j = K
            if sprednjaPreiskovalnaPremica[i].X == arrx[j]:
                idx = np.argwhere(sprednjaPreiskovalnaPremica[i].X == arrx[j])
                arrx = np.delete(arrx, idx)
                K = j
    for x in arrx:
        sprednjaPreiskovalnaPremica = np.append(sprednjaPreiskovalnaPremica, Point(x, randomTocka.Y))
    for point in sprednjaPreiskovalnaPremica:
        print(point)
    sprednjaPreiskovalnaPremica = sorted(sprednjaPreiskovalnaPremica, key=lambda point: point.X)
    for tocka in sprednjaPreiskovalnaPremica:
        if tocka.Klas != 'IGN':
            if tocka.Klas == 'min':
                sprednjaPreiskovalnaPremica1 = \
                    np.append(sprednjaPreiskovalnaPremica1, tocka)
                sprednjaPreiskovalnaPremica1 = \
                    np.append(sprednjaPreiskovalnaPremica1, tocka)
            elif tocka.Klas == 'hmin' or tocka.Klas == 'prevoj':
                sprednjaPreiskovalnaPremica1 = \
                    np.append(sprednjaPreiskovalnaPremica1, tocka)
            elif tocka.Klas == '':
                sprednjaPreiskovalnaPremica1 = \
                    np.append(sprednjaPreiskovalnaPremica1, tocka)
            else:
                continue
    return sprednjaPreiskovalnaPremica1

# Zadnja in sprednja preiskovalna premica bi sedaj morale imeti isto (sodo)
# stevilo tock! V nasprotnem primeru je nekje prislo do napake

if __name__ == "__main__":
    arrTock, data = preberiBin('polygon1.bin', 'out.bin')
    narisi = arrTock
    narisi = np.append(narisi, narisi[0])
    xs = np.array((()))
    ys = np.array((()))
    for x in narisi:
        xs = np.append(xs, x.X)
        ys = np.append(ys, x.Y)
    plt.figure()
    plt.plot(xs, ys)
    plt.show()
    arrTock = Klasificiramo(arrTock)
    polygon = arrTock
    # Sortiraj tocke glede na Y vrednost!
    arrTock = sorted(arrTock, key=lambda point: point.Y)
    # data = sorted(data, key=lambda tocka: tocka[1])
    zadnjaPreiskovalnaPremica, sprednjaPreiskovalnaPremica = zadnjaPremica(arrTock, polygon)
    print('\n')
    for point in zadnjaPreiskovalnaPremica:
        print(point)
    for point in sprednjaPreiskovalnaPremica:
        print(point)
    # for tocka in zadnjaPreiskovalnaPremica:
    #   print(tocka)
    # for tocka in arrTock:
    #   print(tocka)
    # narisi = arrTock
    # narisi = np.append(narisi, narisi[0])
    # xs = np.array((()))
    # ys = np.array((()))
    # for x in narisi:
    #   xs = np.append(xs, x.X)
    #   ys = np.append(ys, x.Y)
    # plt.figure()
    # plt.plot(xs, ys)
    # plt.show()
    pass
