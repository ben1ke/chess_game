# two player chess in python with Pygame!
# pawn double space checking
# castling
# en passant
# pawn promotion

import pygame
from constants import *

pygame.init()


# draw main game board
def draw_board():
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, 'light gray', [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, 'light gray', [700 - (column * 200), row * 100, 100, 100])
        pygame.draw.rect(screen, 'gray', [0, 800, WIDTH, 100])
        pygame.draw.rect(screen, 'gold', [0, 800, WIDTH, 100], 5)
        pygame.draw.rect(screen, 'gold', [800, 0, 200, HEIGHT], 5)
        status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                       'Black: Select a Piece to Move!', 'Black: Select a Destination!']
        screen.blit(big_font.render(status_text[turn_step], True, 'black'), (20, 820))
        for i in range(9):
            pygame.draw.line(screen, 'black', (0, 100 * i), (800, 100 * i), 2)
            pygame.draw.line(screen, 'black', (100 * i, 0), (100 * i, 800), 2)
        screen.blit(medium_font.render('FORFEIT', True, 'black'), (810, 830))
        if white_promote or black_promote:
            pygame.draw.rect(screen, 'gray', [0, 800, WIDTH - 200, 100])
            pygame.draw.rect(screen, 'gold', [0, 800, WIDTH - 200, 100], 5)
            screen.blit(big_font.render('Select Piece to Promote Pawn', True, 'black'), (20, 820))


# draw pieces onto board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
        if turn_step < 2:
            if selection == i:
                pygame.draw.rect(screen, 'red', [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100 + 1,
                                                 100, 100], 2)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
        if turn_step >= 2:
            if selection == i:
                pygame.draw.rect(screen, 'blue', [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100 + 1,
                                                  100, 100], 2)


# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    global castling_moves
    moves_list = []
    all_moves_list = []
    castling_moves = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list, castling_moves = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list


# check king valid moves
def check_king(position, color):
    moves_list = []
    castle_moves = check_castling()
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list, castle_moves


# check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# check bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list

def draw_promotion():
pygame.draw.rect(screen, &#39;dark gray&#39;, [800, 0, 200, 420])
if white_promote:
color = &#39;white&#39;
for i in range(len(white_promotions)):
piece = white_promotions[i]
index = piece_list.index(piece)
screen.blit(white_images[index], (860, 5 + 100 * i))
elif black_promote:
color = &#39;black&#39;
for i in range(len(black_promotions)):
piece = black_promotions[i]
index = piece_list.index(piece)
screen.blit(black_images[index], (860, 5 + 100 * i))
pygame.draw.rect(screen, color, [800, 0, 200, 420], 8)

def check_promo_select():
mouse_pos = pygame.mouse.get_pos()
left_click = pygame.mouse.get_pressed()[0]
x_pos = mouse_pos[0] // 100

y_pos = mouse_pos[1] // 100
if white_promote and left_click and x_pos &gt; 7 and y_pos &lt; 4:
white_pieces[promo_index] = white_promotions[y_pos]
elif black_promote and left_click and x_pos &gt; 7 and y_pos &lt; 4:
black_pieces[promo_index] = black_promotions[y_pos]

# main game loop
black_options = check_options(black_pieces, black_locations, &#39;black&#39;)
white_options = check_options(white_pieces, white_locations, &#39;white&#39;)
run = True
while run:
timer.tick(fps)
if counter &lt; 30:
counter += 1
else:
counter = 0
screen.fill(&#39;dark gray&#39;)
draw_board()
draw_pieces()
draw_captured()
draw_check()
if not game_over:
white_promote, black_promote, promo_index = check_promotion()
if white_promote or black_promote:
draw_promotion()
check_promo_select()
if selection != 100:
valid_moves = check_valid_moves()
draw_valid(valid_moves)
if selected_piece == &#39;king&#39;:

draw_castling(castling_moves)
# event handling
for event in pygame.event.get():
if event.type == pygame.QUIT:
run = False
if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
x_coord = event.pos[0] // 100
y_coord = event.pos[1] // 100
click_coords = (x_coord, y_coord)
if turn_step &lt;= 1:
if click_coords == (8, 8) or click_coords == (9, 8):
winner = &#39;black&#39;
if click_coords in white_locations:
selection = white_locations.index(click_coords)
# check what piece is selected, so you can only draw castling moves if king is selected
selected_piece = white_pieces[selection]
if turn_step == 0:
turn_step = 1
if click_coords in valid_moves and selection != 100:
white_ep = check_ep(white_locations[selection], click_coords)
white_locations[selection] = click_coords
white_moved[selection] = True
if click_coords in black_locations:
black_piece = black_locations.index(click_coords)
captured_pieces_white.append(black_pieces[black_piece])
if black_pieces[black_piece] == &#39;king&#39;:
winner = &#39;white&#39;
black_pieces.pop(black_piece)
black_locations.pop(black_piece)
black_moved.pop(black_piece)
# adding check if en passant pawn was captured

if click_coords == black_ep:
black_piece = black_locations.index((black_ep[0], black_ep[1] - 1))
captured_pieces_white.append(black_pieces[black_piece])
black_pieces.pop(black_piece)
black_locations.pop(black_piece)
black_moved.pop(black_piece)
black_options = check_options(black_pieces, black_locations, &#39;black&#39;)
white_options = check_options(white_pieces, white_locations, &#39;white&#39;)
turn_step = 2
selection = 100
valid_moves = []
# add option to castle
elif selection != 100 and selected_piece == &#39;king&#39;:
for q in range(len(castling_moves)):
if click_coords == castling_moves[q][0]:
white_locations[selection] = click_coords
white_moved[selection] = True
if click_coords == (1, 0):
rook_coords = (0, 0)
else:
rook_coords = (7, 0)
rook_index = white_locations.index(rook_coords)
white_locations[rook_index] = castling_moves[q][1]
black_options = check_options(black_pieces, black_locations, &#39;black&#39;)
white_options = check_options(white_pieces, white_locations, &#39;white&#39;)
turn_step = 2
selection = 100
valid_moves = []
if turn_step &gt; 1:
if click_coords == (8, 8) or click_coords == (9, 8):
winner = &#39;white&#39;

if click_coords in black_locations:
selection = black_locations.index(click_coords)
# check what piece is selected, so you can only draw castling moves if king is selected
selected_piece = black_pieces[selection]
if turn_step == 2:
turn_step = 3
if click_coords in valid_moves and selection != 100:
black_ep = check_ep(black_locations[selection], click_coords)
black_locations[selection] = click_coords
black_moved[selection] = True
if click_coords in white_locations:
white_piece = white_locations.index(click_coords)
captured_pieces_black.append(white_pieces[white_piece])
if white_pieces[white_piece] == &#39;king&#39;:
winner = &#39;black&#39;
white_pieces.pop(white_piece)
white_locations.pop(white_piece)
white_moved.pop(white_piece)
if click_coords == white_ep:
white_piece = white_locations.index((white_ep[0], white_ep[1] + 1))
captured_pieces_black.append(white_pieces[white_piece])
white_pieces.pop(white_piece)
white_locations.pop(white_piece)
white_moved.pop(white_piece)
black_options = check_options(black_pieces, black_locations, &#39;black&#39;)
white_options = check_options(white_pieces, white_locations, &#39;white&#39;)
turn_step = 0
selection = 100
valid_moves = []
# add option to castle
elif selection != 100 and selected_piece == &#39;king&#39;:

for q in range(len(castling_moves)):
if click_coords == castling_moves[q][0]:
black_locations[selection] = click_coords
black_moved[selection] = True
if click_coords == (1, 7):
rook_coords = (0, 7)
else:
rook_coords = (7, 7)
rook_index = black_locations.index(rook_coords)
black_locations[rook_index] = castling_moves[q][1]
black_options = check_options(black_pieces, black_locations, &#39;black&#39;)
white_options = check_options(white_pieces, white_locations, &#39;white&#39;)
turn_step = 0
selection = 100
valid_moves = []
if event.type == pygame.KEYDOWN and game_over:
if event.key == pygame.K_RETURN:
game_over = False
winner = &#39;&#39;
white_pieces = [&#39;rook&#39;, &#39;knight&#39;, &#39;bishop&#39;, &#39;king&#39;, &#39;queen&#39;, &#39;bishop&#39;, &#39;knight&#39;, &#39;rook&#39;,
&#39;pawn&#39;, &#39;pawn&#39;, &#39;pawn&#39;, &#39;pawn&#39;, &#39;pawn&#39;, &#39;pawn&#39;, &#39;pawn&#39;, &#39;pawn&#39;]
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
(0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
white_moved = [False, False, False, False, False, False, False, False,
False, False, False, False, False, False, False, False]
black_pieces = [&#39;rook&#39;, &#39;knight&#39;, &#39;bishop&#39;, &#39;king&#39;, &#39;queen&#39;, &#39;bishop&#39;, &#39;knight&#39;, &#39;rook&#39;,
&#39;pawn&#39;, &#39;pawn&#39;, &#39;pawn&#39;, &#39;pawn&#39;, &#39;pawn&#39;, &#39;pawn&#39;, &#39;pawn&#39;, &#39;pawn&#39;]
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
(0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
black_moved = [False, False, False, False, False, False, False, False,
False, False, False, False, False, False, False, False]

captured_pieces_white = []
captured_pieces_black = []
turn_step = 0
selection = 100
valid_moves = []
black_options = check_options(black_pieces, black_locations, &#39;black&#39;)
white_options = check_options(white_pieces, white_locations, &#39;white&#39;)

if winner != &#39;&#39;:
game_over = True
draw_game_over()

pygame.display.flip()
pygame.quit()