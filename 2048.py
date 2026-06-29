import pygame
import random
import sys
import time

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 400, 500
GRID_SIZE = 4
CELL_SIZE = WIDTH // GRID_SIZE
FPS = 60

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BROWN = (30, 0, 0)

# 블록 색깔 정의
COLOR_DICT = {
    0: (0, 0, 0),        # 검은색 (0에 대한 기본 색상)
    2: (255, 255, 0),    # 노란색
    4: (255, 165, 0),    # 주황색
    8: (255, 69, 0),     # 빨간색
    16: (255, 0, 255),   # 자주색
    32: (0, 255, 0),     # 초록색
    64: (0, 0, 255),     # 파란색
    128: (0, 255, 255),  # 청록색
    256: (128, 0, 128),  # 보라색
    512: (128, 128, 0),  # 올리브색
    1024: (0, 128, 128), # 아쿠아색
    2048: (255, 0, 0)    # 빨간색 (2048은 빨간색으로 표시)
}

# 글꼴 설정
pygame.font.init()
FONT = pygame.font.Font(None, 36)

# 초기화면 생성
def initialize_board():
    return [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

# 새로운 타일 추가
def add_new_tile(board):
    empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = random.choice([2, 4])

# 그리기 함수
def draw_board(screen, board):
    screen.fill(BLACK)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            pygame.draw.rect(screen, COLOR_DICT[board[i][j]], (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if board[i][j] != 0:
                text = FONT.render(str(board[i][j]), True, BROWN)
                text_rect = text.get_rect(center=(j * CELL_SIZE + CELL_SIZE // 2, i * CELL_SIZE + CELL_SIZE // 2))
                screen.blit(text, text_rect)

# 게임 클리어 확인 함수 추가
def check_win(board):
    for row in board:
        if 2048 in row:
            return True
    return False

# 게임 오버 확인 함수 수정
def check_game_over(board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0:
                return False
            if j != GRID_SIZE - 1 and board[i][j] == board[i][j + 1]:
                return False
            if i != GRID_SIZE - 1 and board[i][j] == board[i + 1][j]:
                return False
    return True

# 경과 시간을 표시하기 위한 함수 추가
def draw_elapsed_time(screen, elapsed_time):
    font = pygame.font.Font(None, 36)
    time_text = font.render(f"TIME: {elapsed_time:.1f} s", True, WHITE)
    
    # 텍스트를 아래로 내려줍니다.
    screen.blit(time_text, (10, HEIGHT - 40))

# 게임 클리어 및 게임 오버 메시지를 표시하기 위한 함수 수정
def draw_game_message(screen, message, x_position, y_position):
    font = pygame.font.SysFont(None, 50)

    # 메시지를 그립니다.
    message_text = font.render(message, True, WHITE)
    screen.blit(message_text, (x_position - message_text.get_width() // 2, y_position - message_text.get_height() // 2))


# 이동 함수
def move(board, direction):
    if direction == "left":
        board = [merge(row) for row in board]
    elif direction == "right":
        board = [reverse(merge(reverse(row))) for row in board]
    elif direction == "up":
        board = [merge(column) for column in zip(*board)]
        board = [list(row) for row in zip(*board)]
    elif direction == "down":
        board = [reverse(merge(reverse(column))) for column in zip(*board)]
        board = [list(row) for row in zip(*board)]

    add_new_tile(board)
    return board

# 합치기 함수
def merge(line):
    result = [0] * GRID_SIZE
    index = 0
    for value in line:
        if value != 0:
            if result[index] == 0:
                result[index] = value
            elif result[index] == value:
                result[index] *= 2
                index += 1
            else:
                index += 1
                result[index] = value
    return result

# 역순으로 반환
def reverse(line):
    return line[::-1]

# 게임 실행 함수 수정
def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048 Game")
    clock = pygame.time.Clock()

    board = initialize_board()
    add_new_tile(board)

    start_time = time.time()
    elapsed_time = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    board = move(board, "left")
                elif event.key == pygame.K_RIGHT:
                    board = move(board, "right")
                elif event.key == pygame.K_UP:
                    board = move(board, "up")
                elif event.key == pygame.K_DOWN:
                    board = move(board, "down")

        draw_board(screen, board)
        draw_elapsed_time(screen, elapsed_time)  # 경과 시간 표시 추가
        pygame.display.flip()

        if check_win(board):
            draw_game_message(screen, "GAME CLEAR!", WIDTH // 2, (HEIGHT // 2)+187)
            break
        elif check_game_over(board):
            draw_game_message(screen, "GAME OVER!", WIDTH // 2, (HEIGHT // 2)+187)
            break

        elapsed_time = time.time() - start_time
        clock.tick(FPS)

    # 게임 종료 시간 기록
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total Time: {int(total_time)} s")

    # 화면 갱신
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    main()