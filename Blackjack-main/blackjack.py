import pygame
import math
import random
import copy

pygame.init()

cards = ['2', '3', '4', '5', '6', '7','8', '9', '10', 'J', 'Q', 'K', 'A']
one_deck = cards * 4
decks = 4
WIDTH, HEIGHT = 600, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BLACKJACK")
fps = 60
timer = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 44)
smaller_font = pygame.font.Font('freesansbold.ttf', 36)
diffrent_font = pygame.font.Font('freesansbold.ttf', 20)
active = False
records = [0, 0, 0]
player_score = 0
dealer_score = 0
initial_deal = False
my_hand = []
dealer_hand = []
outcome = 0
reveal_dealer = False
hand_active = False
add_score = False

results = ['', 'PLAYER BUSTED o_O', 'Player WINS! :)', 'DEALER WINS :(', 'TIE GAME...']

def deal_cards(current_hand, current_deck):
    card  = random.randint(0, len(current_deck))
    current_hand.append(current_deck[card-1])
    current_deck.pop(card-1)
    print(f'current_hand{current_hand}\n, currentdeck{current_deck}\n')
    return current_hand, current_deck


#  draw cards visually onto screen
def draw_cards(player, dealer, reveal):
    for i in range(len(player)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 360 + (5 * i), 120, 180], 0, 5)
        screen.blit(diffrent_font.render(player[i], True, 'black'), (75 + 70 * i, 365 + 5 * i))
        # screen.blit(font.render(player[i], True, 'black'), (75 + 70 * i, 535 + 5 * i))
        pygame.draw.rect(screen, 'red', [70 + (70 * i), 360 + (5 * i), 120, 180], 4, 5)

    # if player hasn't finished turn, dealer will hide one card
    for i in range(len(dealer)):
        pygame.draw.rect(screen, 'white', [70 + (70 * i), 10 + (5 * i), 120, 180], 0, 5)
        if i != 0 or reveal:
            screen.blit(diffrent_font.render(dealer[i], True, 'black'), (75 + 70 * i, 15 + 5 * i))
            screen.blit(diffrent_font.render(dealer[i], True, 'black'), (75 + 70 * i, 165 + 5 * i))
        else:
            screen.blit(diffrent_font.render('???', True, 'black'), (75 + 70 * i, 15 + 5 * i))
            screen.blit(diffrent_font.render('???', True, 'black'), (75 + 70 * i, 165 + 5 * i))
        pygame.draw.rect(screen, 'blue', [70 + (70 * i), 10 + (5 * i), 120, 180], 5, 5)

def draw_game(act, record, result):
    button_list = []

    if not act:
        deal = pygame.draw.rect(screen, 'white', [150, 20, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 20, 300, 100], 3, 5)
        deal_text = font.render("DEAL HAND", True, 'black')
        screen.blit(deal_text, (165, 50))
        button_list.append(deal)

    
    else:
        hit = pygame.draw.rect(screen, 'white', [0, 450, 250, 80], 0, 5)
        pygame.draw.rect(screen, 'green', [0, 450, 250, 80], 3, 5)
        hit_text = diffrent_font.render('HIT ME', True, 'black')
        screen.blit(hit_text, (55, 485))
        button_list.append(hit)
        stand = pygame.draw.rect(screen, 'white', [300, 450, 250, 80], 0, 5)
        pygame.draw.rect(screen, 'green', [300, 450, 250, 80], 3, 5)
        stand_text = diffrent_font.render('STAND', True, 'black')
        screen.blit(stand_text, (355, 485))
        button_list.append(stand)
        score_text = diffrent_font.render(f'Wins: {records[0]}   Losses: {records[1]}   Draws: {records[2]}', True, 'white')
        screen.blit(score_text, (15, 560))
        
    if result != 0:
        screen.blit(font.render(results[result], True, 'red'), (15, 25))
        deal = pygame.draw.rect(screen, 'white', [150, 220, 300, 100], 0, 5)
        pygame.draw.rect(screen, 'green', [150, 220, 300, 100], 3, 5)
        pygame.draw.rect(screen, 'black', [153, 223, 294, 94], 3, 5)
        deal_text = diffrent_font.render('NEW HAND', True, 'black')
        screen.blit(deal_text, (165, 250))
        button_list.append(deal)
    return button_list

def calculate_score(hand):
    hand_score = 0
    aces_count = hand.count('A')
    for i in range(len(hand)):
        for j in range(8):
            if hand[i] == cards[j]:
                hand_score += int(hand[i])

        if hand[i] in ['10','J','K','Q']:
            hand_score += 10

        elif hand[i] == "A":
            hand_score += 11 

    if hand_score > 21 and aces_count > 0:
        for i in range (aces_count):
            if hand_score > 21:
                hand_score -= 10
    
    return hand_score

def draw_scores(player , dealer):
    screen.blit(diffrent_font.render(f'Score[{player}]', True, 'white'), (500, 420))
    if reveal_dealer:
        screen.blit(diffrent_font.render(f'Score[{dealer}]', True, 'white'), (500, 50))

def check_endgame(hand_act, deal_score, play_score, result, totals, add):
    if not hand_act and deal_score >= 17:
        if player_score > 21:
            result = 1
        elif deal_score < play_score < 21 or deal_score > 21 or player_score == 21:
            result = 2
        elif play_score < deal_score <= 21:
            result = 3
        else:
            result = 4

        if add:
            if result == 1 or result == 3:
                totals[1] += 1
            elif result == 2:
                totals[0] += 1
            else:
                totals[2] += 1

            add = False

    
    return result, totals, add

run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    if initial_deal:
        for i in range(2):
            my_hand, game_deck = deal_cards(my_hand, game_deck)
            dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        initial_deal = False
        
    if active:
        draw_cards(my_hand, dealer_hand, reveal_dealer)
        player_score = calculate_score(my_hand)
        if reveal_dealer:
            dealer_score = calculate_score(dealer_hand)
            if dealer_score < 17:
                dealer_hand, game_deck = deal_cards(dealer_hand, game_deck)
        draw_scores(player_score, dealer_score)

    buttons = draw_game(active, records, outcome)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONUP:
            if not active:
                if buttons[0].collidepoint(event.pos):
                    active = True
                    initial_deal = True
                    game_deck = copy.deepcopy(decks * one_deck)
                    my_hand = []
                    dealer_hand = []
                    outcome = 0
                    hand_active = True
                    add_score = True
                    
            else:
                if buttons[0].collidepoint(event.pos) and player_score < 21 and hand_active:
                    my_hand, game_deck = deal_cards(my_hand, game_deck)

                elif buttons[1].collidepoint(event.pos) and not reveal_dealer:
                    reveal_dealer = True
                    hand_active = False
                elif len(buttons) == 3:
                    if buttons[2].collidepoint(event.pos):
                        active = True
                        initial_deal = True
                        game_deck = copy.deepcopy(decks * one_deck)
                        my_hand = []
                        dealer_hand = []
                        outcome = 0
                        hand_active = True
                        reveal_dealer = False
                        outcome = 0
                        add_score = True
                        dealer_score = 0
                        player_score = 0

    if hand_active and player_score >= 21:
        hand_active = False
        reveal_dealer = True

    outcome, records, add_score = check_endgame(hand_active, dealer_score, player_score, outcome, records, add_score)

    pygame.display.flip()
pygame.quit()