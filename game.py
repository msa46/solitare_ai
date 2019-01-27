import pygame
from deck import Deck
from ui import Text, Button, RadioGroup, Radio, Checkbox
import settings_manager, history_manager


white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 200, 0)
blue = (50, 50, 190)
red = (190, 50, 50)
grey = (100, 100, 100)
bland = (150,150,150)
display_dimensions = (1100, 800)

pygame.init()

game_display = pygame.display.set_mode(display_dimensions)

pygame.display.set_caption('Solitare')

clock = pygame.time.Clock()
FPS = 10


def quit_game():
    pygame.quit()
    quit()

def win_screen():
    quit_button = Button(display_dimensions, "Quit", (250, 0), (200, 100), red, text_color=white, text_size=25, action="quit")
    play_again_button = Button(display_dimensions, "Play Again", (0, 0), (200, 100), blue, text_color=white, text_size=25, action="play_again")
    start_menu_button = Button(display_dimensions, "Start Menu", (-250, 0), (200, 100), green, text_color=white, text_size=25, action="start_menu")
    buttons = [quit_button, play_again_button, start_menu_button]

    win_text = Text(display_dimensions, (0, -200), "You Win!!!", 60, black)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if event.button == 1:
                        for button in buttons:
                            if button.check_if_clicked(mouse_pos):
                                if button.action == "quit":
                                    quit_game()
                                elif button.action == "play_again":
                                    game_loop()
                                elif button.action == "start_menu":
                                    start_menu()
                                else:
                                    print("Button action: {} does not exist".format(button.action))

        game_display.fill(white)

        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())

        win_text.display(game_display)

        pygame.display.update()
        clock.tick(FPS)
def valid_moves(deck):
    valid_move_set = []
    piles = deck.piles
    #print(deck.selected_cards)
    # print(len(piles))
    for source_pile in piles:
        source_card = 0
        for card in source_pile.cards:
            if card.face_up:
                source_card = card
        if source_card == 0:
            continue
        if source_pile.pile_type == 'foundation':
            continue
        for dest_pile in piles:
            dest_card = 0
            for card in dest_pile.cards:
                if card.face_up:
                    dest_card = card
            if dest_card == 0 :
                if(source_card.rank == 'ace' and dest_pile.pile_type == 'foundation' ):
                    # print(source_card.x , source_card.y)
                    selection, selected_cards, deselect_pile = source_pile.selected((source_card.x, source_card.y), deck.piles)
                    print("IM HERE",selected_cards)
                    if not source_pile.valid_transfer(dest_pile, selected_cards, deck.ranks):
                        print("FUCK YOU")
                    else:
                        # source_pile.transfer_cards(selected_cards,dest_pile,deck.ranks)
                        deck.handle_click((source_card.x , source_card.y))
                        print("FUCK OFF")
                        deck.handle_click((dest_pile.x, dest_pile.y))
                continue

            if(source_card.x != dest_card.x):
                # print("source card x & y is",source_card.x,source_card.y)
                selection, selected_cards, deselect_pile = source_pile.selected((source_card.x, source_card.y), deck.piles)
                # if(dest_pile == "foundation"):
                #     if(source_pile.valid_transfer(dest_pile,selected_cards,deck.ranks)):
                #         print("IT CHECKS OUT")
                if(source_pile.valid_transfer(dest_pile,selected_cards,deck.ranks)):
                    valid_move_set.append((source_pile,dest_pile, selected_cards))
                # if(source.card == "ace" and )
    return valid_move_set
def ai(deck):
    valid_move_set = valid_moves(deck)
    if(len(valid_move_set) == 0 ):
        # deck.piles[7].transfer_cards(,deck.piles[8],deck.ranks)
        deck.handle_click((132,121))
    for possibility in valid_move_set:
        possibility[0].transfer_cards(possibility[2],possibility[1],deck.ranks)
        print("s is", possibility[0].x)
        print("d is", possibility[1].x)
        print("Selected cards are",possibility[2])

    return True
def game_loop():
    #undo_button = Button(display_dimensions, "Undo", (10, 10), (30, 30), grey, centered=False, text_size=11, action="undo")
    ai_button = Button(display_dimensions, "AI", (10, 10), (30, 30), grey, centered=False, text_size=11, action="ai")
    pause_button = Button(display_dimensions, "Pause", (display_dimensions[0]-50, 10), (40, 30), grey, centered=False, text_size=10, action="pause")
    # buttons = [undo_button, pause_button]
    buttons = [ai_button, pause_button]

    enable_ai = False

    deck = Deck()
    deck.load_cards()
    deck.shuffle_cards()
    deck.load_piles(display_dimensions)

    hm = history_manager.HistoryManager(deck)

    while True:
        if deck.check_for_win():
            win_screen()
        if enable_ai:
            ai(deck)
            piles_to_update, valid_move = deck.handle_click((100,0))
            deck.update(piles_to_update, display_dimensions[1])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()
                elif event.key == pygame.K_w:
                    win_screen()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    # if not enable_ai:
                    piles_to_update, valid_move = deck.handle_click(mouse_pos)
                    deck.update(piles_to_update, display_dimensions[1])
                    if valid_move:
                        hm.valid_move_made(deck)

                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            # if button.action == "undo":
                            #     deck = hm.undo(deck)
                            if button.action == "ai":
                                enable_ai = not enable_ai
                                print("enable_ai:",enable_ai)
                if event.button == 3:
                    deck.handle_right_click(mouse_pos)

        game_display.fill(blue)

        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())

        deck.display(game_display)
        pygame.display.update()
        clock.tick(FPS)


def options_menu():
    settings = settings_manager.load_settings()

    title_text = Text(display_dimensions, (0, -370), "Options", 40, black)
    about_text = Text(display_dimensions, (0, 350), "Made in 2017 by Aaron Buckles", 14, black)

    back_button = Button(display_dimensions, "Back", (10, 25), (75, 25), red, centered=False, text_color=white, text_size=14, action="back")
    buttons = [back_button]

    draw_three_checkbox = Checkbox(display_dimensions, (10, 100), centered=False, checked=settings['draw_three'])
    draw_three_label = Text(display_dimensions, (40, 100), "Draw three cards from deck", 14, black, centered=False)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.action == "back":
                                settings_manager.save_settings({'draw_three': draw_three_checkbox.checked})
                                start_menu()
                            else:
                                print("Button action: {} does not exist".format(button.action))

                    draw_three_checkbox.check_if_clicked(mouse_pos)

        game_display.fill(white)

        title_text.display(game_display)
        about_text.display(game_display)

        draw_three_label.display(game_display)
        draw_three_checkbox.display(game_display)

        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())

        pygame.display.update()
        clock.tick(FPS)


def start_menu():
    title = Text(display_dimensions, (0, -100), "Solitaire", 50, black)

    play_button = Button(display_dimensions, "Play", (0, 0), (100, 50), blue, text_color=white, text_size=26, action="start_game")
    quit_button = Button(display_dimensions, "Quit", (200, 0), (100, 50), red, text_color=white, action="quit")
    options_button = Button(display_dimensions, "Options", (-200, 0), (100, 50), grey, text_color=white, action="options")
    buttons = [play_button, quit_button, options_button]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1:
                    for button in buttons:
                        if button.check_if_clicked(mouse_pos):
                            if button.action == "start_game":
                                game_loop()
                            elif button.action == "quit":
                                quit_game()
                            elif button.action == "options":
                                options_menu()
                                pass
                            else:
                                print("Button action: {} does not exist".format(button.action))

        game_display.fill(white)

        title.display(game_display)

        for button in buttons:
            button.display(game_display, pygame.mouse.get_pos())

        pygame.display.update()
        clock.tick(FPS)


start_menu()
