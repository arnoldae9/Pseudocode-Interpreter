# Archivo generado automáticamente desde pseudocódigo

context = {
    'coefA': None,
    'coefB': None,
    'coefC': None,
    'discriminante': None,
    'x1': None,
    'x2': None,
    'xReal': None,
    'xImaginaria': None,
    'haySolucionReal': None,
}

#  Cálculo de raíces usando la fórmula general
def formulaGeneral():
    context['coefA'] = 0.0
    context['coefB'] = 0.0
    context['coefC'] = 0.0
    context['discriminante'] = 0.0
    context['x1'] = 0.0
    context['x2'] = 0.0
    context['xReal'] = 0.0
    context['xImaginaria'] = 0.0
    context['haySolucionReal'] = False
    print("Ingrese el valor de a:", sep='')
    context['coefA'] = float(input())
    print("Ingrese el valor de b:", sep='')
    context['coefB'] = float(input())
    print("Ingrese el valor de c:", sep='')
    context['coefC'] = float(input())
    context['discriminante'] = calcularDiscriminante(context['coefA'], context['coefB'], context['coefC'])
    if context['discriminante'] > 0:
        context['haySolucionReal'] = True
        calcularRaicesDiferentes(context['coefA'], context['coefB'], context['discriminante'], context)
        print("Raíces reales y diferentes:", sep='')
        print("x1 = ", context['x1'], sep='')
        print("x2 = ", context['x2'], sep='')
    else:
        if context['discriminante'] == 0:
            context['haySolucionReal'] = True
            calcularRaizDoble(context['coefA'], context['coefB'], context)
            print("Raíz doble real:", sep='')
            print("x = ", context['x1'], sep='')
        else:
            context['haySolucionReal'] = False
            calcularRaicesImaginarias(context['coefA'], context['coefB'], context['discriminante'], context)
            print("Raíces complejas conjugadas:", sep='')
            print("x1 = ", context['xReal'], " + ", context['xImaginaria'], "i", sep='')
            print("x2 = ", context['xReal'], " - ", context['xImaginaria'], "i", sep='')

def calcularDiscriminante(a: float, b: float, c: float) -> float:
    return b**2 - 4 * a * c

def calcularRaicesDiferentes(a: float, b: float, d: float, context: dict):
    context['x1'] = (-b + d**0.5) / (2 * a)
    context['x2'] = (-b - d**0.5) / (2 * a)

def calcularRaizDoble(a: float, b: float, context: dict):
    context['x1'] = -b / (2 * a)

def calcularRaicesImaginarias(a: float, b: float, d: float, context: dict):
    context['xReal'] = -b / (2 * a)
    context['xImaginaria'] = valorAbsoluto(d) ** 0.5 / (2 * a)

def valorAbsoluto(x: float) -> float:
    if x < 0:
        return -x
    else:
        return x


if __name__ == '__main__':
    formulaGeneral()
