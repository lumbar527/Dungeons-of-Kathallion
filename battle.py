import yaml
import random
from colors import *
from colorama import Fore, Back, Style, init, deinit

# initialize colorama
init()

# battle stats
enemy_max = random.randint(5, 21)
enemy_health = enemy_max
enemy_max_damage = random.randint(4, 8)
enemy_damage = 0
defend = 0
turn = True

#opens "save.yaml"
# with open("save.yaml") as f:
    # player = yaml.safe_load(f)

# if player["xp"] < 0:
#     player["xp"] = 0

def fight(player, item):
    # import stats
    global turn, enemy_health, defend, enemy_max, enemy_max_damage
    armor_protection = player["armor protection"]
    print(" ") # do not merge with possible actions text

    # while player still alive
    while player["health"] > 0:
        while turn:
            # print HP stats and possible actions for the player

            print(str(COLOR_RED) + "Enemy: " + str(enemy_health) + str(COLOR_RESET_ALL) + "/" + str(COLOR_GREEN) + str(enemy_max) + str(COLOR_RESET_ALL) + "; " + str(COLOR_BLUE) + "You: " + str(player["health"]) + str(COLOR_RESET_ALL) + "/" + str(COLOR_GREEN) + str(player["max health"]) + str(COLOR_RESET_ALL))
            action = input("Attack, Defend, Use Item? ")

            # if player attack
            if action.lower().startswith('a'):
                print(" ")
                # attack formula
                enemy_health -= random.randint(0, int(item[player["held item"]]["damage"]))
                print(str(COLOR_RED) + "Enemy: " + str(enemy_health) + str(COLOR_RESET_ALL) + "/" + str(COLOR_GREEN) + str(enemy_max) + str(COLOR_RESET_ALL))
                turn = False

            # if player defend
            elif action.lower().startswith('d'):
                print(" ")
                defend += random.randint(0, int(item[player["held item"]]["defend"]))
                # defend formula
                player["health"] += random.randint(0, 3)
                if player["health"] > player["max health"]:
                    player["health"] = player["max health"]
                turn = False

            # if player use an item
            elif action.lower().startswith('u'):
                print(" ")
                item_input = input(str(player["inventory"]) + " ")
                # use item
                if item_input in player["inventory"]:
                    if item[item_input]["type"] == "Consumable":
                        if item[item_input]["healing level"] == "max health":
                            player["health"] = player["max health"]
                        else:
                            player["health"] += item[item_input]["healing level"]
                        player["max health"] += item[item_input]["max bonus"]
                        player["inventory"].remove(item_input)
                    # hold weapon if it is one
                    if item_input in player["inventory"] and item[item_input]["type"] == "Weapon":
                        player["held item"] = item_input
                        print("You are now holding a/an ", player["held item"])
                print(" ")
            else:
                print("'" + action + "' is not a valid option")
                print(" ")
        # when it's not player turn
        while not turn:
            # if enemy is still alive
            if enemy_health > 0:
                damage = random.randint(0, enemy_max_damage) - defend * ( armor_protection * round(random.uniform(0.50, 0.90), 1) )
                damage = round(damage)
                defend = 0
                if damage > 0:
                    player["health"] -= damage
                print("The enemy dealt ", str(damage), " points of damage.")
                print("You have", str(player["health"]), "health points.")
                print(" ")
                turn = True
            else:
                player["xp"] += enemy_max * enemy_max_damage / 3
                player["health"] += random.randint(0, 3)
                # enemy_max = random.randint(5, 21)
                # enemy_health = enemy_max
                # enemy_max_damage = random.randint(4, 8)
                # defend = 0
                # turn = True
                still_playing = False
                return
    return



still_playing = True

# while still_playing:

#     fight()

#     still_playing = False

#     if player["health"] <= 0:
#         if player["cheat"] < 3:
#             cheatcode = input("What is the not-die code? ")
#             if cheatcode == "4":
#                 # cheat code was correct so keep playing
#                 player["cheat"] += 1
#                 player["health"] = 10
#                 still_playing = True
#             else:
#                 player["health"] = 10
#                 player["max health"] = 10
#                 player["x"] = 0
#                 player["y"] = 0
#                 player["inventory"] = ["Sword", "Healing Potion"]
#                 player["held item"] = "Sword"
#                 player["cheat"] = 0
#                 player["xp"] -= 100
                
#         else:
#             print("YOU DIED")
#             player["health"] = 10
#             player["max health"] = 10
#             player["x"] = 0
#             player["y"] = 0
#             player["inventory"] = ["Sword", "Healing Potion"]
#             player["held item"] = "Sword"
#             player["cheat"] = 0
#             player["xp"] -= 100

# put all the new data in the file
# dumped = yaml.dump(player)

# deinitialize colorama
deinit()

# with open("save.yaml", "w") as f:
#     f.write(dumped)
