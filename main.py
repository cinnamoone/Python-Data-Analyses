from matplotlib import pyplot as plt
from functools import reduce
import math
import numpy as np
import matplotlib.pyplot as plot
import pandas as pd
from scipy import stats

global filtered_students_grade
global filtered_students_absence
x = 0

def parse_lines_to_students(file_name):
    students = []
    with open(file_name) as file:
        file_lines = file.readlines()
        for line in file_lines[1::]:
            properties = line.split(",")
            student = {'address': properties[0],
                       'absences': properties[1],
                       'Mjob': properties[2],
                       'Fjob': properties[3],
                       'math_grade': properties[4]}
            student['math_grade'] = int(student['math_grade'].split("\n")[0])
            student['absences'] = int(student['absences'])
            student['address'] = student['address'].upper()
            students.append(student)
    return students


def filter_students_and_map_to_grades(students, filter_parameter):
    if filter_parameter == None:
        filtered_students_grade = list(map(lambda student: student['math_grade'], students))
    else:
        filtered_students = list(filter(lambda student: student['address'] == filter_parameter, students))
        filtered_students_grade = list(map(lambda student: student['math_grade'], filtered_students))
    return filtered_students_grade


def filter_students_and_map_to_absences(students, filter_parameter):
    if filter_parameter == None:
        filtered_students_absence = list(map(lambda student: student['absences'], students))
    else:
        filtered_students = list(filter(lambda student: student['address'] == filter_parameter, students))
        filtered_students_absence = list(map(lambda student: student['absences'], filtered_students))
    return filtered_students_absence


def calc_average_grade(students, filter_parameter=None):
    if filter_parameter == None:
        avg_grade = reduce((lambda sum, student: sum + student['math_grade']), students, 0) / len(students)
    else:
        filtered_students = list(filter(lambda student: student['address'] == filter_parameter, students))
        avg_grade = reduce((lambda sum, student: sum + student['math_grade']), filtered_students, 0) / len(
            filtered_students)
    return avg_grade


def calc_average_absence(students, filter_parameter=None):
    if filter_parameter == None:
        avg_absence = reduce((lambda sum, student: sum + student['absences']), students, 0) / len(students)
    else:
        filtered_students = list(filter(lambda student: student['address'] == filter_parameter, students))
        avg_absence = reduce((lambda sum, student: sum + student['absences']), filtered_students, 0) / len(
            filtered_students)
    return avg_absence


def calc_median(students, filter_parameter=None):
    filtered_students_grade = filter_students_and_map_to_grades(students, filter_parameter)
    filtered_students_grade.sort()

    if len(filtered_students_grade) % 2 == 0:
        mediana = (filtered_students_grade[len(filtered_students_grade) // 2] + filtered_students_grade[
            len(filtered_students_grade) // 2 + 1]) / 2
    else:
        mediana = filtered_students_grade[(len(filtered_students_grade) // 2) + 1]

    return mediana


def calc_standard_deviation(students, filter_parameter=None):
    average = calc_average_grade(students, filter_parameter)
    nominator = 0
    filtered_students_grade = filter_students_and_map_to_grades(students, filter_parameter)

    for grade in filtered_students_grade:
        nominator = nominator + pow(grade - average, 2)

    n = len(filtered_students_grade)
    standard_deviation = math.sqrt(nominator / n)

    return standard_deviation


def calc_standard_deviation_abs(students, filter_parameter=None):
    average_abs = calc_average_absence(students, filter_parameter)
    nominator = 0
    filtered_students_absence = filter_students_and_map_to_absences(students, filter_parameter)

    for absence in filtered_students_absence:
        nominator = nominator + pow(absence - average_abs, 2)

    n = len(filtered_students_absence)
    standard_deviation_abs = math.sqrt(nominator / n)

    return standard_deviation_abs


def calc_dominant(students, filter_parameter=None):
    counter = 0
    dict_counter_grade = {}
    dominant = []
    filtered_students_grade = filter_students_and_map_to_grades(students, filter_parameter)

    for grade in filtered_students_grade:
        if grade in dict_counter_grade:
            dict_counter_grade[grade] += 1
        else:
            dict_counter_grade[grade] = 1

    for grade in dict_counter_grade:
        if dict_counter_grade[grade] > counter:
            counter = dict_counter_grade[grade]
            dominant = [grade]
        elif dict_counter_grade[grade] == counter:
            dominant.append(grade)
    return dominant


def calc_corelation(students, filter_parameter=None):
    mean_grade = calc_average_grade(students)
    mean_grade_ = calc_average_grade(students, filter_parameter)
    mean_abs = calc_average_absence(students)
    mean_abs_ = calc_average_absence(students, filter_parameter)
    filtered_students_grade = filter_students_and_map_to_grades(students, filter_parameter)
    filtered_students_absence = filter_students_and_map_to_absences(students, filter_parameter)

    lista_grade = []
    for grade in filtered_students_grade:
        if filter_parameter == None:
            czynnik1 = mean_grade - grade
            lista_grade.append(czynnik1)
        else:
            czynnik1 = mean_grade_ - grade
            lista_grade.append(czynnik1)

    lista_abs = []
    for absence in filtered_students_absence:
        if filter_parameter == None:
            czynnik2 = mean_abs - absence
            lista_abs.append(czynnik2)
        else:
            czynnik2 = mean_abs_ - absence
            lista_abs.append(czynnik2)
    # return lista_abs
    # return lista_grade
    pomnozone = []
    for i in range(len(lista_abs)):
        pomnozone.append(lista_abs[i] * lista_grade[i])

    # return pomnozone
    czynnik1_sq = []
    for i in range(len(lista_abs)):
        czynnik1_sq.append(lista_abs[i] * lista_abs[i])

    czynnik2_sq = []
    for i in range(len(lista_grade)):
        czynnik2_sq.append(lista_grade[i] * lista_grade[i])

    suma_pomnozone = sum(pomnozone)
    suma_czynnik1_sq = sum(czynnik1_sq)
    suma_czynnik2_sq = sum(czynnik2_sq)

    # return suma_pomnozone
    # return suma_czynnik1_sq
    # return suma_czynnik2_sq
    corelation = suma_pomnozone / math.sqrt(suma_czynnik1_sq * suma_czynnik2_sq)
    return corelation

#print(lista_abs)

file_name = 'dane_szkoła.csv'
students = parse_lines_to_students(file_name)


#def sumaNieobecnosci():

# średnie:
#print("Średnia ocen wszystkich studentów: ", round(calc_average_grade(students), 2))
#print("Średnia ocen studentów z terenów wiejskich: ", round(calc_average_grade(students, 'R'), 2))
#print("Średnia ocen studentów z terenów miejskich: ", round(calc_average_grade(students, 'U'), 2))

#print('-' * 20)
#print("Średnia nieobecności wszystkich studentów: ", round(calc_average_absence(students), 2))
#print("Średnia nieobecności studentów z terenów wiejskich: ", round(calc_average_absence(students, 'R'), 2))
#print("Średnia nieobecności studentów z terenów miejskich: ", round(calc_average_absence(students, 'U'), 2))
#print('-' * 20)
# mediany:
#print("Mediana ocen wszystkich studentów: ", calc_median(students))
#print("Mediana ocen studentów z terenów wiejskich: ", round(calc_median(students, 'R'), 2))
#print("Mediana ocen studentów z terenów miejskich: ", round(calc_median(students, 'U'), 2))
#print('-' * 20)
# odchylenia_standardowe:
#print("Odchylenie standardowe dla ocen wszystkich studentów: ", round(calc_standard_deviation(students), 2))
#print("Odchylenie standardowe dla ocen studentów z terenów wiejskich: ",
#      round(calc_standard_deviation(students, 'R'), 2))
#print("Odchylenie standarodowe dla ocen studentów z terenów miejskich: ",
#     round(calc_standard_deviation(students, 'U'), 2))
#print('-' * 20)
#print("Odchylenie standardowe dla nieobecności wszystkich studentów: ", round(calc_standard_deviation_abs(students), 2))
#print("Odchylenie standardowe dla nieobecności studentów z terenów wiejskich: ",
#      round(calc_standard_deviation_abs(students, 'R'), 2))
#print("Odchylenie standarodowe dla nieobecności studentów z terenów miejskich: ",
#      round(calc_standard_deviation_abs(students, 'U'), 2))
#print('-' * 20)
# moda
#print("Moda dla ocen wszystkich studentów: ", calc_dominant(students))
#print("Moda dla ocen studentów z terenów wiejskich: ", calc_dominant(students, 'R'))
#print("Moda dla ocen studentów z terenów miejskich: ", calc_dominant(students, 'U'))
#print('-' * 20)
# korelacja
#print("Współczynnik korelacji wszystkich studentów: ", calc_corelation(students))
#print("Współczynnik korelacji studentów z terenów wiejskich: ", calc_corelation(students, 'R'))
#print("Współczynnik korelacji studentów z terenów miejskich: ", calc_corelation(students, 'U'))

###############################
# wyzaczenie wzoru, podpunkt 14

def CountGrade():
    korelacja_R = calc_corelation(students, 'R')
    korelacja_U = calc_corelation(students, 'U')
    odchylenie_grade_R = calc_standard_deviation(students, 'R')
    odchylenie_grade_U = calc_standard_deviation(students, 'U')
    odchylenie_abs_R = calc_standard_deviation_abs(students, 'R')
    odchylenie_abs_U = calc_standard_deviation_abs(students, 'U')
    mean_grade_R = calc_average_absence(students, 'R')
    mean_grade_U = calc_average_absence(students, 'U')

    mean_abs_R = calc_average_absence(students, 'R')
    mean_abs_U = calc_average_absence(students, 'U')

    b_R = round(korelacja_R * (odchylenie_grade_R / odchylenie_abs_R), 2)
    b_U = round(korelacja_U * (odchylenie_grade_U / odchylenie_abs_U), 2)
    a_R = round(mean_grade_R - (b_R * mean_abs_R), 2)
    a_U = round(mean_grade_U - (b_U * mean_abs_U), 2)
    #print(f'Wzór na obliczenie oceny ucznia z miasta na podstawie liczby jego nieobecności: y = {b_U} * x + {a_U}\n')
    #print(f'Wzór na obliczenie oceny ucznia ze wsi na podstawie liczby jego nieobecności: y = {b_R} * x + {a_R}\n')
    #

    uczen = input('\nSkąd pochodzi student? Wprowadź "R" (wieś) albo "U" (miasto): ')
    x = int(input('Podaj liczbę nieobecności studenta: '))
    if uczen == 'U' or uczen == 'u':
        #global ocena
        ocena = b_U * x + a_U
        PrzewidywanaOcena = round(ocena, 0)
        print('Przewidywana ocena studenta to: ', PrzewidywanaOcena)
        return x, ocena, PrzewidywanaOcena
    elif uczen == 'R' or uczen == 'r':
        #global ocena
        ocena = b_R * x + a_R
        PrzewidywanaOcena = round(ocena, 0)
        print('Przewidywana ocena studenta to: ', PrzewidywanaOcena)
        return x, ocena, PrzewidywanaOcena
    else:
        print('invalid syntax')

#CountGrade() - wywołanie funkcji

###############################
# regresja liniowa

df_regression = pd.read_csv('dane_szkoła.csv')
features = df_regression["absences"]
labels = df_regression["math_grade"]
slope, intercept, r, p, std_err = stats.linregress(features, labels)


def lineFunc(x):
    return slope * x + intercept


lineY = list(map(lineFunc, features))
# print(lineY)
corr_matrix = np.corrcoef(lineY, labels)
corr = corr_matrix[0, 1]
R_sq = corr ** 2
print('-' * 20)
print('Wartość współczynnika R^2 wynosi: ', R_sq)
print('-' * 20)
###############################

# wykres regresji
def WykresRegresji():
    plt.style.use('dark_background')
    ax1 = plt.subplot()
    plot.scatter(features, labels, color='cyan', label='wartosci oryginalne', marker='*')
    plot.plot(features, lineY, color='red', label='linia regresji')
    plt.xlabel('liczba nieobecnosci')
    plt.ylabel('liczba zdobytych punktow')
    plt.grid(linestyle='--', color='grey')
    plt.title('Regresja liniowa')
    plt.legend()
    ax1.set_facecolor('grey')
    ax1.patch.set_alpha(.55)
    plt.savefig('RegresjaLiniowa.png')
    plot.show()

# wizualizacje
# dane do wizualizacji
liczba = list(range(395))
praca = ['at_home', 'health', 'other', 'services', 'teacher']
dane = pd.read_csv('dane_szkoła.csv')
oceny = dane["math_grade"]
# punkty = dane["math_grade"].count()
nieobecnosci = dane["absences"]

# wykres slupkowy - praca matki i ojca
def WykresSlupkowy():
    plt.style.use('dark_background')
    ax2 = plt.subplot()
    mjob = dane["Mjob"]
    mjob_filtered = mjob.groupby([mjob])
    suma_mjob = mjob_filtered.size()
    fjob = dane["Fjob"]
    fjob_filtered = fjob.groupby([fjob])
    suma_fjob = fjob_filtered.size()
    width = 0.4
    index = np.arange(len(praca))
    plt.bar(index - width / 2, suma_fjob, width, color='blue', label='praca ojca')
    plt.bar(index + width / 2, suma_mjob, width, color='crimson', label='praca matki')
    plt.xticks(index, praca)
    plt.grid(linestyle='--')
    ax2.set_facecolor('purple')
    ax2.patch.set_alpha(.25)
    # ax.set_xticklabels(praca)
    plt.xlabel('Rodzaj pracy')
    plt.ylabel('Suma osób wykonujących daną pracę')
    plt.title('Praca rodziców')
    plt.legend()
    plt.savefig('PracaRodzicow.png')
    plt.show()

# wykres oceny
def WykresOceny():
    plt.style.use('classic')
    ax3 = plt.subplot()
    punkty = list(set(oceny))
    oceny_filtered = oceny.groupby([oceny])
    suma_oceny = oceny_filtered.count()
    # print(punkty)
    width = 1
    plt.bar(punkty, suma_oceny, width, color='crimson')
    plt.xticks(np.arange(min(punkty), max(punkty) + 1, 1.0))
    plt.yticks(np.arange(0, max(suma_oceny) + 1, 5.0))
    ax3.set_xlim([0, 20])
    plt.grid(linestyle='--')
    ax3.set_facecolor('pink')
    ax3.patch.set_alpha(.25)
    plt.xlabel('Liczba punktów')
    plt.ylabel('Liczba studentów')
    plt.title('Punkty zdobyte przez studentów')
    plt.savefig('WykresOcen.png')
    plt.show()

# wykres nieobecnosci
def WykresNieobecnosci():
    plt.style.use('classic')
    ax4 = plt.subplot()
    frekwencja = list(set(nieobecnosci))
    # print(frekwencja)
    nieobecnosci_filtered = nieobecnosci.groupby([nieobecnosci])
    suma_nieobecnosci = nieobecnosci_filtered.size()
    # print(suma_nieobecnosci)
    plt.bar(frekwencja, suma_nieobecnosci, color='blue')
    plt.xticks(np.arange(min(frekwencja), max(frekwencja) + 1, 3.0))
    plt.yticks(np.arange(0, max(suma_nieobecnosci) + 1, 5.0))
    ax4.set_xlim([0, 76])
    plt.grid(linestyle='--')
    ax4.set_facecolor('lightgreen')
    ax4.patch.set_alpha(.15)
    plt.xlabel('Nieobecności')
    plt.ylabel('Liczba studentów')
    plt.title('Frekwencja studentów')
    plt.savefig('WykresNieobecnosci.png')
    plt.show()

# wykres kolowy udzialu grup wiejska vs miejska
def WykresKolowy():
    plt.style.use('dark_background')
    ax5 = plt.subplot()
    grupy = ['wies', 'miasto']
    adres = dane['address']
    adres_upper = adres.str.upper()
    adress = adres_upper.groupby([adres_upper])
    adres_up = adress.size()
    colors = ['darkcyan', '#8a134e']
    explode = [0, 0.2]
    plt.pie(adres_up, labels=grupy, explode=explode, autopct='%.2f', colors=colors)
    plt.title('Procentowy udział studentów w klasie wg miejsca zamieszkania')
    plt.savefig('GrupyWiejskaMiejska.png')
    plt.show()

# wykres nieobecnosci i ocen
def WykresFrekwencji():
    plt.style.use('dark_background')
    ax6 = plt.subplot()
    plot.scatter(oceny, nieobecnosci, color='lime', label='oceny', marker='v')
    # plt.plot(liczba, oceny, color = 'purple', label = 'nieobecnoci')
    plt.grid(linestyle='--')
    ax6.set_facecolor('blue')
    ax6.patch.set_alpha(.25)
    plt.xlabel('Liczba uzyskanych puntkow')
    plt.ylabel('Liczba opuszconych zajęć')
    plt.title('Frekwencja studentów w stosunku do uzyskanych punktów')
    plt.savefig('NieobecnosciOceny.png')
    plt.show()

WykresSlupkowy()
WykresOceny()
WykresNieobecnosci()
WykresKolowy()
WykresFrekwencji()

Nieobecn, Ocena, PrzewidywanaOcena = CountGrade()

# raport końcowy
nazwa = input("Podaj nazwę i rozszerzenie pliku: ")
file = open(f"{nazwa}", "w", encoding="utf-8")

file.write("RAPORT KOŃCOWY\n")
file.write("Dokument przedstawia wyniki parametrów analizy danych.\n")
file.write("\n")

# średnie:
file.write("***** ŚREDNIE OCEN *****\n")
file.write(f"Średnia ocen wszystkich studentów: {round(calc_average_grade(students), 2)}\n")
file.write(f"Średnia ocen studentów z terenów wiejskich: {round(calc_average_grade(students, 'R'), 2)}\n")
file.write(f"Średnia ocen studentów z terenów miejskich: {round(calc_average_grade(students, 'U'), 2)}\n")

file.write('-' * 20)
file.write("\n")
file.write("***** ŚREDNIE NIEOBECNOŚCI *****\n")
file.write(f"Średnia nieobecności wszystkich studentów: {round(calc_average_absence(students), 2)}\n")
file.write(f"Średnia nieobecności studentów z terenów wiejskich: {round(calc_average_absence(students, 'R'), 2)}\n")
file.write(f"Średnia nieobecności studentów z terenów miejskich: {round(calc_average_absence(students, 'U'), 2)}\n")
file.write('-' * 20)
file.write("\n")

# mediany:
file.write("***** MEDIANY OCEN *****\n")
file.write(f"Mediana ocen wszystkich studentów: {calc_median(students)}\n")
file.write(f"Mediana ocen studentów z terenów wiejskich: {round(calc_median(students, 'R'), 2)}\n")
file.write(f"Mediana ocen studentów z terenów miejskich: {round(calc_median(students, 'U'), 2)}\n")
file.write('-' * 20)
file.write("\n")

# odchylenia_standardowe:
file.write("***** ODCHYLENIE STANDARDOWE OCEN *****\n")
file.write(f"Odchylenie standardowe dla ocen wszystkich studentów: {round(calc_standard_deviation(students), 2)}\n")
file.write(f"Odchylenie standardowe dla ocen studentów z terenów wiejskich: {round(calc_standard_deviation(students, 'R'), 2)}\n")
file.write(f"Odchylenie standardowe dla ocen studentów z terenów miejskich: {round(calc_standard_deviation(students, 'U'), 2)}\n")
file.write('-' * 20)
file.write("\n")

file.write("***** ODCHYLENIE STANDARDOWE NIEOBECNOŚCI *****\n")
file.write(f"Odchylenie standardowe dla nieobecności wszystkich studentów: {round(calc_standard_deviation_abs(students), 2)}\n")
file.write(f"Odchylenie standardowe dla nieobecności studentów z terenów wiejskich: {round(calc_standard_deviation_abs(students, 'R'), 2)}\n")
file.write(f"Odchylenie standardowe dla nieobecności studentów z terenów miejskich: {round(calc_standard_deviation_abs(students, 'U'), 2)}\n")
file.write('-' * 20)
file.write("\n")

# moda
file.write("***** ODCHYLENIE STANDARDOWE OCEN *****\n")
file.write(f"Moda dla ocen wszystkich studentów: {calc_dominant(students)}\n")
file.write(f"Moda dla ocen studentów z terenów wiejskich: {calc_dominant(students, 'R')}\n")
file.write(f"Moda dla ocen studentów z terenów miejskich: {calc_dominant(students, 'U')}\n")
file.write('-' * 20)
file.write("\n")

# korelacja
file.write("***** KORELACJA STUDENTÓW *****\n")
file.write(f"Współczynnik korelacji wszystkich studentów: {calc_corelation(students)}\n")
file.write(f"Współczynnik korelacji studentów z terenów wiejskich: {calc_corelation(students, 'R')}\n")
file.write(f"Współczynnik korelacji studentów z terenów miejskich: {calc_corelation(students, 'U')}\n")
file.write('-' * 20)

file.write("***** PRZEWIDYWANA OCENA *****\n")
file.write(f"Dla studenta, który posiada {Nieobecn} nieobecności, średnia ocen wynosi {round(Ocena,2)}\n")
file.write(f"Przewidywana ocena studenta to: {PrzewidywanaOcena}")

file.close()
