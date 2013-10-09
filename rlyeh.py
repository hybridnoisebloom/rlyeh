import sfml as sf
import collision
import random
import time
import json

### TO-DO LIST! ###

# collision.collides is the collision detection function, it returns a boolean.

# Window creation
w = sf.RenderWindow(sf.VideoMode(640, 480), "R'lyeh - Development Build", sf.Style.TITLEBAR)

thingy = sf.Clock()

bgm = sf.Music.from_file("bgm.flac")
bgm.loop = True
bgm.volume = 50
music_playing = False

startgame = sf.Sound(sf.SoundBuffer.from_file("startgame.wav"))
cthulhuhit = sf.Sound(sf.SoundBuffer.from_file("cthulhuhit.wav"))

bg1 = sf.Sprite(sf.Texture.from_file("titlebg.png"))
bg2 = sf.Sprite(sf.Texture.from_file("gamebg.png"))

logo = sf.Sprite(sf.Texture.from_file("logo.png"))

title1 = sf.Texture.from_file("title1.png") # Actual title part
title2 = sf.Texture.from_file("title2.png") # Play button
title3 = sf.Texture.from_file("title3.png") # Credits button
title4 = sf.Texture.from_file("title4.png") # Exit button

winnar_winnar_chicken_dinner = sf.Sprite(sf.Texture.from_file("sortawinrar.png"))
you_are_a_fucking_failure = sf.Sprite(sf.Texture.from_file("awwman.png"))

t1 = sf.Sprite(title1)
t1.move(sf.Vector2(320-128, 10))
t2 = sf.Sprite(title2)
t2.move(sf.Vector2(320-128, 148))
t3 = sf.Sprite(title3)
t3.move(sf.Vector2(320-128, 148+138))
t4 = sf.Sprite(title4)
t4.move(sf.Vector2(320-128, 148+138+138))

title_buffer = [t1, t2, t3, t4]

credits = sf.Sprite(sf.Texture.from_file("credits.png"))
# The five Lovecraftian deities I'm using as the bosses (or "necromancers" to refer to the original design)
cth = sf.Sprite(sf.Texture.from_file("cthulhu.png"))
nya = sf.Sprite(sf.Texture.from_file("nyarlathotep.png"))
aza = sf.Sprite(sf.Texture.from_file("azathoth.png"))
yog = sf.Sprite(sf.Texture.from_file("yog-sothoth.png"))
shu = sf.Sprite(sf.Texture.from_file("shub-niggurath.png"))

goo_hp = random.randint(10, 500)
# The generic-brand eldritch monsters you fight in the game
eld1 = sf.Sprite(sf.Texture.from_file("eldritch1.png"))
#eld2 = sf.Sprite(sf.Texture.from_file("eldritch2.png"))
#eld3 = sf.Sprite(sf.Texture.from_file("eldritch3.png"))

# The player character
player = sf.Sprite(sf.Texture.from_file("player.png"))
player.position = sf.Vector2(random.randint(0, 640), random.randint(0, 480))
# Player HP, if you get hit 10 times you die.
hp = 50
# Whetier you're attacking or not.
attacking = False
# A clock that makes sure you only get to attack for 20 seconds straight before taking a "breath" per se
attacking_clock = sf.Clock()

move_dict = {sf.Keyboard.W:sf.Vector2(0, -7), sf.Keyboard.A:sf.Vector2(-7, 0), sf.Keyboard.S:sf.Vector2(0, 7), sf.Keyboard.D:sf.Vector2(7, 0)}
refresh_clock = sf.Clock()
spawn_clock = sf.Clock()
goo_dead = False
enemies_list = []
spawning = True
level = -1
# -1 = logo
# 0 = title
# 1 = actual game
logo_clock = sf.Clock()

winrar = False

goo_num = 0 # great old one number, randomised.

goo = [cth, yog, nya, shu, aza]
goo[goo_num].move(sf.Vector2(random.randint(0, 640), random.randint(0, 480)))

difficulty = 1
skill_lvls = 0

while w.is_open:
    if level == 1 and not music_playing:
        bgm.play()
        music_playing = True
    for e in w.events:
        if type(e) is sf.KeyEvent and e.pressed and level == 1:
            if e.code is sf.Keyboard.SPACE:
                if attacking and attacking_clock.elapsed_time.seconds >= 5:
                    attacking = False
                elif not attacking:
                    attacking = True
                    attacking_clock.restart()
            elif e.code is sf.Keyboard.ESCAPE:
                w.close()
            elif e.code is sf.Keyboard.L_BRACKET:
                goo_hp = 0
            elif e.code is sf.Keyboard.R_BRACKET:
                skill_lvls = 999999
                difficulty = 1000000
                goo_hp = 1
            else:
                try:
                    player.move(move_dict[e.code])
                except KeyError:
                    pass
        elif type(e) is sf.MouseButtonEvent and e.pressed and e.button == sf.Mouse.LEFT:
            for i in range(0, len(title_buffer)):
                if title_buffer[i].global_bounds.contains(e.position):
                    if title_buffer[i].texture == title2:
                        startgame.play()
                        level = 1
                        try:
                            difficulty = json.load(open("save.json"))["difficulty"]
                            skill_lvls = json.load(open("save.json"))["skill_lvl"]
                        except IOError:
                            difficulty = 1
                            skill_lvls = 0
                    elif title_buffer[i].texture == title3:
                        thingy.restart()
                        level = 3
                    elif title_buffer[i].texture == title4:
                        w.close()
                    else:
                        pass
        elif type(e) is sf.KeyEvent and e.pressed and e.code == sf.Keyboard.ESCAPE and level == 3:
            level = 0

    if level == 1 and skill_lvls == 1000000:
        winner_clock = sf.Clock()
        hp = pow(100, 100)
        level = 4
        winrar = True
        if winner_clock.elapsed_time.seconds >= 3:
            w.close()

    if logo_clock.elapsed_time.seconds >= 5 and level == -1:
        level = 0

    if attacking_clock.elapsed_time.seconds >= 5 and attacking:
        attacking = False

    if spawn_clock.elapsed_time.seconds >= .10 and not goo_dead and spawning:
        if len(enemies_list) > 20*difficulty:
            del enemies_list[0:5]
        spawn_clock.restart()
        y = sf.Sprite(sf.Texture.from_file("eldritch1.png"))
        y.move(sf.Vector2(player.position.x + random.randint(64, 128), player.position.y + random.randint(64, 128)))
        x = sf.Sprite(sf.Texture.from_file("eldritch1.png"))
        x.move(sf.Vector2(player.position.x + random.randint(64, 128), player.position.y + random.randint(64, 128)))
        z = sf.Sprite(sf.Texture.from_file("eldritch1.png"))
        z.move(sf.Vector2(player.position.x + random.randint(64, 128), player.position.y + random.randint(64, 128)))
        a = sf.Sprite(sf.Texture.from_file("eldritch1.png"))
        a.move(sf.Vector2(player.position.x + random.randint(64, 128), player.position.y + random.randint(64, 128)))
        enemies_list.append(x)
        enemies_list.append(y)
        enemies_list.append(z)
        enemies_list.append(a)

    if not spawning and spawn_clock.elapsed_time.seconds >= 5:
        spawning = True

    if collision.collides(goo[goo_num].global_bounds, player.global_bounds) and attacking:
        cthulhuhit.play()
        goo_hp -= 10
        attacking = False
        spawning = False
        spawn_clock.restart()
        goo[goo_num].position = sf.Vector2(random.randint(0, 596), random.randint(0, 480-64))

    for i in enemies_list:
        if collision.collides(i.global_bounds, player.global_bounds) and refresh_clock.elapsed_time.seconds > 1 and not attacking:
            hp -= 5
            refresh_clock.restart()
        elif collision.collides(i.global_bounds, player.global_bounds) and attacking:
            enemies_list.remove(i)
        else:
            continue

    for i in enemies_list:
        if i.position.x < 0 or i.position.y < 0:
            enemies_list.remove(i)

    if goo[goo_num].position.x < 0 or goo[goo_num].position.y < 0 or goo[goo_num].position.x > 640 or goo[goo_num].position.y > 480:
        goo[goo_num].position = sf.Vector2(random.randint(0, 640-64), random.randint(0, 480-64))

    if player.position.x < 0 or goo[goo_num].position.y < 0 or player.position.x > 640 or player.position.y > 480:
        player.position = sf.Vector2(random.randint(0, 640), random.randint(0, 480))

    if goo_hp <= 0:
        goo_dead = True

    if hp <= 0:
        level = 4
        winrar = False
        loser_clock = sf.Clock()
        if loser_clock.elapsed_time.seconds >= 3:
            w.close()
    if goo_dead:
        goo_num = random.randint(0, 4)
        goo_dead = False
        goo_hp = random.randint(10, 500)
        skill_lvls += 1
        difficulty += 1
        json.dump({"skill_lvl": int(skill_lvls), "difficulty": difficulty}, open("save.json", "w"))

    w.clear(sf.Color.RED)
    if level == -1:
        w.draw(logo)
    elif level == 1:
        w.draw(bg2)
        w.draw(player)
        goo[goo_num].move(sf.Vector2(random.randint(-5, 5), random.randint(-5, 5)))
        w.draw(goo[goo_num])
        for i in range(0, len(enemies_list)):
            enemies_list[i].move(sf.Vector2(random.randint(-10, 10), random.randint(-10, 10)))
            w.draw(enemies_list[i])
    elif level == 0:
        w.draw(bg1)
        for i in range(0, len(title_buffer)):
            w.draw(title_buffer[i])
    elif level == 3:
        w.draw(bg1)
        w.draw(credits)
    elif level == 4:
        if winrar:
            w.draw(winnar_winnar_chicken_dinner)
        elif not winrar:
            w.draw(you_are_a_fucking_failure)
    print "Player HP: "+str(hp)
    print "Boss HP: "+str(goo_hp)
    print "Level: "+str(skill_lvls)
    print "Difficulty: "+str(difficulty)
    w.display()
