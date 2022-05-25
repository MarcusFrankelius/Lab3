import random
import string
import copy


class Clause():
    def __init__(self, pos=set(), neg=set()):
        self.neg = neg
        self.pos = pos

    def __eq__(self, other):
        if isinstance(other, Clause):
            return self.pos == other.pos and self.neg == other.neg

    def __hash__(self):
        temp = ""
        for pos in self.pos:
            temp += pos
        for neg in self.neg:
            temp += "-"
            temp += neg
        return hash(temp)

    @ classmethod
    def fromformulae(self, formulae: string):
        neg = set()
        pos = set()

        formulae = formulae.replace(" ", "")
        formulae = formulae.replace("V", " ")

        formulaeArray = formulae.split()

        for variable in formulaeArray:
            if "-" in variable:
                variable = variable.replace("-", "")
                neg.add(variable)
            else:
                pos.add(variable)

        return self(pos, neg)

    def __str__(self):
        values = []
        for value in self.p:
            values.append(value)
        for value in self.n:
            values.append("-" + value)
        return " V ".join(values)

    def RemoveDuplicates(self):
        temp = set()
        for variable in self.pos:
            if variable in self.neg:
                self.neg.remove(variable)
            else:
                temp.add(variable)
        self.pos = temp

    def Display(self):
        print("[", end='')
        for variable in self.pos:
            if not self.neg and list(self.pos).index(variable) == len(self.pos)-1:
                print(variable, end='')
            else:
                print(variable, end=' V ')
        for variable in self.neg:
            if list(self.neg).index(variable) == len(self.neg)-1:
                print("-"+variable, end='')
            else:
                print("-"+variable, end=' V ')
        print("]")


def Delete_duplicates(S: list):
    temp = list()
    for i in range((len(S)-1)):
        for j in range(len(temp)):
            if S[i].pos == S[j].pos and S[i].neg == S[j].neg:
                S.remove(S[i])
                break


def Resolution(A: Clause, B: Clause):
    C = Clause()

    if not (A.pos & B.neg) and not (A.neg & B.pos):
        return False
    if (A.pos & B.neg):
        a = set(random.choice(list(A.pos & B.neg)))
        A.pos = A.pos - a
        B.neg = B.neg - a
    else:
        a = set(random.choice(list(A.neg & B.pos)))
        A.neg = A.neg - a
        B.pos = B.pos - a

    C.pos = A.pos | B.pos
    C.neg = A.neg | B.neg
    if C.pos & C.neg:
        return False
    # C.RemoveDuplicates()
    return C


class CNF():

    def __init__(self, formulaes: list):
        self.clauses = list()
        for formulae in formulaes:
            self.clauses.append(Clause.fromformulae(formulae))

    def Solver(self):

        while True:
            print("--------")
            KB = copy.deepcopy(self.clauses)
            for clause in self.clauses:
                clause.Display()
            S = set()
            clauses = list(self.clauses)
            for i in range((len(clauses)-1)):
                for j in range(i+1, len(clauses)):
                    C = Resolution(copy.deepcopy(
                        clauses[i]), copy.deepcopy(clauses[j]))
                    if C:
                        S.add(C)

            if not S:
                print("Knowledge base done")
                for clause in self.clauses:
                    clause.Display()
                break
            print("Resolution")
            for clause in S:
                clause.Display()
            if S:
                Delete_duplicates(S)
            self.Incorporate(S)

            if self.clauses == KB:
                print("Knowledge base done")
                for clause in self.clauses:
                    clause.Display()
                break

    def Incorporate(self, S: list):
        for A in S:
            self.Incorporate_clause(A)
        return

    def equals(self, other: list) -> bool:

        if len(self.clauses) != len(other):
            return False
        for i in range(0, len(self.clauses)):
            if self.clauses[i].pos != other[i].pos or self.clauses[i].neg != other[i].neg:
                return False
        return True

    def Incorporate_clause(self, A: Clause):

        for B in list(self.clauses):
            if B.pos.issubset(A.pos) and B.neg.issubset(A.neg):
                return
            if A.pos.issubset(B.pos) and A.neg.issubset(B.neg):
                self.clauses.remove(B)
        self.clauses.append(A)
        return


formulae1 = "-sun V -money V i"
formulae2 = "-money V ice V movie"
formulae3 = "-movie V money"
formulae4 = "-movie V -ice"
formulae5 = "movie"
formulae6 = "sun V money V c"


crime1 = "a V b V c"
crime2 = "-c V a"
crime3 = "-b V a V c"


cnf = CNF([formulae1, formulae2, formulae3, formulae4, formulae5, formulae6])

#cnf = CNF([crime1, crime2, crime3])
cnf.Solver()

# print(x.pos.intersection(x.neg))
