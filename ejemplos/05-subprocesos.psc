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
