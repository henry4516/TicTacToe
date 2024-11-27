### can play 3*3 tic tac toe with AI.
import pygame as pg
import sys
import math
import time
import tic_tac_toe as ttt
import ttt_game_info as info

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800

board_size = 3
game = ttt.TTT(board_size)
grid_size = 80
board_left = SCREEN_WIDTH // 2 - board_size * grid_size // 2
board_up = SCREEN_HEIGHT // 2 - board_size * grid_size // 2
board_right = SCREEN_WIDTH - board_left
board_down = SCREEN_HEIGHT - board_up

dataFile = "tictactoeData.txt"

pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('TIC TAC TOE')

# Colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

# Set font
font = pg.font.SysFont('arial', 36)

frame_count = 0

# text display function
def render_text(message: str, color, x: float, y: float) -> None:
    text_surface = font.render(message, True, color)
    screen.blit(text_surface, (x, y))

restart_width, restart_height = font.size("Restart")
restart_button_left, restart_button_up = 800, 40
restart_button_width, restart_button_height = restart_width + 4, restart_height + 4
restart_left, restart_up = restart_button_left + 2, restart_button_up + 2

AIonoff_width, AIonoff_height = font.size("AI:OFF")
AI_button_left = restart_button_left
AI_button_up = restart_button_up + restart_button_height + 10
AI_button_width = restart_button_width
AI_button_height = restart_button_height
AIonoff_left = AI_button_width // 2 - AIonoff_width // 2 + AI_button_left
AIonoff_height = AI_button_height // 2 - AIonoff_height // 2 + AI_button_up


local_time_start = time.strftime("%d %b %Y %H:%M:%S", time.localtime())

gameData = info.gameInfo()
FPS_LIMIT = 60
clock = pg.time.Clock()
pre_endtime = 0
pre_endframe = 0
round = 0
AI = True ### by default AI is O
current_player = ttt.X
duration = None
running = True
end = False
empty_grids = board_size * board_size
result = None
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                x, y = event.pos
                if AI_button_left < x < AI_button_left + AI_button_width and AI_button_up < y < AI_button_up + AI_button_height:
                    AI = not AI
                if not end:
                    if current_player == ttt.X or not AI: 
                        if board_left < x < board_right and board_up < y < board_down:
                            ### which gird is clicked
                            grid_row = math.ceil((x - board_left) / grid_size) - 1
                            grid_col = math.ceil((y - board_up) / grid_size) - 1
                            ### successful move
                            if game.move(current_player, (grid_row, grid_col)):
                                round += 1
                                empty_grids -= 1
                                if current_player == ttt.X:
                                    current_player = ttt.O
                                elif current_player == ttt.O:
                                    current_player = ttt.X
                                else:
                                    raise TypeError("invalid player")
                                ### check results
                                result = game.complete()
                                ### ends
                                if result != 0 or empty_grids == 0:
                                    end = True
                                    gameData.update(result)
                                    #print("result ", result)
                                    #print("end: ", end)
                ### game has ended, restart
                else:
                    if restart_button_left < x < restart_button_left + restart_button_width and restart_button_up < y < restart_button_up + restart_button_height:
                        game = ttt.TTT(board_size)
                        round = 0
                        current_player = ttt.X
                        pre_endtime = pg.time.get_ticks()
                        pre_endframe = frame_count
                        duration = None
                        running = True
                        end = False
                        empty_grids = board_size * board_size
                        result = None

    ### AI moves
    if not end:
        if AI and current_player == ttt.O:
            AImove, _ = ttt.AIplay(game, ttt.O)
            #print("AI move: ", AImove)
            game.move(ttt.O, AImove)
            current_player = ttt.X
            empty_grids -= 1
            #print("empty grids: ", empty_grids)
            round += 1
            ### check results
            result = game.complete()
            ### ends
            if result != 0 or empty_grids == 0:
                end = True
                gameData.update(result)
                #print("result ", result)
                #print("end: ", end)

    program_time = pg.time.get_ticks()
    game_time = (program_time - pre_endtime) // 1000
    ### game not end, or first time
    if not end or duration is None:
        duration = f"{game_time // 60}:{game_time % 60}"
    
    ### last loop. update data to data file.
    if not running:
        f = open(dataFile, "a")
        f.write(f"Start Time: {local_time_start}" + "\n")
        f.write(f"Duration: [{(program_time // 1000) // 60}:{(program_time // 1000) % 60}]" + "\n")
        f.write(repr(gameData) + "\n")
        f.close()

    frame_count += 1
    FPS = 1
    if game_time > 0:
        FPS = (frame_count - pre_endframe) // game_time

    local_time = time.strftime("%d %b %Y %H:%M:%S", time.localtime())

    clock.tick(FPS_LIMIT)

    ### draw board lines and background
    screen.fill(white)
    for i in range(board_size + 1):
        ### vertical lines
        pg.draw.line(screen, black, (board_left + i * grid_size, board_up), (board_left + i * grid_size, board_down), 2)
        ### hori lines
        pg.draw.line(screen, black, (board_left, board_up + i * grid_size), (board_right, board_up + i * grid_size), 2)
    ### draw pieces
    for x in range(board_size):
        for y in range(board_size):
            ### X(1) is green
            if game.at((x, y)) == ttt.X:
                pg.draw.rect(screen, green, (board_left + x * grid_size + 1, board_up + y * grid_size + 1, grid_size - 1, grid_size - 1))
            ### O(-1) is blue
            elif game.at((x, y)) == ttt.O:
                pg.draw.rect(screen, blue, (board_left + x * grid_size + 1, board_up + y * grid_size + 1, grid_size - 1, grid_size - 1))

    ### text info
    render_text(f"Time: {duration}", black, 70, 100)
    render_text(f"FPS: {FPS}", black, 10, 10)
    render_text(f"Round: {round // 2 + round % 2}", black, 10, 50)
    pg.draw.rect(screen, black, (AI_button_left, AI_button_up, AI_button_width, AI_button_height))
    render_text(f"Games: {gameData.games()}", black, 700, 200)
    render_text(f"X: wins [{gameData.Xwins()}]", black, 700, 250)
    render_text(f"O: wins [{gameData.Owins()}]", black, 700, 300)
    render_text(f"Tie: [{gameData.tie()}]", black, 700, 350)
    render_text(f"X win rate: [{gameData.Xwinrate():.1f}%]", black, 700, 400)
    render_text(f"O win rate: [{gameData.Owinrate():.1f}%]", black, 700, 450)
    if AI:
        render_text("AI: ON", white, AIonoff_left, AIonoff_height)
    else:
        render_text("AI:OFF", white, AIonoff_left, AIonoff_height)
    #render_text(f"empty grids {empty_grids}", black, 10, 20)

    if end:
        if result != 0:
            if result == ttt.X:
                text_width, text_height = font.size("X wins!")
                render_text("X wins!", green, SCREEN_WIDTH // 2 - text_width // 2, board_up - text_height - 20)
            elif result == ttt.O:
                text_width, text_height = font.size("O wins!")
                render_text("O wins!", blue, SCREEN_WIDTH // 2 - text_width // 2, board_up - text_height - 20)
            else:
                raise TypeError("invalid player")
        ### Tie, end because game board is full
        else:
            text_width, text_height = font.size("Tie")
            render_text("Tie", black, SCREEN_WIDTH // 2 - text_width // 2, board_up - text_height - 20)
        ### restart button
        pg.draw.rect(screen, black, (restart_button_left, restart_button_height, restart_button_width, restart_button_height))
        render_text("Restart", white, restart_left, restart_up)
    else:
        if current_player == ttt.X:
            text_width, text_height = font.size("X's move")
            render_text("X's move", green, SCREEN_WIDTH // 2 - text_width // 2, board_up - text_height - 20)
        elif current_player == ttt.O:
            text_width, text_height = font.size("O's move")
            render_text("O's move", blue, SCREEN_WIDTH // 2 - text_width // 2, board_up - text_height - 20)
        else:
            raise TypeError("invalid player")

    pg.display.flip()

pg.quit()
sys.exit()