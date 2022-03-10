import arcade
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def draw_grass():
    """ Draw the ground """
    arcade.draw_lrtb_rectangle_filled(0, SCREEN_WIDTH, SCREEN_HEIGHT / 3, 0, arcade.color.AIR_SUPERIORITY_BLUE)
def draw_robot(x, y):
    """

    :return:
    """
    arcade.draw_point(x, y, arcade.color.RED, 5)
    arcade.draw_rectangle_filled(x +400,y + 500, 50,70,[1,1,1])
    arcade.draw_rectangle_filled(x + 400,y + 450, 70,90,[1,1,1])
    arcade.draw_rectangle_filled(x + 430,y + 400, 30, 50, [1, 1, 1])
    arcade.draw_rectangle_filled(x + 370,y + 400, 30, 50, [1, 1, 1])
    arcade.draw_rectangle_filled(x + 430,y + 480, 80, 20, [1, 1, 1])
    arcade.draw_rectangle_filled(x + 370,y + 480, 80, 20, [1, 1, 1])

def on_draw(delta_time):
    """"""
    arcade.start_render()
    draw_grass()
    draw_robot(on_draw.robot_x,-300)

    on_draw.robot_x += 1
on_draw.robot_x = -300
def main():
    """

    :return:
    """
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Drawing with Functions")
    arcade.set_background_color(arcade.color.DARK_BLUE)
    arcade.schedule (on_draw, 1 / 600)

    arcade.run()


main()

