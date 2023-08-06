"""
Show GUI Elements

Show how to use GUI elements.

python -m arcade.examples.gui_elements_example
"""
import arcade

import arcade.gui

import os



class MyView(arcade.View):
    """
    Main view. Really the only view in this example. """
    def __init__(self):
        super().__init__()

    def on_draw(self):
        """ Draw this view. GUI elements are automatically drawn. """
        arcade.start_render()

        self.platform_1.draw()
        self.platform_1.draw_hit_box()

    def on_show(self):
        """ Called once when view is activated. """
        self.setup()
        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        """ Set up this view. """

        SPRITES_PATH = r'.'
        self.platform_1 = arcade.Sprite(os.path.join(SPRITES_PATH, 'brick_platform_1.png'))
        self.platform_1.center_x = 300
        self.platform_1.center_y = 300

        print(self.platform_1.hit_box)



if __name__ == '__main__':
    window = arcade.Window(title='ARCADE_GUI')
    view = MyView()
    window.show_view(view)
    arcade.run()