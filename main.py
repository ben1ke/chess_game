# Function to draw the chess board
def draw_board():
for i in range(32):
column = i % 4
row = i // 4
# Alternate colors for the squares
if row % 2 == 0:
pygame.draw.rect(screen, &#39;light gray&#39;, [600 - (column * 200), row * 100, 100, 100])
else:
pygame.draw.rect(screen, &#39;light gray&#39;, [700 - (column * 200), row * 100, 100, 100])
# Draw additional board elements
pygame.draw.rect(screen, &#39;gray&#39;, [0, 800, WIDTH, 100])
pygame.draw.rect(screen, &#39;gold&#39;, [0, 800, WIDTH, 100], 5)
pygame.draw.rect(screen, &#39;gold&#39;, [800, 0, 200, HEIGHT], 5)
 # Status text for player turns
status_text = [&#39;White: Select a Piece to Move!&#39;, &#39;White: Select a Destination!&#39;,
&#39;Black: Select a Piece to Move!&#39;, &#39;Black: Select a Destination!&#39;]
screen.blit(big_font.render(status_text[turn_step], True, &#39;black&#39;), (20, 820))
# Draw grid lines for the board
for i in range(9):
pygame.draw.line(screen, &#39;black&#39;, (0, 100 * i), (800, 100 * i), 2)
pygame.draw.line(screen, &#39;black&#39;, (100 * i, 0), (100 * i, 800), 2)
# Forfeit option on the board
screen.blit(medium_font.render(&#39;FORFEIT&#39;, True, &#39;black&#39;), (810, 830))


# draw pieces onto board
def draw_pieces():
# Process each piece in white_pieces array
for i in range(len(white_pieces)):
index = piece_list.index(white_pieces[i])
# Drawing white pieces on the board
if white_pieces[i] == &#39;pawn&#39;:
screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
else:
screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100
+ 10))
# Highlighting the selected piece
if turn_step &lt; 2:
if selection == i:
pygame.draw.rect(screen, &#39;red&#39;, [white_locations[i][0] * 100 + 1, white_locations[i][1] * 100
+ 1,
100, 100], 2)
# Similar logic for drawing black pieces
for i in range(len(black_pieces)):
index = piece_list.index(black_pieces[i])
if black_pieces[i] == &#39;pawn&#39;:
screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
else:

screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 +
10))
if turn_step &gt;= 2:
if selection == i:
pygame.draw.rect(screen, &#39;blue&#39;, [black_locations[i][0] * 100 + 1, black_locations[i][1] * 100
+ 1,
100, 100], 2)

# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
moves_list = []
all_moves_list = []
for i in range((len(pieces))):
location = locations[i]
piece = pieces[i]
if piece == &#39;pawn&#39;:
moves_list = check_pawn(location, turn)
elif piece == &#39;rook&#39;:
moves_list = check_rook(location, turn)
elif piece == &#39;knight&#39;:
moves_list = check_knight(location, turn)
elif piece == &#39;bishop&#39;:
moves_list = check_bishop(location, turn)
elif piece == &#39;queen&#39;:
moves_list = check_queen(location, turn)
elif piece == &#39;king&#39;:
moves_list = check_king(location, turn)
all_moves_list.append(moves_list)
return all_moves_list

# check king valid moves
def check_king(position, color):
moves_list = []
if color == &#39;white&#39;:
enemies_list = black_locations
friends_list = white_locations
else:
friends_list = black_locations
enemies_list = white_locations
# 8 squares to check for kings, they can go one square any direction
targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
for i in range(8):
target = (position[0] + targets[i][0], position[1] + targets[i][1])
if target not in friends_list and 0 &lt;= target[0] &lt;= 7 and 0 &lt;= target[1] &lt;= 7:
moves_list.append(target)
return moves_list

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
if color == &#39;white&#39;:

enemies_list = black_locations
friends_list = white_locations
else:
friends_list = black_locations
enemies_list = white_locations
for i in range(4): # up-right, up-left, down-right, down-left
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
0 &lt;= position[0] + (chain * x) &lt;= 7 and 0 &lt;= position[1] + (chain * y) &lt;= 7:
moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
path = False
chain += 1
else:
path = False
return moves_list


# draw captured pieces on side of screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))


# draw a flashing square around king if in check
def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                              white_locations[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                               black_locations[king_index][1] * 100 + 1, 100, 100], 5)


def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))


# main game loop
black_options = check_options(black_pieces, black_locations, 'black')
white_options = check_options(white_pieces, white_locations, 'white')
run = True
while run:
    timer.tick(fps)
    if counter < 30:
        counter += 1
    else:
        counter = 0
    screen.fill('dark gray')
    draw_board()
    draw_pieces()
    draw_captured()
    draw_check()
    if selection != 100:
        valid_moves = check_valid_moves()
        draw_valid(valid_moves)
    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
            x_coord = event.pos[0] // 100
            y_coord = event.pos[1] // 100
            click_coords = (x_coord, y_coord)
            if turn_step <= 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []
            if turn_step > 1:
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'white'
                if click_coords in black_locations:
                    selection = black_locations.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != 100:
                    black_locations[selection] = click_coords
                    if click_coords in white_locations:
                        white_piece = white_locations.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece])
                        if white_pieces[white_piece] == 'king':
                            winner = 'black'
                        white_pieces.pop(white_piece)
                        white_locations.pop(white_piece)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 0
                    selection = 100
                    valid_moves = []
        if event.type == pygame.KEYDOWN and game_over:
            if event.key == pygame.K_RETURN:
                game_over = False
                winner = ''
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                captured_pieces_white = []
                captured_pieces_black = []
                turn_step = 0
                selection = 100
                valid_moves = []
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')

    if winner != '':
        game_over = True
        draw_game_over()

    pygame.display.flip()
pygame.quit()
