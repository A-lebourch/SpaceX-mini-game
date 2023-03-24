from pyb import SPI, Pin, LED, delay, UART, Timer
import random
import time
from logo import *

def led1(timer):
    LED(1).toggle()

def led2(timer):
    LED(2).toggle()

def led3(timer):
    LED(3).toggle()

def led4(timer):
    LED(4).toggle()

def clear_screen():
    uart.write("\x1b[2J\x1b[?25l")

def move(x, y):
    uart.write("\x1b[{};{}H".format(y, x))

def read_reg(addr):
    CS.low()
    SPI_1.send(addr | 0x80) 
    tab_values = SPI_1.recv(1) 
    CS.high()
    return tab_values[0]

def convert_value(high, low):
    value = (high << 8) | low
    if value & (1 << 15):
        value = value - (1 << 16)
    return value * 0.06
    
def read_acceleration(base_addr):
    low = read_reg(base_addr)
    high = read_reg(base_addr + 1)
    return convert_value(high, low)

def draw_logo(logo:str, x, y):
    lines = logo.splitlines()
    for index, line in enumerate(lines) :
        move(x, y + index)
        uart.write(line)

def clear_logo(logo:str, x, y):
    lines = logo.splitlines()
    for index, line in enumerate(lines) :
        move(x, y + index)
        uart.write(len(line)*" ")

def boundaries (boundaries_x, boundaries_y):
    for i in range(*boundaries_x):
        move(i, boundaries_x[0])
        uart.write("-")
    for i in range(*boundaries_y):
        move(boundaries_y[0], i)
        uart.write("|")

def shooting (curseur_x, curseur_y, entry, ennemy_pos):
    if entry == 1 :
        for rocket_pos in range(7, 175):
            rocket = [curseur_x + rocket_pos, curseur_y + 1]
            move(rocket[0], rocket[1])
            uart.write("🔴")
            delay(2)
            move(rocket[0]-1, rocket[1])
            uart.write(" ")
            rocket_hit_test(ennemy_pos, rocket)
            if rocket[0] == 175:
                move(rocket[0], rocket[1])
                uart.write(" ")
                break
            
def rocket_hit_test (ennemy_pos, rocket):

    for ennemy_x , ennemy_y in ennemy_pos:
        for y_offset in range(3):
            if rocket == [ennemy_x, ennemy_y + y_offset] :     
                move(ennemy_x, ennemy_y)
                uart.write(" \n\b \n\b ")
                # blink_led()
                ennemy_pos.remove([ennemy_x, ennemy_y])
                spawn_ennemy()
                life_bar(150, True)
                
def spawn_ennemy ():
    x = random.randrange(100,175)
    y = random.randrange(5,50)
    ennemy_pos.append([x, y])
    move(x, y)
    uart.write("❌\n\b\b❌\n\b\b❌")

def menu(btn):
    clear_screen()
    draw_logo(logo_play,96,30)
    draw_logo(logo_score,96,42)
    draw_logo(logo_spacex, x=25, y=15)
    draw_logo(logo_arrow,x=80, y=30)
    while (True):
        
        y_accel = read_acceleration(0x2A)

        if y_accel > 300:
            draw_logo(logo_arrow,x=80, y=42)
            clear_logo(logo_arrow, x=80, y=30)  
            if btn.value() == 1:
                score(btn)
                draw_logo(logo_play,96,30)
                draw_logo(logo_score,96,42)
                draw_logo(logo_spacex, x=25, y=15)
                draw_logo(logo_arrow,x=80, y=30)
                   
        
        if y_accel < 0:
            draw_logo(logo_arrow,x=80, y=30)
            clear_logo(logo_arrow, x=80, y=42)
            if btn.value() == 1:
                clear_screen()
                break 

def score(btn):
    clear_screen()
    draw_logo(logo_score_big, x=25, y=15)
    draw_logo(logo_arrow,x=95, y=45)
    draw_logo(logo_back, x=115, y=45)
    draw_logo(logo_points, x=45, y=35)
    while (True):
        if btn.value()==1 :
            clear_screen()
            break

def life_bar (life_lenght, hit = False):
    global start
    global number_hit
    green_char = "🟩"   #🟩 is two char 
    red_char = "🟥"
    one_life_width = 30

    if start :
        for pixels in range(0,life_lenght,2):
            move(pixels,2)
            uart.write(green_char)
        start = False

    if hit  :
        number_hit += 1
        move(life_lenght - number_hit * one_life_width + 1, 2)
        uart.write(15*red_char)
    
    if number_hit == 5 :
        blink()
        restarting()

def restarting ():
    for i in range(2):
        clear_screen()
        draw_logo(logo_win,x=50,y=25) 
        draw_logo(logo_restarting_1,96,35)
        time.sleep(1)
        clear_screen()
        draw_logo(logo_win,x=50,y=25) 
        draw_logo(logo_restarting_2,96,35)
        time.sleep(1)
        clear_screen()
        draw_logo(logo_win,x=50,y=25) 
        draw_logo(logo_restarting_3,96,35)
        time.sleep(1)

def blink():
    t1 = Timer(1, freq=8)
    t2 = Timer(2, freq=10)
    t3 = Timer(3, freq=12)
    t4 = Timer(4, freq=14)
    t1.callback(led1)
    t2.callback(led2)
    t3.callback(led3)
    t4.callback(led4)
    time.sleep(2)
    t1.deinit()
    t2.deinit()
    t3.deinit()
    t4.deinit()
    LED(1).off()
    LED(2).off()
    LED(3).off()
    LED(4).off()

#/////////////////////////////////////////////////////////////////////////////////////////////////////////::                   

CS = Pin("PE3", Pin.OUT_PP)
SPI_1 = SPI(
    1, 
    SPI.MASTER,
    baudrate=50000,
    polarity=0,
    phase=0,  
)

ennemy_pos = []

uart = UART(2, 115200)

push_button = Pin("PA0", Pin.IN,Pin.PULL_DOWN)

addr_who_am_i = 0x0F
addr_ctrl_reg4 = 0x20

while True:

    number_hit = 0
    curseur_x = 20
    curseur_y = 10
    previous_pos_x = curseur_x
    previous_pos_y = curseur_y
    boundaries_x = [4,150]
    boundaries_y = [4,50]
    start = True
    gaming =True
    first_display = True
    clear_screen()
    menu(push_button)
    boundaries(boundaries_x, boundaries_y)
    spawn_ennemy()
    life_bar(150)

    while(number_hit != 5):

        x_accel = read_acceleration(0x28)
        y_accel = read_acceleration(0x2A)
        z_accel = read_acceleration(0x2C)

        delay(50)
            
        if x_accel < 300:
            curseur_x += 1
            if curseur_x > boundaries_x[1]:
                curseur_x -= 1
        
        if x_accel > -300:
            curseur_x -= 1
            if curseur_x < boundaries_x[0]+1:
                curseur_x += 1
            
        if y_accel > 300:
            curseur_y += 1
            if curseur_y > boundaries_y[1]:
                curseur_y -= 1
            
        if y_accel < -300:
            curseur_y -= 1
            if curseur_y < boundaries_y[0]+1:
                curseur_y += 1

        if curseur_x != previous_pos_x or curseur_y != previous_pos_y or first_display == True:
            move(previous_pos_x, previous_pos_y)
            uart.write("    \n\b\b\b    \n\b\b\b\b\b    ")
            previous_pos_x = curseur_x
            previous_pos_y = curseur_y
            move(curseur_x, curseur_y)
            uart.write("🔥◣\n\b\b\b🔥███\n\b\b\b\b\b🔥◤")
            first_display = False

        shooting(curseur_x, curseur_y, push_button.value(), ennemy_pos)
