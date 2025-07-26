// SPDX-License-Identifier: AGPL-3.0-or-later
//
// File: 02-Segun.psc
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

// Switch
Algoritmo segunEjemplo
Inicio
    Definir opcion : entero
    Escribir "Introduce un número entre 1 y 3:"
    Leer opcion

    Segun opcion
        Caso 1
            Escribir "Elegiste UNO"
        Caso 2
            Escribir "Elegiste DOS"
        Caso 3
            Escribir "Elegiste TRES"
        De Otro Modo
            Escribir "Opción no válida"
    FinSegun
Fin
