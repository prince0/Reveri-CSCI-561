import sys

input_file = open('input.txt', 'r')
output_file = open("output.txt", "w")

player1 = input_file.readline()  # Player
player1 = ''.join(c for c in player1 if c not in '\n')
# print(player1)

depth = input_file.readline()  # Depth
depth = ''.join(c for c in depth if c not in '\n')
depth = int(depth)
# print(depth)

if player1 == "X":
    player2 = "O"
else:
    player2 = "X"

# print(player1+player2)



input_board = [['*' for c in range(8)] for c in range(8)]  # Initial board position
for i in range(8):
    line = input_file.readline()
    line.split()
    for j in range(8):
        input_board[i][j] = line[j]

# for i in range(8):
#     for j in range(8):
#         output_file.write(str(input_board[i][j]))
#     output_file.write("\n")

input_file.close()

evaluation_matrix = [[99, -8, 8, 6, 6, 8, -8, 99],
                     [-8, -24, -4, -3, -3, -4, -24, -8],
                     [8, -4, 7, 4, 4, 7, -4, 8],
                     [6, -3, 4, 0, 0, 4, -3, 6],
                     [6, -3, 4, 0, 0, 4, -3, 6],
                     [8, -4, 7, 4, 4, 7, -4, 8],
                     [-8, -24, -4, -3, -3, -4, -24, -8],
                     [99, -8, 8, 6, 6, 8, -8, 99]]

node_i = 'Node'
depth_i = 'Depth'
value_i = 'Value'
alpha = 'Alpha'
beta = 'Beta'

depth_iterate = 0  # will give the depth of current iteration

output_iterate = []
output_iterate.append([])
output_iterate[0].append(node_i)
output_iterate[0].append(depth_i)
output_iterate[0].append(value_i)
output_iterate[0].append(alpha)
output_iterate[0].append(beta)


# print(output_iterate)
# for i in range(len(output_iterate[0])):
#     output_file.write(output_iterate[0][i])
#     if not i == (len(output_iterate[0]) - 1):
#         output_file.write(",")

def alpha_beta_search(state):
    v = player_one_chance(state, float("-inf"), float("inf"))
    return v


def player_one_chance(state, alpha, beta):  # max value
    if terminal_state(state, depth_iterate):
        return 0

    v = float("-inf")
    # for

    return 0


available_state = []


def terminal_state(state, d):
    if d == depth:
        return True
    else:
        for i in range(8):
            if player1 in state[i]:
                row = i
                col = state[i].index(player1)
                index = chr(90 + col) + str(row)
                available_state.append(index)


def utility(state):
    x = 0
    o = 0
    for i in range(8):
        for j in range(8):
            if state[i][j] == player1:


output_file.close()
