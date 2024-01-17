import pygame
pygame.init()


def check_pawn(position, color):
    moves_list = []

    # Check moves for a white pawn
    if color == 'white':
        # Check if the square directly ahead is open
        if (position[0], position[1] + 1) not in white_locations and \
           (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        
        # Check if the pawn is in its initial position and can move two squares ahead
        if (position[0], position[1] + 2) not in white_locations and \
           (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        
        # Check if the pawn can capture an opponent's piece diagonally
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))

        # Check for 'en passant' move
        if (position[0] + 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] - 1, position[1] + 1))

    # Check moves for a black pawn
    else:
if (position[0], position[1] - 1) not in white_locations and \
(position[0], position[1] - 1) not in black_locations and position[1] &gt; 0:
moves_list.append((position[0], position[1] - 1))
# indent the check for two spaces ahead, so it is only checked if one space ahead is also open
if (position[0], position[1] - 2) not in white_locations and \
(position[0], position[1] - 2) not in black_locations and position[1] == 6:
moves_list.append((position[0], position[1] - 2))
if (position[0] + 1, position[1] - 1) in white_locations:
moves_list.append((position[0] + 1, position[1] - 1))
if (position[0] - 1, position[1] - 1) in white_locations:
moves_list.append((position[0] - 1, position[1] - 1))
# add en passant move checker
if (position[0] + 1, position[1] - 1) == white_ep:

moves_list.append((position[0] + 1, position[1] - 1))
if (position[0] - 1, position[1] - 1) == white_ep:
moves_list.append((position[0] - 1, position[1] - 1))
return moves_list

# check valid knight moves
def check_knight(position, color):
moves_list = []
if color == &#39;white&#39;:
enemies_list = black_locations
friends_list = white_locations
else:
friends_list = black_locations
enemies_list = white_locations
# 8 squares to check for knights, they can go two squares in one direction and one in another
targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
for i in range(8):
target = (position[0] + targets[i][0], position[1] + targets[i][1])
if target not in friends_list and 0 &lt;= target[0] &lt;= 7 and 0 &lt;= target[1] &lt;= 7:
moves_list.append(target)
return moves_list

# check for valid moves for just selected piece
def check_valid_moves():
if turn_step &lt; 2:
options_list = white_options
else:
options_list = black_options
valid_options = options_list[selection]

return valid_options

# draw valid moves on screen
def draw_valid(moves):
if turn_step &lt; 2:
color = &#39;red&#39;
else:
color = &#39;blue&#39;
for i in range(len(moves)):
pygame.draw.circle(screen, color, (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)

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
global check
check = False
if turn_step &lt; 2:
if &#39;king&#39; in white_pieces:

king_index = white_pieces.index(&#39;king&#39;)
king_location = white_locations[king_index]
for i in range(len(black_options)):
if king_location in black_options[i]:
check = True
if counter &lt; 15:
pygame.draw.rect(screen, &#39;dark red&#39;, [white_locations[king_index][0] * 100 + 1,
white_locations[king_index][1] * 100 + 1, 100, 100], 5)
else:
if &#39;king&#39; in black_pieces:
king_index = black_pieces.index(&#39;king&#39;)
king_location = black_locations[king_index]
for i in range(len(white_options)):
if king_location in white_options[i]:
check = True
if counter &lt; 15:
pygame.draw.rect(screen, &#39;dark blue&#39;, [black_locations[king_index][0] * 100 + 1,
black_locations[king_index][1] * 100 + 1, 100, 100], 5)

def draw_game_over():
pygame.draw.rect(screen, &#39;black&#39;, [200, 200, 400, 70])
screen.blit(font.render(f&#39;{winner} won the game!&#39;, True, &#39;white&#39;), (210, 210))
screen.blit(font.render(f&#39;Press ENTER to Restart!&#39;, True, &#39;white&#39;), (210, 240))

# check en passant because people on the internet won&#39;t stop bugging me for it
def check_ep(old_coords, new_coords):
if turn_step &lt;= 1:
index = white_locations.index(old_coords)
ep_coords = (new_coords[0], new_coords[1] - 1)

piece = white_pieces[index]
else:
index = black_locations.index(old_coords)
ep_coords = (new_coords[0], new_coords[1] + 1)
piece = black_pieces[index]
if piece == &#39;pawn&#39; and abs(old_coords[1] - new_coords[1]) &gt; 1:
# if piece was pawn and moved two spaces, return EP coords as defined above
pass
else:
ep_coords = (100, 100)
return ep_coords

# add castling
def check_castling():
# king must not currently be in check, neither the rook nor king has moved previously, nothing
between
# and the king does not pass through or finish on an attacked piece
castle_moves = [] # store each valid castle move as [((king_coords), (castle_coords))]
rook_indexes = []
rook_locations = []
king_index = 0
king_pos = (0, 0)
if turn_step &gt; 1:
for i in range(len(white_pieces)):
if white_pieces[i] == &#39;rook&#39;:
rook_indexes.append(white_moved[i])
rook_locations.append(white_locations[i])
if white_pieces[i] == &#39;king&#39;:
king_index = i
king_pos = white_locations[i]

if not white_moved[king_index] and False in rook_indexes and not check:
for i in range(len(rook_indexes)):
castle = True
if rook_locations[i][0] &gt; king_pos[0]:
empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
(king_pos[0] + 3, king_pos[1])]
else:
empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
for j in range(len(empty_squares)):
if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
empty_squares[j] in black_options or rook_indexes[i]:
castle = False
if castle:
castle_moves.append((empty_squares[1], empty_squares[0]))
else:
for i in range(len(black_pieces)):
if black_pieces[i] == &#39;rook&#39;:
rook_indexes.append(black_moved[i])
rook_locations.append(black_locations[i])
if black_pieces[i] == &#39;king&#39;:
king_index = i
king_pos = black_locations[i]
if not black_moved[king_index] and False in rook_indexes and not check:
for i in range(len(rook_indexes)):
castle = True
if rook_locations[i][0] &gt; king_pos[0]:
empty_squares = [(king_pos[0] + 1, king_pos[1]), (king_pos[0] + 2, king_pos[1]),
(king_pos[0] + 3, king_pos[1])]
else:
empty_squares = [(king_pos[0] - 1, king_pos[1]), (king_pos[0] - 2, king_pos[1])]
for j in range(len(empty_squares)):

if empty_squares[j] in white_locations or empty_squares[j] in black_locations or \
empty_squares[j] in white_options or rook_indexes[i]:
castle = False
if castle:
castle_moves.append((empty_squares[1], empty_squares[0]))
return castle_moves

def draw_castling(moves):
if turn_step &lt; 2:
color = &#39;red&#39;
else:
color = &#39;blue&#39;
for i in range(len(moves)):
pygame.draw.circle(screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70), 8)
screen.blit(font.render(&#39;king&#39;, True, &#39;black&#39;), (moves[i][0][0] * 100 + 30, moves[i][0][1] * 100 +
70))
pygame.draw.circle(screen, color, (moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 8)
screen.blit(font.render(&#39;rook&#39;, True, &#39;black&#39;),
(moves[i][1][0] * 100 + 30, moves[i][1][1] * 100 + 70))
pygame.draw.line(screen, color, (moves[i][0][0] * 100 + 50, moves[i][0][1] * 100 + 70),
(moves[i][1][0] * 100 + 50, moves[i][1][1] * 100 + 70), 2)

# add pawn promotion
def check_promotion():
pawn_indexes = []
white_promotion = False
black_promotion = False
promote_index = 100
for i in range(len(white_pieces)):

if white_pieces[i] == &#39;pawn&#39;:
pawn_indexes.append(i)
for i in range(len(pawn_indexes)):
if white_locations[pawn_indexes[i]][1] == 7:
white_promotion = True
promote_index = pawn_indexes[i]
pawn_indexes = []
for i in range(len(black_pieces)):
if black_pieces[i] == &#39;pawn&#39;:
pawn_indexes.append(i)
for i in range(len(pawn_indexes)):
if black_locations[pawn_indexes[i]][1] == 0:
black_promotion = True
promote_index = pawn_indexes[i]
return white_promotion, black_promotion, promote_index



WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60
# game variables and images
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
# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []
# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
black_queen = pygame.image.load('assets/images/black queen.png')
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load('assets/images/black king.png')
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load('assets/images/black rook.png')
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load('assets/images/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load('assets/images/black knight.png')
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load('assets/images/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load('assets/images/white queen.png')
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load('assets/images/white king.png')
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load('assets/images/white rook.png')
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load('assets/images/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load('assets/images/white knight.png')
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load('assets/images/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
white_promotions = ['bishop', 'knight', 'rook', 'queen']
white_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
black_promotions = ['bishop', 'knight', 'rook', 'queen']
black_moved = [False, False, False, False, False, False, False, False,
               False, False, False, False, False, False, False, False]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
# check variables/ flashing counter
counter = 0
winner = ''
game_over = False
white_ep = (100, 100)
black_ep = (100, 100)
white_promote = False
black_promote = False
promo_index = 100
check = False
castling_moves = []