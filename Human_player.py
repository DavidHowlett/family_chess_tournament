"""This file allows a human to compete in the tournament."""


def main(history, white_time, black_time):
    if len(history) < 2:
        print('To play please type moves that look like: E2E4')
    while True:
        response = input('Your move is: ')
        if len(response) != 4:
            print('ERROR: The response needs to be 4 characters long')
            continue
        if not ('A' <= response[0].upper() <= 'H' and '1' <= response[1] <= '8' and
                'A' <= response[2].upper() <= 'H' and '1' <= response[3] <= '8'):
            print('ERROR: bad format')
            continue
        break
    x1 = ord(response[0].upper()) - ord('A')
    y1 = int(response[1]) - 1
    x2 = ord(response[2].upper()) - ord('A')
    y2 = int(response[3]) - 1
    board = history[-1]
    # add piece to destination
    board[y2][x2] = board[y1][x1]
    # remove piece from source
    board[y1][x1] = '.'
    return history[-1]
