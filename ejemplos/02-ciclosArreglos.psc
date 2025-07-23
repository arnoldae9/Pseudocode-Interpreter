// Ejemplo de arreglos
Algoritmo pruebaArreglos
Inicio

    Definir tabla[2][3] : entero
    Definir i, j : entero

// Llenar fila 0 usando Para
    Para j = 0 Hasta 2 Hacer
        Escribir "Ingrese valor para tabla[0][", j, "]:"
        Leer tabla[0][j]
    FinPara

// Llenar fila 1 usando Mientras
    Hacer i = 0
    Mientras i <= 2 Hacer
        Escribir "Ingrese valor para tabla[1][", i, "]:"
        Leer tabla[1][i]
        Hacer i = i + 1
    FinMientras

// Mostrar contenido del arreglo
    Para i = 0 Hasta 1 Hacer
        Para j = 0 Hasta 2 Hacer
            Escribir "tabla[", i, "][", j, "] = ", tabla[i][j]
        FinPara
    FinPara
Fin
