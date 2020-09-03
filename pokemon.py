import pokemon_types
import random

#Supporting Classes & Functions:

def generateXPtable(speed):
    table = {}
    if speed == "fast":
        for i in range(1, 100):
            table.update({str(i): round(4*i**3//5)}) #Faster than cubic
        return table
    if speed == "medium_fast":
        for i in range(1, 100):
            table.update({str(i): round(i**3)}) #cubic
        return table
    if speed == "medium_slow":
        table.update({"1": 0, "2": 8, "3": 24}) #presets levels before the formula's inflection point (avoids negative XP)
        for i in range(4, 100):
            table.update({str(i): round((6/5)*i**3 - 15*i**2 - 100 * i - 140)}) #a bit slower than cubic
        return table
    if speed == "slow":
        for i in range(1,100):
            table.update({str(i): round(5*i**3//4)}) #slower than cubic
        return table
    raise ValueError #The code didn't give a valid formula!

xp_table_fast = generateXPtable("fast") #faster than medium fast
xp_table_medium_fast = generateXPtable("medium_fast") #level up XP = target level ^ 3
xp_table_medium_slow = generateXPtable("medium_slow") #a little slower than medium fast
xp_table_slow = generateXPtable("slow") #slower than medium fast


#Generic class. When pokemon are created as subclasses, fewer parameters are needed.

class Pokemon:
    def __init__(self, dexID, name, level, types, base_attributes, base_health, xp_table, evolves_at_level = -1, *evolves_into):
        self.dexID = dexID #zfill 3 whenever you print this number!
        self.name = name
        self.level = level
        self.types = [] #
        for i in types:
            self.types.append(i)
        self.base_attributes = base_attributes #[ATK, DEF, S_ATK, S_DEF, SPD] By default, at level 100, this pokemon has these stats
        self.attributes = base_attributes//100#*self.level #By default, a lower level pokemon has [level]% percent of base attributes, rounded up.
        self.base_health = base_health #By default, a level 100 pokemon has this health.
        self.max_health = base_health//100*self.level + 50  #By default, a lower level pokemon has [level]% percent of base health, rounded up.
        self.health = self.max_health #Initializes at maximum health
        self.status = "No Status" #Non-faint statuses NYI
        self.learnset = [] #(Level, move learned at level), Moves NYI
        self.moves = [] #NYI
        self.xp_table = xp_table
        self.xp = xp_table[self.level]
        self.effortvalue = 50 #how much XP awarded to opposing pokemon if defeated.
        self.evolves_at_level = evolves_at_level #By default, does not evolve
        self.evolves_into = evolves_into #NYI

    def __repr__(self):
        return self.name
        
    def report(self):
        if len(self.types) == 2:
            return "Lvl. {} {} \n {}/{} \n {}/{} \n {}".format(self.level,self.name,self.types[0],self.types[1],self.health,self.max_health,self.status)
        else:
            return "Lvl. {} {} \n {} \n {}/{} \n {}".format(self.level,self.name,self.types[0],self.health,self.max_health,self.status)

    def attack(self, atktype, target):
        #Pre-Moves implementation simply uses attack type. Eventually, uses the move itself:
        print("{} used {}-type attack.".format(self,atktype))
        #key to continue eventually
        roll = random.randint(1, 100)
        if roll < 90: #Eventually, uses the move's accuracy and own accuracy modifiers.
            self.inflict(atktype, target, 40) #Eventually, uses the move's power.
        else:
            print("{0}'s attack missed!".format(self.name)) #Missed!
            return


    #Resolve if the user's offensive move resolves and hits the defender.
    def inflict(self, atktype, target, amount):

        modifier = -1
        #Same Type Attack Bonus
        if atktype in self.types:
          modifier = modifier * 1.5
        #Target Type
        for i in target.types:
            if i in atktype.nullify_vs:
                modifier = 0
                print("The attack doesn't affect {}!".format(target.name))
            if i in atktype.strong_vs:
                modifier = modifier * 2
                print("It's super effective!")
            if i in atktype.weak_vs:
                modifier = modifier * 0.5
                print("It's not very effective...")
        target.damage(round(amount * modifier)) #Does the damage

    #Always express inflicted damage amounts as a negative number, and healing as a positive number.
    def damage(self, amount):
        print(amount)
        if self.health + amount >= self.max_health:
            self.health = self.max_health #Prevent overheal
            print(self.report())
            return
        if self.health + amount <= 0:
            self.knock_out() #run the knockout method, which changes health and status
            return
        self.health += amount #Inflict or heal damage to an amount less than max, more than zero
        print(self.report())

    #invoke when HP is zero, or a One-Hit KO effect resolves    
    def knock_out(self):
            self.health = 0
            self.status = "Fainted"
            print("{} has fainted!".format(self))

    #invoke when revived by an item or "Pokemon Center" (resetting the scenario)       
    def revive(self, newamount):
            self.health = newamount
            self.status = "No Status"
            print(self.report())

    #invoke when the opposing pokemon is knocked out
    def gainXP(self, amount): #amount = defending pokemon's XP value. Eventually, divide this amongst each pokemon that fought the defender
        self.xp += amount
        #Levels up however many times it can.
        while self.xp >= self.xp_table[str(self.level+1)]:
            self.level_up()

    def level_up(self):
        self.level += 1
        print("{0} has levelled up to {1}!".format(self.name, self.level))
        if self.level >= self.evolves_at_level:
            self.evolve()

    def evolve(self):
        print("Evolution condition reached, but evolving not yet implemented")
        pass #NYI




#All Pokemon Classes

class Bulbasaur_001(Pokemon):
    def __init__(self, level, moveList = []):
        self.dexID = 1
        self.name = "Bulbasaur"
        self.level = level
        self.types = [pokemon_types.ptypes["Grass"], pokemon_types.ptypes["Poison"]]
        self.base_attributes = [49, 49, 65, 65, 45]
        self.attributes = self.base_attributes #*level//100
        self.base_health = 45
        self.max_health = self.base_health*level//100+50 #50 modifier temporary
        self.health = self.max_health 
        self.status = "No Status" #Non-faint statuses NYI
        #self.learnset = []
        #self.moves = [self.learnset[]]
        self.xp_table = xp_table_medium_fast
        self.xp_table = xp_table_medium_fast[str(self.level)]
        self.effortvalue = 50
        self.evolves_at_level = 16
        #self.evolves_into = Ivysaur_002

class Charmander_004(Pokemon):
    def __init__(self, level, moveList = []):
        self.dexID = 4
        self.name = "Charmander"
        self.level = level
        self.types = [pokemon_types.ptypes["Fire"]]
        self.base_attributes = [52, 43, 60, 50, 65]
        self.attributes = self.base_attributes #*level//100
        self.base_health = 39
        self.max_health = self.base_health*level//100+50 #50 modifier temporary
        self.health = self.max_health 
        self.status = "No Status" #Non-faint statuses NYI
        #self.learnset = []
        #self.moves = [self.learnset[]]
        self.xp_table = xp_table_medium_fast
        self.xp_table = xp_table_medium_fast[str(self.level)]
        self.effortvalue = 50
        self.evolves_at_level = 16
        #self.evolves_into = Charmeleon_005

class Squirtle_007(Pokemon):
    def __init__(self, level, moveList = []):
        self.dexID = 7
        self.name = "Squirtle"
        self.level = level
        self.types = [pokemon_types.ptypes["Water"]]
        self.base_attributes = [48, 65, 50, 64, 43]
        self.attributes = self.base_attributes #*level//100
        self.base_health = 44
        self.max_health = self.base_health*level//100+50 #50 modifier temporary
        self.health = self.max_health
        self.status = "No Status" #Non-faint statuses NYI
        #self.learnset = []
        #self.moves = [self.learnset[]]
        self.xp_table = xp_table_medium_fast
        self.xp_table = xp_table_medium_fast[str(self.level)]
        self.effortvalue = 50
        self.evolves_at_level = 16
        #self.evolves_into = Wartortle_008
