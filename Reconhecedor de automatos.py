
# **************************************************************************
#                                                                          *
#   Edivan Azevedo & Gustavo Teixera 							           *
#                 Última alteração em: 10/02/2023                          *
# **************************************************************************

with open("output.txt", "a") as file:
    file.write(
        '------------------RESULTADOS GERADOS A PARTIR DO ALGORITMO DE LFA------------------\n\n\n')

class gramatica:
    def __init__(self, config_file: str):
        self.V = set()
        self.Sigma = set()
        self.P = dict()
        self.I = set()
        self.F = set()
        # igualmente dos automatos, lê todas as linhas do arquivo da gramática adicionando os dados nos devidos atributos
        with open(config_file, 'r') as f:
            for line in f:
                if ' = ' in line:
                    key, value = line.strip().split(' = ')
                    if key == 'V':
                        self.V = set(value[1:-1].split(';'))
                    elif key == 'Sigma':
                        self.Sigma = set(value[1:-1].split(';'))
                    elif key == 'P':
                        self.P = {tuple(j.split('->'))
                                  for j in value[1:-1].split(';')}
                    elif key == 'I':
                        self.I = set(value)

#
    def print(self):
        with open("output.txt", "a") as file:
            file.write('\n\nGramática Carregada:'+"\n")
            file.write('Vocabulário =' + str(self.V) + "\n")
            file.write('Alfabeto =' + str(self.Sigma) + "\n")
            file.write('Regras de substituição =' + str(self.P) + "\n")
            file.write('Simbolo Inicial =' + str(self.I) + "\n\n")

    def convert_gramatica(self):
        self.Q = set()
        self.F = set()
        self.delta = set()
        new_delta = set()
        final = []
        # verifica se a gramatica é linear a direita
        # se cada regra de substituição tem um único simbolo a direita
        for j in self.P:
            tamanho = 0
            if j[1][0].isupper() and len(j[1]) != 1:
                with open("output.txt", "a") as file:
                    file.write('\nEssa grmática não é linear a Direita'+"\n")
                return
            for i in j[-1]:
                if i.isupper():
                    tamanho = tamanho+1
            if tamanho >= 1 and j[1][-1].islower():
                with open("output.txt", "a") as file:
                    file.write('\nEssa grmática é linear a Direita'+"\n")
                return
            # coleta os dados da gramática
        for i in self.V:
            if i.isupper():
                self.Q.add(i)
        for i in self.P:
            if "' '" in i:
                final.append(i[0])
            if i[-1].islower():
                self.F.add('qf')
                self.Q.add('qf')
            
                self.delta.add('('+i[0]+','+i[-1]+')->'+'qf')
        #se o síbolo for maiusculo a transição é adicionado em delta
        for j in self.P:
            if j[1][-1].isupper():
                self.delta.add(
                    '('+j[0]+','+j[1].replace(j[1][-1], '')+')->'+j[1][-1])
        for i in self.P:
            if i[-1].isupper() and len(i[-1]) == 1:
                self.delta.add('('+i[0]+','+"' '"+')->'+i[-1])
                
        for i in final:
            self.delta.add('('+i+','+"' '"+')->'+'qf')
        for k in self.delta:
            if k[3].isupper() or k[3] == ')':
                new_delta.add(k)
            #remove as transições que comece com maiusculo e subtrai do conjunto original
        self.delta = self.delta - new_delta
        with open("output.txt", "a") as file:
            file.write('\n\nAutomato gerado:\n')
            file.write('Estados =' + str(self.Q) + "\n")
            file.write('Alfebeto =' + str(self.Sigma) + "\n")
            file.write('Transações =' + str(self.delta) + "\n")
            file.write('Estado inicial =' + str(self.I) + "\n")
            file.write('Estado Final =' + str(self.F) + "\n\n")


class Automato:
    def __init__(self, config_file: str):
        # incia os atributos da classe automato
        self.Q = set()
        self.Sigma = set()
        self.delta = dict()
        self.I = set()
        self.F = set()
        with open(config_file, 'r') as f:
            # lê linha por linha
            # se houver = na linha ele parte a linha
            for line in f:
                if ' = ' in line:
                    key, value = line.strip().split(' = ')
                    if key == 'Q':
                        self.Q = set(value[1:-1].split(';'))
                    elif key == 'Sigma':
                        self.Sigma = set(value[1:-1].split(';'))
                    elif key == 'delta':
                        self.delta = {tuple(j.split('->'))
                                      for j in value[1:-1].split(';')}
                    elif key == 'I':
                        self.I = set(value[1:-1].split(';'))
                    elif key == 'F':
                        self.F = set(value[1:-1].split(';'))

    def determinisco(self):
        for i in self.delta:
            if i[0].split(',')[1].split(')')[0][0] not in self.Sigma and i[0].split(',')[1].split(')')[0] != "' '":
                with open("output.txt", "a") as file:
                    file.write('Não foi possível determinar' + "\n\n")
                return
        # Verficica se o simbolo da transação pertence ao alfabeto
        for state, _ in self.delta:
            if len([j for j in self.delta if j[0] == state]) > 1:
                with open("output.txt", "a") as file:
                    file.write('Autômato não determinístico' + "\n\n")
                return 0
        # Verfica se existe algum estado com uma transação em vazio
        for cont in self.delta:
            if "' '" in cont[0]:
                with open("output.txt", "a") as file:
                    file.write('Autômato não determinístico' + "\n\n")
                return 0
        # Verfica se ah mais de um estado inicial ou final
        if len(self.I) > 1 or len(self.F) > 1:
            with open("output.txt", "a") as file:
                file.write('Autômato não determinístico' + "\n\n")
            return 0
        # caso nenhum dos casos acima seja atendido, o automato é determinístico
        with open("output.txt", "a") as file:
            file.write('Automato determininístico' + "\n\n")
        return

    # Verifica se dentro do delta existe o símbolo vazio
    def vazio(self):
        v = "' '"
        for cont in self.delta:
            if v in cont[0]:
                return True
        return False

    def remove_vazio(self):
        for i in self.delta:
            if i[0].split(',')[1].split(')')[0][0] not in self.Sigma and i[0].split(',')[1].split(')')[0] != "' '":
                with open("output.txt", "a") as file:
                    file.write('ERRO' + "\n\n")
                return
        # chama a função vazio, caso retorne falso, o automato não possui transação em vazio
        if self.vazio() == False:
            with open("output.txt", "a") as file:
                file.write(
                    'O autômato não possui transições em vazio.' + "\n\n")
            return
        # cria conjunto de transações em vazio
        new_delta = set()
        #se a transição não for vazia, é adicionada no new delta
        for j in self.delta:
            if "' '" not in j[0]:
                new_delta.add(j[0]+'->'+j[1])
                
            else:
                for j2 in self.delta:
                    if j[0].split(',')[0] == j2[0].split(',')[0] and "' '" not in j2[0].split(',')[1]:
                        new_delta.add(j2[0]+'->'+j[1])
                    elif j2[1] == j[0].split(',')[0].split('(')[1] and "' '" in j[0]:
                        new_delta.add(j2[0]+'->'+j[1])
        # caso exista adicione na nova variável
        self.delta = new_delta
        self.delta = {tuple(j.split('->'))
                      for j in new_delta}
        if len(self.delta) == 1:
            for i in self.delta:
                self.I = set()
                self.I.add(i[0].split(',')[0].split('(')[1])
                self.F = set()
                self.F.add(i[1])

        new_delta = set()
        for j in self.delta:
            if "' '" not in j[0]:
                new_delta.add(j[0]+'->'+j[1])

        self.delta = new_delta

        # escreve no txt o novo automato
        self.delta = {tuple(j.split('->'))
                      for j in new_delta}
        with open("output.txt", "a") as file:
            file.write(
                '\n\nAutômato finito equivalente sem ligações em vazio criado:'+"\n")
            file.write('Estado =' + str(self.Q) + "\n")
            file.write('Alfabeto =' + str(self.Sigma) + "\n")
            file.write('Transações:' + str(self.delta) + "\n")
            file.write('Estados Iniciais =' + str(self.I) + "\n")
            file.write('Estados Finais =' + str(self.F) + "\n\n")

    def useless(self):
        # cria conjunto de estados  com todos os estados destido das transições
        estados = set()
        new_delta = set()
        # para cada transação verifica se o estado inicia da transação não está no conjunto de estados e se não é um estado inicial
        for t in self.delta:
            estados.add(t[1])

        for cont in self.delta:
            #if verifica se o estado inicial está presente em estados
            #e verifica se não pertence aos iniciais
            if cont[0].split(',')[0].split('(')[1] not in estados and cont[0].split(',')[0].split('(')[1] not in self.I:
                new_delta.add(cont)
            i = 0
            # se não houver nenhuma (igual a 0) transição para este estado e esse estado não for estado final a transição é adicionada no
            for cont2 in self.delta:
                if cont[1] == cont2[0].split(',')[0].split('(')[1]:
                    i += 1
            if i == 0 and cont[1] not in self.F:
                new_delta.add(cont)
        # se não estiver a transição é adicionada no novo conjunto de transições
        self.delta = self.delta-new_delta

        # por fim, atualiza a variável com transições
        if len(self.delta) == 1:
            for i in self.delta:
                self.I = set()
                self.I.add(i[0].split(',')[0].split('(')[1])
                self.F = set()
                self.F.add(i[1])
        with open("output.txt", "a") as file:
            file.write(
                '\n\nAutômato finito equivalente sem sem estados useless/acessiveis criado:'+"\n")
            file.write('Estado =' + str(self.Q) + "\n")
            file.write('Alfabeto =' + str(self.Sigma) + "\n")
            file.write('Delta:' + str(self.delta) + "\n")
            file.write('Estados Iniciais =' + str(self.I) + "\n")
            file.write('Estados Finais =' + str(self.F) + "\n\n")

    def gramatica(self):
        self.vocabular = set()
        self.P = set()
        self.inicial = set()
        self.inicial.add('S')
        # adiciona cada simbolo do alfabeto do automato ao vocabulario da gramática
        for v in self.Sigma:
            self.vocabular.add(v)
            self.vocabular.add(v.upper())
        # para cacda transição verifica se é possível produzir aquela transição
        for h in self.delta:
            for g in self.delta:
                if g[0].split(',')[0].split('(')[1] in self.I:
                    self.P.add('S->'+g[0].split(',')[1].split(')')
                               [0]+g[0].split(',')[1].split(')')[0][0].upper())

                if g[1] == h[0].split(',')[0].split('(')[1]:
                    self.P.add(g[0].split(',')[1].split(')')[0][0].upper() +
                               '->'+h[0].split(',')[1].split(')')
                                [0]+h[0].split(',')[1].split(')')[0][0].upper())

                if g[1] and g[0].split(',')[0].split('(')[1] in self.F:
                    self.P.add(g[0].split(',')[1].split(')')
                               [0][0].upper() + "->' '")

                if (g[1] in self.F or g[0].split(',')[0].split('(')[1] in self.F) and "' '" not in self.P:
                    self.P.add(g[0].split(',')[1].split(')')
                                [0][0].upper() + "->' '")
        with open("output.txt", "a") as file:
            file.write('\n\nGramática linear a direita gerada:'+"\n")
            file.write('Vocabulario' + str(self.vocabular.union('S')) + "\n")
            file.write('Alfabeto' + str(self.Sigma) + "\n")
            file.write('Produções' + str(self.P) + "\n")
            file.write('Simbolo Inicial' + str(self.inicial) + "\n\n")


# *****************************FUNÇÕES*********************************************
james = Automato('mod_automato.txt')
tucupi = gramatica('mod_gramatica.txt')
james.determinisco()
james.remove_vazio()
james.useless()
james.gramatica()
tucupi.print()
tucupi.convert_gramatica()
