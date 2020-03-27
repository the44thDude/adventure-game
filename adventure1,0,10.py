import random
import os.path
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
    print('attempting check at a DC: '+str(b)+' and mod +'+str(a))
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
        print('Health is also a stat but it will be determined by difficulty level')
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
                health=30
            elif com=='/medium':
                health=20
            elif com=='/hard':
                health=10
            elif com=='/extreme':
                health=5
            elif com=='/1hit':
                health=1
            elif com=='/god':
                health=99
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
    global MaxHealth
    stats=CharacterCreate()
    MaxHealth=stats[0]
    with open('characters.txt','a') as wfc:
            wfc.write('\n')
            wfc.write(characterName+', health,  '+str(stats[0])+'\n')
            wfc.write(characterName+', strength,  '+str(stats[1])+'\n')
            wfc.write(characterName+', stealth,  '+str(stats[2])+'\n')
            wfc.write(characterName+', sight,  '+str(stats[3])+'\n')
            wfc.write(characterName+', armor,  '+str(stats[4])+'\n')
            wfc.write(characterName+', weapon,    \n')
            wfc.write('\n')
#function to retreave information form the txt file with stats in it for monsters or characters
def getstat(file,Name,stat):
    with open(file,'r') as rf:
        rf.seek(0)
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
        rf.seek(0)
        while repeat==True:
            line=rf.readline()
            linevalue=linevalue+len(line)
            if Name in line and stat in line:
                rf.seek(linevalue-3)
                rf.write(str(newstat)+'\n')
                repeat=False
            else:
                repeat=True
def terrainset():
    terrains=['desert', 'grasslands', 'forest', 'mountains','marshlands', 'hills', 'windy planes']
    newterrain=random.choice(terrains)
    return newterrain

def encounter(terrain,sneak):
    global playername
    run=0
    if terrain=='desert':
        print('the worm fights you')
        monster='worm'
    elif terrain=='mountains':
        print('the yeti fights you')
        monster='yeti'
    elif terrain=='grasslands':
        print('the tigerbear fights you')
        monster='tigerbear'
    elif terrain=='forest':
        print('the troll fights you')
        monster='troll'
    elif terrain=='marshlands':
        print('the crocodile attacks you')
        monster='crocodile'
    elif terrain=='hills':
        print('a goblin jumps out from behind a bush!')
        monster='goblin'
    elif terain=='windy planes':
        print('an eagle swwops down from above!')
        monster='eagle'
    monsterlife=getstat('monsters.txt',monster,'health')
    monsterarmor=getstat('monsters.txt',monster,'armor')
    monsterattack=getstat('monsters.txt',monster,'attack')
    PlayerHealth=getstat('characters.txt', playername,'health')
    PlayerArmor=getstat('characters.txt', playername,'armor')
    if sneak==True:
        PlayerAttack=getstat('characters.txt',playername,'stealth')+getstat('characters.txt',playername,'strength')
    else:
        PlayerAttack=getstat('characters.txt',playername,'strength')
    while monsterlife>0 and run<5:
        print('type /attack to attack or /dodge to dodge')
        com=input()
        if com=='/attack':
            valid=True
            hit=skillcheck(PlayerAttack,monsterarmor)
            if hit==True:
                print('you hit the monster!')
                damage=(roll(1,6)+PlayerAttack)
                print('you dealt '+str(damage))
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
            space()
            print('it is the monster`s turn')
            hit=skillcheck(monsterattack,PlayerArmor)
            if hit==True:
                print('the monster hit you')
                damage=(roll(1,6)+monsterattack)
                print('they dealt '+str(damage))
                PlayerHealth=PlayerHealth-damage
                print('your health is at: '+str(PlayerHealth))
            else:
                run=run+1
                print('you evaded the monster`s attack!')
        if PlayerHealth<=0:
            break
    if PlayerHealth<=0:
        return [False,False]
    elif run==5:
        changestat('characters.txt',playername,'health',PlayerHealth)
        print('you have tired the monster out and can run away.')
        return [False,True]
    else:
        changestat('characters.txt',playername,'health',PlayerHealth)
        return [True,False]
def journey():
    global playername
    exp=0
    day=0
    end=False
    strength=getstat('characters.txt',playername,'strength')
    stealth=getstat('characters.txt',playername,'stealth')
    sight=getstat('characters.txt',playername,'sight')
    while exp<3:
        PlayerHealth=getstat('characters.txt',playername,'health')
        valid=False
        fight=True
        sneak=False
        terrain=terrainset()
        if day==0:
            print('you begin your great adventure to find the dragon by setting out into the '+terrain)
        else:
            print('you wake up a new day, and travel into the '+terrain+' by noon.')
        while terrain=='desert'and valid==False:
            print('the sun is very hot, and you are growing tired do you choose to rest a moment or continue through the desert?')
            print('type /rest to rest or /go to continue through the desert')
            com=input()
            if com=='/rest':
                valid=True
                Pass=skillcheck(strength,9+day)
                if Pass==False:
                    end=True
                    print('you fell asleep in the desert and withered away without water.')
                    break
                elif Pass==True:
                    print('your rest was just enough to get through the desert quickly you sleep near the edge of it')
                    fight=False
                    exp=exp+1
            elif com=='/go':
                valid=True
            else:
                print('invalid command please try again')
                valid=False
        if end==True:
            break
        while terrain=='forest' and valid==False:
            print('you are coming around a corner on the forest path when you spot a troll ahead.')
            print('type /sneak to sneak by or /attack to attack it')
            com=input()
            if com=='/sneak':
                valid=True
                Pass=skillcheck(stealth,9+day)
                if Pass==False:
                    print('you wake the troll and it runs to attack you!.')
                elif Pass==True:
                    print('you sneak past the troll and find your way to the edge of the forest where you camp for the night.')
                    fight=False
                    exp=exp+1
            elif com=='/attack':
                valid=True
            else:
                print('invalid command please try again')
                valid=False
        while terrain=='mountains' and valid==False:
            print('As you come to a narrow pass near the mountains top you hear a strange sound')
            print('do you suddenly run as fast as you can towards the end of the pass or look around for the source of the sound?')
            print('type /run to run or /look to look around')
            com=input()
            if com=='/run':
                valid=True
                Pass=skillcheck(strength,9+day)
                if Pass==False:
                    end=True
                    print('you ran toward the end of the pass but did not make it before a huge avalanche burried you.')
                    break
                elif Pass==True:
                    print('you run toward the edge of the pass and just barely make it ahead of a huge sideways tsunami of snow fills the pass.')
                    exp=exp+1
            elif com=='/look':
                valid=True
                Pass=skillcheck(sight,9+day)
                if Pass==False:
                    end=True
                    print('you look around the pass but do not see a huge avalanche in time to escape before it buries you.')
                    break
                elif Pass==True:
                    print('you see an avalanche and run in the correct direction to escape before snow fills the pass.')
                    exp=exp+1
            else:
                print('invalid command please try again')
                valid=False
        if end==True:
            break
        if terrain=='grasslands':
            Pass=skillcheck(sight,15)
            if Pass==False:
                print('you are surprised as a tigerbear bursts from the tall grass and pounces on you!')
                damage=roll(1,6)+getstat('monsters.txt','tigerbear','attack')
                print('he dealt ' +str(damage)+' points of damage!')
                PlayerHealth=PlayerHealth-damage
                print('you are now at '+str(PlayerHealth)+' health')
                if PlayerHealth<=0:
                    end=True
                changestat('characters.txt',playername,'health',PlayerHealth)
            elif Pass==True:
                print('you see a tigerbear attempting to sneak up on you.')
        if terrain=='marshlands':
            print('the marsh gives way below you and you attempt to swim towards the land!')
            Pass=skillcheck(strength,9+day)
            if Pass==False:
                print('you are sucked into the swamp and drown')
                end=True
            elif Pass==True:
                print('you manage to swim to shore and pull yourself out you are alive, but wet and gross.')
        if terrain=='windy planes' or 'hills':
            print('you relax, there is no skill check and the road here is very well worn.')
        if end==True:
            break
        if fight==True:
            valid=True
            if terrain=='desert':
                print('you see a worm in the desert sands')
                sneak=skillcheck(stealth,10)
                if sneak== True:
                    print('you manage to approach unheard and will get a sneak attack')
            if terrain=='mountains':
                print('you see a yeti in the snow')
                sneak=skillcheck(stealth,10)
                if sneak==True:
                    print('you manage to approach unheard and will gety a sneak attack')
            WinFight=encounter(terrain,sneak)
            if WinFight[0]==True and WinFight[1]==False:
                loot=['an axe','a sheild','a lifestone']
                monloot=loot[random.randint(0,2)]
                print('you found '+monloot+' in the remains')
                if monloot=='an axe':
                    strength=strength+1
                    changestat('characters.txt',playername,'strength',strength)
                elif monloot=='a sheild':
                    armor=getstat('characters.txt',playername,'armor')
                    armor=armor+1
                    changestat('characters.txt',playername,'armor',armor)
                elif monloot=='a lifestone':
                    PlayerHealth=PlayerHealth+5
                    changestat('characters.txt',playername,'health',PlayerHealth)
                exp=exp+1
            elif WinFight[0]==False and WinFight[1]==True:
                print('you escaped the monster and settled down for the night')
                exp=exp+1
            else:
                end=True
                break
        day=day+1
        if exp==3:
            end=False
        elif end==True:
            break
    if end==True:
        return False
    else:
        return True
def Dragonfight():
    terrain=terrainset()
    if terrain=='hills' or 'windy planes' or 'mountains' or 'desert':
        monster='dragon'
    elif terrain== 'grasslands' or 'marshlands' or 'forest':
        monster='hag'
    monsterarmor=getstat('monsters.txt',monster,'armor')
    monsterattack=getstat('monsters.txt',monster,'attack')
    monsterlife=getstat('monsters.txt',monster,'health')
    stealth=getstat('characters.txt',playername,'stealth')
    while valid==False:
        print('you awake a new day and soon find you are nearing the end of your journey. by noon you find yourself at the lair of a '+monster)
        print('do you attempt to sneak in or do you charge in and use your powerful thighs to make an extra powerful smack on the dragon?')
        print('type /sneak to sneak in or /run to run in')
        com=input()
        if com=='/sneak':
            valid=True
            Pass=skillcheck(stealth,12)
            if Pass==True:
                sneak=True
                print('you snuck up on the '+monster+' and will hit him very hard the first time')
            else:
                sneak=False
                print('the '+monster+' sees you and you must now prepare for battle!')
        elif com=='/run':
            valid=False
            sneak=False
            print('you run in and your blood boils with battle energy as you attack the '+monster+'!')
        else:
            print('invalid command please try again')
            valid=False
    PlayerHealth=getstat('characters.txt', playername,'health')
    PlayerArmor=getstat('characters.txt', playername,'armor')
    if sneak==true:
        PlayerAttack=getstat('characters.txt',playername,'stealth')+getstat('characters.txt',playername,'strength')
    else:
        PlayerAttack=getstat('characters.txt',playername,'strength')
    while monsterlife>0:
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
        elif 'seduce' in com:
            valid=False
            print('the '+monster+' finds you VERY ATRACTIVE but still wants to kill you and fuck your corpse so you gotta fight')
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
def endscreen(win):
    global wins
    global losses
    global playername
    valid=False
    with open('highscores.txt','a') as wfh:
        wfh.write('\n'+playername+', score,    \n')
    changestat('highscores.txt',playername,'score', wins)
    with open('highscores.txt','r') as rf:
        contents=rf.read()
    print(contents)
    if win==True:
        print('you have won the game. type /exit to exit the game or /return to restart')
        wins=wins+1
    if win==False:
        losses=losses+1
        print('you were killed you have lost the game. type /exit to exit the game or /return to restart')
    while valid==False:
        com=input()
        if com=='/exit':
            valid=True
            return False
        elif com=='/return':
            print('you have restarted the game. wins:'+str(wins)+' loses:'+str(losses))
            valid=True
            return True
        else:
            print('invalid command please try again.')
def SameCharecterQuerie(wins,losses):
    global playername
    global MaxHealth
    if wins>0 or losses >0:
        valid=False
        while valid==False:
            print ('would you like to make a new charecter? type /yes or /no')
            com=input()
            if com=='/no':
                valid=True
                changestat('characters.txt',playername,'health',MaxHealth)
                break
            elif com=='/yes':
                valid2=False
                while valid2==False:
                    playername=input('name:')
                    with open('characters.txt','r') as f:
                        content=f.read()
                    if playername in content:
                        print('please choose a different name')
                    else:
                        valid2=True
                SaveCharacter(playername)
            else:
                valid=False
    else:
        valid2=False
        while valid2==False:
            playername=input('name:')
            with open('characters.txt','r') as f:
                content=f.read()
            if playername in content:
                print('please choose a different name')
            else:
                valid2=True
        SaveCharacter(playername)
#game instructions
print('Welcome to Caleb`s great adventure game version 10! this is still in development if you experience issues let me know and tell me what choices you made.')
print('to play: enter simple commands from the list and try to defeat as many bosses as possible.')
print('currently there are two bosses: dragon and hag.')
print('*')
print('inorder to get to the boss you must suvive three days of your journey through randomly generated terrains')
print('every day consists of a skill check based off the terrain you are in, and an encounter with a monster')
print('some skillchecks will end in player death if failed and some will bypass the monster fight')
print('*')
print('once you reach a boss it will be randomly determined which boss you fight')
print('after the fight you will either win or lose the game, your wins and losses will be recorded')
print('you will have to restart the game via /return after the boss fight and your health will be restored')
print('*')
print('you may only enter a command that is listed as an option in the question.')
print('all commands are one word proceeded by a foreward slash in the format "/command"')
print('enter the name  of your adventurer to play')
makenew=os.path.isfile('characters.txt')
if makenew==False:
    with open ('characters.txt','w') as f:
        pass
makenew=os.path.isfile('highscores.txt')
if makenew==False:
    with open('highscores.txt', 'w') as f:
        pass
runprog=True
wins=0
losses=0
while runprog==True:
    win=0
    cont=0
    with open('monsters.txt','w') as wfm:
        wfm.write('\n dragon, health, 20\n dragon, armor, 12\n dragon, attack, 5\n')
        wfm.write('\n yeti, health, 10\n yeti, armor, 8\n yeti, attack, 3\n')
        wfm.write('\n worm, health, 5\n worm, armor, 10\n worm, attack, 1\n')
        wfm.write('\n troll, health, 15\n troll, armor, 7\n troll, attack, 3\n')
        wfm.write('\n tigerbear, health, 5\n tigerbear, armor, 6\n tigerbear, attack, 5\n')
        wfm.write('\n crocodile, health, 8\n crocodile, armor, 10\n crocodile, attack, 3\n')
        wfm.write('\n goblin, health, 1\n goblin, armor, 1\n goblin, attack, 1\n')
        wfm.write('\n eagle, health, 3\n eagle, armor, 10\n eagle, attack, 2\n')
        wfm.write('\n hag, health, 20\n hag, armor, 10\n hag, attack, 5\n')
    SameCharecterQuerie(wins,losses)
    cont=journey()
    if cont==False:
        win=False
    else:
        win=Dragonfight()
    runprog=endscreen(win)