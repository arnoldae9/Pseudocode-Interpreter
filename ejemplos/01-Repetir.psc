// SPDX-License-Identifier: AGPL-3.0-or-later
//
// File: 01-Repetir.psc
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

//While
Algoritmo repetirEjemplo
Inicio
    Definir n : entero
    Repetir
        Escribir "Introduce un número positivo: "
        Leer n
        Escribir "Número ingresado: ", n
    Hasta Que n < 0
Fin
