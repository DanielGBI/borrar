import math
import random
import arcade




SPRITE_SCALING_PLAYER= 0.2
SPRITE_SCALING_BULLET= 0.2
SPRITE_SCALING_COIN=0.4
SCREEN_WIDTH=800
SCREEN_HEIGHT=600
BULLET_SPEED= 5
MOVEMENT_SPEED= 7


class pez(arcade.Sprite):
    def __init__(self,filename,sprite_scaling):
        super().__init__(filename, sprite_scaling)








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
class MyGame(arcade.Window):
    def __init__(self):
        """Initializer"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, "Sprite Example")
        self.player_list= None
        self.bullet_list = None
        self.coin_list = None
        self.obstaculo_list = None
        #player info
        self.ship = None
        self.enemigo_list=None
        self.ataques_list=None


        self.score = 0

        arcade.set_background_color(arcade.color.AMAZON)



    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.enemigo_list=arcade.SpriteList()
        self.ataques_list=arcade.SpriteList()
        self.ship = arcade.Sprite("barco.png", SPRITE_SCALING_PLAYER)
        self.ship.center_x= 100
        self.ship.center_y=80
        self.player_list.append(self.ship)
        enemigo = pez("barco.png", SPRITE_SCALING_PLAYER)
        enemigo.center_x = 30
        enemigo.center_y = 400
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

    def on_draw(self):
            """ Render the screen. """

            # This command has to happen before we start drawing
            arcade.start_render()

            # Draw all the sprites.
            self.coin_list.draw()
            self.bullet_list.draw()
            self.player_list.draw()
            self.enemigo_list.draw()
            self.ataques_list.draw()
    def on_key_press(self, key, modifiers):
            """Called whenever a key is pressed. """

            if key == arcade.key.UP:
                self.ship.change_y = MOVEMENT_SPEED
            elif key == arcade.key.DOWN:
                self.ship.change_y = -MOVEMENT_SPEED
            elif key == arcade.key.LEFT:
                self.ship.change_x = -MOVEMENT_SPEED
            elif key == arcade.key.RIGHT:
                self.ship.change_x = MOVEMENT_SPEED
    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.ship.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.ship.change_x = 0

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
    def disparo_enemigo(self, delta_time):
        for enemigo in self.enemigo_list:
            ataque = arcade.Sprite("coin_01.png", SPRITE_SCALING_BULLET)
            start_x = enemigo.center_x
            start_y = enemigo.center_y
            ataque.center_x = start_x
            ataque.center_y = start_y
            ataque.change_y = -BULLET_SPEED
            self.ataques_list.append(ataque)

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
                hit_list = arcade.check_for_collision_with_list(player, self.coin_list)
                for coin in hit_list:
                    coin.remove_from_sprite_lists()
                    self.score += 1
            for bullet in self.bullet_list:

                # Check this bullet to see if it hit a coin
                hit_list = arcade.check_for_collision_with_list(bullet, self.coin_list)

                # If it did, get rid of the bullet
                if len(hit_list) > 0:
                    bullet.remove_from_sprite_lists()

                # For every coin we hit, add to the score and remove the coin
                for coin in hit_list:
                    coin.remove_from_sprite_lists()
                    self.score += 1

                # If the bullet flies off-screen, remove it.
                if bullet.bottom > self.width or bullet.top < 0 or bullet.right < 0 or bullet.left > self.width:
                    bullet.remove_from_sprite_lists()



def main():
        game = MyGame()
        game.setup()
        arcade.run()


if __name__ == "__main__":
        main()
