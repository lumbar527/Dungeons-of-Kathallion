import yaml
import random
from colors import *
from colorama import Fore, Back, Style, init, deinit

# initialize colorama
init()

# battle stats
defend = 0
turn = True
fighting = True

def encounter_text_show(player, item, enemy, map, map_location, enemies_remaining, lists):
    # import stats
    global turn, defend, fighting, already_encountered
    global enemy_singular, enemy_plural, enemy_max, enemy_health, enemy_max_damage, enemy_min_damage, enemy_agility, enemy_damage, choosen_item
    player_agility = player["agility"]
    print(" ") # do not merge with possible actions text
    # load and create enemies list type

    enemies_number = map["point" + str(map_location)]["enemy"]

    if enemies_number > 1:
        print("You encounter a group of foes that won't let you pass.")
    else:
        print("You find a/an " + str(enemy_singular) + " on your way.")

    startup_action = input("[R]un Away, [F]ight, [U]se Item? ")

    if startup_action.lower().startswith('r'):
        # run away chance
        if player["agility"] / round(random.uniform(1.10, 1.25), 2) > enemy_agility:
            print("You succeeded in running away from your enemy!")
            fighting = False
        else:
            print("You failed in running away from your enemy! You now have to fight him!")
    elif startup_action.lower().startswith('f'):
            pass
    elif startup_action.lower().startswith('u'):
        print(" ")
        item_input = input(str(player["inventory"]) + " ")
        # use item
        if item_input in player["inventory"]:
            if item[item_input]["type"] == "Consumable" or item[item_input]["type"] == "Food":
                if item[item_input]["healing level"] == "max health":
                    player["health"] = player["max health"]
                else:
                    player["health"] += item[item_input]["healing level"]
                player["max health"] += item[item_input]["max bonus"]
                player["inventory"].remove(item_input)
            # hold weapon/armor piece if it is one
            if item_input in player["inventory"] and item[item_input]["type"] == "Weapon":
                player["held item"] = item_input
                print("You are now holding a/an ", player["held item"])
            elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Chestplate":
                player["held chestplate"] = item_input
                print("You are now wearing a/an ", player["held chestplate"])
            elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Leggings":
                player["held leggings"] = item_input
                print("You are now wearing a/an ", player["held leggings"])
            elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Boots":
                player["held boots"] = item_input
                print("You are now wearing a/an ", player["held boots"])
            elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Shield":
                player["held shield"] = item_input
                print("You are now wearing a/an ", player["held shield"])
    else:
        print("'" + startup_action + "' is not a valid option")


    print(" ")

def get_enemy_stats(player, item, enemy, map, map_location, lists):
    global enemy_singular, enemy_plural, enemy_max, enemy_health, enemy_max_damage, enemy_min_damage, enemy_agility, enemy_damage, choosen_item
    # load enemy stat

    list_enemies = lists[ map["point" + str(map_location)]["enemy type"]]

    choose_rand_enemy = random.randint(0, len(list_enemies) - 1)
    choose_rand_enemy = list_enemies[choose_rand_enemy]

    choosen_enemy = enemy[choose_rand_enemy]

    # enemy stats
    enemy_singular = choose_rand_enemy
    enemy_plural = choosen_enemy["plural"]
    enemy_max = choosen_enemy["health"]["max health level"]
    enemy_health = random.randint(choosen_enemy["health"]["min spawning health"], choosen_enemy["health"]["max spawning health"])
    enemy_max_damage = choosen_enemy["damage"]["max damage"]
    enemy_min_damage = choosen_enemy["damage"]["min damage"]
    enemy_damage = 0
    enemy_agility = choosen_enemy["agility"]

    # calculate enemy inventory stuff

    enemy_total_inventory = choosen_enemy["inventory"]
    enemy_items_number = len(enemy_total_inventory)
    choosen_item = enemy_total_inventory[random.randint(0, enemy_items_number - 1)]

    player["enemies list"].append(choose_rand_enemy)

def fight(player, item, enemy, map, map_location, enemies_remaining, lists):
    # import stats
    global turn, defend, fighting, already_encountered
    global enemy_singular, enemy_plural, enemy_max, enemy_health, enemy_max_damage, enemy_min_damage, enemy_agility, enemy_damage, choosen_item
    armor_protection = player["armor protection"]
    player_agility = player["agility"]
    # load and create enemies list type

    enemies_number = map["point" + str(map_location)]["enemy"]

    # while the player is still fighting (for run away)

    while fighting:

        # while player still alive
        while player["health"] > 0:
            while turn:

                # print HP stats and possible actions for the player

                print(str(COLOR_RED) + "Enemy: " + str(enemy_health) + str(COLOR_RESET_ALL) + "/" + str(COLOR_GREEN) + str(enemy_max) + str(COLOR_RESET_ALL) + "; " + str(COLOR_BLUE) + "You: " + str(player["health"]) + str(COLOR_RESET_ALL) + "/" + str(COLOR_GREEN) + str(player["max health"]) + str(COLOR_RESET_ALL))
                action = input("[A]ttack, [D]efend, [U]se Item? ")

                # if player attack
                if action.lower().startswith('a'):
                    player_damage = random.randint(0, int(item[player["held item"]]["damage"]))
                    if "ammo" in item[player["held item"]]:
                        if player["ammo"][item[player["held item"]]["ammo"]] > 0:
                            player["ammo"][item[player["held item"]]["ammo"]] -= 1
                        else:
                            print("Uh oh! You're out of ammo!")
                            player_damage = 0
                    print(" ")
                    # attack formula
                    enemy_dodged = False
                    enemy_dodge_chance = round(random.uniform(0.10, enemy_agility), 2)
                    if enemy_dodge_chance > round(random.uniform(.50, .90), 2):
                        enemy_dodged = True
                        print(f"The {enemy_singular} dodged your attack!")
                    if not enemy_dodged:
                        enemy_health -= player_damage
                        print(str(COLOR_RED) + "Enemy: " + str(enemy_health) + str(COLOR_RESET_ALL) + "/" + str(COLOR_GREEN) + str(enemy_max) + str(COLOR_RESET_ALL))
                        print("You dealt " + str(player_damage) + f" damage to the {enemy_singular}.")
                    turn = False

                # if player defend
                elif action.lower().startswith('d'):
                    print(" ")
                    defend += random.randint(0, int(item[player["held item"]]["defend"])) * player_agility
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
                        if item[item_input]["type"] == "Consumable" or item[item_input]["type"] == "Food":
                            if item[item_input]["healing level"] == "max health":
                                player["health"] = player["max health"]
                            else:
                                player["health"] += item[item_input]["healing level"]
                            player["max health"] += item[item_input]["max bonus"]
                            player["inventory"].remove(item_input)
                         # hold weapon/armor piece if it is one
                        if item_input in player["inventory"] and item[item_input]["type"] == "Weapon":
                            player["held item"] = item_input
                            print("You are now holding a/an ", player["held item"])
                        elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Chestplate":
                            player["held chestplate"] = item_input
                            print("You are now wearing a/an ", player["held chestplate"])
                        elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Leggings":
                            player["held leggings"] = item_input
                            print("You are now wearing a/an ", player["held leggings"])
                        elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Boots":
                            player["held boots"] = item_input
                            print("You are now wearing a/an ", player["held boots"])
                        elif item_input in player["inventory"] and item[item_input]["type"] == "Armor Piece: Shield":
                            player["held shield"] = item_input
                            print("You are now holding a/an ", player["held shield"])
                    print(" ")
                else:
                    print("'" + action + "' is not a valid option")
                    print(" ")
            # when it's not player turn
            while not turn:
                # if enemy is still alive
                if enemy_health > 0:
                    damage = random.randint(enemy_min_damage, enemy_max_damage) - defend * ( armor_protection * round(random.uniform(0.50, 0.90), 1) )
                    damage = round(damage)
                    defend = 0
                    player_dodged = False
                    player_dodge_chance = round(random.uniform(0.10, player_agility), 2)
                    if player_dodge_chance > round(random.uniform(.50, .90), 2):
                        player_dodged = True
                        print("You dodged your enemy attack!")
                    if damage > 0 and not player_dodged:
                        player["health"] -= damage
                        print("The enemy dealt ", str(damage), " points of damage.")
                    print("You have", str(player["health"]), "health points.")
                    print(" ")
                    turn = True
                else:
                    player["xp"] += enemy_max * enemy_max_damage / 3
                    player["health"] += random.randint(0, 3)
                    enemies_remaining -= 1
                    still_playing = False
                    return
        return



still_playing = True

# deinitialize colorama
deinit()
