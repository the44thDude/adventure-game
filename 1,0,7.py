import random

#function to roll dice
def roll(d,n,add=0,adv=0,disadv=0):
    rolls=0
    result=[]
    for dice in range(d):
        roll=random.randint(1,n)
        result.append(roll)
        print('roll d'+str(n)+' = '+str(roll))
    total = sum(result)
    if add==True:
        return total
    elif adv==True:
        return max(result)
    elif disadv==True:
        return min(result)
    else:
        return result[0]
#function for d20 rolls against a DC
def skillcheck(a,b):
    print('attempting check at a DC: '+str(b))
    value=roll(1,20)
    value=value+a
    if value<b:
        print('check failed')
        return False
    else:
        print('check passed')
        return True
#function to space out lines of text
def space():
    print('*')
    print('*')
    print('*')
#function to create a charecter
def CharacterCreate():
    create=True
    while create==True:
        strength=1
        stealth=1
        sight=1
        armor=8
        health=0
        valid=0
        print('to play this game you must first create an adventurer. this adventurer will be who is travelling to defeat the Dragon.')
        print('every adventurer has four basic stats.')
        space()
        print('Strength determines you adventurer`s ability to hit and to hit hard.')
        print('Stealth is your adventurer`s ability to be hidden and go unnoticed')
        print('Sight is your adventurer`s ability to spot other creatures or search an area.')
        print('Armor is your adventurer`s defense it is what an attacker needs to roll above to hit your adventurer.')
        space()
        print('Health is also a stat but it will be determined seperately.')
        statpoints=3
        while statpoints!=0:
            print('you have '+str(statpoints)+' points to invest in your charecter`s stats.')
            print('to invest a point in strength, type "/strength". in stealth, type "/stealth". in sight, type "/sight". and in armor, type "/armor"')
            com=input()
            if com=='/strength':
                strength=strength+1
                statpoints=statpoints-1
            elif com=='/stealth':
                stealth=stealth+1
                statpoints=statpoints-1
            elif com=='/sight':
                sight=sight+1
                statpoints=statpoints-1
            elif com=='/armor':
                armor=armor+2
                statpoints=statpoints-1
            else:
                print ('invalid command please retry')
        while health==0:
            print('now we must determine your adventurer`s health.')
            print('choose a difficulty level: easy, medium, hard, extreme, or 1 hit wonder.')
            print('type /easy for easy, /medium for medium, /hard for hard, /extreme for extreme, or /1hit to die after one hit')
            com=input()
            if com=='/easy':
                health=20
            elif com=='/medium':
                health=15
            elif com=='/hard':
                health=10
            elif com=='/extreme':
                health=5
            elif com=='/1hit':
                health=1
            elif com=='/god':
                health=100
            else:
                print('invalid command please retry')
        while valid!=True:
            print('these are your adventurer`s stats: type /okay if these are what you want if you want to make a different adventurer type /retry')
            print('health='+str(health)+' strength='+str(strength)+' stealth='+str(stealth)+' sight='+str(sight)+' armor='+str(armor))
            com=input()
            if com=='/okay':
                valid=True
                create=False
                return (health, strength, stealth, sight, armor)
            elif com=='/retry':
                valid=True
                print('resetting stats...')
                create=True
            else:
                valid=False
                print('invalid command try again')
#function to write character's stats in a txt file
def SaveCharacter(characterName):
    stats=CharacterCreate()
    with open('characters.txt','w') as wf:
            wf.write(characterName+', health, '+str(stats[0])+'\n')
            wf.write(characterName+', strength, '+str(stats[1])+'\n')
            wf.write(characterName+', stealth, '+str(stats[2])+'\n')
            wf.write(characterName+', sight, '+str(stats[3])+'\n')
            wf.write(characterName+', armor, '+str(stats[4])+'\n')
#function to retreave information form the txt file with stats in it for monsters or characters
def getstat(file,Name,stat):
    with open(file,'r') as rf:
        repeat=True
        while repeat==True:
            line=rf.readline()
            if Name in line and stat in line:
                value=int(line[-2])
                if '1' in line[-3] or '2' in line[-3] or '3' in line[-3] or '4' in line[-3] or '5' in line[-3]:
                    value=value+(int(line[-3])*10)
                elif '6' in line[-3] or '7' in line[-3] or '8' in line[-3] or '9' in line[-3]:
                    value=value+(int(line[-3])*10)
                repeat= False
                return value
            else:
                repeat=True
#function to edit stats in the a txt file:
def changestat(file,Name,stat,newstat):
    with open(file,'r+') as rf:
        repeat=True
        linevalue=0
        while repeat==True:
            line=rf.readline()
            linevalue=linevalue+len(line)
            if Name in line and stat in line:
                rf.seek(linevalue)
                rf.write(' '+str(newstat)+'\n')
                repeat=False
            else:
                repeat=True
def terrainset():
    terrains=['desert', 'grassland', 'forest', 'mountain']
    newterrain=random.choice(terrains)
    return newterrain

def encounter(terrain,sneak):
    global playername
    if terrain=='desert':
        print('the worm fights you')
        monsterarmor=getstat('monsters.txt','worm','armor')
        monsterattack=getstat('monsters.txt','worm','attack')
        monsterlife=getstat('monsters.txt','worm','attack')
    elif terrain=='mountain':
        print('the yeti fights you')
        monsterarmor=getstat('monsters.txt','yeti','armor')
        monsterattack=getstat('monsters.txt','yeti','attack')
        monsterlife=getstat('monsters.txt','yeti','attack')
    elif terrain=='grassland':
        print('the tigerbear fights you')
        monsterarmor=getstat('monsters.txt','tigerbear','armor')
        monsterattack=getstat('monsters.txt','tigerbear','attack')
        monsterlife=getstat('monsters.txt','tigerbear','attack')
    elif terrain=='forest':
        print('the troll fights you')
        monsterarmor=getstat('monsters.txt','troll','armor')
        monsterattack=getstat('monsters.txt','troll','attack')
        monsterlife=getstat('monsters.txt','troll','attack')
    PlayerHealth=getstat('characters.txt', playername,'health')
    PlayerArmor=getstat('characters.txt', playername,'armor')
    if sneak==true:
        PlayerAttack=getstat('characters.txt',playername,'stealth')+getstat('characters.txt',playername,'strength')
    else:
        PlayerAttack=getstat('characters.txt',playername,'strength')
    while monsterlife>=0:
        print('type /attack to attack or /dodge to dodge')
        com=input()
        if com=='/attack':
            valid=True
            hit=skillcheck(PlayerAttack,monsterarmor)
            if hit==True:
                damage=(roll(1,6)+PlayerAttack)
                monsterlife=monsterlife-damage
            else:
                print('you did not hit the monster.')
        elif com=='/dodge':
            valid=True
            PlayerArmor=PlayerArmor+5
        else:
            print('invalid command please try again')
            valid=False
        if valid==True:
            hit=skillcheck(monsterattack,PlayerArmor)
            if hit==True:
                damage=(roll(1,6)+monsterattack)
                PlayerHealth=PlayerHealth-damage
            else:
                print('you evaded the monster`s attack!')
        if PlayerHealth<=0:
            break
    if PlayerHealth<=0:
        return False
    else:
        return True

#game instructions
print('Welcome to Caleb`s great adventure game version 6! this is still in development if you experience issues let me know and tell me what choices you made.')
print('to play: enter simple commands from the list and try to defeat the dragon!')
print('you may only enter a command that is listed as an option in the question.')
print('when you fight the dragon your attacks are rolled against his armor and your damage is added')
print('press enter to play the game')
with open('monsters.txt','w') as f:
    f.write(' dragon, health, 30\n dragon, armor, 12\n dragon, attack, 5\n yeti, health, 10\n yeti, armor, 8\n yeti, attack, 3\n worm, health, 5\n worm, armor, 10\n worm, attack, 1\n troll, health, 15\n troll, armor, 7\n troll, attack, 3\n tigerbear, health, 5\n tigerbear, armor, 6\n tigerbear, attack, 5')
gamestart=input()
