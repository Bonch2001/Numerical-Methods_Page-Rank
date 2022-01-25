"""
Page Rank

Colocviu la Metode Numerice

Baciu George Cosmin si Bonciu Alin

Grupa 323AC

26 februarie 2022

"""

import numpy as np
from graphviz import Digraph

# functie ce implementeaza metoda puterii, algoritm folosit la calculul vectorului propriu corespunzator valorii proprii dominante
def metoda_puterii(A, tol, maxiter):
    err = []
    y = np.transpose(A[0])
    y = y / np.linalg.norm(y)
    i = 0
    e = 1
    while (e > tol):
        if i > maxiter:
            print(
                "S-a atins numarul maxim de iteratii fara a se fi obtinut nivelul prescris al tolerantei")
            break
        z = np.dot(A, y)
        z = z / np.linalg.norm(z)
        e = np.abs(1 - np.abs(np.dot(np.transpose(z), y)))
        err.append(e)
        y = z
        i = i + 1
    return y, err, i

# functie ce ne creeaza o matrice de adiacenta, populata asimetric cu valori de 0 si 1
def creare_matrice(n):
    sw = 0
    while(sw == 0):
        sw = 1
        A = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                A[i][j] = np.random.choice([0, 1])
            A[i][i] = 0
        """         
        A = [[0, 0, 0, 0, 1, 0],
        [1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [1, 1, 0, 0, 1, 0],
        [1, 0, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0]]  
        """
        """
        Pagina 1 poate fi accesata direct doar de pagina 5 si poate accesa direct paginile 2, 4, 5 si 6.
        Pagina 2 poate fi accesata direct doar de pagina 1 si poate accesa direct paginile 3 si 4.
        .
        .
        .
        La modul general: 
        Pagina x poate fi accesata de paginile avand ca numar indicele de coloana corespunzator valorilor de 1 pe linia x
        Pagina y poate accesa paginile avand ca numar indicele de linie corespunzator valorilor de 1 de pe coloana y.
        """
        # cream un graph pentru a putea vizualiza mai usor legaturile dintre pagini
        dot = Digraph()
        for i in range(n):
            dot.node('{}'.format(i+1), 'Webpage {}'.format(i+1))
        links = []
        for i in range(n):
            for j in range(n):
                if (A[i][j] == 1):
                    links.append('{}{}'.format(j+1, i+1))
        dot.edges(links)
        B = np.zeros((n, n))
        sum_list = []
        for i in range(n):
            s = 0
            p = 0
            for j in range(n):
                s = s + A[j][i]
                p = p + A[i][j]
            if (s == 0 or p == 0):
                sw = 0
            for j in range(n):
                if (s == 0):
                    B[j][i] = A[j][i]
                else:
                    B[j][i] = A[j][i] / s
            sum_list.append(s)
            """         for i in range(n-1):
            for j in range(i+1, n):
                if (sum_list[i] == sum_list[j]):
                    sw = 0 """
    return A, B, dot

# aplicatia propriu-zisa
n = 6

A, B, dot = creare_matrice(n)
print("Matricea A:\n", A, '\n')
print("Matricea A prelucrata:\n", B, '\n')
# Matricea corespunzatoare probabilitatilor pe care o pagina le are ca sa fie accesata de alta.
print(dot.source)
dot.render(view=True)

[y, e, it] = metoda_puterii(B, 0.0001, 1000)
lambda1 = (np.transpose(y) @ B @ y) / (np.transpose(y) @ y)
print("Valori calculate folosind metoda puterii:", "\nValoare proprie: ",
      lambda1, "\nVector propriu: ", y / np.linalg.norm(y))

""" 
valori_proprii, vectori_proprii = np.linalg.eig(B)
val_max = valori_proprii[n-1].real
for i in range(n-1):
    if(valori_proprii[i].real > val_max):
        val_max = valori_proprii[i].real
for i in range(n):
    if(val_max == valori_proprii[i].real):
        pozitia = i
print("\nValori calculate folosind functia din numpy:", "\nValoare proprie: ",
      valori_proprii[pozitia].real, "\nVector propriu: ", vectori_proprii[pozitia] / np.linalg.norm(vectori_proprii[pozitia]))
"""

v_max = y[n-1]
poz = n
for i in range(n-1):
    if(y[i] > v_max):
        v_max = y[i]
for i in range(n):
    if(v_max == y[i]):
        poz = i
print("Pagina la care se face referire cel mai mult este Webpage {}".format(poz+1))
