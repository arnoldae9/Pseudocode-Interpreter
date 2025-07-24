//Ejemplo completo

Algoritmo sistemaNotas

Inicio
    Definir nombres[3] : cadena
    Definir calificaciones[3][2] : real
    Definir promedios[3] : real
    Definir aprobados : entero
    Definir continuar : logico
    Definir opcion : caracter

    Hacer aprobados = 0

    Para i = 0 Hasta 2 Hacer
        Escribir "Nombre del estudiante ", i , ": "
        Leer nombres[i]

        Para j = 0 Hasta 1 Hacer
            Escribir "Calificación ", j , " de ", nombres[i], ": "
            Leer calificaciones[i][j]
        FinPara

        Llamar calcularPromedio(nombres[i], calificaciones[i][0], calificaciones[i][1], promedios, i)

        Si promedios[i] >= 6.0 Entonces
            Escribir nombres[i], " ha aprobado con promedio de ", promedios[i]
            Hacer aprobados = aprobados + 1
        Sino
            Escribir nombres[i], " ha reprobado con promedio de ", promedios[i]
        FinSi
    FinPara

    Escribir "Total de aprobados: ", aprobados

    Repetir
        Escribir "¿Deseas consultar un promedio? (s/n): "
        Leer opcion

        Segun opcion
            Caso 's'
                Definir idx : entero
                Escribir "Ingresa el índice del estudiante (0 a 2): "
                Leer idx
                Si idx < 0 O idx > 2 Entonces
                    Escribir "Índice no válido."
                Sino
                    Escribir "El promedio de ", nombres[idx], " es ", promedios[idx]
                FinSi
            Caso 'n'
                Escribir "Consulta finalizada."
            De Otro Modo
                Escribir "Opción no válida. Intenta de nuevo."
        FinSegun
    Hasta Que opcion == 'n'
Fin

Subproceso calcularPromedio(nombre : cadena, n1 : real, n2 : real, promedios : real, pos : entero)
    Definir promedio : real
    Hacer promedio = (n1 + n2) / 2
    Hacer promedios[pos] = promedio
    Escribir "Promedio de ", nombre, ": ", promedio
FinSubproceso