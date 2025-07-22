import re
import sys

class PseudoInterpreter:
    def __init__(self):
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
            "str": "",
            "bool": False
        }

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

        #print(nombre, paramList)
        self.functions[nombre]= {k.strip(): v.strip() for k, v in (item.split(':') for item in paramList)}
        paramList = ['context: dict']

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
            self.codeLines.append("# Error al procesar Definir")
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
                if self.esSubproceso:
                    self.context[nombre+"_"+self.SubprocesoActual] = eval(init)
                    self.codeLines.append(f"{self.indent * self.currentIndent}context['{nombre+"_"+self.SubprocesoActual}'] = {init}")
                else:
                    self.context[nombre] = eval(init)
                    self.codeLines.append(f"{self.indent * self.currentIndent}context['{nombre}'] = {init}")
            else:
                if self.esSubproceso:
                    self.context[var+"_"+self.SubprocesoActual] = valorInicial
                    self.codeLines.append(f"{self.indent * self.currentIndent}context['{var+"_"+self.SubprocesoActual}'] = {valorInicial}")
                else:
                    self.context[var] = valorInicial
                    self.codeLines.append(f"{self.indent * self.currentIndent}context['{var}'] = {valorInicial}")
        return
    
    def NoReconocido(self,line):
        self.codeLines.append(f"{self.indent * self.currentIndent}# No procesado: {line}")
        return
    

    def _isCamelCase(self, identifier):
        return bool(re.fullmatch(r'[a-z]+(?:[A-Z][a-z0-9]*)*', identifier))


    def run(self, filename):
        with open(filename, 'r') as f:
            for line in f:
                self.parseLine(line)


        fullCode = "\n".join(self.codeLines)
        print("===== Código generado =====")
        print(fullCode)

        print(self.context)
        print(self.functions)
        #execEnv = {}
        #exec(fullCode, execEnv)
        #if self.mainName:
        #    execEnv[self.mainName]()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python interpreter.py archivo.psc")
        sys.exit(1)

    archivo = sys.argv[1]
    pi = PseudoInterpreter()
    pi.run(archivo)