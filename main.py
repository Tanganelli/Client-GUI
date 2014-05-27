import time
import pygame
from pygame.constants import MOUSEBUTTONDOWN
from FrameBuffer import PyScope
import xml.etree.ElementTree as ET

__author__ = 'jacko'


class ReadConfiguration(object):
    def __init__(self, conf_file):
        tree = ET.parse(conf_file)
        root = tree.getroot()
        for t in root.findall('type'):
            name = t.get('name')
            image = t.find('file').text
            print name, image

    def create_gui(self):
        scope = PyScope()
        button = scope.create_button()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == MOUSEBUTTONDOWN:
                    if button.pressed(pygame.mouse.get_pos()):
                        pygame.quit()
                        return


conf = ReadConfiguration("conf.xml")
conf.create_gui()
#scope.display_image()
