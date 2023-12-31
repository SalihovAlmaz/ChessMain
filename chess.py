O_A =  ord("A")
O_H =  ord("H")
class Cell:
    "Ячейка из доски"
    dangerous = False
    def __init__(self,nomer = -1,Figure=None):
        self.nomer = nomer
        if Figure != None:
            self.Figure = Figure
    def __repr__(self):
        if hasattr(self,"Figure"):
            return f"{self.nomer} {self.Figure.__repr__()}".ljust(17)
        else:
            return f"{self.nomer} empty".ljust(17)
    def __setitem__(self, key, value=None):
        if value is None:
            pass
        else:
            self.Figure = value
    def set_figure(self, figure):
        self.Figure = figure
    def get_figure(self):
        return self.Figure
    def get_nomer(self):
        return (self.nomer[0],int(self.nomer[1]))
    def info(self):
        if hasattr(self,Figure):
            return self.Figure
        else:
            False
class Doska:
    __instance = None
    "Доска для игры в щахматы"
    def __new__(cls, *args, **kwargs): #Реализуем синглтон
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return super().__new__(cls)

    def __init__(self, **kwargs):
        self.field = kwargs
        self.doska = {}
        for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
            self.doska[i] = {n: Cell(i + str(n)) for n in range(8, 0, -1)}
    def __getitem__(self, item):
        letter, nomer = item
        if O_A <= ord(letter) and ord(letter) <= O_H and nomer >= 1 and nomer <= 8:
            return self.doska[letter][nomer]
        else:
            return None
    def __setitem__(self, key, value):
        item1, item2 = key
        cell = self.doska[item1][item2]
        cell[item1, item2] = value
    def set_l(self,index,value=None,letter=None):
        if letter is None:
            for c in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                cell = self.doska[c][index]
                cell.set_figure(value)
        else:
            cell = self.doska[letter][index]
            cell.set_figure(value)
    def print(self):
        for n in range(8, 0, -1):
            for c in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
                print(self[(c, n)], end=' ')
            print()
    def stepFigure(self,letter_now,nomer_now,letter,nomer):
        if (letter,nomer) in self.doska[letter_now][nomer_now].get_figure().opportunity_steps(letter_now,nomer_now,self) and self.doska[letter][nomer].get_figure() is None:
            self.doska[letter][nomer].set_figure(self.doska[letter_now][nomer_now].get_figure())
            self.doska[letter_now][nomer_now].set_figure(None)
        else:
            raise TypeError("Невозможный ход")
    def taking_Figure(self, letter_now, nomer_now, letter, nomer):
        if (letter, nomer) in self.doska[letter_now][nomer_now].get_figure().opportunity_taking(letter_now, nomer_now,self) and not self.doska[letter][nomer].get_figure() is None:
            self.doska[letter][nomer].set_figure(self.doska[letter_now][nomer_now].get_figure())
            self.doska[letter_now][nomer_now].set_figure(None)
        else:
            raise TypeError("Нет фигуры для взятия")
    def White_Taking_list(self):#Теперь я работаю тута
        wh_l = []

class Figure:
    "Какая то фигура в шахматах"
    def __init__(self, name, color):
        self.name = name
        self.color = color
    def __repr__(self):
        return f"{self.color} {self.name}"

    def opportunity_steps(self, letter, nomer, doska):
        raise ValueError("Нет фигуры в ячейке")
class Pawn(Figure):
    def __init__(self, name, color):
        super().__init__(name, color)

    def opportunity_steps(self,letter,nomer,doska):
         if doska[(letter, nomer)].get_figure().color == "White" and  not doska[(letter, nomer+1)].get_figure() and not doska[(letter, nomer+2)].get_figure():
             return [(letter,nomer+1),(letter,nomer + 2)]
         elif doska[(letter, nomer)].get_figure().color == "Black" and not doska[(letter, nomer-1)].get_figure() and not doska[(letter, nomer-2)].get_figure():
             return [(letter, nomer - 1), (letter, nomer -2)]
         elif doska[(letter, nomer)].get_figure().color == "White" and  not doska[(letter, nomer+1)].get_figure():
             return [(letter, nomer + 1)]
         elif doska[(letter, nomer)].get_figure().color == "Black" and not doska[(letter, nomer-1)].get_figure():
             return [(letter, nomer - 1)]
    def opportunity_taking(self,letter,nomer,doska):
        if doska[(letter, nomer)].get_figure().color == "White":
            return [(chr(ord(letter)-1), nomer + 1),(chr(ord(letter)+1), nomer + 1)]
        elif doska[(letter, nomer)].get_figure().color == "Black":
            return [(chr(ord(letter) - 1), nomer - 1), (chr(ord(letter) + 1), nomer - 1)]
class Horse(Figure):
    def __init__(self,name, color):
        super().__init__(name, color)

    def opportunity_steps(self, letter, nomer, doska):
        opportunity_steps = []
        for i in [-1,1]:
            for j in [-1,1]:
                if O_A <= ord(letter)-2*i and ord(letter)-2*i <= O_H and nomer +1*j >= 1 and nomer+1*j <= 8:
                    opportunity_steps.append(doska[(chr(ord(letter)-2*i),nomer+1*j)])
                if O_A <= ord(letter)-1*i and ord(letter)-1*i <= O_H and nomer +2*j >= 1 and nomer+2*j <= 8:
                    opportunity_steps.append(doska[(chr(ord(letter) - 1 * i),nomer + 2 * j)])
        return list(map(lambda x: x.get_nomer(),list(filter(lambda x: x.get_figure() is None,opportunity_steps))))
    def opportunity_taking(self, letter, nomer, doska):
        opportunity_steps = []
        for i in [-1, 1]:
            for j in [-1, 1]:
                if O_A <= ord(letter) - 2 * i and ord(
                        letter) - 2 * i <= O_H and nomer + 1 * j >= 1 and nomer + 1 * j <= 8:
                    opportunity_steps.append(doska[(chr(ord(letter) - 2 * i), nomer + 1 * j)])
                if O_A <= ord(letter) - 1 * i and ord(
                        letter) - 1 * i <= O_H and nomer + 2 * j >= 1 and nomer + 2 * j <= 8:
                    opportunity_steps.append(doska[(chr(ord(letter) - 1 * i), nomer + 2 * j)])
        return list(map(lambda x: x.get_nomer(), list(filter(lambda x: x.get_figure() is None, opportunity_steps))))
class Elephant(Figure):
    def __init__(self,name, color):
        super().__init__(name, color)

    def opportunity_steps(self, letter, nomer, doska):
        opportunity_steps = []
        possible_step_l = ord(letter)
        possible_step_n = nomer
        for i in [-1, 1]:
            for j in [-1, 1]:
                step = 1
                while not doska[(chr(possible_step_l + step*i),possible_step_n + step*j)] is None:
                    if not doska[(chr(possible_step_l + step * i), possible_step_n + step * j)].get_figure() is None:
                        opportunity_steps.append(doska[(chr(possible_step_l + step*i),possible_step_n + step*j)])
                        break
                    opportunity_steps.append(doska[(chr(possible_step_l + step*i),possible_step_n + step*j)])
                    step += 1

        return(list(map(lambda x: x.get_nomer(),opportunity_steps)))
    def opportunity_taking(self, letter, nomer, doska):
        opportunity_steps = []
        possible_step_l = ord(letter)
        possible_step_n = nomer
        for i in [-1, 1]:
            for j in [-1, 1]:
                step = 1
                while not doska[(chr(possible_step_l + step * i), possible_step_n + step * j)] is None:
                    if not doska[(chr(possible_step_l + step * i), possible_step_n + step * j)].get_figure() is None:
                        opportunity_steps.append(doska[(chr(possible_step_l + step * i), possible_step_n + step * j)])
                        break
                    opportunity_steps.append(doska[(chr(possible_step_l + step * i), possible_step_n + step * j)])
                    step += 1
class Queen(Figure):
    def __init__(self,name, color):
        super().__init__(name, color)

    def opportunity_steps(self, letter, nomer, doska):
        return Rook.opportunity_steps(self, letter, nomer, doska) + Elephant.opportunity_steps(self, letter, nomer, doska)
    def opportunity_taking(self, letter, nomer, doska):
        return Rook.opportunity_steps(self, letter, nomer, doska) + Elephant.opportunity_steps(self, letter, nomer,doska)
class King(Figure):
    def __init__(self,name, color):
        super().__init__(name, color)
    def opportunity_steps(self, letter, nomer, doska):
        opportunity_steps = []
        for i in [-1, 1, 0]:
            for j in [-1, 1, 0]:
                if not doska[(chr(ord(letter) + i), nomer + j)] is None:
                    opportunity_steps.append(doska[(chr(ord(letter) + i), nomer + j)])
        return (list(map(lambda x: x.get_nomer(), opportunity_steps)))
    def opportunity_taking(self, letter, nomer, doska):
        opportunity_steps = []
        for i in [-1, 1, 0]:
            for j in [-1, 1, 0]:
                if not doska[(chr(ord(letter) + i), nomer + j)] is None:
                    opportunity_steps.append(doska[(chr(ord(letter) + i), nomer + j)])
        return (list(map(lambda x: x.get_nomer(), opportunity_steps)))
class Rook(Figure):
    def __init__(self,name, color):
        super().__init__(name, color)

    def opportunity_steps(self, letter, nomer, doska):
        opportunity_steps = []
        possible_step_l = ord(letter)
        possible_step_n = nomer
        for i in [-1, 1]:
            step = 1
            while not doska[(chr(possible_step_l + step * i), possible_step_n)] is None:
                if not doska[(chr(possible_step_l + step * i), possible_step_n )].get_figure() is None:
                    opportunity_steps.append(doska[(chr(possible_step_l + step * i), possible_step_n)])
                    break
                opportunity_steps.append(doska[(chr(possible_step_l + step * i), possible_step_n)])
                step += 1
            step = 1
            while not doska[(chr(possible_step_l), possible_step_n + step * i)] is None:
                if not doska[(chr(possible_step_l), possible_step_n + step * i)].get_figure() is None:
                    opportunity_steps.append(doska[(chr(possible_step_l), possible_step_n + step * i)])
                    break
                opportunity_steps.append(doska[(chr(possible_step_l), possible_step_n + step * i)])
                step += 1
        return (list(map(lambda x: x.get_nomer(), opportunity_steps)))
    def opportunity_taking(self,letter,nomer,doska):
        opportunity_steps = []
        possible_step_l = ord(letter)
        possible_step_n = nomer
        for i in [-1, 1]:
            step = 1
            while not doska[(chr(possible_step_l + step * i), possible_step_n)] is None:
                if not doska[(chr(possible_step_l + step * i), possible_step_n)].get_figure() is None:
                    opportunity_steps.append(doska[(chr(possible_step_l + step * i), possible_step_n)])
                    break
                opportunity_steps.append(doska[(chr(possible_step_l + step * i), possible_step_n)])
                step += 1
            step = 1
            while not doska[(chr(possible_step_l), possible_step_n + step * i)] is None:
                if not doska[(chr(possible_step_l), possible_step_n + step * i)].get_figure() is None:
                    opportunity_steps.append(doska[(chr(possible_step_l), possible_step_n + step * i)])
                    break
                opportunity_steps.append(doska[(chr(possible_step_l), possible_step_n + step * i)])
                step += 1
        return (list(map(lambda x: x.get_nomer(), opportunity_steps)))
# doska = {}
# for i in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']:
#     doska[i] = {n:Cell(i+str(n)) for n in range(8, 0, -1)}
# doska['C'][7] = Pawn("Pawn","White") #Через setitem давай!!!!!!!!!!!
# Doska1[('C',7)] = Pawn("Pawn","White")
class Player:

    def __init__(self, color, figures, name="Incognito",):
        self.name = name
        self.color = color
        self.figures = figures
class Game:
    def fill_doska(self):
        for n in range(8, 0, -1):
            if n == 2:
                self.Doska1.set_l(n, Pawn("Pawn", "White"))
            elif n == 7:
                self.Doska1.set_l(n, Pawn("Pawn", "Black"))
            elif n == 1:
                self.Doska1.set_l(n, Rook("Rook", "White"), 'A')
                self.Doska1.set_l(n, Rook("Rook", "White"), 'H')
                self.Doska1.set_l(n, Horse("Horse", "White"), 'B')
                self.Doska1.set_l(n, Horse("Horse", "White"), 'G')
                self.Doska1.set_l(n, Elephant("Elephant", "White"), 'C')
                self.Doska1.set_l(n, Elephant("Elephant", "White"), 'F')
                self.Doska1.set_l(n, Queen("Queen", "White"), 'E')
                self.Doska1.set_l(n, King("King", "White"), 'D')
            elif n == 8:
                self.Doska1.set_l(n, Rook("Rook", "Black"), 'A')
                self.Doska1.set_l(n, Rook("Rook", "Black"), 'H')
                self.Doska1.set_l(n, Horse("Horse", "Black"), 'B')
                self.Doska1.set_l(n, Horse("Horse", "Black"), 'G')
                self.Doska1.set_l(n, Elephant("Elephant", "Black"), 'C')
                self.Doska1.set_l(n, Elephant("Elephant", "Black"), 'F')
                self.Doska1.set_l(n, Queen("Queen", "Black"), 'E')
                self.Doska1.set_l(n, King("King", "Black"), 'D')
            else:
                self.Doska1.set_l(n)
    def __init__(self,Name_player_White,Name_player_Black):
        self.Doska1 = Doska()
        self.fill_doska()
        WhiteSet = []
        BlackSet = []
        for value in self.Doska1.doska.values():
            WhiteSet.append(value[1].get_figure())
            WhiteSet.append(value[2].get_figure())
            BlackSet.append(value[7].get_figure())
            BlackSet.append(value[8].get_figure())
        self.player_White = Player("White",WhiteSet,Name_player_White)
        self.player_Black = Player("White",BlackSet,Name_player_Black)
    def stepFigure(self,letter_now,nomer_now,letter,nomer):
        return self.Doska1.stepFigure(letter_now,nomer_now,letter,nomer)
    def taking_Figure(self,letter_now,nomer_now,letter,nomer):
        return self.Doska1.taking_Figure(letter_now,nomer_now,letter,nomer)
    def print(self):
        return self.Doska1.print()


Game1 = Game("Almaz","Ilnaz")
Game1.stepFigure('F',2,'F',4)
Game1.stepFigure('E',1,'G',3)
Game1.stepFigure('G',3,'G',6)
Game1.taking_Figure('G',6,'G',7)

print(Game1.player_White.figures)

#Doska1.stepFigure('G',8,'F',6)
#Doska1.stepFigure('C',4,'C',5)
Game1.print()
# for i in field:
#     if i[1] == '2':
#         print(field[i])


