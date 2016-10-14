import pygame
import sys
import time, random
from pygame.locals import *
import pygbutton
import platform
from lottery import *
from threading import Timer

FPS = 30
window_width = 1000
window_height = 650
white_color = (255, 255, 255)

# initialize several values
current_first_prob = 0
current_second_prob = 0
current_mode = "SequentialMode"

result_on_screen = ""
waiting_seconds_after_click_play = 2
earned_dollars_of_each_win = 5

# initial result is neither WIN or LOSE, or we set it to be "UNKNOWN"
result_in_first_stage = "UNKNOWN" 

# from the input file, how many lines with TOP CE can be chosen
num_lottaries_to_play = 3 

num_win = 0
num_play = 0

timer = []

screen = pygame.display.set_mode((window_width, window_height))
play_button = pygbutton.PygButton((250, 450, 200, 30), 'Play!')

def show_text_on_screen(font_size, string, position_x, position_y):
    font = pygame.font.Font(None, font_size)
    text_on_screen = font.render(string, 1, (255, 0, 0))
    screen.blit(text_on_screen, (position_x, position_y))

def show_background_image():
    location = pygame.Rect(0, 0, 50, 50)
    background_image = pygame.image.load('background.jpg')
    screen.blit(background_image, location)

def show_UI():
    show_two_probabilities_on_screen(current_first_prob, current_second_prob, current_mode, result_in_first_stage)

    global num_play, num_win
    show_text_on_screen(30, "win: " + str(num_win), 300, 500)
    show_text_on_screen(30, "played: " + str(num_play), 300, 520)

    total_earned = get_total_earned_money()
    show_text_on_screen(50, "Your Earned Money: $" + str(total_earned) + "!", 300, 540)

    global timer
    if timer != [] and timer.isAlive():
        play_button.visible = False
    else:
        play_button.visible = True

def show_two_probabilities_on_screen(first_prob, second_prob, mode, result_in_first_stage):
    # if in simutanious mode, show two numbers right away when game starts
    # if in sequential mode, show the first number first, if wins, show the second. 
    # the parameter "result_in_first_stage" is only valid for sequential mode

    first_prob_string = str(first_prob * 100) + "%"
    second_prob_string = str(second_prob * 100) + "%"

    if mode == "SimutaniousMode":
        show_text_on_screen(160, first_prob_string, 50, 200)
        show_text_on_screen(160, second_prob_string, 450, 200)
    elif mode == "SequentialMode":
        show_text_on_screen(160, first_prob_string, 50, 200)
        if result_in_first_stage != "UNKNOWN":
            show_text_on_screen(160, second_prob_string, 450, 200)

def update_message_on_screen_based_on_lottary_result(lottary_result, mode):
    global result_on_screen
    global result_in_first_stage
    global num_win
     
    if mode == "SimutaniousMode":
        if lottary_result == "WIN":
            result_on_screen = "[Simutanious Mode] You WIN!"
            num_win += 1
        else:
            result_on_screen = "[Simutanious Mode] Ah, you LOSE!"

    elif mode == "SequentialMode":
        if lottary_result == ["LOSE", "LOSE"]:
            result_on_screen = "[Sequential Mode] Sorry, you lose in the first stage!"
            result_in_first_stage = "LOSE"

        elif lottary_result == ["WIN", "LOSE"]:
            result_on_screen = "[Sequential Mode] Sorry, you win in the first stage, but lose in the second stage!"
            result_in_first_stage = "WIN"

        elif lottary_result == ["WIN", "WIN"]:
            result_on_screen = "[Sequential Mode] Congratulations! You WIN!"
            result_in_first_stage = "WIN"
            num_win += 1

def play_lottary_simutanious_mode(first_prob, second_prob, num_items):
    global num_play
    global result_on_screen
    result_on_screen = "[Simutanious Mode] Calculating ..."
    lottary_result = play_game_using_two_bags_simutaniously(first_prob, second_prob, num_items)
    num_play += 1
    
    # Give computer several seconds to calculate the lottary result.  
    global timer
    timer = Timer(waiting_seconds_after_click_play, update_message_on_screen_based_on_lottary_result, [lottary_result, "SimutaniousMode"])
    timer.start()

def play_lottary_sequential_mode(first_prob, second_prob, num_items):
    global num_play
    global result_on_screen
    result_on_screen = "[Sequential Mode] Calculating ..."
    lottary_result = play_game_using_two_bags_sequentially(first_prob, second_prob, num_items)
    num_play += 1

    # Give computer several seconds to calculate the lottary result.  
    global timer
    timer = Timer(waiting_seconds_after_click_play, update_message_on_screen_based_on_lottary_result, [lottary_result, "SequentialMode"])
    timer.start()

def play_lottary_by_mode(first_prob, second_prob, mode):
    if mode == "SimpleMode" or mode == "SimutaniousMode":
        play_lottary_simutanious_mode(first_prob, second_prob, 1000)
    elif mode == "SequentialMode":
        global result_in_first_stage
        result_in_first_stage = "UNKNOWN"
        play_lottary_sequential_mode(first_prob, second_prob, 1000)

def play_Nth_lottary(selected_lottaries, index):
    # from all lottaries that are loaded from file, play the one that has index number 'index'
    if index >= len(selected_lottaries) or index < 0:
        print "Your index number is wrong! Cannot process the selected lottary"
        sys.exit()

    lottary = selected_lottaries[index]
    first_prob = float(lottary[0])
    second_prob = float(lottary[1])
    CE = float(lottary[2])
    mode_number = lottary[3]

    mode = ""

    if mode_number == "1":
        mode = "SimpleMode"
    elif mode_number == "2":
        mode = "SimutaniousMode"
    elif mode_number == "3":
        mode = "SequentialMode"

    global current_mode, current_first_prob, current_second_prob
    current_mode = mode
    current_first_prob = first_prob
    current_second_prob = second_prob

    play_lottary_by_mode(first_prob, second_prob, mode)

def load_probabilities_from_file(how_many_lines_to_choose):
    with open("inputs.txt", "r") as f:
        lines = f.readlines()

    # 
    valid_lines = [line.strip().split() for line in lines if len(line.strip()) != 0]
    
    if how_many_lines_to_choose > len(valid_lines):
        print "Your want to choose %s CE from file, but in the file there are only %s lines!" \
                % (how_many_lines_to_choose, len(valid_lines))
        how_many_lines_to_choose = len(valid_lines)

    # now sort those lines based on the CE column
    sorted_lines_by_CE = sorted(valid_lines, key = lambda line: line[2], reverse=True)
    return sorted_lines_by_CE[0 : how_many_lines_to_choose]

def get_total_earned_money():
    global num_win
    total_earned = num_win * earned_dollars_of_each_win
    return total_earned

def main_program():
    pygame.init()
    fps_clock = pygame.time.Clock()
    pygame.display.set_caption('Decision Making App')

    selected_lottaries = load_probabilities_from_file(num_lottaries_to_play)
    print selected_lottaries
    num_processed_lottaries = 0
    current_lottary_index = 0

    while num_processed_lottaries <= num_lottaries_to_play: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            button_events = play_button.handleEvent(event)
            if 'click' in button_events:
                num_processed_lottaries += 1
                play_Nth_lottary(selected_lottaries, current_lottary_index)
                current_lottary_index += 1
                
        screen.fill(white_color)
        show_background_image()
        show_UI()
        play_button.draw(screen)

        show_text_on_screen(40, result_on_screen, 30, 70)
        pygame.display.update()
        fps_clock.tick(FPS)

if __name__ == '__main__':
    main_program()

