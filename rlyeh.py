import sfml as sf
import collision
import random
import time

### TO-DO LIST! ###
## TODO: Add logo screen ##
## TODO: Add JSON save games ##
## TODO: Multiple levels (randomize which Great Old One is in which level) ##

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

title1 = sf.Texture.from_file("title1.png") # Actual title part
title2 = sf.Texture.from_file("title2.png") # Play button
title3 = sf.Texture.from_file("title3.png") # Credits button
title4 = sf.Texture.from_file("title4.png") # Exit button

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

cth.move(sf.Vector2(random.randint(200, 500), random.randint(200, 450)))

cth_hp = 50
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
cth_dead = False
enemies_list = []
spawning = True
level = 0
# 0 = logo
# 1 = title
# 2 = actual game

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
                    elif title_buffer[i].texture == title3:
                        thingy.restart()
                        level = 3
                    elif title_buffer[i].texture == title4:
                        w.close()
                    else:
                        pass
        elif type(e) is sf.KeyEvent and e.pressed and e.code == sf.Keyboard.ESCAPE and level == 3:
            level = 0

    if attacking_clock.elapsed_time.seconds >= 5 and attacking:
        attacking = False

    if spawn_clock.elapsed_time.seconds >= .10 and not cth_dead and spawning:
        if len(enemies_list) > 20:
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

    if collision.collides(cth.global_bounds, player.global_bounds) and attacking:
        cthulhuhit.play()
        cth_hp -= 10
        attacking = False
        spawning = False
        spawn_clock.restart()
        cth.position = sf.Vector2(random.randint(0, 596), random.randint(0, 480-64))

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

    if cth.position.x < 0 or cth.position.y < 0 or cth.position.x > 640 or cth.position.y > 480:
        cth.position = sf.Vector2(random.randint(0, 640-64), random.randint(0, 480-64))

    if player.position.x < 0 or cth.position.y < 0 or player.position.x > 640 or player.position.y > 480:
        player.position = sf.Vector2(random.randint(0, 640), random.randint(0, 480))

    if cth_hp <= 0:
        cth_dead = True

    if hp <= 0:
        w.close()
        print "You lose!"

    if cth_dead:
        w.close()
        print "You win!"
    w.clear()
    if level == 1:
        w.draw(bg2)
        w.draw(player)
        cth.move(sf.Vector2(random.randint(-5, 5), random.randint(-5, 5)))
        w.draw(cth)
        for i in range(0, len(enemies_list)):
            enemies_list[i].move(sf.Vector2(random.randint(-10, 10), random.randint(-10, 10)))
            w.draw(enemies_list[i])
    elif level == 0:
        w.draw(bg1)
        for i in range(0, len(title_buffer)):
            w.draw(title_buffer[i])
            print title_buffer
    elif level == 3:
        w.draw(bg1)
        w.draw(credits)
    print hp
    print len(enemies_list)
    print attacking
    w.display()
