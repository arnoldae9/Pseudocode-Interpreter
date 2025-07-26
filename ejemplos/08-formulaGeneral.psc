// SPDX-License-Identifier: AGPL-3.0-or-later
//
// File: 08-formulaGeneral.psc
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

// Cálculo de raíces usando la fórmula general
Algoritmo formulaGeneral

Inicio
    Definir coefA, coefB, coefC, discriminante, x1, x2, xReal, xImaginaria : real
    Definir haySolucionReal : logico

    Escribir "Ingrese el valor de a:"
    Leer coefA
    Escribir "Ingrese el valor de b:"
    Leer coefB
    Escribir "Ingrese el valor de c:"
    Leer coefC

    Hacer discriminante = calcularDiscriminante(coefA, coefB, coefC)

    Si discriminante > 0 Entonces
        Hacer haySolucionReal = Verdadero
        Llamar calcularRaicesDiferentes(coefA, coefB, discriminante)
        Escribir "Raíces reales y diferentes:"
        Escribir "x1 = ", x1
        Escribir "x2 = ", x2

    Sino
        Si discriminante == 0 Entonces
            Hacer haySolucionReal = Verdadero
            Llamar calcularRaizDoble(coefA, coefB)
            Escribir "Raíz doble real:"
            Escribir "x = ", x1
        Sino
            Hacer haySolucionReal = Falso
            Llamar calcularRaicesImaginarias(coefA, coefB, discriminante)
            Escribir "Raíces complejas conjugadas:"
            Escribir "x1 = ", xReal, " + ", xImaginaria, "i"
            Escribir "x2 = ", xReal, " - ", xImaginaria, "i"
        FinSi
    FinSi
Fin

Subproceso calcularDiscriminante(a : real, b : real, c : real) : real
    Regresar b^2 - 4 * a * c
FinSubproceso

Subproceso calcularRaicesDiferentes(a : real, b : real, d : real)
    Hacer x1 = (-b + d^0.5) / (2 * a)
    Hacer x2 = (-b - d^0.5) / (2 * a)
FinSubproceso

Subproceso calcularRaizDoble(a : real, b : real)
    Hacer x1 = -b / (2 * a)
FinSubproceso

Subproceso calcularRaicesImaginarias(a : real, b : real, d : real)
    Hacer xReal = -b / (2 * a)
    Hacer xImaginaria = valorAbsoluto(d) ^ 0.5 / (2 * a)
FinSubproceso

Subproceso valorAbsoluto(x : real) : real
    Si x < 0 Entonces
        Regresar -x
    Sino
        Regresar x
    FinSi
FinSubproceso
