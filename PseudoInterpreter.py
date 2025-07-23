import re
import sys

class PseudoInterpreter:
    def __init__(self,filename=""):
        self.filename=filename
        self.codeLines = []
        self.context = {}
        self.functions = {}
        self.indent = "    "
        self.currentIndent = 0
        self.esSubproceso = False
        self.SubprocesoActual = ""
        self.typesMap = {
            "entero": "int",
            "real": "float",
            "caracter": "str",
            "cadena": "str",
            "logico": "bool"
        }
        self.neutralValues = {
            "int": 0,
            "float": 0.0,
            "str": "''",
            "bool": False
        }
        self.iniciaSubprocesos()

    def parseSubproceso(self,line):
        line = line.strip()
        match line:
            case _ if not line:
                return 
            
            case _ if line.startswith("Subproceso"):
                self.Subproceso(line)

            case "FinSubproceso":
                self.FinSubproceso(line)
            
            case _:
                self.SaltarLinea(line)


    def parseLine(self, line):
        line = line.strip()
        match line:
            case _ if not line:
                return 
            
            case _ if line.startswith("//"):
                self.Comentario(line)
            
            case _ if line.startswith("Algoritmo"):
                self.Algoritmo(line)

            case "Inicio":
                self.Inicio(line)
            
            case "Fin":
                self.Fin(line)
            
            case _ if line.startswith("Subproceso"):
                self.Subproceso(line)

            case "FinSubproceso":
                self.FinSubproceso(line)

            case _ if line.startswith("Definir"):
                self.Definir(line)
            
            case _ if line.startswith("Hacer"):
                self.Hacer(line)

            case _ if line.startswith("Llamar"):
                self.Llamar(line)

            case _:
                self.NoReconocido(line)


    def Algoritmo(self,line):
        if line.split()[1].isidentifier() and self._isCamelCase(line.split()[1]):
            self.mainName = line.split()[1]
        else:
            self.mainName = "main"        
        return
    
    def Inicio(self,line):
        line += ""
        self.codeLines.append(f"def {self.mainName}():")
        self.currentIndent += 1
        return
    
    def Fin(self,line):
        line += ""
        self.currentIndent -= 1
        self.codeLines.append("")
        return
    
    def Comentario(self,line):
        self.codeLines.append(line.replace("//", "# "))
        return
    
    def Subproceso(self,line):
        patron = r"Subproceso\s+(\w+)\((.*?)\)(\s*:\s*(\w+))?"
        match = re.match(patron, line)
        if not match:
            self.codeLines.append("# Error al procesar Subproceso")
            return
        nombre = match.group(1)
        parametros = match.group(2)
        tipoRetorno = match.group(4)

        paramList = []
        if parametros:
            for p in parametros.split(","):
                nombreParam, tipoParam = p.strip().split(":")
                tipoParam = self.typesMap.get(tipoParam.strip(), "Any")
                paramList.append(f"{nombreParam.strip()}: {tipoParam}")

        self.functions[nombre] = {k.strip(): v.strip() for k, v in (item.split(':') for item in paramList)}
        
        if paramList:
            if not tipoRetorno:
                paramList += ['context: dict']

        defLine = f"def {nombre}({', '.join(paramList)})"
        if tipoRetorno:
            tipoPy = self.typesMap.get(tipoRetorno.strip(), "Any")
            defLine += f" -> {tipoPy}"

        defLine += ":"
        self.codeLines.append(defLine)
        self.currentIndent += 1
        self.esSubproceso = True
        self.SubprocesoActual = nombre
        return
    
    def FinSubproceso(self,line):
        line += ""
        self.codeLines.append("")
        self.currentIndent -= 1
        self.esSubproceso = False
        self.SubprocesoActual = ""
        return
    
    def Definir(self,line):
        patron = r"Definir (.+) *: *(\w+)"
        match = re.match(patron, line)
        if not match:
            self.codeLines.append(f"{self.indent * self.currentIndent}# Error al procesar Definir")
            return
        nombreVariables, tipoVariables = match.groups()
        tipoVariables = tipoVariables.strip().lower()
        valorInicial = self.neutralValues.get(self.typesMap.get(tipoVariables), "None")
        variables = [v.strip() for v in nombreVariables.split(",")]
        for var in variables:
            if "[" in var:
                nombre = var.split("[")[0]
                dims = list(map(int, re.findall(r"\[(\d+)\]", var)))
                init = valorInicial
                for dim in reversed(dims):
                    init = f"[{init} for _ in range({dim})]"
                self.context[nombre] = eval(init)
                self.codeLines.append(f"{self.indent * self.currentIndent}context['{nombre}'] = {init}")
            else:
                self.context[var] = valorInicial
                self.codeLines.append(f"{self.indent * self.currentIndent}context['{var}'] = {valorInicial}")
        return
    
    def Hacer(self,line):
        patron = r"Hacer (.+) *= *(.*)"
        match = re.match(patron, line)
        if not match:
            self.codeLines.append(f"{self.indent * self.currentIndent}# Error al procesar Hacer")
            return
        var_expr, expr = match.groups()
        var_expr = var_expr.strip()
        expr = expr.strip()
        
        expr = self._convertExpression(expr)
        # Detecta si es acceso tipo a[i][j]
        if "[" in var_expr and "]" in var_expr:
            arreglo = var_expr.split("[")[0].strip()
            indices = re.findall(r"\[(.*?)\]", var_expr)
            acceso = f"context['{arreglo}']"
            for idx in indices:
                idx = idx.strip()
                if idx.isdigit():
                    acceso += f"[{idx}]"
                else:
                    acceso += f"[context['{idx}']]"
            self.codeLines.append(f"{self.indent * self.currentIndent}{acceso} = {expr}")
        else:
            # Variable 
            self.codeLines.append(f"{self.indent * self.currentIndent}context['{var_expr}'] = {expr}")
        return

    def Llamar(self,line):
        m = re.match(r"Llamar (\w+)\((.*)\)", line)
        if m:
            func, args = m.groups()
            args = [a.strip() for a in args.split(",") if a.strip()]
            param_names = self.functions.get(func, None)
            print(param_names)
            if not param_names:
                self.codeLines.append(f"{self.indent * self.currentIndent}{line}")
                return
            print(args)
            for param, arg in zip(param_names, args):
                expr = self._convertExpression(arg)
                #self.codeLines.append(f"{self.indent * self.currentIndent}context['{param}'] = {expr}")

            self.codeLines.append(f"{self.indent * self.currentIndent}{func}({", ".join(args)}, context)")
            return
        return
    
    def NoReconocido(self,line):
        self.codeLines.append(f"{self.indent * self.currentIndent}# No procesado: {line}")
        return
    
    def SaltarLinea(self,line):
        self.codeLines.append(f"{self.indent * self.currentIndent}{line}")
        return

    def _isCamelCase(self, identifier):
        return bool(re.fullmatch(r'[a-z]+(?:[A-Z][a-z0-9]*)*', identifier))

    
    def _convertExpression(self, expr):
        expr = expr.strip()
        expr = expr.replace("^","**")

        patron = r"""
            '[^']*'             |   # comillas simples
            "[^"]*"             |   # comillas dobles
            \b\d+\.\d+\b        |   # flotantes tipo 10.00
            \b\d+\.\b           |   # flotantes tipo 5.
            \b\.\d+\b           |   # flotantes tipo .5
            \b\d+\b             |   # enteros
            \bVerdadero\b       |   # booleano True
            \bFalso\b               # booleano False
        """

        
        # Extraer cadenas literales y reemplazarlas por tokens

        string_literals = re.findall(patron, expr, re.VERBOSE)
        replacements = {}

        for i, lit in enumerate(string_literals):
            lit = lit.strip()
            # Detectar tipo
            if lit in ("True", "False"):
                key = f"__bool_{i}__"
            elif re.match(r'^\d+\.\d+$|^\.\d+$|^\d+\.$', lit):  # flotante
                key = f"__float_{i}__"
            elif re.match(r'^\d+$', lit):  # entero
                key = f"__int_{i}__"
            else:  # cadena
                key = f"__str_{i}__"
            replacements[key] = lit
        
        def replace_literal(match):
            texto = match.group(0)
            for key, val in replacements.items():
                if val == texto:
                    return key
            return texto  # fallback (por si no se encuentra)

        expr = re.sub(patron, replace_literal, expr, flags=re.VERBOSE)
        # Reemplazar variables por context['var']
        tokens = re.findall(r"\b\w+(?:\[\w+(?:\[\w+\])?\])?\b", expr)
        for t in sorted(set(tokens), key=len, reverse=True):
            if t in replacements:
                continue
            expr = re.sub(rf'\b{re.escape(t)}\b', f"{t}", expr)

                

        # Restaurar cadenas literales
        for key, val in replacements.items():
            expr = expr.replace(key, val)


        return expr

    def iniciaSubprocesos(self):
        with open(self.filename, 'r') as f:
            for line in f:
                self.parseSubproceso(line)
        return

    def run(self):
        with open(self.filename, 'r') as f:
            for line in f:
                self.parseLine(line)


        fullCode = "\n".join(self.codeLines)
        print("===== Código generado =====")
        print(fullCode)

        #for k,v in self.context.items():
        #    print(k,v)
        
        for k,v in self.functions.items():
            print(k,v)
        #execEnv = {}
        #exec(fullCode, execEnv)
        #if self.mainName:
        #    execEnv[self.mainName]()


if __name__ == '__main__':
    #if len(sys.argv) < 2:
    #    print("Uso: python interpreter.py archivo.psc")
    #    sys.exit(1)

    archivo = 'ejemplos/ejemplo.psc'#sys.argv[1]
    pi = PseudoInterpreter(archivo)
    pi.run()