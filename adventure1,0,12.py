import random
import os.path

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
def getstat(file,Name,stat):
    with open(file,'r') as rf:
        rf.seek(0)
        repeat=True
        while repeat==True:
            line=rf.readline()
            if Name in line and stat in line:
                line=line.split(',')
                value=int(line[2])
                repeat= False
                return value
            else:
                repeat=True
class monster:
    def __init__(self, health, armor, attack):
        self.health=health
        self.attack=attack
        self.armor=armor

    def attackf(self):
        hit=skillcheck(self.attack, player.armor)
        if hit==True:
            print('you got hit')
        else:
            print('the monster missed')

class character:
    def __init__(self,health,strength,stealth,sight,armor,weapon):
        self.maxhealth=health
        self.health=health
        self.strength=strength
        self.stealth=stealth
        self.sight=sight
        self.armor=armor
        self.weapon=weapon

def space():
    print('*')
    print('*')
    print('*')

def CharacterCreate():
    global playername
    create=True
    while create==True:
        strength=1
        stealth=1
        sight=1
        armor=8
        health=0
        valid=0
        print('type in the name of your previous character to reload them')
        print('if the computer does not recognize what you type as a previous character you will make a new one')
        playername=input('name:')
        with open('characters.txt','r') as rf:
            contents=rf.read()
        if playername in contents:
            print('loading previous save...')
            health=getstat('characters.txt',playername,'health')
            strength=getstat('characters.txt',playername,'strength')
            stealth=getstat('characters.txt',playername,'stealth')
            sight=getstat('characters.txt',playername,'sight')
            armor=getstat('characters.txt',playername,'armor')
            break
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
    return (health, strength, stealth, sight, armor)

def SaveCharacter():
    global player
    stats=CharacterCreate()
    player=character(stats[0],stats[1],stats[2],stats[3],stats[4],1)

def terrainset():
    terrains=['desert', 'grasslands', 'forest', 'mountains','marshlands', 'hills', 'windy planes']
    newterrain=random.choice(terrains)
    return newterrain

def encounter(terrain,sneak):
    global playername
    run=0
    if terrain=='desert':
        print('the worm fights you')
        enemy=worm
    elif terrain=='mountains':
        print('the yeti fights you')
        enemy=yeti
    elif terrain=='grasslands':
        print('the tigerbear fights you')
        enemy=tigerbear
    elif terrain=='forest':
        print('the troll fights you')
        enemy=troll
    elif terrain=='marshlands':
        print('the crocodile attacks you')
        enemy=crocodile
    elif terrain=='hills':
        print('a goblin jumps out from behind a bush!')
        enemy=goblin
    elif terrain=='windy planes':
        print('an eagle swwops down from above!')
        enemy=eagle
    monsterlife=enemy.health
    monsterarmor=enemy.armor
    monsterattack=enemy.attack
    PlayerHealth=player.health
    PlayerArmor=player.armor
    if sneak==True:
        PlayerAttack=player.stealth+player.strength+player.weapon
    else:
        PlayerAttack=player.strength+player.weapon
    while monsterlife>0 and run<5:
        print('type /attack to attack or /dodge to dodge')
        com=input()
        if com=='/attack':
            valid=True
            hit=skillcheck(PlayerAttack,monsterarmor)
            if hit==True:
                print('you hit the monster!')
                damage=(roll(1,6)+PlayerAttack)
                print('you dealt '+str(damage)+' damage!')
                monsterlife=monsterlife-damage
            else:
                print('you did not hit the monster.')
        elif com=='/dodge':
            valid=True
            PlayerArmor=PlayerArmor+5
        else:
            print('invalid command please try again')
            valid=False
        if valid==True and monsterlife>0:
            space()
            print('it is the monster`s turn')
            hit=skillcheck(monsterattack,PlayerArmor)
            if hit==True:
                print('the monster hit you')
                damage=(roll(1,6)+monsterattack)
                print('they dealt '+str(damage)+' damage!')
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
        player.health=PlayerHealth
        print('you have tired the monster out and can run away.')
        return [False,True]
    else:
        print('you killed the monster!')
        player.health=PlayerHealth
        return [True,False]
def journey():
    exp=0
    day=0
    end=False
    strength=player.strength
    stealth=player.stealth
    sight=player.sight
    while exp<3:
        PlayerHealth=player.health
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
                player.health=PlayerHealth
            elif Pass==True:
                print('you see a tigerbear attempting to sneak up on you.')
        elif terrain=='marshlands':
            print('the marsh gives way below you and you attempt to swim towards the land!')
            Pass=skillcheck(strength,9+day)
            if Pass==False:
                print('you are sucked into the swamp and drown')
                end=True
            elif Pass==True:
                print('you manage to swim to shore and pull yourself out you are alive, but wet and gross.')
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
                    print('you manage to approach unheard and will get a sneak attack')
            WinFight=encounter(terrain,sneak)
            if WinFight[0]==True and WinFight[1]==False:
                loot=['a better weapon','a sheild','a lifestone']
                monloot=loot[random.randint(0,2)]
                print('you found '+monloot+' in the remains')
                if monloot=='a better weapon':
                    player.weapon= player.weapon+1
                elif monloot=='a sheild':
                    player.armor=player.armor+1
                elif monloot=='a lifestone':
                    PlayerHealth=PlayerHealth+5
                    player.health=PlayerHealth
                    print('you gained five health. you are now at '+str(player.health))
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
def BossFight():
    terrain=terrainset()
    if terrain=='hills' or 'mountains':
        boss=dragon
        name='dragon'
    elif terrain=='windy planes' or 'desert' or 'grasslands':
        boss=roc
        name='roc'
    elif terrain=='marshlands' or 'forest':
        boss=hag
        name='hag'
    monsterarmor=boss.armor
    monsterattack=boss.attack
    monsterlife=boss.health
    stealth=player.stealth
    valid=False
    while valid==False:
        print('you awake a new day and soon find you are nearing the end of your journey. by noon you find yourself at the lair of a '+name)
        print('do you attempt to sneak in or do you charge in and use your powerful thighs to make an extra powerful smack on the dragon?')
        print('type /sneak to sneak in or /run to run in')
        com=input()
        if com=='/sneak':
            valid=True
            Pass=skillcheck(stealth,12)
            if Pass==True:
                sneak=True
                print('you snuck up on the '+name+' and will hit him very hard the first time')
            else:
                sneak=False
                print('the '+name+' sees you and you must now prepare for battle!')
        elif com=='/run':
            valid=True
            sneak=False
            print('you run in and your blood boils with battle energy as you attack the '+name+'!')
        else:
            print('invalid command please try again')
            valid=False
    PlayerHealth=player.health
    PlayerArmor=player.armor
    if sneak==True:
        PlayerAttack=player.stealth+player.strength+player.weapon
    else:
        PlayerAttack=player.strength+player.weapon
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
            print('the '+name+' finds you VERY ATRACTIVE but still wants to kill you and fuck your corpse so you gotta fight')
        else:
            print('invalid command please try again')
            valid=False
        if valid==True:
            hit=skillcheck(monsterattack,PlayerArmor)
            if hit==True:
                damage=(roll(1,6)+monsterattack)
                PlayerHealth=PlayerHealth-damage
                print('they dealt '+str(damage)+' damage')
                print('your health is now:'+str(PlayerHealth))
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
    if win==True:
        print('you have defeated the boss. you find some coins in the lair and make your way back to town')
        valid=False
        while valid==False:
            print('do you want to purchase something from the shop?')
            print('/yes or /no')
            com=input()
            if com=='/yes':
                print('choose: "/sheild"(+1 armor), "/weapon"(+ attack), "/cloak"(+1 stealth)')
                com=input('buy:')
                if com=='/sheild':
                    player.armor=player.armor+1
                    valid=True
                if com=='/weapon':
                    player.weapon=player.weapon+1
                    valid=True
                if com=='/cloak':
                    player.stealth=player.stealth+1
                    valid=True
            if com=='/no':
                print('I have not built in a money system yet so you will lose you should probably get something')
        print('would you like to go out and try and fight another boss or quit the game?')
        print('/exit, or /return')
        wins=wins+1
    elif win==False:
        losses=losses+1
        print('you were killed you have lost the game. type /exit to exit the game or /return to restart')
    valid=False
    while valid==False:
        com=input()
        if com=='/exit':
            valid=True
            stats=[player.health,player.strength,player.stealth,player.sight,player.armor,player.weapon]
            with open('highscores.txt','a') as wfh:
                wfh.write('\n'+playername+', score,  '+str(wins)+'\n')
            with open('highscores.txt','r') as rf:
                contents=rf.read()
            print(contents)
            with open('characters.txt','a') as wfc:
                wfc.write('\n')
                wfc.write(playername+', health,  '+str(stats[0])+'\n')
                wfc.write(playername+', strength,  '+str(stats[1])+'\n')
                wfc.write(playername+', stealth,  '+str(stats[2])+'\n')
                wfc.write(playername+', sight,  '+str(stats[3])+'\n')
                wfc.write(playername+', armor,  '+str(stats[4])+'\n')
                wfc.write(playername+', weapon,  '+str(stats[5])+'\n')
                wfc.write('\n')
            return False
        elif com=='/return':
            with open('highscores.txt','a') as wfh:
                wfh.write('\n'+playername+', score,  '+str(wins)+'\n')
            with open('highscores.txt','r') as rf:
                contents=rf.read()
            print(contents)
            print('you have restarted the game. wins:'+str(wins)+' losses:'+str(losses))
            player.health=player.maxhealth
            valid=True
            return True
        else:
            print('invalid command please try again.')
dragon=monster(20,12,5)
yeti=monster(10,8,3)
worm=monster(5,10,1)
troll=monster(15,7,3)
tigerbear=monster(5,6,5)
crocodile=monster(8,10,3)
goblin=monster(5,7,1)
eagle=monster(3,10,2)
hag=monster(25,10,5)
roc=monster(20,10,7)
print('Welcome to Caleb`s great adventure game version 12! this is still in development if you experience issues let me know and tell me what choices you made.')
print('to play: enter simple commands from the list and try to defeat as many bosses as possible.')
print('currently there are three bosses: dragon, roc, and hag.')
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
newcharacter=0
while runprog==True:
    win=0
    cont=0
    if newcharacter==0:
        SaveCharacter()
    cont=journey()
    if cont==False:
        win=False
    else:
        win=BossFight()
    restart=endscreen(win)
    runprog=restart
    newcharacter=restart