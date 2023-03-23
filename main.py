from pyb import SPI, Pin, LED, delay, UART, Timer
import random

CS = Pin("PE3", Pin.OUT_PP)
SPI_1 = SPI(
    1,  # PA5, PA6, PA7
    SPI.MASTER,
    baudrate=50000,
    polarity=0,
    phase=0,  
)

def led1(timer):
    LED(1).toggle()

def led2(timer):
    LED(2).toggle()

def led3(timer):
    LED(3).toggle()

def led4(timer):
    LED(4).toggle()

time_time = Timer(4, freq=2)

ennemy_pos = []

uart = UART(2, 115200)

push_button = Pin("PA0", Pin.IN,Pin.PULL_DOWN)

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
  
def write_reg(addr, value):
    CS.low()
    SPI_1.send(addr & 0x7F)  
    SPI_1.send(value)
    CS.high()
    
def convert_value(high, low):
    value = (high << 8) | low
    if value & (1 << 15):
        value = value - (1 << 16)
    return value * 0.06
    
def read_acceleration(base_addr):
    low = read_reg(base_addr)
    high = read_reg(base_addr + 1)
    return convert_value(high, low)

def blink_led():
    time_time.callback(led1)
    time_time.callback(led2)
    time_time.callback(led3)
    time_time.callback(led4)

    

#/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

logo_spacex = """\
   ▄████████    ▄███████▄    ▄████████  ▄████████    ▄████████      ▀████    ▐████▀ 
  ███    ███   ███    ███   ███    ███ ███    ███   ███    ███        ███▌   ████▀  
  ███    █▀    ███    ███   ███    ███ ███    █▀    ███    █▀          ███  ▐███    
  ███          ███    ███   ███    ███ ███         ▄███▄▄▄             ▀███▄███▀    
▀███████████ ▀█████████▀  ▀███████████ ███        ▀▀███▀▀▀             ████▀██▄     
         ███   ███          ███    ███ ███    █▄    ███    █▄         ▐███  ▀███    
   ▄█    ███   ███          ███    ███ ███    ███   ███    ███       ▄███     ███▄  
 ▄████████▀   ▄████▀        ███    █▀  ████████▀    ██████████      ████       ███▄ 
                                                                                    
    """

logo_arrow = """\
           ▄    
          ▐░▌   
           ▐░▌  
            ▐░▌ 
 ▄▄▄▄▄▄▄▄▄▄▄ ▐░▌
▐░░░░░░░░░░░▌▐░▌
 ▀▀▀▀▀▀▀▀▀▀▀ ▐░▌
            ▐░▌ 
           ▐░▌  
          ▐░▌   
           ▀    
    """

logo_win = """\
▄██   ▄    ▄██████▄  ███    █▄        ▄█     █▄   ▄█  ███▄▄▄▄   
███   ██▄ ███    ███ ███    ███      ███     ███ ███  ███▀▀▀██▄ 
███▄▄▄███ ███    ███ ███    ███      ███     ███ ███▌ ███   ███ 
▀▀▀▀▀▀███ ███    ███ ███    ███      ███     ███ ███▌ ███   ███ 
▄██   ███ ███    ███ ███    ███      ███     ███ ███▌ ███   ███ 
███   ███ ███    ███ ███    ███      ███     ███ ███  ███   ███ 
███   ███ ███    ███ ███    ███      ███ ▄█▄ ███ ███  ███   ███ 
 ▀█████▀   ▀██████▀  ████████▀        ▀███▀███▀  █▀    ▀█   █▀  
                                                                
    """
logo_play = """\
  _____  _             
 |  __ \| |            
 | |__) | | __ _ _   _ 
 |  ___/| |/ _` | | | |
 | |    | | (_| | |_| |
 |_|    |_|\__,_|\__, |
                  __/ |
                 |___/ 
    """

logo_score = """\
   _____                    
  / ____|                   
 | (___   ___ ___  _ __ ___ 
  \___ \ / __/ _ \| '__/ _ \ 
  ____) | (_| (_) | | |  __/
 |_____/ \___\___/|_|  \___|
                            
                            
    """
logo_score_big = """\
   ▄████████  ▄████████  ▄██████▄     ▄████████    ▄████████ 
  ███    ███ ███    ███ ███    ███   ███    ███   ███    ███ 
  ███    █▀  ███    █▀  ███    ███   ███    ███   ███    █▀  
  ███        ███        ███    ███  ▄███▄▄▄▄██▀  ▄███▄▄▄     
▀███████████ ███        ███    ███ ▀▀███▀▀▀▀▀   ▀▀███▀▀▀     
         ███ ███    █▄  ███    ███ ▀███████████   ███    █▄  
   ▄█    ███ ███    ███ ███    ███   ███    ███   ███    ███ 
 ▄████████▀  ████████▀   ▀██████▀    ███    ███   ██████████ 
                                     ███    ███              
    """

logo_back = """\
  ____             _    
 |  _ \           | |   
 | |_) | __ _  ___| | __
 |  _ < / _` |/ __| |/ /
 | |_) | (_| | (__|   < 
 |____/ \__,_|\___|_|\_\ 
                        
                            
    """
logo_points ="""\
           _                 ___  _____ _____         _       
     /\   | |            _  |__ \| ____| ____|       | |      
    /  \  | | _____  __ (_)    ) | |__ | |__    _ __ | |_ ___ 
   / /\ \ | |/ _ \ \/ /       / /|___ \|___ \  | '_ \| __/ __|
  / ____ \| |  __/>  <   _   / /_ ___) |___) | | |_) | |_\__ \ 
 /_/    \_\_|\___/_/\_\ (_) |____|____/|____/  | .__/ \__|___/
                                               | |            
                                               |_|            
    """
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
        for rocket_pos in range(7, 150):
            rocket = [curseur_x + rocket_pos, curseur_y + 1]
            move(rocket[0], rocket[1])
            uart.write("🔴")
            delay(2)
            move(rocket[0]-1, rocket[1])
            uart.write(" ")
            rocket_hit_test(ennemy_pos, rocket)

def rocket_hit_test (ennemy_pos, rocket):

    for ennemy_x , ennemy_y in ennemy_pos:
        for y_offset in range(3):
            if rocket == [ennemy_x, ennemy_y + y_offset] :     
                move(ennemy_x, ennemy_y)
                uart.write(" \n\b \n\b ")
                blink_led()
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
        print(y_accel)

        if y_accel > 300:
            draw_logo(logo_arrow,x=80, y=42)
            clear_logo(logo_arrow, x=80, y=30)  
            if btn.value() == 1:
                score(btn)
                draw_logo(logo_play,96,30)
                draw_logo(logo_score,96,42)
                draw_logo(logo_spacex, x=25, y=15)
                draw_logo(logo_arrow,x=80, y=30)
                   
        
        if y_accel < -300:
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
        move(life_lenght - number_hit * one_life_width, 2)
        uart.write(15*red_char)
        print(number_hit)
    
    if number_hit == 5 :
        clear_screen()
        draw_logo(logo_win,x=50,y=25)          

#/////////////////////////////////////////////////////////////////////////////////////////////////////////::                   

clear_screen()

number_hit = 0
curseur_x = 20
curseur_y = 10
previous_pos_x = curseur_x
previous_pos_y = curseur_y
boundaries_x = [4,150]
boundaries_y = [4,50]
start = True

# menu(push_button)

boundaries(boundaries_x, boundaries_y)
spawn_ennemy()
life_bar(150)

while True:

    x_accel = read_acceleration(0x28)
    y_accel = read_acceleration(0x2A)
    z_accel = read_acceleration(0x2C)
    
    delay(50)
        
    if x_accel < +300:
        curseur_x += 1
        if curseur_x > boundaries_x[1]:
            curseur_x -= 1
    
    if x_accel > -300:
        curseur_x -= 1
        if curseur_x < boundaries_x[0]:
            curseur_x += 1
        
    if y_accel > 300:
        curseur_y += 1
        if curseur_y > boundaries_y[1]:
            curseur_y -= 1
        
    if y_accel < -300:
        curseur_y -= 1
        if curseur_y < boundaries_y[0]:
            curseur_y += 1
    
    print(y_accel)
    print(x_accel)

    if curseur_x != previous_pos_x or curseur_y != previous_pos_y :
        move(previous_pos_x, previous_pos_y)
        uart.write("    \n\b\b\b    \n\b\b\b\b\b    ")
        previous_pos_x = curseur_x
        previous_pos_y = curseur_y
        move(curseur_x, curseur_y)
        uart.write("🔥◣\n\b\b\b🔥███\n\b\b\b\b\b🔥◤")

    shooting(curseur_x, curseur_y, push_button.value(), ennemy_pos)
