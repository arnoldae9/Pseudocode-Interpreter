// SPDX-License-Identifier: AGPL-3.0-or-later
//
// File: 06-ciclosArreglos.psc
// Author: Luis A. Gutierrez-Rodriguez
// License: GNU Affero General Public License version 3 or later
//
// This file is part of a project licensed under the AGPLv3.
// You may use, modify, and distribute this code under the terms of that license.
//
// This software is provided “AS IS”, without any warranty.
//
// For more information about the license, see:
// https://www.gnu.org/licenses/agpl-3.0.html

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
        Escribir " "
    FinPara
Fin
