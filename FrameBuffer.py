import array
import cairo
import rsvg
import os
import pygame
from pygame.constants import MOUSEBUTTONDOWN
from button import buttons

__author__ = 'jacko'


class PyScope:
    screen = None

    def __init__(self):

        """Ininitializes a new pygame screen using the framebuffer"""
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)

        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break

        if not found:
            raise Exception('No suitable video driver found!')

        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        self.screen_size = size
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()


    def __del__(self):
        """Destructor to make sure pygame shuts down, etc."""

    def test(self):
        # Fill the screen with red (255, 0, 0)
        red = (255, 255, 255)
        self.screen.fill(red)
        # Update the display
        pygame.display.update()

    def display_image(self):
        svg = rsvg.Handle(file="images/thermometer.svg")
        width, height, dw, dh = svg.get_dimension_data()
        data = array.array('c', chr(0) * width * height * 4)
        surface = cairo.ImageSurface.create_for_data(
            data, cairo.FORMAT_ARGB32, width, height, width * 4)

        ctx = cairo.Context(surface)
        screen_width = self.screen_size[0]
        screen_height = self.screen_size[1]

        factor_x = (screen_width / 100.0) * 10
        factor_y = (screen_height / 100.0) * 10

        factor = min(factor_x, factor_y)
        ctx.scale(factor / width, factor / height)
        svg.render_cairo(ctx)

        image = pygame.image.frombuffer(data.tostring(), (width, height), "ARGB")
        self.screen.blit(image, (10, 10))
        # Render the screen
        pygame.display.update()

    def create_button(self):
        button = buttons.Button()
        #Parameters:               surface,      color,       x,   y,   length, height, width,    text,      text_color
        button.create_button(self.screen, (107, 142, 35), 225, 135, 200,    100,    0, "Example", (255, 255, 255))
        pygame.display.flip()
        return button
