// SPDX-License-Identifier: AGPL-3.0-or-later
//
// File: 05-subprocesos.psc
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

// Ejemplo
Algoritmo pruebaDemo

Inicio
    Definir x, y, rubik[3][3][3] : entero
    Definir arreglo[3], tabla[2][3] : real
    Hacer x = 5 + 3
    Hacer y = suma(3,2) + 1
    Escribir "La suma es: ", y
    Hacer rubik[1][1][1] = 2
    Llamar pitagoras(3,4)
    Llamar holaMundo('Luis')
    Llamar noParams()
Fin
//Texto libre no válido
Subproceso suma(a : entero, b : entero) : entero
    Regresar a+b
FinSubproceso

Subproceso pitagoras(a : real, b : real)
    Definir c : real
    Hacer c = (a^2 + b^2)^(1/2)
    Escribir "La hipotenusa es: ", c
FinSubproceso

Subproceso holaMundo(nombre : cadena)
    Escribir "Hola Mundo, hola ", nombre
FinSubproceso

Subproceso noParams()
    Escribir "Sin parametros"
FinSubproceso