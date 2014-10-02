from tronclient.Client import *
import copy
from random import randint


class PlayerAI():
    def __init__(self):
        return

    def new_game(self, game_map, player_lightcycle, opponent_lightcycle):
        return

    def checkAllDirections(self, current_x, current_y, current_direction, player_lightcycle, game_map, queue, moveNumber):

        possible_directions = self.makeDictionaryDirection(current_x, current_y, current_direction)
        list_directions_weight = []

        for direction, position in possible_directions.iteritems():
            directions_weight = [0]

            x = position[0]
            y = position[1]

            if game_map[x][y] == POWERUP:
                if player_lightcycle['hasPowerup']:
                    directions_weight[0] += 12
                else:
                    directions_weight[0] += 18
                    directions_weight.append(direction)
                    list_directions_weight.append(directions_weight)
                    queue.append([x, y, self.movDir_to_currentDir(direction)])
            elif game_map[x][y] == EMPTY:
                directions_weight[0] += 5
                directions_weight.append(direction)
                list_directions_weight.append(directions_weight)
                queue.append([x, y, self.movDir_to_currentDir(direction)])
            '''
            elif player_lightcycle['hasPowerup'] and game_map[x][y] == TRAIL:
                #powerupType = player_lightcycle['powerupType']
                directions_weight[0] += 1
                directions_weight.append(direction+5)
                list_directions_weight.append(directions_weight)
                queue.append([x,y,self.movDir_to_currentDir(direction)])
            '''
            #if len(queue) == 0:
            #    print('Inside: Queue', len(queue), 'move',moveNumber )
        return list_directions_weight

    def makeDictionaryDirection(self, current_x, current_y, current_direction):
        if current_direction == 0:
            return {3: [current_x - 1, current_y], 4: [current_x + 1, current_y], 1: [current_x, current_y - 1]}
        elif current_direction == 1:
            return {4: [current_x + 1, current_y], 2: [current_x, current_y + 1], 1: [current_x, current_y - 1]}
        elif current_direction == 2:
            return {3: [current_x - 1, current_y], 4: [current_x + 1, current_y], 2: [current_x, current_y + 1]}
        elif current_direction == 3:
            return {3: [current_x - 1, current_y], 2: [current_x, current_y + 1], 1: [current_x, current_y - 1]}

    def movDir_to_currentDir(self, moving_direction):
        if moving_direction == 1:
            return 0
        elif moving_direction == 2:
            return 2
        elif moving_direction == 3:
            return 3
        else:
            return 1

    def findState(self, list_directions_weight):
        weights = []
        for path in list_directions_weight:
            weights.append(path[0])

        max_num = max(weights)
        # if max_num == turns:
        #return 'Far'
        #else:
        index = weights.index(max_num)
        return [list_directions_weight[index], max_num]

    def iteratePathTurns(self, possible_paths, queue_positionstocheck, game_map, player_lightcycle, moveNumber):
        length = len(possible_paths)

        for i in range(length):
            check_position = queue_positionstocheck.pop(0)
            possible_paths_next = self.checkAllDirections(check_position[0], check_position[1], check_position[2],
                                                          player_lightcycle, game_map, queue_positionstocheck, moveNumber)

            for j in range(len(possible_paths_next)):
                possible_paths.append(copy.copy(possible_paths[i]))
                possible_paths[-1][0] += possible_paths_next[j][0]
                possible_paths[-1].extend([possible_paths_next[j][1]])

        del possible_paths[0:length]
        return possible_paths

    def get_move(self, game_map, player_lightcycle, opponent_lightcycle, moveNumber):

        my_position = player_lightcycle['position']
        my_x = my_position[0]
        my_y = my_position[1]
        my_direction = player_lightcycle['direction']

        opp_position = opponent_lightcycle['position']
        opp_x = opp_position[0]
        opp_y = opp_position[1]
        opp_direction = opponent_lightcycle['direction']

        distance = abs(opp_x-my_x) + abs(opp_y-my_y)


        queue_positionstocheck = [[my_x, my_y, my_direction]]

        check_position = queue_positionstocheck.pop(0)
        possible_paths = self.checkAllDirections(check_position[0], check_position[1], check_position[2],player_lightcycle, game_map, queue_positionstocheck, moveNumber)

        possible_paths = self.iteratePathTurns(possible_paths, queue_positionstocheck, game_map, player_lightcycle, moveNumber)
        possible_paths = self.iteratePathTurns(possible_paths, queue_positionstocheck, game_map, player_lightcycle, moveNumber)
        possible_paths = self.iteratePathTurns(possible_paths, queue_positionstocheck, game_map, player_lightcycle, moveNumber)
        possible_paths = self.iteratePathTurns(possible_paths, queue_positionstocheck, game_map, player_lightcycle, moveNumber)
        possible_paths = self.iteratePathTurns(possible_paths, queue_positionstocheck, game_map, player_lightcycle, moveNumber)

        total_paths = [[0,0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [0, 8], [0, 9] ]
        for eachmainpath in possible_paths:
            if eachmainpath[1] == 0:
                total_paths[0][0] += eachmainpath[0]
            elif eachmainpath[1] == 1:
                total_paths[1][0] += eachmainpath[0]
            elif eachmainpath[1] == 2:
                total_paths[2][0] += eachmainpath[0]
            elif eachmainpath[1] == 3:
                total_paths[3][0] += eachmainpath[0]
            elif eachmainpath[1] == 4:
                total_paths[4][0] += eachmainpath[0]
            elif eachmainpath[1] == 5:
                total_paths[5][0] += eachmainpath[0]
            elif eachmainpath[1] == 6:
                total_paths[6][0] += eachmainpath[0]
            elif eachmainpath[1] == 7:
                total_paths[7][0] += eachmainpath[0]
            elif eachmainpath[1] == 8:
                total_paths[8][0] += eachmainpath[0]
            elif eachmainpath[1] == 9:
                total_paths[9][0] += eachmainpath[0]

        #if moveNumber == 1:
        #    print('total_paths', total_paths)

        [best_path, weight] = self.findState(total_paths)

       # if weight <=8:
       #     print('queue', queue_positionstocheck)
       #     print('possible', possible_paths)
       #     print(moveNumber,'- total paths: ',total_paths)


        if weight <= 4 and player_lightcycle['hasPowerup']:
            return best_path[1] + 5
        else:
            return best_path[1]


