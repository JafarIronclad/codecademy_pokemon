import pokemon_types

#Generic class. When pokemon are created as subclasses, fewer parameters are needed.

class Pokemon:
    def __init__(self, dexID, name, level, types, base_attributes, base_health, evolves_at_level = -1, *evolves_into):
        self.dexID = dexID #zfill 3 whenever you print this number!
        self.name = name
        self.level = level
        self.types = [] #
        for i in types:
            self.types.append(i)
        self.base_attributes = base_attributes #[ATK, DEF, S_ATK, S_DEF, SPD] By default, at level 100, this pokemon has these stats
        self.attributes = base_attributes//100*self.level #By default, a lower level pokemon has [level]% percent of base attributes, rounded up.
        self.base_health = base_health #By default, a level 100 pokemon has this health.
        self.max_health = base_health//100*self.level  #By default, a lower level pokemon has [level]% percent of base health, rounded up.
        self.health = self.max_health #Initializes at maximum health
        self.status = "No Status" #Non-faint statuses NYI
        self.learnset = [] #(Level, move learned at level), Moves NYI
        self.moves = [] #NYI
        self.evolves_at_level = evolves_at_level #By default, does not evolve
        self.evolves_into = evolves_into #NYI

    def __repr__(self):
        return self.name
        
    def report(self):
        if len(self.types) == 2:
            return "Lvl. {} {} \n {}/{} \n {}/{} \n {}".format(self.level,self.name,self.types[0],self.types[1],self.health,self.max_health,self.status)
        else:
            return "Lvl. {} {} \n {} \n {}/{} \n {}".format(self.level,self.name,self.types[0],self.health,self.max_health,self.status)

    

        #Resolve if the user's offensive move resolves and hits the defender.
    def attack(self, atktype, target, amount):
        print("{} used {}-type attack.".format(self,atktype))
        modifier = -1
        #Same Type Attack Bonus
        #if atktype in ####:
        #  modifier = modifier * 1.5
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
        
    def knock_out(self):
            self.health = 0
            self.status = "Fainted"
            print("{} has fainted!".format(self))
        
    def revive(self, newamount):
            self.health = newamount
            self.status = "No Status"
            print(self.report())

class Bulbasaur_001(Pokemon):
    def __init__(self, level, moveList = []):
        self.dexID = 1
        self.name = "Bulbasaur"
        self.level = level
        self.types = [pokemon_types.ptypes["Grass"], pokemon_types.ptypes["Poison"]]
        self.base_attributes = [49, 49, 65, 65, 45]
        self.attributes = self.base_attributes #*level//100
        self.base_health = 45
        self.max_health = self.base_health*level//100+10
        self.health = self.max_health 
        self.status = "No Status" #Non-faint statuses NYI
        #self.learnset = []
        #self.moves = [self.learnset[]]
        #self.evolves_at_level = 16
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
        self.max_health = self.base_health*level//100+10
        self.health = self.max_health 
        self.status = "No Status" #Non-faint statuses NYI
        #self.learnset = []
        #self.moves = [self.learnset[]]
        #self.evolves_at_level = 16
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
        self.max_health = self.base_health*level//100+10
        self.health = self.max_health
        self.status = "No Status" #Non-faint statuses NYI
        #self.learnset = []
        #self.moves = [self.learnset[]]
        #self.evolves_at_level = 16
        #self.evolves_into = Wartortle_008
