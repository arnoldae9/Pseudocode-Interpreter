// SPDX-License-Identifier: AGPL-3.0-or-later
//
// File: 00-moduloDivisionEntera.psc
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


Algoritmo modulo
Inicio
    Definir a,b : entero
    Hacer a = 10 // 3
    Hacer b = 5 % 3
    Escribir "El división entera es: ", a
    Escribir "El módulo es: ", b
    Llamar holaMundo()
Fin

Subproceso holaMundo()
    Escribir "Hola mundo"
FinSubproceso
