#Minecraft Text Game


from random import randint
from random import choice

#variables

location = "forest"

time = 0
day = 1

nighttime = 20
daytime = 36

moves = 0

health = 10

score = 0

luck = 1.0

cheats = False
cheated = False

done = False
win = -1
show_hearts = False


#all the items that the player can collect 
inventory = {
    "wood" : 0,
    "stone" : 0,
    "iron" : 0,
    "diamond" : 0,
    
    "stick" : 0,
    "bed" : 0,
    "crafting_table" : 0,
    
    "wooden_pickaxe" : 0,
    "stone_pickaxe" : 0,
    "iron_pickaxe" : 0,
    "diamond_pickaxe" : 0,

    "wooden_sword" : 0,
    "stone_sword" : 0,
    "iron_sword" : 0,
    "diamond_sword" : 0,

    "iron_armour" : 0,
    "diamond_armour" : 0,
    "dragon_armour" : 0,

    "apple" : 0,

    "meat" : 0,
    "rotten_flesh" : 0,
    "spider_eye" : 0,

    "satay" : 0,

    "potion_bottle" : 0,
    "health_potion" : 0,

    "eye_of_ender" : 0,
    "portal_frame" : 0,
    "end_portal" : 0,

    "dragon_egg" : 0,
    "dragon_skin" : 0
    
}

#tools that the player is using

pickaxe = "nothing"

sword = "nothing"
attack_damage = 1

armour = "nothing"
armour_protection = 0

#objects in the surroundings of locations

forest_surr = {
    "tree" : 8,
    "cave" : 1,
    "chest" : 0
}

cave_surr = {
    "stone" : float("inf"),
    "iron" : 0,
    "diamond" : 0,
    "chest" : 0
}


#mob info

forest_passive_mobs =  {}
forest_hostile_mobs = {}
cave_hostile_mobs = {}
end_hostile_mobs = {}
ed = {}

forest_passive_mob_cap = 3
forest_hostile_mob_cap = 2
cave_hostile_mob_cap = 2


#intro

def intro():
    print("""
Welcome to the Minecraft Text Game, a text-RPG based on Minecraft.
Please type "help" to find out more about the game.

Goal: kill the enderdragon
    """)


#experience / score
def gain_xp(amount):
    global score
    score += amount


#winning
def winning():
    if win >= 0:
        print("You have completed the game! Great job!\n")
        print("Moves taken to complete:", win)
        if cheated == False:
            
            #grades your winning
            if win <= 200:
                print("That is legendary!")
                gain_xp(100)
            elif win <= 300:
                print("That is epic!")
                gain_xp(80)
            elif win <= 400:
                print("That is superb!")
                gain_xp(50)
            elif win <= 500:
                print("That is awesome!")
                gain_xp(20)
            else:
                print("That is great!")
        else:
            print("That is great!")
        print("")


#updating items

#when you get new items, will check and update the current tools you are using
#if you have a better tool
        
def update_pickaxe(m, e=""):
    global pickaxe
    
    changed = False
    if m == "diamond_pickaxe":
        if pickaxe != m:
            pickaxe = m
            changed = True
    elif m == "iron_pickaxe":
        if pickaxe=="wooden_pickaxe" or pickaxe=="stone_pickaxe" or \
           pickaxe=="nothing":
            pickaxe = m
            changed = True
    elif m == "stone_pickaxe":
        if pickaxe == "wooden_pickaxe" or pickaxe == "nothing":
            pickaxe = m
            changed = True
    elif m == "wooden_pickaxe":
        if pickaxe == "nothing":
            pickaxe = m
            changed = True
    if changed:
        print("You are now using", m, e)

def update_sword(m, e=""):
    global sword
    global attack_damage

    changed = False
    
    if m == "diamond_sword":
        if sword != m:
            sword = m
            attack_damage = 10
            changed = True
            
    elif m == "iron_sword":
        if sword=="wooden_sword" or sword=="stone_sword" or \
           sword=="nothing":
            sword = m
            attack_damage = 7
            changed = True
            
    elif m == "stone_sword":
        if sword == "wooden_sword" or sword == "nothing":
            sword = m
            attack_damage = 5
            changed = True
            
    elif m == "wooden_sword":
        if sword == "nothing":
            sword = m
            attack_damage = 3
            changed = True
            
    if changed:
        print("You are now using ", m, " (", \
              attack_damage, " attack damage)"+e, sep = "")

    
def update_armour(m, e = ""):
    global armour
    global armour_protection

    changed = False
    
    if m == "diamond_armour":
        if armour == "nothing" or armour =="iron_armour":
            armour = m
            armour_protection = 3
            changed = True
            
    elif m == "iron_armour":
        if armour=="nothing":
            armour = m
            armour_protection = 2
            changed = True
    elif m == "dragon_armour":
        if armour != m:
            armour = m
            armour_protection = 4
            changed = True
            
    if changed:
        print("You are now eqquiped with ", m, " (", \
              armour_protection, " protection)"+e, sep = "")



#crafting

#all the crafting recipes
crafting = {

    #crafted item : {
    #   ingredient 1 : amount, ingredient 2 : amount ...
    #}
    "stick" : {
        "wood" : 1
    },
    
    "wooden_pickaxe" : {
        "stick" : 1, "wood" : 2
    },
    
    "stone_pickaxe" : {
        "stick" : 1, "stone" : 2
    },

    "iron_pickaxe" : {
        "stick" : 1, "iron" : 2
    },
    
    "diamond_pickaxe" : {
        "stick" : 1, "diamond" : 2
    },
    
    "bed" : {
        "wood" : 3
    },

    "crafting_table" : {
        "wood" : 4
    },

    "wooden_sword" : {
        "stick" : 1, "wood" : 1
    },
    
    "stone_sword" : {
        "stick" : 1, "stone" : 1
    },

    "iron_sword" : {
        "stick" : 1, "iron" : 1
    },
    
    "diamond_sword" : {
        "stick" : 1, "diamond" : 1
    },

    "iron_armour" : {
        "iron" : 3
    },

    "diamond_armour" : {
        "diamond" : 3
    },
    "health_potion" : {
        "potion_bottle" : 1, "spider_eye" : 1
    },
    "portal_frame" : {
        "stone" : 4, "iron" : 2, "diamond" : 1
    },
    "end_portal" : {
        "eye_of_ender" : 3, "portal_frame" : 3
    },
    "satay" : {
        "meat" : 1, "stick" : 1
    },
    "dragon_armour" : {
        "dragon_skin" : 1
    }
    

}

#shows a specific crafting recipe in the format
# (amount) ingedient + (amount) ingredient + ... => output
def print_crafting(m, e="\n"):
    x = crafting[m]
    n = len(x)
    count = 0
    for i in x:
        count += 1
        if x[i] == 1:
            #omits coefficient if only 1
            print(i, end=" ")
        else:
            print(x[i], i, end=" ")
        if count <= n-1:
            print("+ ", end="")
    print("=>", m, end=e)    


def craft(m):

    #alternative spellings 
    if m == "sticks":
        m = "stick"
    elif m == "wood_pickaxe":
        m = "wooden_pickaxe"
    elif m == "wood_sword":
        m = "wooden_sword"
    if m[-5:] == "armor":
        m = m[:-5]+"armour"

    if not m in inventory:
        print("No such item\n")
        return -1
        
    if not m in crafting:
        print("You cannot craft \"", m, "\"\n", sep="")
        return -1

    recipe = crafting[m]

    #checking the player has enough ingredients
    for ingredient in recipe:
        if inventory[ingredient] < recipe[ingredient]:
            print("Cannot craft " + m + ": not enough " + ingredient)
            print_crafting(m)
            print("You only have:", inventory[ingredient], ingredient)
            print("")
            return -1

    print("Crafted " + m + "!")
    print_crafting(m)
    inventory[m] += 1
    for ingredient in recipe:
        inventory[ingredient] -= recipe[ingredient]
        print(ingredient, "left:", inventory[ingredient])

    #if crafted a better tool, or armour, will need to update
    update_pickaxe(m)
    update_armour(m)
    update_sword(m)
    return 0



#help 

#0: General
def help0():
    print(
"""
0 : General

This is a text RPG with flexible gameplay. This game is based on Minecraft, a popular sandbox video game by Mojang. 

In this game, you can collect resources from the world by using the "mine" command. You can use these resources to make further equipment such as tools, weapons and armour by using the "craft" command. 

There is an in-game time, which increments for every successful active move you make. For times 0 to 19, it is daytime. For times 20 to 35, it is nighttime and the cycle repeats afterwards. In the daytime, trees grow, animals like pigs spawn and the player can collect resources. At night, hostile mobs (monsters) such as zombies and endermen start to spawn and will attack the player. The player has 10 health. The player can battle these mobs and they may even drop valuable resources upon death. However, if the player is killed, the game ends. The player can choose to skip the night by sleeping in a bed. 

The goal of the game is to journey to the end and kill the enderdragon, an evil boss mob. 

In the following rough guide, commands that can be typed to perform the actions are shown in [""].

The player begins in the forest location, where trees will grow and mobs (creatures) can spawn. The player can begin by collecting wood ["chop tree" or "mine tree"]. The wood can be used to craft a wooden_pickaxe ["craft wooden_pickaxe"] which allows the player to mine stone. 

The player can enter the cave ["enter cave"] and mine stone ["mine stone"]. The cave can randomly generate other valuable resources such as iron and diamond. diamond can only generate from the second day and after. spider is a hostile mob that can spawn in the cave, even in the daytime. However, they deal much less damage in the daytime than nighttime. 

The player can exit the cave ["exit"] and use the stone collected to craft other tools such as stone_pickaxe ["craft stone_pickaxe"] and stone_sword ["craft stone_sword"]. A stone_pickaxe is required to mine iron ["mine iron"], and an iron_pickaxe is required to mine diamond ["mine diamond"]. 

pig is a friendly mob (creature) that spawns in the forest randomly. When mobs spawn, you will see a message like "You see a (mob type), (mob name)". e.g. "You see a pig, pig0". Mob names are assigned as follows: pig0, pig1, pig2, pig3 etc. The player can attack mobs ["attack (mob name)" or "kill (mob name)"]. The damage that is dealt is determined by the current sword that the player has. Remember that hostile mobs such as spider and zombie can attack the player too! For more info about the mobs, see "Mobs". For more info on swords and armour, see "Items". For more info on how to make these items and others, see "Crafting"

The pig drops meat upon death. Meat can be eaten ["eat meat"] to heal health. Sometimes trees also give you apple which can also be eaten to heal health ["eat apple"]. 

Chests can generate rarely in the forest or cave. You can open them ["open chest"] and you may get valuable loot!

When the in-game time reaches 20, it becomes nighttime and hosile mobs will begin to spawn. The hostile mobs are zombie, witch and enderman. witch and enderman are much stronger and will only spawn from the second night onwards. For more information about these mobs, see "Mobs". To avoid facing these mobs, the player can make a bed ["craft bed"] and sleep ["sleep"]. 

The enderman, a mob that spawns from the second night and after, drops eye_of_ender upon death, which can be used to craft end_portal ["craft end_portal"] to allow the player to journey to the end ["enter end"] to battle the enderdragon. For more info about the end, see "End". The witch drops many useful items such as potion_bottle which can be used to make health_potion ["craft health_potion"]. For more info on how to make these items, see "Crafting". For more info on what these items do, see "Items"
""")


#1: commands
def help1():

    u = input("Show detailed version? (Y/N): ")
    print("""
Commands are what you type to perform actions in the game. You can type commands after the "==>" prompt. 

Commands are not case-sensitive. Those that require an object, location etc. following the keyword are required to be seperated by a space. Items that contain multiple words are to be separated by an underscore (_) e.g. "wooden_pickaxe". 

The following is the list of all commands. 
""")
    if u == "Y":
        print("""
quit / done
Exits the game. A confirm message will be displayed. 

hearts 
Toggles whether to show the player's health using hearts every move. This is off by default. Here is an example hearts of a player with 7 health:
(\/)(\/)(\/)(\/)(\/)(\/)(\/)::::::::::::
 \/  \/  \/  \/  \/  \/  \/  ::  ::  :: 
 
details 
Shows details (time, moves, location, health, pickaxe, sword, armour)

help
Displays help information 

time / t
Displays the in-game time. Format: Time: [numerical value] ([day or night]); Day [day number]
Remember that time 0-19 is daytime and 20-35 is nighttime. The cycle repeats afterwards. Note that there is no time in the end. 

moves
Displays the number of moves the player has made

location / where
Displays where the player is (forest, cave or end)

health / h
Displays the amount of health the player has. Maximum health: 10

pickaxe / pick / pic / tool / tools
Displays the best pickaxe that the player has, and is the one that will be used to mine objects

sword / weapon 
Displays the best sword that the player has, and is the one that will be used to attack mobs (creatures)

armour / armor / protection
Displays the best armour that the player has, and is the one that will be used to block damage from attacks

view / look / v
Displays the objects and mobs in the surroundings of the location that the player is in

inventory / i / e
Displays the player's inventory, i.e. the objects that the player has

*mine / break / destroy / harvest / gather / dig / m / collect / take / get / chop / cut (object)
Destroys an object in the game world and collects items yielded 
e.g. mine stone, chop tree

*go / enter / goto / go_to / into (location)
Changes player's location if the location is accessible
e.g. (from forest) enter cave, (from forest, with an end_portal) enter end

*out / return / back / escape
Changes player's location back to the forest if possible
e.g. (from cave) exit (equivalent to "enter forest")

*craft / make / create / c / brew (item) 
Creates item by combining resources if possible (this consumes the ingredients). For more information on what is required to craft certain items, see "Crafting". A crafting_table is required for crafting in locations other than the forest. 

*wait / w
Does nothing and allows time to pass. This also allows ores to generate, trees to grow, mobs to spawn and attack etc. 

*sleep
Allows the player to skip the night and changes the time directly to the next day. This requires a bed. You can only sleep at night and in the forest and when there are no hostile mobs around. 

*attack / kill / fight / k (mob name)
Attacks the mob with the player's sword. Remember to type the mob name in full (e.g. zombie0, pig1)

*eat / drink / consume (food)
Consumes the food and heals health. 

cheats (on/off, true/false)
Changes whether cheats are turned on for the game. Cheats enable you to perform cheating commands, and can be used for testing purposes. Cheats are off by default. If you enable cheats any time during the game, it will be reflected when the game is over. 

give (item) [amount]
Requires cheats to be turned on. Gives the player the item and that amount (1 if unspecified). You can enter "give gear" to obtain all diamond tools and armour, food, health_potion, and end_portal. 

spawn / summon (mob type)
Requires cheats to be turned on. Spawns the given mob. Due to limitations, this command only works in the location where the mob originally spawns. 

heal / set_health (integer health amount)
Requires cheats to be turned on. Changes your health to the given health amount, capped at 10. This will kill you if you input 0 or a negative integer. 

luck / set_luck (floating number or integer luck value)
Requires cheats to be turned on. Changes the in-game "luck" value to the given value. By default, it is 1.0. The luck value infuences the probablilty of certain random beneficial events in the game such as generating chests. The higher the luck, the more likely. 


*Asterisks mark active moves that will allow 1 unit of time to pass.
""")
    
    else:
        print("""
quit
hearts
details 
help
time
moves
location
health
pickaxe
sword
armour
view
inventory
mine (object)
go (location)
back 
craft (item)
wait
sleep
attack (mob name)
eat (food item)
""")

#2 : Items
def help2():
    u = input("Show detailed version? (Y/N): ")
    
    print("""
2 : Items

Items are objects that the player can collect and keep in their inventory. Enter "inventory" or "i" or "e" to check your inventory. 

Items have many uses. Some items can be obtained from crafting and other can be used to craft other items. Some items can be eaten to heal health. 

Pickaxes are required to mine certain objects. Swords are what determine the damage dealt to mobs when you attack them. Armour will block damage from mob attacks. 

The player begins with no pickaxe, no sword (which deals 1 damage) and no armour. When pickaxes, swords and armour are crafted, the game will automatically update the current pickaxe, armour or sword that the player is using or eqquipped with, if the new one is better than the current one. Hence, the game will automatically ensure that the player is always using the best pickaxe, armour or weapon all the time. You can check your current pickaxe, sword or armour by typing "pickaxe", "sword" or "armour".

Remember to spell items correctly and with an underscore if it has multiple words (e.g. wooden_pickaxe) when typing commands. 

The following is a list of items, in the order that they appear in the inventory. 
""")
    if u == "Y":
        print("""
wood
Obtained from harvesting trees. Can be used to craft sticks and wooden tools. 

stone
Obtained from mining stone in the cave. Can be used to craft stone tools and portal_frame. 

iron 
Obtained from mining iron in the cave. Iron generates randomly in the cave. When iron generates, you will be notified with a message "You found iron". Can be used to craft iron_armour, iron_pickaxe, iron_sword, and portal_frame

diamond
Obtained from mining diamond in the cave. Diamond generates randomly in the cave from the second day onwards. When diamond generates, you will be notified with a message "You found diamond". Can be used to craft diamond_armour, diamond_pickaxe, diamond_sword, and portal_frame

stick
Crafting: wood => stick
Can also be obtained by harvesting a tree. Used to craft pickaxes and swords. 

bed
Crafting: 3 wood => bed
This is needed to sleep at night to skip to the nest day. Remember that you can only sleep at night and in the forest and when you have full health. 

crafting_table
Crafting: 4 wood => crafting_table
This is needed to craft items when not in the forest. For each use of the crafting_table, there is a small chance that it will break and be consumed.

wooden_pickaxe
Crafting: stick + 2 wood => wooden_pickaxe
Can be used to mine stone

stone_pickaxe
Crafting: stick + 2 stone => stone_pickaxe
Can be used to mine stone and iron

iron_pickaxe
Crafting: stick + 2 iron => iron_pickaxe
Can be used to mine stone, iron and diamond

diamond_pickaxe
Crafting: stick + 2 diamond => diamond_pickaxe
Can be used to mine stone, iron and diamond

wooden_sword
Crafting: stick + wood => wooden_sword
Deals 3 damage

stone_sword
Crafting: stick + stone => stone_sword
Deals 5 damage

iron_sword
Crafting: stick + iron => iron_sword
Deals 7 damage

diamond_sword
Crafting: stick + diamond => diamond_sword
Deals 10 damage

iron_armour
Crafting: 3 iron => iron_armour
Blocks 2 damage from each mob attack

diamond_armour
Crafting: 3 diamond => diamond armour
Blocks 3 damage from each mob attack

dragon_armour
Crafting: dragon_skin => dragon_armour
Obtained by crafting using dragon_skin, dropped by the enderdragon upon death. Blocks 4 damage from each attack

apple
Drops ocasionally when harvesting a tree and drops sometimes by witch upon their death. Can be eaten to heal 3 health

meat
Dropped by pigs when they die. Can be eaten to heal 2 health. Can also be crafted into satay 

rotten_flesh
Dropped by zombies when they die. Can be eaten to heal 1 health

spider_eye
Dropped by spiders when they die, and occasionally, witches. If you eat it, you will be poisoned of 2 health. Can be used to craft health_potion. 

satay
Crafting: meat + stick => satay
Can be eaten to heal 3 health

potion_bottle
Dropped by witches when they die. Can be used to craft health_potion. 

health_potion
Crafting: potion_bottle + spider_eye => health_potion
Can be consumed to heal 8 health.

eye_of_ender
Dropped by endermen when they die. Can be used to craft end_portal to journey to the end.

portal_frame
Crafting: 4 stone + 2 iron + diamond => portal frame
Used to craft end_portal to journey to the end.

end_portal
Crafting: 3 eye_of_ender + 3 portal_frame => end portal
Needed to journey to the end to fight the enderdragon boss mob.

dragon_egg
Collected by successfully defeating the enderdragon

dragon_skin
Collected by successfully defeating the enderdragon. Can be used to craft dragon_armour, the most powerful armour
""")
    else:
        print("""
wood
stone
iron
diamond
stick
bed
crafting_table
wooden_pickaxe
stone_pickaxe
iron_pickaxe
diamond_pickaxe
wooden_sword
stone_sword
iron_sword
diamond_sword
iron_armour
diamond_armour
dragon_armour
apple
meat
rotten_flesh
spider_eye
satay
potion_bottle
health_potion
eye_of_ender
portal_frame
end_portal
dragon_egg
dragon_skin
""")

#3 : Crafting
def help3():
    print("""
3 : Crafting

Crafting is done by using the "craft" command. You must also specify the item that you are crafting. 

You need to have a crafting_table to craft items when not in the forest, e.g. in the cave. When doing so, there is a small chance that the crafting_table will break and be consumed. 

The following is a list of all the items that can be crafted and what is needed to do so. For more info on these items, see "Items".


wood => stick
stick + 2 wood => wooden_pickaxe
stick + 2 stone => stone_pickaxe
stick + 2 iron => iron_pickaxe
stick + 2 diamond => diamond_pickaxe
3 wood => bed
4 wood => crafting_table
stick + wood => wooden_sword
stick + stone => stone_sword
stick + iron => iron_sword
stick + diamond => diamond_sword
3 iron => iron_armour
3 diamond => diamond_armour
potion_bottle + spider_eye => health_potion
4 stone + 2 iron + diamond => portal_frame
3 eye_of_ender + 3 portal_frame => end_portal
meat + stick => satay
dragon_skin => dragon_armour
""")

#4 : Mobs
def help4():
    print("""
4 : Mobs

Mobs are creatures that spawn (appear) randomly in their spawning location if the player is in that location too. When a mob spawns, you will see the message "You see a (mob type), (mob name)" e.g. "You see a pig, pig0". Mob names are assigned as follows: pig0, pig1, pig2, pig3 etc. 

Mobs have health. The player can attack mobs by using the "attack" command, followed by the mob name. The damage that is dealt is determined by the current sword that the player has. When mobs die, they have a chance to drop certain items, some can be highly valuable. 

Hostile mobs will also begin to attack the player one unit of time after spawning, continuing to do so every unit of time afterwards until they are killed or the player is, or the player moves to another location. The damage dealt will be reduced if the player is equipped with armour.  

Mobs begin to attack the player 1 unit of time after spawning, so it is not immediate. Since attacking mobs is processed before mob attacking players, if you kill a mob in one hit, it will not have the chance to attack you. 

Mobs cannot change their location, i.e. they cannot follow the player into the cave or into the end. 

Only one mob of the same type spawns at once, but different mobs can spawn at the same time. Multiple mobs can appear and attack simultaneously. There is a mob cap that prevents too many mobs to appear at once, however the hostile mob cap is increased as time goes by. If you wish to avoid facing mobs at night, you can choose to sleep to skip the night.

Mobs can also spawn by using the "spawn" or "summon" command, which needs cheats to be turned on. 

The following is a list of all the mob types. 


pig
Friendly
Spawning: forest, anytime,lower chance at night
Drops: 1-3 meat 
Health: 4

zombie 
Hostile
Spawning: forest, at night
Burns in sunlight in the day
Drops: 0-2 rotten_flesh, 0-1 iron (very rare)
Health: 10
Attack damage: 2
Has a small chance of attacking through armour

spider
Hostile
Spawning: cave, anytime, much higher chance at night and on second day onwards
Drops: 0-2 spider_eye 
Health: 8
Attack damage: 1-2 (daytime), 2-5 (nighttime)

enderman
Hostile
Spawning: forest, at night, day 2 and after only, in the end, when the enderdragon summons them mid-battle (see "End")
Drops: 0-2 eye_of_ender, 0-1 diamond (very rare)
Health: 20
Attack damage: 4-5
Has a small chance to not attack 

witch
Hostile
Spawning: forest, at night, day 2 and after only
Drops: 1-2 potion_bottle, 0-1 spider_eye, 0-1 apple, 0-1 health_potion (rare)
Health: 15
Attack damage: 3-4
Can heal itself
""")


def help5():
    print("""
5 : End

To win the game, the player has to journey to the end to kill the enderdragon. To do so, the player must make an end_portal. See the following crafting recipes:

4 stone + 2 iron + diamond => portal_frame

3 eye_of_ender + 3 portal_frame => end_portal

eye_of_ender is dropped by endermen upon death. 

You cannot return to the forest once you are in the end, until you defeat the enderdragon. If you do so, you can return to the forest. After that, if you enter the end again, another enderdragon will spawnand you also cannot leave until you defeat it. Each enderdragon you kill will drop a dragon_skin, but only the first one will drop the dragon_egg


enderdragon

Health: 200
Example health bar:
                    ENDERDRAGON
+--------------------------------------------------+
|////////////////////////////////////////          |
+--------------------------------------------------+

Name: enderdragon or ed

Spawing: end, once when the player enters

Drops: dragon_egg (first enderdragon only), dragon_skin

Behaviour:

When the dragon is above half health, it is in stage 1. When the dragon is below half health, it is in stage 2. When the enderdragon reaches half health, it will fly off and summon 3 endermen, and only come back when they are killed. 

For stage 1, the enderdragon attacks once every unit of time for 3 consecutive units of time, then flies off for 1 unit of time. For stage 2, the enderdragon attacks once every unit of time for 4 to 5 consecutive units of time and flies off for 2 units of time. 

The enderdragon cannot attack or be damaged when it is flown off. For each unit of time that enderdragon is flying off, it will regenerate 1-3 health (stage 1) or 3-5 health (stage 2). 

When attacking, out of each group of 3-4 attacks, exactly one will be an acid attack (acid breath) and the rest will be melee attacks (bumping into you).

Acid attack damage: 5 - 7 
Melee attack damage: 4 (stage 1), 4 - 5 (stage 2)


When the enderdragon is killed, you will gain the dragon_egg, and will be prompted to return to the forest, which completes the game. You can carry on playing though. 

Just for fun, we grade your performance based on your number of moves taken to complete the game. (Only if you did not turn on cheats)

<= 200: legenday! 
201 - 300: epic!
301 - 350: superb!
401 - 500: awesome!
> 500: great!
""")

def show_help():

    v = input("""

Help Page

0 : General
1 : Commands
2 : Items 
3 : Crafting
4 : Mobs 
5 : End

Which section do you wish to view? (0 to 5): """)

    if v == "0":
        help0()
    elif v == "1":
        help1()
    elif v == "2":
        help2()
    elif v == "3":
        help3()
    elif v == "4":
        help4()
    elif v == "5":
        help5()
    else:
        print("Exited help page")



#location description

def desc_location(line1=True):
    if location == "forest":
        if line1:
            print("You are in a forest")

        for x in forest_surr:
            if forest_surr[x] == 1:
                print("There is a", x)
            elif forest_surr[x] > 1:
                print("There are", forest_surr[x], x+'s')
        for x in forest_passive_mobs:
            print("There is a ", forest_passive_mobs[x]["type"],\
                  ", ", x, sep="")
        for x in forest_hostile_mobs:
            print("There is a ", forest_hostile_mobs[x]["type"], \
                  ", ", x, sep="")

    elif location == "cave":
        if line1:
            print("You are in a cave")

        for x in cave_surr:
            if x == "stone":
                print("There is stone")
            elif cave_surr[x] > 0:
                print("There is", cave_surr[x], x)
        for x in cave_hostile_mobs:
            print("There is a ", cave_hostile_mobs[x]["type"], \
                  ", ", x, sep="")
            
    elif location == "end":
        if line1:
            print("You are in the end")
        if ed != {}:
            print("There is the enderdragon, ", end = "")
            if ed["active"]:
                print("ready to attack")
            else:
                print("flying around")
        for x in end_hostile_mobs:
            print("There is an ", end_hostile_mobs[x]["type"], \
                  ", ", x, sep="")


#details display

def print_time(e):
    print("Time: ", end="")
    if time < 0:
        print("undefined", end=e)
    elif time < nighttime:
        print(time, "(day); Day", day, end=e)
    else:
        print(time, "(night); Day", day, end=e)


def print_moves(e):
    print("Moves:", moves, end=e)


def print_location(e):
    print("Location:", location, end=e)


def print_health(e):
    print("Health:", health, end=e)
    
def print_pickaxe(e):
    print("Pickaxe:", pickaxe, end=e)

def print_sword(e):
    print("Sword: ", sword, " (", attack_damage, " attack damage)",\
          sep="",end=e)

def print_armour(e):
    print("Armour: ", armour, " (", armour_protection, \
          " protection)", sep="", end=e) 

def print_details():
    t = "   |   "
    print_time(t)
    print_moves(t)
    print_location(t)
    print_health("\n")
    print_pickaxe(t)
    print_sword(t)
    print_armour("\n")

def print_hearts():
    # (\/)(\/)::::
    #  \/  \/  :: 
    s = health*"(\/)"
    s += (10-health)*"::::" + "\n"
    s += health*" \/ "
    s += (10-health)*" :: "
    print(s)

#time

def check_time():
    global time
    global day
    global forest_hostile_mob_cap
    global cave_hostile_mob_cap

    if location == "end":
        time == -1    
    elif time == nighttime:
        #prints a message when it reaches night time
        print("\nIt is now night! Sleep or beware of monsters!")
    elif time == daytime:
        time = 0
        day += 1
        #prints a message when it reaches day time (new day)
        print("\nIt is now day. It is day", day)

        if day == 2:
            forest_hostile_mob_cap = 3
            cave_hostile_mob_cap = 3
        elif day == 3:
            forest_hostile_mob_cap = 4
            

def sleep():
    global time
    global day

    #need to have a bed
    if inventory["bed"] == 0:
        print("You need to have a bed to sleep\n")
        return -1
    #need to be at night
    if time < nighttime:
        print("You can only sleep at night\n")
        return -1
    #need to be in the forest
    if location != "forest":
        print("You can only sleep in the forest\n")
        return -1
    #need to have no hostile mobs around
    if len(forest_hostile_mobs)>0:
        print("You may not rest now, there are monsters nearby\n")
        return -1
    
    print("zzz...")
    time = -1
    day += 1
    print("You have skipped to the day. It is day", day)
    


#health


def die():
    #called when health decreased to 0
    global health
    global done
    
    if health > 0:
        print("Error, you did not die")
        return
    health = 0
    done = True
    #ends the game


def heal_health(amount):
    global health
    health += amount
    if health > 10:
        health = 10
    print("You now have", health, "health")


def damage_health(amount):
    global health
    health -= amount 
    if health <= 0:
        health = 0
    print("You now have", health, "health")
    


#generating objects

def generate_iron():
    global cave_surr
    #chance to generate iron
    if randint(1, 100) <= 25*luck:
        print("\nYou find iron")
        cave_surr["iron"] += 1


def generate_diamond():
    global cave_surr
    #only start generating diamonds from day 2
    if day == 1:
        return
    #chance to generate diamonds
    if randint(1, 100) <= 14*luck:
        print("\nYou find diamond!")
        cave_surr["diamond"] += 1
        
    
def generate_ores():
    generate_iron()
    generate_diamond()

def grow_trees():
    #only grow trees in day time
    if time >= nighttime:
        return
    global forest_surr
    if forest_surr["tree"] >= 10:
        return

    chance = 10
    if day > 1:
        chance += 10
    chance += max(0,5*(8-forest_surr["tree"])//2)
    
    if randint(1, 100) <= chance*luck:
        print("\nA tree has grown")
        forest_surr["tree"] += 1

#treasure chests generated randomly
def generate_chest():
    global cave_surr
    global forest_surr
    surr  = {}
    if location == "forest":
        surr = forest_surr
    elif location == "cave":
        surr = cave_surr
    else:
        return
    #will not generate if already have a chest
    if surr["chest"] > 0:
        return
    
    chance = 3
    if randint(1, 100) <= chance*luck:
        surr["chest"] += 1
        print("\nYou find a chest. There may be treasure inside!")


#chest loot
        
chest_loot = [
[ #0 : common loot 
    ("wood", (8, 16)),
    ("apple", (3, 5)),
    ("rotten_flesh", (4, 10)),
    ("stick", (2, 5)),
    ("crafting_table", (1, 3)),
    ("spider_eye", (1, 4))
],
[ #1 : tools loot
    "stone_pickaxe",
    "stone_sword",
    "iron_pickaxe",
    "iron_sword",
    "iron_armour",
    "diamond_pickaxe", 
    "diamond_sword", 
    "diamond_armour",
    "wooden_sword",
    "wooden_pickaxe"
], 
[ #2 : rare loot
    ("iron", (2, 5)),
    ("stone", (16, 26))
], 
[ #3 : epic loot
    ("diamond", (1, 2)),
    ("health_potion", (1, 1)),
    ("portal_frame",(1, 1)),
    ("eye_of_ender", (1, 1))
] ]

def open_chest():
    global inventory
    global cave_surr
    global forest_surr

    #checking there is a chest
    surr  = {"chest" : 0}
    if location == "forest":
        surr = forest_surr
    elif location == "cave":
        surr = cave_surr

    if surr["chest"] < 1:
        print("There is no chest here\n")
        return -1
    surr["chest"] -= 1 

    nothing = True
    #the amount of loot from each category
    loot_amount = [randint(0, 2), randint(0, 2), randint(0, 2), 0]
    if randint(1, 100) <= 30:
        loot_amount[3] = 1
        if randint(1, 100) <= 25:
            loot_amount[3] += 1

    #duplicate the list because we will remove elements
    loot2 = []
    for i in chest_loot:
        v=[]
        v.extend(i)
        loot2.append(v)
        
    loot2.extend(chest_loot)
    
    #i is the category
    for i in range(4):
        #in category i, we choose loot_amount[i] things
        for j in range(loot_amount[i]):
            
            #choose a random (item : (lo, hi)) from loot2[i]
            l = choice(loot2[i])
            item = l
            k = 0
            if i == 1:
                k = 1
            if i != 1:
                #if in other categories, we choose based on the lower and
                #upper bound
                item = l[0]
                k = randint(l[1][0], l[1][1])

            #remove the chosen item so no duplicates
            loot2[i].remove(l)
            
            print("You got", k, item)
            nothing = False
            inventory[item] += k
            
            update_armour(item)
            update_pickaxe(item)
            update_sword(item)
            
    #if there is nothing
    if nothing:
        print("You got nothing :(")
    return 0
    

#mobs


#mob death

#mob drops
# mob type : {
#   drop item : {
#       quantity : percent chance } } 

mob_drops = {
    "pig" : {
        "meat" : {
            1 : 33,
            2 : 50,
            3 : 100
        }
    },
    "zombie" : {
        "rotten_flesh" : {
            1 : 33,
            2 : 50
        },
        "iron" : {
            1 : 6
        }
    },
    "spider" : {
        "spider_eye" : {
            1 : 33,
            2 : 50            
        }
    },
    "enderman" : {
        "eye_of_ender" : {
            1 : 33,
            2 : 50
        },
        "diamond" : {
            1 : 5
        }
    },
    "witch" : {
        "potion_bottle" : {
            1 : 50,
            2 : 100,
        },
        "spider_eye" : {
            1 : 50
        },
        "apple" : {
            1 : 50
        },
        "health_potion" : {
            1 : 10
        }
    }    
}


def kill_mob(m, moblist):
    global forest_passive_mobs
    global forest_hostile_mobs
    global cave_hostile_mobs
    global end_hostile_mobs
    global inventory

    print(m, "died")
    
    mob_type = moblist[m]["type"]
    drops = mob_drops[mob_type]

    #drop all items
    for drop_item in drops:
        for drop_amount in drops[drop_item]:
            chance = drops[drop_item][drop_amount]
            if randint(1, 100) <= chance*luck:
                print(m, " dropped ", drop_amount, " ", drop_item, \
                      ". You gain ", drop_amount," ", drop_item, sep="")
                inventory[drop_item] += drop_amount
                break
    moblist.pop(m)

    if mob_type == "pig":
        gain_xp(2)
    elif mob_type == "zombie":
        gain_xp(5)
    elif mob_type == "enderman" or mob_type == "witch":
        gain_xp(8)
    elif mob_type == "spider":
        gain_xp(3)

    

def attack_mob(m):
    global forest_passive_mobs
    global forest_hostile_mobs
    global cave_hostile_mobs
    global end_hostile_mobs
    moblist = {}
    
    if location == "forest":
        
        if m in forest_passive_mobs:
            moblist = forest_passive_mobs
        elif m in forest_hostile_mobs:
            moblist = forest_hostile_mobs
        else:
            print("There is no ", m, " here\n", sep="\"")
            return -1
        
    elif location == "cave" :
        moblist = cave_hostile_mobs
        if not m in moblist:
            print("There is no ", m, " here\n", sep="\"")
            return -1

    elif location == "end":
        moblist = end_hostile_mobs
        if not m in moblist:
            print("There is no ", m, " here\n", sep="\"")
            return -1
            
    
    print("You attacked ", m, " with ", sword, ". ", sep="", end="")
    print("You dealt", attack_damage, "damage")

    moblist[m]["health"] -= attack_damage
    #if health reaches 0, kill it
    if moblist[m]["health"] <= 0:
        kill_mob(m, moblist)
    
    else:
        print(m, "has", moblist[m]["health"], "health left")


    return 0
    


#pig

pig_count = 0

def spawn_pig():
    global pig_count
    new_pig = {"type" :  "pig",
                "health" : 4,
                "lifetime" : 0}
    name = "pig" + str(pig_count)
    forest_passive_mobs[name] = new_pig
    print("\nYou see a pig,", name)
    pig_count += 1

def move_pig(m):
    global forest_passive_mobs
    moblist = forest_passive_mobs
    moblist[m]["lifetime"] += 1

#zombie

zombie_count = 0


def spawn_zombie():
    global zombie_count
    new_mob = {"type" :  "zombie",
                "health" : 10,
                "lifetime" : 0}
    name = "zombie" + str(zombie_count)
    forest_hostile_mobs[name] = new_mob
    print("\nYou see a zombie,", name)
    zombie_count += 1      

def move_zombie(m):
    global forest_hostile_mobs
    moblist = forest_hostile_mobs
    moblist[m]["lifetime"] += 1
    
    damage = 2

    #small chance to attack through armour
    if armour_protection > 0 and  randint(1, 100) <= 22:
        print("\n", m, " attacked you through your armour! "\
                "You take ", damage, " damage", sep = "")
        damage_health(damage)
        if health <= 0:
            print("You were slain by zombie")
            die()
    else:
        #armour reduces damage, but cap at 0
        damage_taken = max(0, damage - armour_protection)
        print("\n", m, " attacked you! You take ", damage ," - ", armour_protection, \
          " = ", damage_taken, " damage", sep = "")
        damage_health(damage_taken)
        if health <= 0:
            print("You were slain by a zombie")
            die()

    if time < nighttime:
        damage = randint(4, 7)
        print("")
        print(m, "burnt in sunlight. It takes", damage, "damage")
        moblist[m]["health"] -= damage
        if moblist[m]["health"] <= 0:
            return "kill"
        else:
            print(m, "has", moblist[m]["health"], \
                "health left")
    
    return ""

#spider

spider_count = 0


def spawn_spider():
    global spider_count
    
    new_mob = {"type" :  "spider",
                "health" : 6,
                "lifetime" : 0}
    name = "spider" + str(spider_count)
    cave_hostile_mobs[name] = new_mob
    print("\nYou see a spider,", name)
    spider_count += 1      

def move_spider(m):
    global cave_hostile_mobs
    moblist = cave_hostile_mobs
    moblist[m]["lifetime"] += 1

    
    damage = 1
    #higher damage on second day
    if day >= 2:
        damage = randint(1, 2)
    #higher damage at night 
    if time >= nighttime:
        damage = randint(2, 4)
        if day >= 2:
            damage = randint(4, 5)

    #armour reduces damage, but cap at 0
    damage_taken = max(0, damage - armour_protection)
    print("\n", m, " bit you! You take ", damage ," - ", armour_protection, \
          " = ", damage_taken, " damage", sep = "")
    damage_health(damage_taken)
    if health <= 0:
        print("You were bitten by spider")
        die()

    
    return ""


#enderman

enderman_count = 0


def spawn_enderman(end = False):
    
    global forest_hostile_mobs
    global end_hostile_mobs
    moblist = forest_hostile_mobs
    if end:
        moblist = end_hostile_mobs
    
    global enderman_count
    new_mob = {"type" :  "enderman",
                "health" : 20,
                "lifetime" : 0}
    name = "enderman" + str(enderman_count)
    moblist[name] = new_mob
    print("\nYou see an enderman,", name)
    enderman_count += 1
        

def move_enderman(m, end = False):
    global forest_hostile_mobs
    global end_hostile_mobs
    moblist = forest_hostile_mobs
    
    if end:
        moblist = end_hostile_mobs
        
    moblist[m]["lifetime"] += 1

    if moblist[m]["lifetime"] <= 1 and end:
        return ""

    #small chance to not attack
    if randint(1, 100) <= 10:
        print(m, "teleported around")
        return ""
    
    damage = randint(4, 5)
    #armour reduces damage, but cap at 0
    damage_taken = max(0, damage - armour_protection)
    print("\n", m, " hit you! You take ", damage ," - ", armour_protection, \
          " = ", damage_taken, " damage", sep = "")
    damage_health(damage_taken)
    if health <= 0:
        print("You were killed by enderman")
        die()
    
    return ""




#witch

witch_count = 0


def spawn_witch():

    global witch_count
    
    new_mob = {"type" :  "witch",
                "health" : 15,
                "lifetime" : 0}
    name = "witch" + str(witch_count)
    forest_hostile_mobs[name] = new_mob
    print("\nYou see witch,", name)
    witch_count += 1      

def move_witch(m):
    global forest_hostile_mobs
    moblist = forest_hostile_mobs
    moblist[m]["lifetime"] += 1

    #chance to heal itself
    mob_health = moblist[m]["health"]
    will_heal = False
    if mob_health <= 10:
        if randint(1, 100) <= 50:
            will_heal = True

    if not will_heal:
        #attack
        damage = 4
        #armour reduces damage, but cap at 0
        damage_taken = max(0, damage - armour_protection)
        print("\n", m, " poisoned you! You take ", damage ," - ", armour_protection, \
              " = ", damage_taken, " damage", sep = "")
        damage_health(damage_taken)
        if health <= 0:
            print("You were poisoned by witch")
            die()
        
    else:
        #healing
        healing = randint(7, 12)
        if mob_health + healing > 15:
            healing = 15 - mob_health 
        moblist[m]["health"] += healing
        print("")
        print(m, "drank a health potion and healed",healing, "health.")
        print(m, "now has", moblist[m]["health"], "health")
        

    return ""


#enderdragon


def spawn_enderdragon():
    global ed
    
    new_mob = {
        "type" : "enderdragon",
        "health" : 200,
        "max_health" : 200,
        "lifetime" : 0,
        "stage" : 1,
        "active" : True,
        "waiting" : False,
        "cycle_time" : 0,
        "cycle_length" : 3,
        "acid_attack" : 2
    }
    ed = new_mob
    print("The enderdragon appears and flies towards you, ready to attack.")


def print_enderdragon_health():
    
    if ed == {}:
        return
    
    #                    ENDERDRAGON
    #+--------------------------------------------------+
    #|////////////////////////////////////////          |
    #+--------------------------------------------------+

    h = ed["health"]
    #each slash (bar) corresponds to 4 health
    bars = h//4
    if bars == 0:
        bars = 1
    s = " "*20 + "ENDERDRAGON"
    s += "\n+" + 50*"-" + "+\n|"
    s += bars*"/" + (50-bars)*" " +"|\n"
    s += "+" + 50*"-" + "+\n"
    print(s)
        


def kill_enderdragon():
    global ed
    global inventory
    
    print("\nThe enderdragon hovers upwards, shakes violently and fades away")
    print("Congratulations! You have slain the enderdragon")
    ed = {}
    #get dragon_skin
    print("You gain dragon_skin!")
    inventory["dragon_skin"] += 1
    gain_xp(150)
    if win == -1:
        #get dragon_egg, but only the first time ed. is killed.
        #if have killed ed. before, then win would be the number of moves
        print("\nYou gain the legendary dragon_egg!")
        print("Return to the forest to complete the game")
        inventory["dragon_egg"] += 1
    else:
        print("You may return to the forest now")
    


def attack_enderdragon():
    global ed

    if ed["active"] == False:
        print("You cannot reach the enderdragon when it is flying\n")
        return -1

    print("You hit at the enderdragon with ", sword, ". ", sep="", end="")
    print("You dealt", attack_damage, "damage")

    ed["health"] -= attack_damage
    if ed["health"] <= 0:
        kill_enderdragon()
        
    else:
        print("The enderdragon has", ed["health"], \
        "health left")
    return 0
    

def enderdragon_attack():
    #acid attack, more damage
    #only happens once per cycle
    if ed["cycle_time"] == ed["acid_attack"]:
        damage = randint(5,7)
        damage_taken = max(0, damage-armour_protection)
        print("\nThe enderdragon spews acid at you! You take ", \
                damage ," - ", armour_protection, \
                " = ", damage_taken, " damage", sep = "")
        damage_health(damage_taken)
        if health <= 0:
            print("\nYou were burnt by enderdragon's acid breath")
            die()
    #normal attack, less damage
    #all other attacks
    else:
        damage = 4
        if ed["stage"] == 2:
            damage = randint(4, 5)
        damage_taken = max(0, damage - armour_protection)
        print("\nThe enderdragon bumps into you. You take ", \
                damage ," - ", armour_protection, \
                " = ", damage_taken, " damage", sep = "")
        damage_health(damage_taken)
        if health <= 0:
            print("\nYou were killed by enderdragon")
            die()
                


def move_enderdragon():
    global ed
    if ed == {}:
        return
    
    
    ed["lifetime"] += 1

    if ed["stage"] == 1:
        #when the ed. reaches 100 health, it enters stage 2
        if ed["health"] <= 100:
            ed["stage"] = 2
            print("\nThe enderdragon roars. It enters the second stage")

            if ed["active"]:
                print("The enderdragon flies off.")
            print("The enderdragon may have a surprise for you...")
            
            ed["cycle_time"] = 0
            ed["cycle_length"] = -2
            ed["waiting"] = True
            ed["active"] = False

            return
            
            
    if ed["lifetime"] <= 1:
        return

    #waiting for player to kill enderman
    if ed["waiting"]:
        if ed["cycle_length"] == -2:
            for i in range(3):
                spawn_enderman(True)
            ed["cycle_length"] = -1
            return
        if end_hostile_mobs == {}:
            ed["cycle_time"] = -1
        else:
            return

    #actively attacking
    if ed["active"]:
        enderdragon_attack()
        ed["cycle_time"] += 1

        #if done with attacking, fly off
        if ed["cycle_time"] == ed["cycle_length"]:
            ed["cycle_time"] = 0

            ed["cycle_length"] = 1
            if ed["stage"] == 2:
                ed["cycle_length"] = 2
            
            ed["active"] = False
            print("The enderdragon flies off.")

    #flying off 
    else:
        regen = randint(1, 3)
        if ed["stage"] == 2:
            regen = randint(3, 5)
        print("\nThe enderdragon regenerates", regen, "health")
        ed["health"] += regen
        if ed["health"] > 200:
            ed["health"] = 200

        ed["cycle_time"] += 1

        #if done with flying off, go back and attack 
        if ed["cycle_time"] == ed["cycle_length"] or \
           ed["waiting"]:
            ed["waiting"] = False
            ed["cycle_time"] = 0
            ed["active"] = True
            
            ed["cycle_length"] = 3
            if ed["stage"] == 2:
                ed["cycle_length"] = randint(4, 5)
            
            next_acid = randint(0, ed["cycle_length"]-1)
            ed["acid_attack"] = next_acid
            
            print("The enderdragon flies back, ready to attack")

        


#general
        
def spawn_mobs():
    if location == "forest":

        #pig
        if len(forest_passive_mobs) < forest_passive_mob_cap:
            chance = 17
            if time >= nighttime:
                chance = 5
            if randint(1, 100) <= chance:
                spawn_pig()

        #nighttime hostile mobs   
        if time >= nighttime and len(forest_hostile_mobs) < \
           forest_hostile_mob_cap:
            #zombie
            if randint(1, 100) <= 20:
                spawn_zombie()

            #second day mobs
            if time >= nighttime and day >= 2:
                #enderman
                if randint(1, 100) <= 12:
                    spawn_enderman()
                    
                #witch
                if randint(1, 100) <= 15:
                    spawn_witch()

    #cave mobs
    elif location == "cave":
        if len(cave_hostile_mobs) < cave_hostile_mob_cap:
            #spider
            chance = 5
            if day >= 2:
                chance += 5
            if day >= 3:
                chance += 5
            if time >= nighttime:
                chance += 15
        
            if randint(1, 100) <= chance:
                spawn_spider()


          
def move_mobs():
    #move all the mobs
    if location == "forest":
        for mob in forest_passive_mobs:
            mob_type = forest_passive_mobs[mob]["type"]
            if done:
                return
            #pig
            if mob_type == "pig":
                move_pig(mob)
                
        killed_mobs = []
        
        for mob in forest_hostile_mobs:
            if done:
                return
            mob_type = forest_hostile_mobs[mob]["type"]
            #zombie
            if mob_type == "zombie":
                res = move_zombie(mob)
                #when the zombie burns and dies
                if res == "kill":
                    killed_mobs.append(mob)
            #enderman
            elif mob_type == "enderman":
                move_enderman(mob)
            #witch      
            elif mob_type == "witch":
                res = move_witch(mob)
                
        for i in killed_mobs:
            kill_mob(i, forest_hostile_mobs)
            
    elif location == "cave":
        for mob in cave_hostile_mobs:
            if done:
                return
            mob_type = cave_hostile_mobs[mob]["type"]
            #spider
            if mob_type == "spider":
                res = move_spider(mob)

    elif location == "end":
        move_enderdragon()
        for mob in end_hostile_mobs:
            if done:
                return
            mob_type = end_hostile_mobs[mob]["type"]
            #enderman in the end
            if mob_type == "enderman":
                res = move_enderman(mob, True)

                


#eating

food_list = {
    #food : health given by eating
    "meat" : 2,
    "rotten_flesh" : 1,
    "spider_eye": -2,
    "apple" : 3,
    "health_potion" : 8,
    "satay" : 3
}

def eat(m):
    global inventory
    
    if not m in inventory:
        print("No such item\n")
        return -1
    if not m in food_list:
        print("You cannot eat that!\n")
        return -1
    #check the player has the item
    if inventory[m] == 0:
        print("You do not have any", m, "\n")
        return -1

    print("You consumed ",m,". ", sep="",end="")
    inventory[m] -= 1
    healing = food_list[m]

    #heal health
    if healing >= 0:
        print("You heal ",healing, " health", sep ="")
        heal_health(healing)
    #damage health
    else:
        print("You take ",-healing, " damage", sep ="")
        damage_health(-healing)
        if health <= 0:
            print("You were poisoned!")
            die()
    
    return 0
    


#inventory display

def print_inventory():
    print("Inventory")
    empty = True
    for p in inventory:
        if inventory[p] > 0:
            #star * tools that are currently used
            if p==pickaxe or p==sword or p==armour:
                print("*", end="")
            
            print(p, inventory[p], sep=": ")
            empty = False
    #if there is nothing, i.e. all 0
    if empty:
        print("(empty)")



#mining

def mine(m):
    if location == "forest":
        #chopping tree
        if m == "tree" or m == "wood":
            if forest_surr["tree"] > 0:
                print("You chopped down a tree. You gain 4 wood", end = "")
                #chance to get a stick
                if randint(1, 100) <= 75*luck:
                    print(", 1 stick", end = "")
                    inventory["stick"] += 1
                #chance to get an apple
                if randint(1, 100) <= 25*luck:
                    print(", 1 apple", end = "")
                    inventory["apple"] += 1

                print("")
                forest_surr["tree"] -= 1
                inventory["wood"] += 4

                if randint(1, 100) <= 50:
                    gain_xp(1)
            else:
                print("There are no more trees\n")
                return -1
        elif not m in forest_surr:
            print("No such thing here\n", sep="\"")
            return -1                    
        else:
            print("You cannot mine that!\n")
            return -1
    elif location == "cave":
        if not m in cave_surr:
            print("There is no ", m, " here\n", sep="\"")
            return -1
        if cave_surr[m] == 0:
            print("You have not found", m, "\n")
            return -1

        #mining stone 
        if m == "stone":
            #need a pickaxe
            if pickaxe == "wooden_pickaxe" or \
                pickaxe == "stone_pickaxe" or \
                pickaxe ==  "iron_pickaxe" or \
                pickaxe =="diamond_pickaxe":
                print("You mined stone. You gain 1 stone")
                inventory["stone"] += 1
                if randint(1, 100) <= 50:
                    gain_xp(1)
            else:
                print("You need a pickaxe to mine stone!\n")
                return -1
            
        #mining iron
        elif m == "iron":
            #need stone pickaxe or better
            if pickaxe == "stone_pickaxe" or \
                pickaxe ==  "iron_pickaxe" or \
                pickaxe =="diamond_pickaxe":
                print("You mined iron. You gain 1 iron")
                inventory["iron"] += 1
                cave_surr["iron"] -= 1
                gain_xp(randint(3, 4))
            else:
                print("You need a stone_pickaxe or better to mine iron!\n")
                return -1
            
        #mining diamond
        elif m == "diamond":
            #need iron_pickaxe or better
            if pickaxe == "iron_pickaxe" or \
               pickaxe == "diamond_pickaxe":
                print("You mined diamond! You gain 1 diamond")
                inventory["diamond"] += 1
                cave_surr["diamond"] -= 1
                gain_xp(10)
            else:
                print("You need an iron_pickaxe or better to mine diamond!\n")
                return -1
            
        else:
            print("You cannot mine that\n")
            return -1
    else:
        print("There is nothing to mine here\n")
        return -1
    return 0




#location change

def goto(m):
    global location
    global time
    
    if location == "forest":
            
        if m == "forest":
            print("You are already in the forest\n")
            return -1
        #go to cave
        elif m == "cave":    
            location = "cave"
            print("You entered the cave")
            desc_location(False)
        #go to end
        elif m == "end":
            #need end portal
            if inventory["end_portal"] == 0:
                print("You need an end_portal to go to the end\n")
                return -1
            else:
                print("Entering the end...\n")
                print("You are in the end")
                location = "end"
                spawn_enderdragon()
                time = -1
                gain_xp(20)
            
        else:
            print("You cannot enter that\n")
            return -1
            
    elif location == "cave":
        
        if m == "cave":
            print("You are already in the cave\n")
            return -1
        #go back to forest
        if m == "forest":    
            location = "forest"
            print("You returned to the forest")
            desc_location(False)
        else:
            print("There is no", m, "here\n")
            return -1
    elif location == "end":
        if ed == {}:
            #go back to forest (after killing ed.)
            if m=="forest":
                global win
                global forest_hostile_mobs
                global day
                
                
                print("You return to the forest")
                location = "forest"
                if win == -1:
                    win = moves + 1
                    winning()
                forest_hostile_mobs = {}
                day += 1
                desc_location(False)
            else:
                print("You can't go there\n")
                return -1
        else:
            print("There is nowhere to hide\n")
            return -1
    return 0



#commands    

def make_move():

    #prompt
    #not case sensitive
    s = input("==> ").lower()
    
    m = s.split()
    global location
    global done
    global forest_surr
    global cave_surr
    global show_hearts
    global moves
    global time
    global day
    global cheats
    global cheated
    global luck

    #blank command
    if len(m) == 0:
        
        print("Expected command\n")
        return
    
    #exit game command
    elif m[0] == "done" or m[0] == "quit":
        #confirm message
        s = input("Are you sure you want to end the game? (YES/NO): ")
        if s == "YES":
            done = True
        else:
            print("Game continues")
        print("")
        return
        

    #help command
    elif m[0]=="help":
        show_help()
        return

    #hearts command
    elif m[0]=="hearts":
        #toggle
        show_hearts = not show_hearts
        print("")
        if show_hearts:
            print_hearts()
        return

    #details command
    elif m[0] == "details":
        print_details()
        print("")
        return

    #time command
    elif m[0] == "time" or m[0] == "t":
        print_time("\n\n")
        return

    #moves command
    elif m[0] == "moves":
        print_moves("\n\n")
        return

    #location command
    elif m[0] == "location" or m[0] == "where":
        print_location("\n\n")
        return

    #health command
    elif m[0] == "health" or m[0] == "h":
        print_health("\n\n")
        return

    #pickaxe command
    elif m[0] == "pickaxe" or m[0] == "pick" or m[0] == "pic"\
         or m[0]=="tool" or m[0]=="tools":
        print_pickaxe("\n\n")
        return

    #sword command
    elif m[0] == "sword" or m[0] == "weapon":
        print_sword("\n\n")
        return

    #armour command
    elif m[0]=="armour" or m[0]=="armor" or m[0]=="protection":
        print_armour("\n\n")
        return

    #view command
    elif m[0] == "look" or m[0] == "view" or m[0]=="v":
        desc_location()
        print("")
        return

    #inventory command
    elif m[0]=="i" or m[0]=="e" or m[0]=="inventory":
        print_inventory()
        print("")
        return

    #mine command
    elif m[0]=="break" or m[0]=="mine" or m[0]=="destroy" \
        or m[0]=="harvest" or  m[0]=="gather" or m[0]=="dig"\
        or m[0]=="m" or m[0]=="collect" or m[0]=="take" or \
        m[0] == "get" or m[0]=="chop" or m[0]=="cut":
        if len(m) < 2:
            print("An object was expected\n")
            return
        res = mine(m[1])
        if res == -1:
            return        
            
    #go command
    elif m[0]=="go" or m[0]=="enter" or m[0]=="goto" \
         or m[0]=="go_to" or m[0]=="into":
        if len(m) < 2:
            print("A location was expected\n")
            return
        
        res = goto(m[1])
        if res == -1:
            return

    #wait command         
    elif m[0] == "wait" or m[0] == "w":
        print("Time passes")

    #back command
    elif m[0]=="out" or m[0]=="return" or \
         m[0]=="back" or m[0]=="escape":
        #just go back to the forest
        res = goto("forest")
        if res == -1:
            return
            

    #craft command
    elif m[0] == "craft" or m[0] == "make" or m[0] == "create"\
        or m[0] == "c" or m[0] == "brew":
        if len(m) == 1:
            print("Expected an item to be crafted\n")
            return

        #need a crafting table if not in forest
        if location != "forest" and inventory["crafting_table"] == 0:
            print("You need a crafting table to craft items when not in the forest!\n")
            return 
        
        res = craft(m[1])
        if res == -1:
            return
        
        #crafting table can break when not in forest
        if location != "forest" and randint(1, 5) == 1:
            inventory["crafting_table"] -= 1
            print("Your crafting_table broke! crafting_table left:", end = " ")
            print(inventory["crafting_table"])


    #sleep command
    elif m[0] == "sleep":
        res = sleep()
        if res == -1:
            return

    #attack command
    elif m[0]=="attack" or m[0]=="kill" or[0]=="fight" or m[0]=="k":
        if len(m) == 1:
            print("Expected mob\n")
            return
        #enderdragon
        if (m[1] == "enderdragon" or m[1] == "ed") and\
           ed != {} and location == "end":
            res = attack_enderdragon()
        #other mobs
        else:
            res = attack_mob(m[1])
        if res == -1:
            return

    #eat command
    elif m[0]=="eat" or m[0]=="drink" or m[0]=="consume":
        if len(m) == 1:
            print("Expected food item\n")
            return
        res = eat(m[1])
        if res == -1:
            return
        
    #open command
    elif m[0] == "open":
        if len(m) == 1:
            print("Expected object to open\n")
            return
        #open chest
        if m[1] != "chest":
            print("No such thing here\n")
            return

        res = open_chest()
        if res == -1:
            return
        
    #cheats

    elif m[0] == "cheats":
        if len(m) == 1:
            print("Cheats on or cheats off?\n")
            return
        if m[1] == "off" or m[1] == "false":
            cheats = False
            print("Cheats turned off\n")
            return
        elif m[1] == "on" or m[1] == "true":
            cheats = True
            print("Cheats turned on\n")
            cheated = True
            return
        else:
            print("Cheats on or cheats off?\n")
            return
        
    #give command (cheats)
    elif m[0] == "give":
        if cheats == False:
            print("Enable cheats to use this command\n")
            return
        if len(m) == 1:
            print("Expected item\n")
            return
        item = m[1]
        k = 1
        try:
            k = int(m[2])
            if k < 0:
                k = 0
        except:
            pass
        #give a lot of stuff
        if item == "gear":
            inventory["diamond_sword"] += 1
            inventory["diamond_pickaxe"] += 1
            inventory["diamond_armour"] += 1
            inventory["apple"] += 1000
            inventory["health_potion"] += 7
            inventory["end_portal"] += 1
            update_armour("diamond_armour", "\n")
            update_sword("diamond_sword", "\n")
            update_pickaxe("diamond_pickaxe", "\n")
            return
        try:
            inventory[item] += k
            print("You got", k, item, "\n")
            update_armour(item, "\n")
            update_sword(item, "\n")
            update_pickaxe(item, "\n")
            return
        except:
            print("No such item\n")
            return

    #summon command (cheats)
    elif m[0] == "summon" or m[0] == "spawn":
        if cheats == False:
            print("Enable cheats to use this command\n")
            return 
        mob = ""
        try:
            mob = m[1]
        except:
            print("Expected mob\n")
            return

        #spawn the mob
        if location == "forest":
            if mob == "pig":
                spawn_pig()
            elif mob == "zombie":
                spawn_zombie()
            elif mob == "enderman":
                spawn_enderman()
            elif mob == "witch":
                spawn_witch()
            elif mob == "spider" or mob == "enderdragon" or mob == "ed":
                print("Sorry, you can't spawn that here\n")
                return
            else:
                print("No such mob\n")
                return
                
        elif location == "cave":
            if mob == "spider":
                spawn_spider()
            elif mob=="pig" or mob=="zombie" or mob=="enderman" or\
                 mob=="witch" or mob=="enderdragon" or mob=="ed":
                print("Sorrry, you can't spawn that here\n")
                return
            else:
                print("No such mob\n")
                return

        elif location == "end":
            if mob == "enderman":
                spawn_enderman(True)
            elif mob=="pig" or mob=="zombie" or mob=="spider" or\
                 mob=="witch" or mob=="enderdragon" or mob=="ed": 
                print("Sorry, you can't spawn that here\n")
                return
            else:
                print("No such mob\n")
                return
                
        print("")
        return

    #heal command (cheats)
    elif m[0] == "heal" or m[0] == "set_health":
        if cheats == False:
            print("Enable cheats to use this command\n")
            return
        
        new_health = 10
        try:
            new_health = int(m[1])
        except:
            print("Invalid health input\n")
            return
        
        #cap at 10
        if new_health > 10:
            new_health = 10
        #cap at 0
        if new_health < 0:
            new_health = 0
            
        global health
        health = new_health
        print("You now have", health, "health")
        #die
        if health <= 0:
            print("You were killed by thinking too hard")
            die()
        print("")
        return
    
    #luck command (cheats)
    elif m[0] == "luck" or m[0] == "set_luck":
        if cheats == False:
            print("Enable cheats to use this command\n")
            return
        new_luck = 1.0
        try:
            new_luck = float(m[1])
        except:
            print("Invalid luck input\n")
            return
        print("Changed luck from", luck, "to", new_luck)
        luck = new_luck
        print("")
        return
            
    #command not recognised    
    else:
        print("The command ",m[0]," was not recognised", sep="\"")
        print("")
        return

    #if did not return, means it is an active move
    #increase number of moves and time 
    moves += 1
    
    if location == "forest" or location == "cave":
        time += 1
        check_time()

    #do all the other stuff that happens when time passes
        
    move_mobs()
    spawn_mobs()

    if location == "forest":
        grow_trees()
    elif location == "cave":
        generate_ores()
    generate_chest()

    #will print the enderdragon health if in the end
    print("")
    if location == "end":
        print_enderdragon_health()

    #will show the hearts if turned on
    if show_hearts:
        print_hearts()
    

def main():
    #start the game, intro
    intro()
    desc_location()
    global done
    print("")

    #keep inputting a move
    while True:
        make_move()
        if done:
            break


    #Game End
    print("Game Over!\n")

    #check if used cheats
    if cheated:
        print("Cheats were used in this game\n")
    else:
        print("No cheats were used\n")

    #print inventory, moves, and winning
        
    print_inventory()
    print("")
    print_moves("\n\n")
    print("Score:", score, "\n")

    winning()
    
    print("\nThank you for playing.")
    
main()

input("Enter anything to exit the program ")
