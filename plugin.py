import yaml

def create_plugin(name):
    with open("TEMPLATE/map.yaml") as f:
        map_template = yaml.safe_load(f)

    dumped = yaml.dump(map_template)

    file = f"plugin/{name}/map.yaml"
    with open(file, "w") as f:
        f.write(dumped)

    with open("TEMPLATE/ammo.yaml") as f:
        ammo_template = yaml.safe_load(f)

    dumped = yaml.dump(ammo_template)

    file = f"plugin/{name}/ammo.yaml"
    with open(file, "w") as f:
        f.write(dumped)

    with open("TEMPLATE/enemies.yaml") as f:
        enemy_template = yaml.safe_load(f)

    dumped = yaml.dump(enemy_template)

    file = f"plugin/{name}/enemies.yaml"
    with open(file, "w") as f:
        f.write(dumped)

    with open("TEMPLATE/items.yaml") as f:
        item_template = yaml.safe_load(f)

    dumped = yaml.dump(item_template)

    file = f"plugin/{name}/items.yaml"
    with open(file, "w") as f:
        f.write(dumped)

    with open("TEMPLATE/lists.yaml") as f:
        list_template = yaml.safe_load(f)

    dumped = yaml.dump(list_template)

    file = f"plugin/{name}/lists.yaml"
    with open(file, "w") as f:
        f.write(dumped)

    with open("TEMPLATE/plot.yaml") as f:
        plot_template = yaml.safe_load(f)

    dumped = yaml.dump(plot_template)

    file = f"plugin/{name}/plot.yaml"
    with open(file, "w") as f:
        f.write(dumped)

    with open("TEMPLATE/start.yaml") as f:
        start_template = yaml.safe_load(f)

    dumped = yaml.dump(start_template)

    file = f"plugin/{name}/start.yaml"
    with open(file, "w") as f:
        f.write(dumped)

def create_map_point(x,y,folder):
    with open(f"plugin/{folder}/map.yaml") as f:
        points = yaml.safe_load(f)
    with open(f"plugin/{folder}/plot.yaml"):
        dialogs = yaml.safe_load(f)
    with open(f"plugin/{folder}/enemies.yaml") as f:
        enemies = yaml.safe_load(f)
    with open(f"plugin/{folder}/lists.yaml") as f:
        lists = yaml.safe_load(f)
    with open(f"plugin/{folder}/items.yaml") as f:
        items_list = yaml.safe_load(f)
    point = points["point0"]
    point["x"] = x
    point["y"] = y
    point["map zone"] = input("Map Zone: ")
    dialog = input("Enter a dialog name or hit 'n' to have no dialog.")
    if not dialog.lower().startswith("n"):
        if dialog in dialogs:
            point["dialog"] = dialog
        else:
            question = input("That dialog does not exist. Do you want to create a new dialog? ")
            if question.lower().startswith("y"):
                name = input("Please name your dialog: ")
                text = input("What will your dialog say? ")
                dialogs[name]["text"] = text
                point["dialog"] = dialog
    items = input("What item should the point have? ('None' for no items.)")
    if items in items_list:
        point["item"] = [items]
    else:
        question = input("That item does not exist. Create a new one? ")
        if question.lower().startswith("y"):
            name = input("Please name your item: ")
            item_types = ['Weapon','Consumable','Utility','Chestplate','Boots','Leggings','Shield','Bag','Food','Misc']
            item_type = input("What type of item will this be? ['Weapon','Consumable','Utility','Chestplate','Boots','Leggings','Shield','Bag','Food','Misc']")
            if item_type in item_types:
                items_list[name]["type"] = item_type
            # Finish this
    enemy_count = input("How many enemies? ")
    point["enemy"] = int(enemy_count)
    if int(enemy_count) > 0:
        enemy_type = input("What category of enemies? ")
        if enemy_type in lists:
            point["enemy type"] = enemy_type
        else:
            question = input("That list of enemies does not exist. Do you want to create one? ")
            if question.lower().startswith("y"):
                name = input("Please name the list: ")
                lists[name] = []
                point["enemy type"] = name
                # Note: add list creation and then enemy creation
    north = input("Can you go North? ")
    if north.lower().startswith("n"):
        point["blocked"].append("North")
    south = input("Can you go South? ")
    if south.lower().startswith("n"):
        point["blocked"].append("South")
    east = input("Can you go East? ")
    if east.lower().startswith("n"):
        point["blocked"].append("East")
    west = input("Can you go West? ")
    if west.lower().startswith("n"):
        point["blocked"].append("West")

    count = len(points)
    points[f"point{count}"] = point

    dumped = yaml.dump(points)

    with open(f"plugin/{folder}/map.yaml", "w") as f:
        f.write(dumped)