from copy import deepcopy


class Reversi(object):
    BOARD_SIZE = 8  # Constant board size
    evaluation_matrix = [[99, -8, 8, 6, 6, 8, -8, 99],
                         [-8, -24, -4, -3, -3, -4, -24, -8],
                         [8, -4, 7, 4, 4, 7, -4, 8],
                         [6, -3, 4, 0, 0, 4, -3, 6],
                         [6, -3, 4, 0, 0, 4, -3, 6],
                         [8, -4, 7, 4, 4, 7, -4, 8],
                         [-8, -24, -4, -3, -3, -4, -24, -8],
                         [99, -8, 8, 6, 6, 8, -8, 99]]  # Evaluation Matrix

    @staticmethod
    def get_printable_value(val):
        if val == float("Inf"):
            return "Infinity"
        elif val == -float("Inf"):
            return "-Infinity"
        return val

    def __init__(self):
        input_file = open('input.txt', 'r')
        self.player1 = input_file.readline()  # Playing player
        self.player1 = ''.join(c for c in self.player1 if c not in '\n')
        # print self.player1
        if self.player1 == 'X':
            self.player2 = 'O'
        else:
            self.player2 = 'X'

        self.max_depth = input_file.readline()  # Max Depth
        self.max_depth = ''.join(c for c in self.max_depth if c not in '\n')
        self.max_depth = int(self.max_depth)
        # print self.max_depth

        self.init_board = [['*' for c in range(self.BOARD_SIZE)] for c in
                           range(self.BOARD_SIZE)]  # Initial board position
        for i in range(self.BOARD_SIZE):
            line = input_file.readline()
            line.split()
            for j in range(self.BOARD_SIZE):
                self.init_board[i][j] = line[j]
        # print self.init_board
        self.output = []  # Data to be printed on output file

    def print_node(self, node):
        printable_coordinates = ["a", "b", "c", "d", "e", "f", "g", "h"]
        if node['move'] == "root" or node['move'] == "pass":
            move = node['move']
        else:
            move = printable_coordinates[node['move'][1]] + str(node['move'][0] + 1)

        value = self.get_printable_value(node['value'])
        alpha = self.get_printable_value(node['alpha'])
        beta = self.get_printable_value(node['beta'])
        self.output.append("\n{0},{1},{2},{3},{4}".format(move, node['current_depth'], value, alpha, beta))

    def find_next_move(self, parent, max_depth=1):
        has_move = False
        depth = parent['current_depth'] + 1
        if depth > max_depth:
            return

        if depth % 2 == 0:
            value = -float('Inf')
            player1 = self.player2
            player2 = self.player1
        else:
            value = float('Inf')
            player1 = self.player1
            player2 = self.player2

        added_nodes = parent['children']

        for x in range(self.BOARD_SIZE):
            for y in range(self.BOARD_SIZE):
                new_board = self.get_valid_board((x, y), parent['current_board'], player1, player2)
                if new_board == None:
                    continue

                if depth == max_depth:
                    value = self.utility(new_board)

                next_coordinates = (x, y)

                node = {"move": next_coordinates, "current_depth": depth, "current_board": new_board, "value": value,
                        "alpha": parent['alpha'], "beta": parent['beta'], "children": []}  # Store the state
                has_move = True
                self.print_node(node)
                self.find_next_move(node, max_depth)

                if (depth % 2 == 1 and node['value'] >= parent['beta'] or (  # Pruning tree
                                    depth % 2 == 0 and node['value'] <= parent['alpha'])):  # Pruning tree
                    if depth % 2 == 1:  # Max chooses
                        parent['value'] = max(parent['value'], node['value'])
                    else:  # Min chooses
                        parent['value'] = min(parent['value'], node['value'])
                    added_nodes.append(node)
                    self.print_node(parent)
                    return
                else:
                    if depth % 2 == 1:  # Max chooses
                        parent['value'] = max(parent['value'], node['value'])
                        parent['alpha'] = max(parent['alpha'], min(node['value'], node['beta']))
                    else:  # Min chooses
                        parent['value'] = min(parent['value'], node['value'])
                        parent['beta'] = min(parent['beta'], max(node['value'], node['alpha']))
                    added_nodes.append(node)
                    self.print_node(parent)

        if not has_move:
            if parent['move'] == 'pass':
                value = self.utility(parent['current_board'])

            node = {"move": "pass", "current_depth": depth, "current_board": parent['current_board'], "value": value,
                    "alpha": parent['alpha'], "beta": parent['beta'], "children": []}

            self.print_node(node)
            if not parent['move'] == 'pass':
                self.find_next_move(node, max_depth)

            if (depth % 2 == 0 and node['value'] <= parent['alpha'] or (
                                depth % 2 == 1 and node['value'] >= parent['beta'])):
                if depth % 2 == 1:
                    parent['value'] = max(parent['value'], node['value'])
                else:
                    parent['value'] = min(parent['value'], node['value'])
                added_nodes.append(node)
                self.print_node(parent)
                return
            else:
                if depth % 2 == 1:
                    parent['value'] = max(parent['value'], node['value'])
                    parent['alpha'] = max(parent['alpha'], min(node['value'], node['beta']))
                else:
                    parent['value'] = min(parent['value'], node['value'])
                    parent['beta'] = min(parent['beta'], max(node['value'], node['alpha']))
                added_nodes.append(node)
                self.print_node(parent)

    def get_valid_board(self, next_coordinate, board, player1, player2):
        if not board[next_coordinate[0]][next_coordinate[1]] == "*":
            return

        for x in range(-1, 2):
            for y in range(-1, 2):
                if x == 0 and y == 0 or not self.is_on_board((next_coordinate[0] + x, next_coordinate[1] + y)):
                    continue
                tempb = deepcopy(board)

                tempb[next_coordinate[0]][next_coordinate[1]] = player1

                if board[next_coordinate[0] + x][next_coordinate[1] + y] == player2:  # When opponent is present
                    tempb[next_coordinate[0] + x][next_coordinate[1] + y] = player1
                    for i in range(2, self.BOARD_SIZE):
                        tempc = (next_coordinate[0] + (x * i), next_coordinate[1] + (y * i))
                        if not self.is_on_board(tempc) or board[tempc[0]][
                            tempc[1]] == "*":  # If he finds gap so it was not a legal move
                            break
                        if board[tempc[0]][tempc[1]] == player1:  # If he finds his player on other side
                            return tempb
                        tempb[tempc[0]][tempc[1]] = player1

    def utility(self, board):  # Used to find value at given state
        player1 = 0
        player2 = 0
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if board[i][j] == self.player1:
                    player1 += self.evaluation_matrix[i][j]
                elif board[i][j] == self.player2:
                    player2 += self.evaluation_matrix[i][j]
        return player1 - player2

    def alpha_beta(self, depth):
        root = {"value": -float('Inf'), "current_board": deepcopy(self.init_board), "current_depth": 0,
                "alpha": -float('Inf'), "beta": float('Inf'), "move": 'root', "children": []}

        self.output.append("Node,Depth,Value,Alpha,Beta")
        self.print_node(root)

        self.find_next_move(root, depth)

        best_node = None
        for temp in root['children']:
            if best_node == None or temp['move'][0] * 10 + temp['move'][1] < best_node['move'][0] * 10 + \
                    best_node['move'][1]:
                best_node = temp

        output_file = open("output.txt", "w")
        for i in best_node['current_board']:
            output_file.write("".join(i) + '\n')
        for k in self.output:
            output_file.write(k)

        output_file.close()

    def is_on_board(self, coord):
        if (0 <= coord[0] < self.BOARD_SIZE) and (0 <= coord[1] < self.BOARD_SIZE):
            return True
        else:
            return False

    def start(self):
        self.alpha_beta(self.max_depth)


reversi = Reversi()
reversi.start()
