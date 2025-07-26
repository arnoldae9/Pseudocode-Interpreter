# SPDX-License-Identifier: AGPL-3.0-or-later
#
# File: interprete.py
# Author: Luis Gutiérrez
# License: GNU Affero General Public License version 3 or later
#
# This file is part of a project licensed under the AGPLv3.
# You may use, modify, and distribute this code under the terms of that license.
#
# This software is provided “AS IS”, without any warranty.
#
# For more information about the license, see:
# https://www.gnu.org/licenses/agpl-3.0.html


import re
import argparse
import os

version_major = 1
version_minor = 30
version_patch = 5
beta = True

VERSION = f"{version_major}.{version_minor}.{version_patch}" + ("-beta" if beta else "")


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

            case _ if line.startswith("Si "):
                self.Si(line)
            
            case _ if line.startswith("Sino"):
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

            case "Repetir":
                self.Repetir(line)

            case _ if line.startswith("Hasta "):
                self.HastaQue(line)

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
        line = line.replace("//", "# ")
        self.codeLines.append(f"{self.indent * self.currentIndent}{line}")
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

        # Obtener parámetros actuales (o conjunto vacío si no estamos en un subproceso)
        parametrosActuales = set()
        if self.SubprocesoActual and self.SubprocesoActual in self.functions:
            parametrosActuales = set(self.functions[self.SubprocesoActual].keys())

        # 👉 Caso acceso tipo arreglo: promedios[pos]
        if "[" in varExpr and "]" in varExpr:
            arreglo = varExpr.split("[")[0].strip()
            indices = re.findall(r"\[(.*?)\]", varExpr)

            # El arreglo es parámetro o contexto
            if arreglo in parametrosActuales:
                acceso = arreglo
            else:
                acceso = f"context['{arreglo}']"

            for idx in indices:
                idx = idx.strip()
                if idx.isdigit() or idx in parametrosActuales:
                    acceso += f"[{idx}]"
                else:
                    acceso += f"[context['{idx}']]"

            self.codeLines.append(f"{self.indent * self.currentIndent}{acceso} = {expr}")

        else:
            # 👉 Variable normal: local (context) o parámetro
            if varExpr in parametrosActuales:
                self.codeLines.append(f"{self.indent * self.currentIndent}{varExpr} = {expr}")
            else:
                self.codeLines.append(f"{self.indent * self.currentIndent}context['{varExpr}'] = {expr}")




    def Llamar(self, line):
        m = re.match(r"Llamar (\w+)\((.*)\)", line)
        if m:
            func, args = m.groups()
            args = [a.strip() for a in args.split(",") if a.strip()]
            paramNames = self.functions.get(func, None)

            if not paramNames:
                self.codeLines.append(f"{self.indent * self.currentIndent}# No se encontró el subproceso {func}")
                return

            traducidos = []
            for arg in args:
                # Acceso tipo arreglo tabla[i][j]
                if "[" in arg and "]" in arg:
                    arreglo = arg.split("[")[0]
                    indices = re.findall(r"\[(.*?)\]", arg)
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
                    traducidos.append(acceso)

                # Variable simple
                elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', arg):
                    if self.esSubproceso:
                        params = self.functions.get(self.subprocesoActual, {})
                        if arg in params:
                            traducidos.append(arg)
                        else:
                            traducidos.append(f"context['{arg}']")
                    else:
                        traducidos.append(f"context['{arg}']")

                # Número o literal
                else:
                    traducidos.append(arg)

            self.codeLines.append(f"{self.indent * self.currentIndent}{func}({', '.join(traducidos)}, context)")

    
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
        enCadena = False
        comillaActual = ""

        # 👉 Separación segura por comas respetando comillas
        for c in texto:
            if c in ['"', "'"]:
                if not enCadena:
                    enCadena = True
                    comillaActual = c
                    actual += c
                elif c == comillaActual:
                    enCadena = False
                    actual += c
                else:
                    actual += c
            elif c == ',' and not enCadena:
                partes.append(actual.strip())
                actual = ""
            else:
                actual += c
        if actual:
            partes.append(actual.strip())

        def procesarExpresion(expr):
            # 👉 Si es número, retorna como está
            if expr.isdigit():
                return expr

            # 👉 Si es string literal, retorna como está
            if (expr.startswith('"') and expr.endswith('"')) or (expr.startswith("'") and expr.endswith("'")):
                return expr

            # 👉 Si es acceso tipo arreglo como nombres[i][j]
            if "[" in expr and "]" in expr:
                arreglo = expr.split("[")[0]
                indices = re.findall(r"\[(.*?)\]", expr)
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
                            params = self.functions.get(self.SubprocesoActual, {})
                            if idx in params:
                                acceso += f"[{idx}]"
                            else:
                                acceso += f"[context['{idx}']]"
                        else:
                            acceso += f"[context['{idx}']]"
                return acceso

            # 👉 Si es variable simple
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', expr):
                if self.esSubproceso:
                    params = self.functions.get(self.SubprocesoActual, {})
                    if expr in params:
                        return expr
                    else:
                        return f"context['{expr}']"
                else:
                    return f"context['{expr}']"

            # 👉 Si es expresión con operadores: reemplazar variables
            def reemplazarVar(m):
                var = m.group(0)
                if self.esSubproceso:
                    params = self.functions.get(self.SubprocesoActual, {})
                    if var in params:
                        return var
                return f"context['{var}']"

            # Solo reemplazar identificadores válidos
            return re.sub(r'\b[a-zA-Z_]\w*\b', reemplazarVar, expr)

        traducidas = [procesarExpresion(p.strip()) for p in partes]

        self.codeLines.append(f"{self.indent * self.currentIndent}print({', '.join(traducidas)}, sep='')")


    def Leer(self,line):
        m = re.match(r"Leer\s+(.+)", line)
        if m:
            variablesALeer = [v.strip() for v in m.group(1).split(",")]
            for varExpr in variablesALeer:
                # Acceso a arreglo
                if "[" in varExpr and "]" in varExpr:
                    arreglo = varExpr.split("[")[0]
                    indices = re.findall(r"\[(.*?)\]", varExpr)
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
                    var = varExpr
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

    def Si(self, line):
        m = re.match(r"Si (.+) Entonces", line)
        if m:
            #print(m.group(1))
            cond = self._convertCondition(m.group(1))
            #print(cond)
            self.codeLines.append(f"{self.indent * self.currentIndent}if {cond}:")
            self.currentIndent += 1
            return



    def Sino(self,line):
        if line == "Sino":
            self.currentIndent -= 1
            self.codeLines.append(f"{self.indent * self.currentIndent}else:")
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
        
    def Repetir(self, line):
        if line == "Repetir":
            self.codeLines.append(f"{self.indent * self.currentIndent}while True:")
            self.currentIndent += 1
            return

    def HastaQue(self, line):
        m = re.match(r"Hasta Que (.+)", line)
        if m:
            cond = self._convertCondition(m.group(1))
            self.codeLines.append(f"{self.indent * self.currentIndent}if {cond}:")
            self.currentIndent += 1
            self.codeLines.append(f"{self.indent * self.currentIndent}break")
            self.currentIndent -= 2  # Cierra el if y el while
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

        # Preservar cadenas de texto
        stringLiterals = re.findall(r"'[^']*'|\"[^\"]*\"", cond)
        replacements = {}
        for i, lit in enumerate(stringLiterals):
            key = f"__str_{i}__"
            replacements[key] = lit
            cond = cond.replace(lit, key)

        # Convertir expresión (variables simples)
        cond = self._convertExpression(cond)

        # --- NUEVO: procesar índices ---
        # Detecta cualquier cosa como context['var'][index] o similar
        def replaceIndex(match):
            var = match.group(1)
            index = match.group(2).strip()
            # Si el índice es un identificador (no un número ni ya envuelto en context)
            if re.fullmatch(r"[a-zA-Z_]\w*", index) and not index.startswith("context["):
                index = f"context['{index}']"
            return f"{var}[{index}]"

        cond = re.sub(r"(context\['\w+'\])\[(.*?)\]", replaceIndex, cond)

        # Variables simples aún no envueltas
        tokens = re.findall(r"\b[a-zA-Z_]\w*\b", cond)
        for token in tokens:
            if token in self.context:
                if not re.search(rf"context\[\s*['\"]{token}['\"]\s*\]", cond):
                    cond = re.sub(rf'\b{token}\b', f"context['{token}']", cond)

        # Reemplazar = por ==
        cond = re.sub(r"(?<![=!<>])=(?!=)", "==", cond)

        # Restaurar literales
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

        stringLiterals = re.findall(patron, expr, re.VERBOSE)
        replacements = {}

        for i, lit in enumerate(stringLiterals):
            lit = lit.strip()
            if lit in ("Verdadero", "Falso"):
                key = f"__bool_{i}__"
            elif re.match(r'^\d+\.\d+$|^\.\d+$|^\d+\.$', lit):
                key = f"__float_{i}__"
            elif re.match(r'^\d+$', lit):
                key = f"__int_{i}__"
            else:
                key = f"__str_{i}__"
            replacements[key] = lit

        def replaceLiteral(match):
            texto = match.group(0)
            for key, val in replacements.items():
                if val == texto:
                    return key
            return texto

        expr = re.sub(patron, replaceLiteral, expr, flags=re.VERBOSE)

        tokens = re.findall(r"\b[a-zA-Z_]\w*\b", expr)
        for t in sorted(set(tokens), key=len, reverse=True):
            if t in replacements:
                continue
            if t in self.context:
                expr = re.sub(rf'\b{re.escape(t)}\b', f"context['{t}']", expr)

        for key, val in replacements.items():
            expr = expr.replace(key, val)

        expr = expr.replace("Verdadero", "True")
        expr = expr.replace("Falso", "False")

        return expr


    def iniciaSubprocesos(self):
        with open(self.filename, 'r') as f:
            for line in f:
                self.parseSubproceso(line)
        return
    

    def run(self, ejecutar=True):
        self.codeLines.clear()
        with open(self.filename, 'r') as f:
            for line in f:
                self.parseLine(line)

        fullCode = "\n".join(self.codeLines)
        if ejecutar:
            execEnv = {'context':self.context}
            exec(fullCode, execEnv)
            if self.mainName:
                execEnv[self.mainName]()


    def exportPython(self):
        if not hasattr(self, 'filename'):
            print("Error: No se ha definido el nombre del archivo de entrada (.psc).")
            return

        baseName = os.path.splitext(self.filename)[0]
        outputFile = baseName + ".py"

        # Construir contexto con valores neutros
        neutralContext = {}
        for var, tipo in self.contextTypes.items():
            pyType = self.typesMap.get(tipo)
            if pyType is not None:
                neutralContext[var] = self.neutralValues.get(pyType, "None")
            else:
                neutralContext[var] = "None"

        try:
            with open(outputFile, "w", encoding="utf-8") as f:
                f.write("# Archivo generado automáticamente desde pseudocódigo\n\n")
                f.write("context = {\n")
                for k, v in neutralContext.items():
                    f.write(f"    '{k}': {v},\n")
                f.write("}\n\n")
                for line in self.codeLines:
                    f.write(line + "\n")
                f.write("\n")
                f.write("if __name__ == '__main__':\n")
                f.write(f"    {self.mainName}()\n")

            print(f"Archivo exportado correctamente: {outputFile}")

        except Exception as e:
            print(f"Error al exportar archivo Python: {e}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Intérprete de pseudocódigo.", prog='PseudoInterpreter')
    parser.add_argument("archivo", help="Archivo de entrada con extensión .psc")
    parser.add_argument("--export", action="store_true", help="Exportar a archivo Python (.py)")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}", help="Mostrar versión del programa y salir")

    args = parser.parse_args()

    archivo = args.archivo
    pi = PseudoInterpreter(archivo)
    if not args.export:
        pi.run()

    if args.export:
        pi.run(ejecutar=False)
        pi.exportPython()
