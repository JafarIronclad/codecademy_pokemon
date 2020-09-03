import random
import pokemon
import pokemon_types
import cfg
from sys import exit

#MASTER LISTS:

validEffects = ["Heal"]

#HELPER FUNCTIONS:

#Use to compare input string to any number of acceptable cases for a given prompt.
def isValidInput(input, *args):
  if not args:
    return False #Accept no input if the function does not define one.
  for arg in args:
    if input == arg:
      return True #Check the given args to see if the input matches at least one. True if so.
  return False

#Pauses gameplay. Accepts any input with enter. Can be modified for logging/debugging.
def input_to_continue():
  input("\n\n[ENTER]")

#CLASSES

class Item:

  def __init__(self,name,effect,amount):
    self.name = name
    self.effect = effect
    self.amount = amount

  def __repr__(self):
    return self.name
  
  def isValid(self):
    if self.effect in validEffects:
      return True
    else:
      return False
  
 #use: affects targeted Pokemon 
  def use(self, target):
    if self.effect == "Heal":
      target.damage(self.amount)
    else:
      print("Item had no type but was still activated. Error!")
      

class Trainer:
  def __init__(self,name,pokemon,items,isPlayer = False):
    self.name = name
    self.pokemon = []
    for i in pokemon:
      self.pokemon.append(i)
    self.items = []
    for i in items:
      self.items.append(i)
    self.actPokeIdx = 0 #index of active pokemon on roster
    self.activePokemon = self.pokemon[self.actPokeIdx]
    self.isPlayer = isPlayer
    
  def __repr__(self):
    returnMe = self.name + ": with \n"
    return returnMe

  def prompt(self, opponent):
    while(True):
      print("What will {0} do? \n".format(self.activePokemon))
      action = input(" [F]ight [I]tem \n [P]kmn  [R]un \n \n ACTION: ")
      if isValidInput(action.upper(),"F"):
        #Choose Move NYI
        if self.fight(opponent):
          input_to_continue()
          return #End turn if action resolves and comes back True
        continue #Tries again if cancelled or can't resolve
      elif isValidInput(action.upper(),"I"):
        #Choose Item NYI
        itemidx = 0
        if self.useItem(itemidx):
          input_to_continue()
          return #End turn if action resolves and comes back True
        continue #Tries again if cancelled or can't resolve
      elif isValidInput(action.upper(),"P"):
        if self.changePokemon():
          input_to_continue()
          return #End turn if action resolves and comes back True
        continue #Tries again if cancelled or can't resolve
      elif isValidInput(action.upper(),"R"):
        #No Map layer to return to, so just quits the program.
        input("Ran away safely! \n\n Press enter to exit the program.")
        exit(0)
      else:
        print("Command not recognized. Try again!")

  def ai_turn(self, opponent):
    choice = self.ai_chooseAction(opponent)
    while(True):
      if choice == "Fight":
        if self.fight(opponent): #Tries to fight if roll is high enough
          return
        continue #Reroll
      if choice == "Item":
        if self.useItem(0): #Tries to use an item (potion) if available
          return
      if choice == "Pokemon":
        if self.changePokemon(self.ai_choosePokemon()):
          return

  def ai_chooseAction(self, opponent, strategy = None):
    fightWeight = 100 #by default, the AI trainer will use one of their pokemon's moves, regardless of roll.
    itemWeight = 0 #by default, the AI trainer will not use an item, regardless of roll.
    changeWeight = 0 #by default, the AI trainer will not change pokemon, regardless of roll.

    #Conditions which make certain choices appealing.
    #When pokemon below half health, more likely to use a potion.
    if self.activePokemon.health < self.activePokemon.max_health//2:
      itemWeight += 50
    #When pokemon in peril, more likely to change to someone else.
    if self.activePokemon.health < self.activePokemon.max_health//4:
      changeWeight += 50

    #Conditions under which actions are impossible
    if self.countReadyPokemon() == 1: #Can't change if down to last pokemon!
      changeWeight = 0
    if not self.items: #Can't use an item without items!
      itemWeight = 0

    #Weighting complete. Roll for fighting as an option.
    roll = random.randint(1,fightWeight+itemWeight+changeWeight)
    if roll <= fightWeight:
      return "Fight"
    #If fighting ruled out, roll for using an item. Certain if unable to change pokemon.
    roll = random.randint(1,itemWeight+changeWeight)
    if roll <= itemWeight:
      return "Item"
    #If Item ruled out
    return "Pokemon" #Last possible choice


  def fight(self, opponent):
    attacker = self.activePokemon #Defines who's using the move
    defender = opponent.activePokemon #Defines who's defending against the move
    if attacker.status == "Fainted": #Error check: Pokemon with zero hp can't use moves.
      print("{} has no will to fight!".format(attacker))
      return False
    attacker.attack(attacker.types[0],defender) #Uses the move
    return True

  def useItem(self,itemindex):
    useThis = self.items[itemindex]
    recipient = self.activePokemon
    if useThis.isValid():
      print("{0} used {1} on {2}".format(self.name,useThis.name,recipient.name))
      self.items[itemindex].use(self.activePokemon)

      self.items.pop(itemindex)
      return True
    else:
      print("Item is not valid")
      return False


  #changePokemon handles all pokemon swaps. With no arguments, player chooses a pokemon or can cancel back to main menu.
  #Pass a chosenIdx integer for an AI trainer change or a random swap. This integer should already be checked for validity before calling the function.
  #Pass chosenIdx as None and mandatory as 'True' for when the active pokemon just fainted. This prevents cancelling out and forces a valid change if possible (or defeat if impossible!)     
  def changePokemon(self, chosenIdx = None, mandatory = False):  
    if self.countReadyPokemon() == 0: #Having no valid Pokemon to send out ends the battle in defeat!
      self.defeated()
      return True #Right now not reachable, but in case defeat no longer ends the scenario

    if chosenIdx: #Skipped if function is run with no arguments or with an explicit 'None' as first argument.
      print("{}, come back!".format(self.activePokemon))
      self.actPokeIdx = chosenIdx #Changes the index of the now-active pokemon in the roster
      self.activePokemon = self.pokemon[self.actPokeIdx] #Chosen pokemon is now active!
      print("Go, {}!".format(self.activePokemon))
      print(self.activePokemon.report())
      return True #Success
    while(True): #If there's a valid pokemon to switch to, keep trying unless cancelled.


      for i in range(0, len(self.pokemon)):
        print("[{0}] for: {1}".format(i, self.pokemon[i].report()))
      if mandatory:
        newIndex = int(input("Which Pokemon will you switch to?\n Enter the corresponding number to select. \n\n SELECT:"))
      else:
        newIndex = int(input("Which Pokemon would you like to switch to?\n Enter the corresponding number to select, \n or any other input to cancel. \n\n SELECT:"))
      if isValidInput(newIndex, 0, 1, 2, 3, 4, 5): #Accepts only a number input from 0 to 5.
        if newIndex > len(self.pokemon): #Error check: index too high for # of pokemon on team.
          print("No pokemon at {0}!".format(newIndex))
          continue #Prompt again.
        elif self.pokemon[newIndex].status == "Fainted": #Error check: can't switch to a pokemon with zero HP.
          print("{} has no will to fight!".format(self.pokemon[newIndex]))
          continue
        elif newIndex == self.actPokeIdx: #Error check: active pokemon can't switch with itself.
          print("{} is already active at index {}".format(self.activePokemon, self.actPokeIdx))
          continue #Prompt again.

        else: #No errors caught.
          print("{}, come back!".format(self.activePokemon))
          self.actPokeIdx = newIndex #Changes the index of the now-active pokemon in the roster
          self.activePokemon = self.pokemon[self.actPokeIdx] #Chosen pokemon is now active!
          print("Go, {}!".format(self.activePokemon))
          print(self.activePokemon.report())
          return True #Success
      if mandatory:
        continue #If the change is required.
      else:
        return False #Go back to main prompt with any other key

  def ai_choosePokemon(self):
    options = []
    for i in range(0, len(self.pokemon) - 1):
      if self.pokemon[i].status == "Fainted" or i == self.actPokeIdx: #Error check: can't switch to a pokemon with zero HP.
        continue #Don't include as an option if not valid
      else:
        options.append(i) #Include if valid
    #Pick a pokemon from the valid options
    return random.choice(options)

  def aftermath(self): #Check statuses after action.
    if self.activePokemon.status == "Fainted":
      if self.isPlayer:
        self.changePokemon(None, True) #Must change pokemon, or defeated if unable
      else:
        self.changePokemon(self.ai_choosePokemon, True) #Must change pokemon, or defeated if unable

  def countReadyPokemon(self):
    count = 0
    for i in range(0, len(self.pokemon)):
      if self.pokemon[i].status != "Fainted":
        count += 1
    return count

  def defeated(self):
    print ("{0} was defeated!".format(self.name))
    input_to_continue()
    exit(0) #Ends the program for now


        
#Initialize Program

potion = Item("Potion","Heal",20)
pokemon_types.generateTypes()


  
  
# Run Program
print("Starting Pokemon Battle Test")
playerTrainer = Trainer("Ash",[pokemon.Bulbasaur_001(10),pokemon.Squirtle_007(10)],[potion, potion, potion, potion], True)
opponentTrainer = Trainer("Gary",[pokemon.Charmander_004(10)],[potion, potion, potion, potion])

print(playerTrainer)
print(opponentTrainer)

while(True):
  playerTrainer.prompt(opponentTrainer)
  playerTrainer.aftermath()
  opponentTrainer.aftermath()
  opponentTrainer.ai_turn(playerTrainer)
  playerTrainer.aftermath()
  opponentTrainer.aftermath()
#playerTrainer.fight(opponentTrainer)
#playerTrainer.changePokemon(1)
#playerTrainer.changePokemon(0)