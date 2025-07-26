// SPDX-License-Identifier: AGPL-3.0-or-later
//
// File: 04-doWhile.psc
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

// Do ... While 
Algoritmo menuEjemplo
Inicio
    Definir opcion : caracter

    Repetir
        Escribir "----- MENÚ -----"
        Escribir "a) Saludar"
        Escribir "b) Mostrar hora"
        Escribir "c) Salir"
        Escribir "Elige una opción: "
        Leer opcion

        Segun opcion
            Caso 'a'
                Escribir "¡Hola, usuario!"
            Caso 'b'
                Escribir "La hora actual no está disponible en pseudocódigo."
            Caso 'c'
                Escribir "Saliendo del menú..."
            De Otro Modo
                Escribir "Opción no válida. Intenta de nuevo."
        FinSegun
    Hasta Que opcion = 'c'
Fin
