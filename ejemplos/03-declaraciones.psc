// SPDX-License-Identifier: AGPL-3.0-or-later
//
// File: 03-declaraciones.psc
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

//Codigo PruebaGeneral

Algoritmo pruebaGeneral

Inicio
    Definir a, b : entero
    Definir x : real
    Definir ok : logico
    Escribir "Ingresa a:"
    Leer a
    Escribir "Ingresa a:"
    Leer b
    Hacer x = a ^ 2 + b ^ 2
    Escribir "Resultado: ", x
    Hacer ok = (x>10)
    Si ok Entonces
        Escribir "Es mayor que diez"
    Sino
        Escribir "No es mayor que diez"
    FinSi
Fin
