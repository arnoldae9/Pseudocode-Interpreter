// Cálculo de raíces usando la fórmula general
Algoritmo formulaGeneral

Inicio
    Definir a, b, c, discriminante, x1, x2, xReal, xImaginaria : real
    Definir haySolucionReal : logico

    Escribir "Ingrese el valor de a:"
    Leer a
    Escribir "Ingrese el valor de b:"
    Leer b
    Escribir "Ingrese el valor de c:"
    Leer c

    Hacer discriminante = calcularDiscriminante(a, b, c)

    Si discriminante > 0 Entonces
        Hacer haySolucionReal = Verdadero
        Llamar calcularRaicesDiferentes(a, b, discriminante, x1, x2)
        Escribir "Raíces reales y diferentes:"
        Escribir "x1 = ", x1
        Escribir "x2 = ", x2

    Sino
        Si discriminante == 0 Entonces
            Hacer haySolucionReal = Verdadero
            Llamar calcularRaizDoble(a, b, x1)
            Escribir "Raíz doble real:"
            Escribir "x = ", x1
        Sino
            Hacer haySolucionReal = Falso
            Llamar calcularRaicesImaginarias(a, b, discriminante, xReal, xImaginaria)
            Escribir "Raíces complejas conjugadas:"
            Escribir "x1 = ", xReal, " + ", xImaginaria, "i"
            Escribir "x2 = ", xReal, " - ", xImaginaria, "i"
        FinSi
    FinSi
Fin

Subproceso calcularDiscriminante(a : real, b : real, c : real) : real
    Regresar b^2 - 4 * a * c
FinSubproceso

Subproceso calcularRaicesDiferentes(a : real, b : real, discriminante : real, x1 : real, x2 : real)
    Hacer x1 = (-b + discriminante^0.5) / (2 * a)
    Hacer x2 = (-b - discriminante^0.5) / (2 * a)
FinSubproceso

Subproceso calcularRaizDoble(a : real, b : real, x1 : real)
    Hacer x1 = -b / (2 * a)
FinSubproceso

Subproceso calcularRaicesImaginarias(a : real, b : real, discriminante : real, xReal : real, xImaginaria : real)
    Hacer xReal = -b / (2 * a)
    Hacer xImaginaria = valorAbsoluto(discriminante) ^ 0.5 / (2 * a)
FinSubproceso

Subproceso valorAbsoluto(discriminante : real) : real
    Si discriminante < 0 Entonces
        Regresar -discriminante
    Sino
        Regresar discriminante
    FinSi
FinSubproceso
