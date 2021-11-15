from pygame import time
import pygame
from constants import *
class TextBox:
    def __init__(self,location, size, bg = COOL_BLACK, fg = COOL_BLACK, text = "",font_familly = None,font_size= 16, border = True, broder_width = 2, padding = (5,5)):
        self.location = location
        self.size = size
        self.bg = bg
        self.fg = fg
        self.border = border
        self.border_width = broder_width
        self.padding = padding
        self.text = text
        self.rect = pygame.Rect(location[0], location[1], size[0], size[1])
        self.font = pygame.font.Font(font_familly, font_size)
        self.text_surfaces = []
        self.get_text_surfaces()
    def get_text_surfaces(self):
        if self.check_if_text_can_be_full_line_on_surface(self.text):
            self.text_surfaces = [self.font.render(self.text, True, self.fg)]
        else:
            self.get_text_splitted(self.text)
         
    def check_if_text_can_be_full_line_on_surface(self,text):
        width = self.size[0]
        text_width = self.font.render(text, True, self.fg).get_width()
        return text_width <= width -self.padding[0]
            
    def get_text_splitted(self, text):
        words = text.split()
        accumulated = ""
        for index, word in enumerate(words):
            accumulated += " "+word
            accumulated_surface_width = self.font.render(accumulated, True, self.fg).get_width()
            
            if accumulated_surface_width > self.size[0] - self.padding[0]:
                self.text_surfaces.append(self.font.render(" ".join(words[:index]), True, self.fg))
                left_over = " ".join(words[index:])
                
                if self.check_if_text_can_be_full_line_on_surface(left_over):
                    
                    self.text_surfaces.append(self.font.render(left_over, True, self.fg))
                    break
                else:
                    self.get_text_splitted(left_over)
                    break
        
    def draw(self,screen):
        surfaces_height_sum = sum([surface.get_height() for surface in self.text_surfaces])
        height = self.size[1]
        if surfaces_height_sum + self.padding[1] > height:
            self.rect.height = surfaces_height_sum + self.padding[1]
        for i,surface in enumerate(self.text_surfaces):
            surface_height = surface.get_height()
            
            screen.blit(surface, (self.rect.x+self.padding[0], self.rect.y+self.padding[1]+ surface_height*i))
        # Blit the rect.
        if self.border:
            pygame.draw.rect(screen, self.bg, self.rect, self.border_width)
        else:
            pygame.draw.rect(screen, self.bg, self.rect)
class InputBox:

    def __init__(self,location, size, text='', bg = GREY, active_color = COOL_BLACK, inactive_color = GREY,font_size = 32, padding = (5,15), border = True, border_width = 2):
        self.rect = pygame.Rect(location[0],location[1], size[0], size[1])
        self.bg = bg
        self.fg_active= active_color
        self.fg_inactive = inactive_color
        self.fg = inactive_color
        self.text = text
        self.border = border
        self.border_width = border_width
        self.padding = padding
        self.FONT = pygame.font.Font(None, font_size)
        self.txt_surface = self.FONT.render(text, True, self.fg)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
                self.text = ""
            else:
                self.active = False
            # Change the current color of the input box.
            self.fg = self.fg_active if self.active else self.fg_inactive
            self.bg = self.fg_active if self.active else self.fg_inactive
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 4:
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.fg)

    def update(self):
        # Resize the box if the text is too long.
        width = max(50, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + self.padding[0], self.rect.y+ self.padding[1]))
        # Blit the rect.
        if self.border:
            pygame.draw.rect(screen, self.bg, self.rect, self.border_width)
        else:
            pygame.draw.rect(screen, self.bg, self.rect)
class Button:
    def __init__(self, text, location, action, bg=COOL_BLACK, fg=WHITE,hover_color = GREY, size=(175, 40), font_name="FreeMono, Monospace", font_size=16, active = True):
        self.color = bg  # the static (normal) color
        self.bg = bg  # actual background color, can change on mouseover
        self.fg = fg  # text color
        self.hover_color = hover_color
        self.size = size
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text = text
        self.text_surf = self.font.render(self.text, 1, self.fg)
        self.text_rect = self.text_surf.get_rect(center=[s//2 for s in self.size])

        self.surface = pygame.surface.Surface(size)
        self.rect = self.surface.get_rect(center=location)

        self.call_back_ = action
        self.active = active

    def draw(self, window):
        self.mouseover()

        self.surface.fill(self.bg)
        self.surface.blit(self.text_surf, self.text_rect)
        window.blit(self.surface, self.rect)

    def mouseover(self):
        self.bg = self.color
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            self.bg = self.hover_color if self.active else self.bg
    def call_back(self):
        if self.active:
            self.call_back_()
    def activate(self):
        self.active = True
        pygame.display.update()
    def deactivate(self):
        self.active = False
        pygame.display.update()

class Node:
    def __init__(self, value, location, size = (15,15), bg= COOL_BLACK, fg = COOL_BLACK):
        self.value = value
        self.location = location
        self.size = size
        self.bg = bg
        self.fg = fg
        self.active = False
        self.is_key_location = False
        self.font = pygame.font.SysFont('FreeMono, Monospace', 24)
       
    def draw(self, window):
        if self.active:
            if self.is_key_location:
                pygame.draw.rect(window, (COOL_GREEN), (self.location , self.size))
            else:
                pygame.draw.rect(window, (COOL_RED), (self.location , self.size))
        else:
            pygame.draw.rect(window, (self.bg), (self.location, self.size),2)
        window.blit(self.font.render(self.value, True, self.bg), (self.location[0] + (5 if len(self.value) > 1 else 10), self.location[1] + 20))
        
    def animate_as_key(self, func_callback, window, delay= 2000):
        self.active = True
        self.is_key_location = True
        func_callback(window)
        pygame.display.update()
        time.delay(delay)
        self.active = False
        self.is_key_location = False
        pygame.display.update()
    def animate_as_passed_by(self, func_callback,window, delay = 500):
        self.active = True
        func_callback(window)
        pygame.display.update()
        time.delay(delay)
        self.active = False
        func_callback(window)
        pygame.display.update()

    def __str__(self):
        return "Node value" + str(self.value)
    def __repr__(self):
        return str(self.value)
