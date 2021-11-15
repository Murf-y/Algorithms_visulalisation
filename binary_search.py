
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
pygame.display.set_caption("Binary Search")

class Nodes():
    def __init__(self):
        self.nodes = []
    def add_node(self, node:Node):

        self.nodes.append(node)
        self.nodes.sort(key=lambda x: int(x.value))
       
    def draw_nodes(self,window):
        for node in self.nodes:
            node.draw(window)
            
    def delete_node(self):
        self.nodes.pop()
    def clear(self):
        self.nodes.clear()
    def __len__(self):
        return len(self.nodes)
    def __iter__(self):
        return iter(self.nodes)

running = True
nodes = Nodes()
values_added = []
buttons = []
def draw_nodes(window):
    nodes.draw_nodes(window)
def get_non_generated_random_number(min,max):
    number = random.randint(min,max)
    while number in values_added:
        number = random.randint(min,max)
    return number
def init_n_nodes(n):
    def gen():
        number = get_non_generated_random_number(1,50)
        values_added.append(number)
        return number
    numbers = [gen() for _ in range(0,n)]
    numbers.sort()
    for i, num in enumerate(numbers):
        nodes.add_node(Node(str(num), (30 + i * 50, 200), (40,65), COOL_BLACK, WHITE))

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
        values_added.sort()
        nodes.clear()
        for i,num in enumerate(values_added):
            nodes.add_node(Node(str(num), (30 + i * 50, 200), (40,65), COOL_BLACK, WHITE))
        
        pygame.display.update()
def delete_node():
    if len(nodes)>1:
        nodes.delete_node()
        values_added.pop()
    pygame.display.update()
def shuffle_nodes():
    n = len(nodes)
    nodes.clear()
    values_added.clear()
    init_n_nodes(n)
def binary_search_algo(key):
    low = 0
    high = len(nodes) - 1
    nodes.nodes[low].animate_as_passed_by(draw_nodes, window, delay = 700)
    nodes.nodes[high].animate_as_passed_by(draw_nodes, window,  delay = 700)

    while low <= high:
        mid = (low + high) // 2
        nodes.nodes[mid].animate_as_passed_by(draw_nodes, window, delay = 700)
        if int(nodes.nodes[mid].value) == key:
            nodes.nodes[mid].animate_as_key(draw_nodes, window, delay = 4000)
            return mid
        elif int(nodes.nodes[mid].value) > key:
            high = mid - 1
        else:
            low = mid + 1
    return -1

def binary_search():
    global text_box_1
    key = get_key_from_box()
    result_index = binary_search_algo(key)
    print(f"{result_index=}")
    text_box_1 = TextBox((70,500), (120,50), text=f"Key is {key} at index {result_index}")

start_button = Button("Binary Search", (100, 580 ), binary_search)
shuflle_button = Button("shuffle", (850, 490 ),shuffle_nodes)
add_node_button = Button("Add Node", (850, 550), add_node)
delete_node_button = Button("Delete Node", (850,610),delete_node)
buttons.append(start_button)
buttons.append(add_node_button)
buttons.append(delete_node_button)
buttons.append(shuflle_button)
input_box = InputBox((13.5,500),(25,50),"0")
text_box_1 = TextBox((70,500), (120,50), text="Enter a key to search for its index in the list", padding=(15,10))
text_box_2 = TextBox((450,470), (300,160), text="Binary search is a search algorithm that eliminates unessecary subsequent to find the key, O(Log2(n)).", font_size=32, padding=(20,20))
def draw_things(window):
    for button in buttons:
        button.draw(window)
    draw_nodes(window)
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