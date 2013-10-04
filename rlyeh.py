import sfml as sf
import collision
import random

# collision.collides is the collision detection function, it returns a boolean.

# Window creation
w = sf.RenderWindow(sf.VideoMode(640, 480), "R'lyeh - Development Build", sf.Style.TITLEBAR)

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

while w.is_open:
    for e in w.events:
        if type(e) is sf.KeyEvent and e.pressed:
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

    if collision.collides(cth.global_bounds, player.global_bounds) and attacking:
        cth_hp -= 1
        attacking = False
        cth.position = sf.Vector2(random.randint(0, 596), random.randint(0, 480-64))

    for i in enemies_list:
        if collision.collides(i.global_bounds, player.global_bounds) and refresh_clock.elapsed_time.seconds > 1 and not attacking:
            hp -= 5
            refresh_clock.restart()
        elif collision.collides(i.global_bounds, player.global_bounds) and attacking:
            enemies_list.remove(i)
        else:
            continue

    if cth_hp <= 0:
        cth_dead = True

    if hp <= 0:
        w.close()
        print "You lose!"

    if cth_dead:
        w.close()
        print "You win!"
    w.clear()
    w.draw(player)
    cth.move(sf.Vector2(random.randint(-5, 5), random.randint(-5, 5)))
    w.draw(cth)
    for i in range(0, len(enemies_list)):
        enemies_list[i].move(sf.Vector2(random.randint(-10, 10), random.randint(-10, 10)))
        w.draw(enemies_list[i])
    print hp
    print len(enemies_list)
    print attacking
    w.display()
