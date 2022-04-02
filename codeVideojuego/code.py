import math
import random
import arcade
from pyglet.math import Vec2



SPRITE_SCALING_PLAYER= 0.2
SPRITE_SCALING_BULLET= 0.2
SPRITE_SCALING_COIN=0.4
SCREEN_WIDTH=800
SCREEN_HEIGHT=600
BULLET_SPEED= 5
MOVEMENT_SPEED= 7
an_vel=10
ENEMY_MOVEMENT=7

class player(arcade.Sprite):
    def __init__(self,filename, SPRITE_SCALING_PLAYER):
        super().__init__(filename, SPRITE_SCALING_PLAYER)
        self.speed=0
        self.respawning=0
        self.vida=3
        self.respawn()
    def respawn(self):
        self.respawning=0
        self.change_x=0
        self.change_y = 0
        self.center_x =70
        self.center_y=100

    def update(self):
        if self.respawning:
            self.respawning+=1
            self.alpha=self.respawning
            if self.respawning>250:
                self.respawning=0
                self.alpha=255
        if self.center_x==0:
            self.center_x-=self.angle
        self.angle=self.change_angle
        self.center_x+= self.angle
        self.center_y+=self.speed
class pez(arcade.Sprite):
    def __init__(self,filename,sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.vida=2
        self.speed=0
        self.numero=0
        self.control=0
        self.start_x=0
        self.start_y=0
        self.center_x=0
        self.center_y=0
        self.action=30
        self.act0=30
        self.limite_abajo=50
        self.x=20
        self.y=20
    def update(self):
        if self.center_x>=SCREEN_HEIGHT or self.center_y<=0 or self.limite_abajo<50:
            self.center_y += MOVEMENT_SPEED - 2
            self.center_x -=1
            self.control += 1
            self.limite_abajo-=1
        elif self.center_x<=0  or self.act0<30:
            self.center_x += MOVEMENT_SPEED - 2
            self.control += 1
            self.act0-=1
        elif self.center_y>=SCREEN_WIDTH or self.action<30 or self.center_y>=self.start_y+50:
            self.center_x += -5
            self.center_y += -5
            self.control += 1
            self.action-=1
        elif False == (self.center_x - self.start_x >= 30):
            self.center_x += MOVEMENT_SPEED - 2
            self.control += 1
        elif self.center_x-self.start_x>=30 :
            self.center_y+=MOVEMENT_SPEED-2
            self.control += 1

        if self.action==0 or self.act0==0 or self.limite_abajo==0:
            self.action=30
            self.act0=30
            self.limite_abajo=50
class ataque_pez(arcade.Sprite):
    def __init__(self,filename,sprite_scaling):
        super().__init__(filename, sprite_scaling)
        self.speed=0
        self.center_x = 0
        self.center_y = 10
    def update(self):
        self.center_y+=-BULLET_SPEED
class obstaculo(arcade.Sprite):

    def __init__(self, filename, sprite_scaling):
        """ Constructor. """
        # Call the parent class (Sprite) constructor
        super().__init__(filename, sprite_scaling)

        # Current angle in radians
        self.circle_angle = 0

        # How far away from the center to orbit, in pixels
        self.circle_radius = 0

        # How fast to orbit, in radians per frame
        self.circle_speed = 0.008

        # Set the center of the point we will orbit around
        self.circle_center_x = 0
        self.circle_center_y = 0

    def update(self):

        """ Update the ball's position. """
        # Calculate a new x, y
        self.center_x = self.circle_radius * math.sin(self.circle_angle) \
            + self.circle_center_x
        self.center_y = self.circle_radius * math.cos(self.circle_angle) \
            + self.circle_center_y

        # Increase the angle in prep for the next round.
        self.circle_angle += self.circle_speed
class InstructionView(arcade.View):
    def __init__(self):
        super().__init__()
        self.texture=arcade.load_texture("mapa1.png")
        self.texture2=arcade.load_texture("coin_01.png")

        arcade.set_viewport(0, SCREEN_HEIGHT-1,0,SCREEN_WIDTH-1)
    def on_draw(self):
        arcade.start_render()
        self.texture.draw_sized(SCREEN_HEIGHT/2,SCREEN_WIDTH/2,SCREEN_HEIGHT,SCREEN_WIDTH)
        self.texture2.draw_sized(SCREEN_HEIGHT-100,SCREEN_WIDTH-100,100,100)
    def on_mouse_press(self,_x,_y,_button, _modifiers):
        print(_x,_y)
        if _x in range(SCREEN_HEIGHT-150,SCREEN_HEIGHT-50) and _y in range(SCREEN_WIDTH-150,SCREEN_WIDTH-50):
            game_view=MyGame(SCREEN_HEIGHT,SCREEN_WIDTH,"Sprite Example")
            game_view.setup()
            self.window.show_view(game_view)
class MyGame(arcade.View):
    def __init__(self,Width,heiht,title):
        """Initializer"""
        super().__init__()
        self.player_list= None
        self.bullet_list = None
        self.coin_list = None
        self.obstaculo_list = None
        #player info
        self.ship = None
        self.enemigo_list=None
        self.ataques_list=None
        self.background_list=None

        self.score = 0
        self.camera_sprites = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.camera_gui = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        arcade.set_background_color(arcade.color.AMAZON)
    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemigo_list=arcade.SpriteList()
        self.ataques_list=arcade.SpriteList()
        self.ship = player("barco.png", SPRITE_SCALING_PLAYER)
        self.ship.center_x= 100
        self.ship.center_y=80
        self.player_list.append(self.ship)

        for i in range(8):
            enemigo = pez("barco.png", SPRITE_SCALING_PLAYER)
            enemigo.center_x = random.randrange(SCREEN_HEIGHT)
            enemigo.center_y = random.randrange(SCREEN_WIDTH)
            enemigo.start_x = enemigo.center_x
            enemigo.start_y = enemigo.center_y
            self.enemigo_list.append(enemigo)

        for i in range(50):

            # Create the coin instance
            # Coin image from kenney.nl
            coin = obstaculo("coin_01.png", SPRITE_SCALING_COIN /3)

            # Position the center of the circle the coin will orbit
            coin.circle_center_x = random.randrange(SCREEN_HEIGHT)
            coin.circle_center_y = random.randrange(SCREEN_WIDTH)

            # Random radius from 10 to 200
            coin.circle_radius = random.randrange(10, 200)

            # Random start angle from 0 to 2pi
            coin.circle_angle = random.random() * 2 * math.pi
            coin.center_x=random.randrange(SCREEN_HEIGHT)
            coin.center_y = random.randrange(SCREEN_WIDTH)
            # Add the coin to the lists
            self.coin_list.append(coin)

            self.background_list = arcade.SpriteList()

            self.background_sprite = arcade.Sprite("mapa1.png",1.5)

            self.background_sprite.center_x = (SCREEN_WIDTH // 2)-100
            self.background_sprite.center_y = 700
            self.background_sprite.change_y = -2

            self.background_list.append(self.background_sprite)

            # second background image
            self.background_sprite_2 = arcade.Sprite("mapa1.png",1.5)

            self.background_sprite_2.center_x = SCREEN_WIDTH // 2
            self.background_sprite_2.center_y = SCREEN_HEIGHT +800
            self.background_sprite_2.change_y = -2

            self.background_list.append(self.background_sprite_2)
    def on_draw(self):
            """ Render the screen. """

            # This command has to happen before we start drawing
            arcade.start_render()

            # Draw all the sprites.

            self.background_list.draw()
            self.coin_list.draw()
            self.bullet_list.draw()
            self.player_list.draw()
            self.enemigo_list.draw()
            self.ataques_list.draw()

            arcade.draw_text('Score : ' + str(self.ship.vida), 150.0, 500.0,
                     arcade.color.RED, 20, 180, 'left')
    def on_key_press(self, key, modifiers):
            """Called whenever a key is pressed. """

            if key == arcade.key.UP:
                self.ship.speed = MOVEMENT_SPEED
            elif key == arcade.key.DOWN:
                self.ship.speed = -MOVEMENT_SPEED
            elif key == arcade.key.LEFT:
                self.ship.change_angle = -an_vel
            elif key == arcade.key.RIGHT:
                self.ship.change_angle = an_vel
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.ship.speed = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.ship.change_angle = 0

    def on_mouse_press(self, x, y, button, modifiers):
        """ Called whenever the mouse button is clicked. """

        # Create a bullet
        bullet = arcade.Sprite("coin_01.png", SPRITE_SCALING_BULLET)

        # Position the bullet at the player's current location
        start_x = self.ship.center_x
        start_y = self.ship.center_y
        bullet.center_x = start_x
        bullet.center_y = start_y

        bullet.change_y = BULLET_SPEED

        # Add the bullet to the appropriate lists
        self.bullet_list.append(bullet)

    def disparo_enemigo(self):

        for enemigo in self.enemigo_list:

            if type(enemigo)==pez:
                if enemigo.control==42:
                    ataque = ataque_pez("coin_01.png", SPRITE_SCALING_BULLET)
                    start_x = enemigo.center_x
                    start_y = enemigo.center_y
                    ataque.center_x = start_x
                    ataque.center_y = start_y
                    self.ataques_list.append(ataque)
                    enemigo.control=0

    def on_update(self, delta_time):
            """ Movement and game logic """

            # Call update on all sprites
            self.bullet_list.update()
            self.player_list.update()
            self.enemigo_list.update()
            self.disparo_enemigo()
            self.ataques_list.update()

            # Loop through each bullet
            for player in self.player_list:
                if player.vida==0:
                    player.remove_from_sprite_lists()
                hit_list = arcade.check_for_collision_with_list(player, self.coin_list)
                for coin in hit_list:
                    coin.remove_from_sprite_lists()
                    self.score += 1
            for ataque in self.ataques_list:
                hit_list= arcade.check_for_collision_with_list(ataque, self.player_list)
                if len(hit_list)>0:
                    self.ship.vida-=1
                    ataque.remove_from_sprite_lists()
            for bullet in self.bullet_list:

                # Check this bullet to see if it hit a coin
                hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)
                hit_list_enemigo= arcade.check_for_collision_with_list(bullet, self.enemigo_list)
                # If it did, get rid of the bullet
                if len(hit_list) > 0:
                    bullet.remove_from_sprite_lists()
                for enemigo in hit_list_enemigo:
                    enemigo.vida-=1
                    if enemigo.vida==0:
                        enemigo.remove_from_sprite_lists()
                # For every coin we hit, add to the score and remove the coin
                for coin in hit_list:
                    coin.remove_from_sprite_lists()
                    self.score += 1

                # If the bullet flies off-screen, remove it.
                if bullet.bottom > SCREEN_WIDTH or bullet.top < 0 or bullet.right < 0 or bullet.left > SCREEN_WIDTH:
                    bullet.remove_from_sprite_lists()
            if self.background_sprite.center_y <= -300 :
                self.background_sprite.center_y = SCREEN_HEIGHT + 900 // 2

            if self.background_sprite_2.center_y <= -300:
                self.background_sprite_2.center_y = SCREEN_HEIGHT + 900 // 2

            self.background_list.update()



    def scroll_to_player(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        position = Vec2(self.ship.center_x - SCREEN_WIDTH / 2,
                        self.ship.center_y - SCREEN_HEIGHT / 2)
        self.camera_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self,SCREEN_WIDTH,SCREEN_HEIGHT):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(int(SCREEN_WIDTH), int(SCREEN_HEIGHT))
        self.camera_gui.resize(int(SCREEN_WIDTH), int(SCREEN_HEIGHT))


def main():
        Window=arcade.Window(SCREEN_HEIGHT,SCREEN_WIDTH,"Sprite Example")
        start_View=InstructionView()
        Window.show_view(start_View)
        arcade.run()

if __name__ == "__main__":
        main()
