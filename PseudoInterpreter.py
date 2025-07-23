import re
import sys

class PseudoInterpreter:
    def __init__(self,filename=""):
        self.filename=filename
        self.codeLines = []
        self.context = {}
        self.contextTypes = {}
        self.functions = {}
        self.indent = "    "
        self.currentIndent = 0
        self.esSubproceso = False
        self.SubprocesoActual = ""
        self.SegunVar = None
        self.EnSegun = False
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

            case _ if line.startswith("Regresar"):
                self.Regresar(line)

            case _ if line.startswith("Escribir"):
                self.Escribir(line)

            case _ if line.startswith("Leer"):
                self.Leer(line)

            case _ if line.startswith("Si"):
                self.Si(line)
            
            case "Sino":
                self.Sino(line)

            case "FinSi":
                self.FinSi(line)

            case _ if line.startswith("Segun"):
                self.Segun(line)

            case _ if line.startswith("Caso"):
                self.Caso(line)

            case "De Otro Modo":
                self.DeOtroModo(line)

            case "FinSegun":
                self.FinSegun(line)

            case _ if line.startswith("Para"):
                self.Para(line)

            case "FinPara":
                self.FinPara(line)

            case _ if line.startswith("Mientras"):
                self.Mientras(line)

            case "FinMientras":
                self.FinMientras(line)

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
                self.contextTypes[nombre] = self.typesMap.get(tipoVariables)
                self.codeLines.append(f"{self.indent * self.currentIndent}context['{nombre}'] = {init}")
            else:
                self.context[var] = valorInicial
                self.contextTypes[var] = self.typesMap.get(tipoVariables)
                self.codeLines.append(f"{self.indent * self.currentIndent}context['{var}'] = {valorInicial}")
            

        return
    
    def Hacer(self, line):
        patron = r"Hacer (.+) *= *(.*)"
        match = re.match(patron, line)
        if not match:
            self.codeLines.append(f"{self.indent * self.currentIndent}# Error al procesar Hacer")
            return
        varExpr, expr = match.groups()
        varExpr = varExpr.strip()
        expr = expr.strip()

        expr = self._convertExpression(expr)

        # 👉 Acceso tipo arreglo a[i][j]
        if "[" in varExpr and "]" in varExpr:
            arreglo = varExpr.split("[")[0].strip()
            indices = re.findall(r"\[(.*?)\]", varExpr)
            acceso = f"context['{arreglo}']"
            for idx in indices:
                idx = idx.strip()
                if idx.isdigit():
                    acceso += f"[{idx}]"
                else:
                    acceso += f"[context['{idx}']]"
            self.codeLines.append(f"{self.indent * self.currentIndent}{acceso} = {expr}")
        else:
            # 👉 Variable normal: decide si va en context o no
            if varExpr in self.context:
                self.codeLines.append(f"{self.indent * self.currentIndent}context['{varExpr}'] = {expr}")
            else:
                self.codeLines.append(f"{self.indent * self.currentIndent}{varExpr} = {expr}")


    def Llamar(self,line):
        m = re.match(r"Llamar (\w+)\((.*)\)", line)
        if m:
            func, args = m.groups()
            args = [a.strip() for a in args.split(",") if a.strip()]
            paramNames = self.functions.get(func, None)
            #print(paramNames)
            if not paramNames:
                self.codeLines.append(f"{self.indent * self.currentIndent}{line}")
                return

            self.codeLines.append(f"{self.indent * self.currentIndent}{func}({", ".join(args)}, context)")
            return
        return
    
    def Regresar(self,line):
        m = re.match(r"Regresar (.+)", line)
        if m:
            expr = self._convertExpression(m.group(1))
            self.codeLines.append(f"{self.indent * self.currentIndent}return {expr}")
            return
        
    def Escribir(self, line):
        m = re.match(r"Escribir\s+(.+)", line)
        if not m:
            self.codeLines.append(f"{self.indent * self.currentIndent}# Error al procesar Escribir")
            return

        texto = m.group(1).strip()
        partes = []
        actual = ""
        en_cadena = False
        comilla_actual = ""

        # 👉 Separación segura por comas respetando comillas
        for c in texto:
            if c in ['"', "'"]:
                if not en_cadena:
                    en_cadena = True
                    comilla_actual = c
                    actual += c
                elif c == comilla_actual:
                    en_cadena = False
                    actual += c
                else:
                    actual += c
            elif c == ',' and not en_cadena:
                partes.append(actual.strip())
                actual = ""
            else:
                actual += c
        if actual:
            partes.append(actual.strip())

        traducidas = []
        for parte in partes:
            parte = parte.strip()

            # 👉 Cadena literal
            if (parte.startswith('"') and parte.endswith('"')) or (parte.startswith("'") and parte.endswith("'")):
                traducidas.append(parte)

            # 👉 Acceso tipo arreglo tabla[i][j]
            elif "[" in parte and "]" in parte:
                arreglo = parte.split("[")[0]
                indices = re.findall(r"\[(.*?)\]", parte)
                if self.esSubproceso:
                    acceso = arreglo
                else:
                    acceso = f"context['{arreglo}']"
                for idx in indices:
                    idx = idx.strip()
                    if idx.isdigit():
                        acceso += f"[{idx}]"
                    else:
                        if self.esSubproceso:
                            params = self.functions.get(self.subprocesoActual, {})
                            if idx in params:
                                acceso += f"[{idx}]"
                            else:
                                acceso += f"[context['{idx}']]"
                        else:
                            acceso += f"[context['{idx}']]"
                traducidas.append(acceso)

            # 👉 Variable simple
            elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', parte):
                if self.esSubproceso:
                    params = self.functions.get(self.SubprocesoActual, {})
                    if parte in params:
                        traducidas.append(parte)
                    else:
                        traducidas.append(f"context['{parte}']")
                else:
                    traducidas.append(f"context['{parte}']")

            # 👉 Número literal
            elif parte.isdigit():
                traducidas.append(parte)

            # 👉 Texto plano como fallback
            else:
                traducidas.append(f"'{parte}'")

        self.codeLines.append(f"{self.indent * self.currentIndent}print({', '.join(traducidas)}, sep='')")

    def Leer(self,line):
        m = re.match(r"Leer\s+(.+)", line)
        if m:
            variables_a_leer = [v.strip() for v in m.group(1).split(",")]
            for var_expr in variables_a_leer:
                # Acceso a arreglo
                if "[" in var_expr and "]" in var_expr:
                    arreglo = var_expr.split("[")[0]
                    indices = re.findall(r"\[(.*?)\]", var_expr)
                    acceso = f"context['{arreglo}']"
                    for idx in indices:
                        idx = idx.strip()
                        if idx.isdigit():
                            acceso += f"[{idx}]"
                        else:
                            acceso += f"[context['{idx}']]"
                    tipo = self.contextTypes.get(arreglo, "str").lower()
                    if tipo == "float":
                        self.codeLines.append(f"{self.indent * self.currentIndent}{acceso} = float(input())")
                    elif tipo == "int":
                        self.codeLines.append(f"{self.indent * self.currentIndent}{acceso} = int(input())")
                    elif tipo == "bool":
                        self.codeLines.append(f"{self.indent * self.currentIndent}{acceso} = input().strip().lower() in ['verdadero', 'true']")
                    else:
                        self.codeLines.append(f"{self.indent * self.currentIndent}{acceso} = input()")

                # Variable simple
                else:
                    var = var_expr
                    tipo = self.contextTypes.get(var, "str").lower()
                    if tipo == "float":
                        self.codeLines.append(f"{self.indent * self.currentIndent}context['{var}'] = float(input())")
                    elif tipo == "int":
                        self.codeLines.append(f"{self.indent * self.currentIndent}context['{var}'] = int(input())")
                    elif tipo == "bool":
                        self.codeLines.append(f"{self.indent * self.currentIndent}context['{var}'] = input().strip().lower() in ['verdadero', 'true']")
                    else:
                        self.codeLines.append(f"{self.indent * self.currentIndent}context['{var}'] = input()")
            return

    def Si(self,line):
        m = re.match(r"Si (.+) Entonces", line)
        if m:
            cond = self._convertCondition(m.group(1))
            self.codeLines.append(f"{self.indent()}if {cond}:")
            self.currentIndent += 1
            return

    def Sino(self,line):
        if line == "Sino":
            self.currentIndent -= 1
            self.codeLines.append(f"{self.indent()}else:")
            self.currentIndent += 1
            return

    def FinSi(self,line):
        if line == "FinSi":
            self.currentIndent -= 1
            return
        
    def Segun(self, line):
        m = re.match(r"Segun (.+)", line)
        if m:
            self.SegunVar = self._convertExpression(m.group(1))
            self.EnSegun = False
            return

    def Caso(self, line):
        m = re.match(r"Caso (.+)", line)
        if m:
            val = m.group(1).strip()
            cond = f"{self.SegunVar} == {val}"

            if not self.EnSegun:
                self.codeLines.append(f"{self.indent * self.currentIndent}if {cond}:")
                self.EnSegun = True
            else:
                self.currentIndent -= 1  # 👈 cerrar bloque anterior
                self.codeLines.append(f"{self.indent * self.currentIndent}elif {cond}:")
            self.currentIndent += 1
            return

    def DeOtroModo(self, line):
        if line.strip() == "De Otro Modo":
            self.currentIndent -= 1  # 👈 cerrar bloque anterior
            self.codeLines.append(f"{self.indent * self.currentIndent}else:")
            self.currentIndent += 1
            return

    def FinSegun(self, line):
        if line.strip() == "FinSegun":
            self.currentIndent -= 1
            self.SegunVar = None
            self.EnSegun = False
            return

    def Para(self, line):
        m = re.match(r"Para (\w+) *= *(.+) Hasta (.+) Hacer", line)
        if m:
            var, inicio, fin = m.groups()
            inicio = self._convertExpression(inicio.strip())
            fin = self._convertExpression(fin.strip())
            self.codeLines.append(f"{self.indent * self.currentIndent}for context['{var}'] in range({inicio}, {fin} + 1):")
            self.currentIndent += 1
            return

    
    def FinPara(self,line):
        if line == "FinPara":
            self.currentIndent -= 1
            self.codeLines.append("")
            return

    def Mientras(self,line):
        m = re.match(r"Mientras (.+) Hacer", line)
        if m:
            cond = self._convertCondition(m.group(1))
            self.codeLines.append(f"{self.indent * self.currentIndent}while {cond}:")
            self.currentIndent += 1
            return

    def FinMientras(self,line):
        if line == "FinMientras":
            self.currentIndent -= 1
            self.codeLines.append("")
            return
    
    def NoReconocido(self,line):
        self.codeLines.append(f"{self.indent * self.currentIndent}# No procesado: {line}")
        return
    
    def SaltarLinea(self,line):
        self.codeLines.append(f"{self.indent * self.currentIndent}{line}")
        return

    def _isCamelCase(self, identifier):
        return bool(re.fullmatch(r'[a-z]+(?:[A-Z][a-z0-9]*)*', identifier))
    
    def _convertCondition(self, cond):
        cond = cond.replace(" Y ", " and ").replace(" O ", " or ").replace("NO ", "not ")

        # Preservar cadenas de texto (entre comillas simples o dobles)
        string_literals = re.findall(r"'[^']*'|\"[^\"]*\"", cond)
        replacements = {}
        for i, lit in enumerate(string_literals):
            key = f"__str_{i}__"
            replacements[key] = lit
            cond = cond.replace(lit, key)

        cond = self._convertExpression(cond)
        cond = re.sub(r"(?<![=!<>])=(?!=)", "==", cond)  # convierte = a == donde corresponde

        # Restaurar strings
        for key, val in replacements.items():
            cond = cond.replace(key, val)

        return cond

    
    def _convertExpression(self, expr):
        expr = expr.strip()
        expr = expr.replace("^", "**")

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

        # Extraer y reemplazar literales por tokens temporales
        stringLiterals = re.findall(patron, expr, re.VERBOSE)
        replacements = {}

        for i, lit in enumerate(stringLiterals):
            lit = lit.strip()
            if lit in ("Verdadero", "Falso"):
                key = f"__bool_{i}__"
            elif re.match(r'^\d+\.\d+$|^\.\d+$|^\d+\.$', lit):  # flotante
                key = f"__float_{i}__"
            elif re.match(r'^\d+$', lit):  # entero
                key = f"__int_{i}__"
            else:  # cadena
                key = f"__str_{i}__"
            replacements[key] = lit

        def replaceLiteral(match):
            texto = match.group(0)
            for key, val in replacements.items():
                if val == texto:
                    return key
            return texto

        expr = re.sub(patron, replaceLiteral, expr, flags=re.VERBOSE)

        # Buscar tokens que podrían ser variables (o funciones, etc.)
        tokens = re.findall(r"\b\w+\b", expr)
        for t in sorted(set(tokens), key=len, reverse=True):
            if t in replacements:
                continue
            if t in self.context:
                expr = re.sub(rf'\b{re.escape(t)}\b', f"context['{t}']", expr)

        # Restaurar literales
        for key, val in replacements.items():
            expr = expr.replace(key, val)

        # Reemplazar booleanos por equivalentes Python
        expr = expr.replace("Verdadero", "True")
        expr = expr.replace("Falso", "False")

        return expr


    def iniciaSubprocesos(self):
        with open(self.filename, 'r') as f:
            for line in f:
                self.parseSubproceso(line)
        return

    def run(self):
        self.codeLines.clear()
        with open(self.filename, 'r') as f:
            for line in f:
                self.parseLine(line)


        fullCode = "\n".join(self.codeLines)
        print("===== Código generado =====")
        print(fullCode)

        #for k,v in self.context.items():
        #    print(k,v)
        
        #for k,v in self.contextTypes.items():
        #    print(k,v)

        #for k,v in self.functions.items():
        #    print(k,v)
        #execEnv = {'context':self.context}
        #exec(fullCode, execEnv)
        #if self.mainName:
        #    execEnv[self.mainName]()


if __name__ == '__main__':
    #if len(sys.argv) < 2:
    #    print("Uso: python interpreter.py archivo.psc")
    #    sys.exit(1)

    archivo = 'ejemplos/03-segun.psc'#sys.argv[1]
    pi = PseudoInterpreter(archivo)
    pi.run()