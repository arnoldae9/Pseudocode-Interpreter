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
