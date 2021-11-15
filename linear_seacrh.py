
import pygame
from pygame import time
from constants import *
import random
from utils import InputBox, TextBox, Button, Node


"""
Visualization of the linear search algorithm using pygame
"""


width = 1000
height = 650

pygame.init()
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Linear Search")

running = True
nodes = []
values_added = []
buttons = []
def draw_nodes(window):
    for node in nodes:
        node.draw(window)
        pygame.display.update()
def get_non_generated_random_number(min,max):
    number = random.randint(min,max)
    while number in values_added:
        number = random.randint(min,max)
    return number
def init_n_nodes(n):
    for i in range(0,n):
        number = get_non_generated_random_number(1,50)
        values_added.append(number)
        nodes.append(Node(str(number), (30 + i * 50, 200), (40,65), COOL_BLACK, WHITE))
init_n_nodes(10)
def get_key_from_box():
    text = input_box.text
    if text.isnumeric():
        return int(text)
    else:
        return 0
def add_node():
    if len(nodes) < 19:
        number = get_non_generated_random_number(1,50)
        values_added.append(number)
        node = Node(str(number), (30 + len(nodes) * 50, 200), (40,65), COOL_BLACK, WHITE)
        nodes.append(node)
        pygame.display.update()
def delete_node():
    if len(nodes)>1:
        nodes.pop()
        values_added.pop()
    pygame.display.update()
def shuffle_nodes():
    n = len(nodes)
    nodes.clear()
    values_added.clear()
    init_n_nodes(n)
def linear_search_algo(key):
    for index , node in enumerate(nodes):
        if key == int(node.value):
            node.animate_as_key(draw_nodes, window)
            return index
        
        node.animate_as_passed_by(draw_nodes, window, delay = len(nodes)* 10)
    return -1
def linear_search():
    global text_box_1
    key = get_key_from_box()
    result_index = linear_search_algo(key)
    text_box_1 = TextBox((70,450), (120,50), text=f"Key is {key} at index {result_index}")
start_button = Button("Linear Search", (100, 580 ), linear_search)
shuflle_button = Button("shuffle", (850, 490 ),shuffle_nodes)
add_node_button = Button("Add Node", (850, 550), add_node)
delete_node_button = Button("Delete Node", (850,610),delete_node)
buttons.append(start_button)
buttons.append(add_node_button)
buttons.append(delete_node_button)
buttons.append(shuflle_button)
input_box = InputBox((13.5,500),(25,50),"0")
text_box_1 = TextBox((70,500), (120,50), text="Enter a key to search for its index in the list", padding=(15,10))
text_box_2 = TextBox((450,470), (300,160), text="Linear search is a search algorithm that loop sequentially through the list to find the key, O(n).", font_size=32, padding=(20,20))
def draw_things(window):
    for button in buttons:
        button.draw(window)
    for node in nodes:
        node.draw(window)
    input_box.draw(window)
    text_box_1.draw(window)
    text_box_2.draw(window)
def mouse_button_down():
    pos = pygame.mouse.get_pos()
    for button in buttons:
        if button.rect.collidepoint(pos):
            if button.active:
                button.call_back()
while running:
    window.fill(COOL_WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        input_box.handle_event(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_button_down()
    draw_things(window)
    input_box.update()
    pygame.display.update()
pygame.quit()
