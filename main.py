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
  def __init__(self,name,pokemon,items):
    self.name = name
    self.pokemon = []
    for i in pokemon:
      self.pokemon.append(i)
    self.items = []
    for i in items:
      self.items.append(i)
    self.actPokeIdx = 0 #index of active pokemon on roster
    self.activePokemon = self.pokemon[self.actPokeIdx]
    
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
        exit()
      else:
        print("Command not recognized. Try again!")

  def ai_turn(self, opponent):
    roll = random.randint(1, 100)
    while(True):
      if roll >= 20:
        if self.fight(opponent): #Tries to fight if roll high enough
          input_to_continue()
          return
        roll = random.randint(10,20)
        continue #Reroll
      if 10 < roll < 20:
        if self.useItem(0): #Tries to use an item (potion) if available
          input_to_continue()
          return
        roll = random.randint(1, 10)
      if roll < 10:
        if self.changePokemon():
          input_to_continue()
          return
        
      

  def fight(self, opponent):
    attacker = self.activePokemon #Defines who's using the move
    defender = opponent.activePokemon #Defines who's defending against the move
    if attacker.status == "Fainted": #Error check: Pokemon with zero hp can't use moves.
      print("{} has no will to fight!".format(attacker))
      return False
    attacker.attack(attacker.types[0],defender) #Uses the move
    input_to_continue()
    return True

  def useItem(self,itemindex):
    useThis = self.items[itemindex]
    recipient = self.activePokemon
    if useThis.isValid():
      print("{0} used {1} on {2}".format(self.name,useThis.name,recipient.name))
      self.items[itemindex].use(self.activePokemon)

      self.items.pop(itemindex)
      input_to_continue()
      return True
    else:
      print("Item is not valid")
      return False
          
  def changePokemon(self, mandatory = False): #Use 'True' for when the active pokemon just fainted."
    if self.isRosterAllFainted(): #Having no valid Pokemon to send out ends the battle in defeat!
      self.defeated()
      return True #Right now not reachable, but in case defeat no longer ends the scenario
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
          input_to_continue()
          return True #Success
      if mandatory:
        continue #If the change is required.
      else:
        return False #Go back to main prompt with any other key

  #def ai_changePokemon(self, index, mandatory = False):
  #  while(True):

  def isRosterAllFainted(self):
    for i in range(0, len(self.pokemon)):
      if self.pokemon[i].status != "Fainted":
        return False
    else:
      return True

  def defeated(self):
    print ("{0} was defeated!".format(self.name))
    input_to_continue()
    exit() #Ends the program for now
  





        
#Initialize Program

potion = Item("Potion","Heal",20)
pokemon_types.generateTypes()
print(pokemon_types.ptypes)


  
  
# Run Program
print("Starting Pokemon Battle Test")
playerTrainer = Trainer("Ash",[pokemon.Bulbasaur_001(10),pokemon.Squirtle_007(10)],[potion, potion, potion, potion])
opponentTrainer = Trainer("Gary",[pokemon.Charmander_004(10)],[potion, potion, potion, potion])

print(playerTrainer)
print(opponentTrainer)

playerTrainer.prompt(opponentTrainer)
opponentTrainer.fight(playerTrainer)
playerTrainer.prompt(opponentTrainer)
opponentTrainer.useItem(0)
playerTrainer.prompt(opponentTrainer)
opponentTrainer.fight(playerTrainer)
#playerTrainer.fight(opponentTrainer)
#playerTrainer.changePokemon(1)
#playerTrainer.changePokemon(0)