#A Type is a property of Pokemon (Each Pokemon has either one or two Types),
# and a property of Moves (Each Move has a single type)
#Basic level: Moves interact with based on catalogued
# strengths, weaknesses, and immunities of respective types.
#Additionally, if a Pokemon uses an offensive move whose Type matching one of its Types,
# it receives a damage multiplier bonus (larger if pokemon has a single type)


class Pokemon_Type:

    def __init__(self, name):
        print("I'm making a type")
        self.name = name
        self.strong_vs = [] #Listed Pokemon types take more damage from self's move type.
        self.weak_vs = [] #Listed Pokemon types take less damage from self's move type.
        self.nullify_vs = [] #Listed Pokemon types are completely unaffected by self's move type.
        print(self)

    def __repr__(self):
        return self.name

    def setStrong_vs(self, *args): #Run once per type when initialized.
        self.strong_vs = [strength for strength in args]

    def setWeak_vs(self, *args): #Run once per type when initialized.
        self.weak_vs = [weakness for weakness in args]

    def setNullify_vs(self, *args): #Run once per type when initialized.
        self.nullify_vs = [immunity for immunity in args]

def getTypes():
    if not ptypes:
        generateTypes()
    return ptypes

ptypes = {"Normal": Pokemon_Type("Normal"),
    "Fire": Pokemon_Type("Fire"),
    "Water": Pokemon_Type("Water"),
    "Grass": Pokemon_Type("Grass"),
    "Poison": Pokemon_Type("Poison")} #Dictionary of type names with their Pokemon_Type as values.


#Set strengths, weaknesses, and immunities for MOVES of each type:
def generateTypes():
    print("I'm generating type weaknesses")



    #Normal - N strengths, weak vs. Fighting & Steel, no effect

    #Fire - Strong vs. Grass, Weak vs. Water
    ptypes["Fire"].setStrong_vs(ptypes["Grass"])
    ptypes["Fire"].setWeak_vs(ptypes["Water"])

    #Water - Strong vs. Fire, Weak vs. Grass
    ptypes["Water"].setStrong_vs(ptypes["Fire"])
    ptypes["Water"].setWeak_vs(ptypes["Grass"])

    #Grass - Strong vs. Water, Weak vs. Fire
    ptypes["Grass"].setStrong_vs(ptypes["Water"])
    ptypes["Grass"].setWeak_vs(ptypes["Fire"])

    print(ptypes)






