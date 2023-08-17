"""
The following program runs a connect four game where a player can play against an AI, the player who wins is the one who gets the most connect fours in the
game
"""

class GameBoard:
    def __init__(self, size):
        self.size = size
        self.num_entries = [0] * size
        self.items = [[0] * size for i in range(size)]
        self.points = [0] * 2
        
    def num_free_positions_in_column(self, column):
        return self.items[column].count(0)
        
    def game_over(self):
        count_empty_spaces = 0
        for column in range(len(self.items)):
            count_empty_spaces += self.num_free_positions_in_column(column)
        return True if count_empty_spaces == 0 else False
        
    def display(self):
        print("=" * 32)
        print("|" + "-" * ((self.size * 2) - 1) + "|")
        for row in range(self.size - 1,- 1,- 1):
            for column in range(self.size):
                if column == 0:
                    item = self.items[column][row]
                    if item == 0:
                        print("| ", end = " ")
                    if item == 1:
                        print("|o", end = " ")
                    if item == 2:
                        print("|x", end = " ")
                elif column == self.size - 1:
                    item = self.items[column][row]
                    if item == 0:
                        print(" |", end = " ")
                    if item == 1:
                        print("o|", end = " ")
                    if item == 2:
                        print("x|", end = " ")
                else:
                    item = self.items[column][row]
                    if item == 0:
                        print(" ", end = " ")
                    if item == 1:
                        print("o", end = " ")
                    if item == 2:
                        print("x", end = " ")
            print()
            
        print("|" + "-" * ((self.size * 2) - 1) + "|")
        
        for number in range(0, self.size-1):
            if number == 0:
                print("|" + str(number), end = " ")
            else:
                print(number, end = " ")
  
        print(str(self.size - 1) + "|")
        print(f"Points player 1: {self.points[0]}")
        print(f"Points player 2: {self.points[1]}")
        print("=" * 32)
        
    def num_new_points(self, column, row, player):
        num_new_points = 0
        count_points = 0
        board_size = self.size
        
        #first diagonal check
        for num in range(4):
            for n in range(4):
                if 0 <= column - n + num < board_size and 0 <= row - n + num < board_size:
                    if self.items[column - n + num][row - n + num] == player:
                        count_points += 1
            if count_points == 4:
                num_new_points += 1
            count_points = 0

        #second diagonal check
        for num in range(4):
            for n in range(4):
                if 0 <= column - n + num < board_size and 0 <= row + n - num < board_size:
                    if self.items[column - n + num][row + n - num] == player:
                        count_points += 1
            if count_points == 4:
                num_new_points += 1
            count_points = 0

        #horizontal check
        for num in range(4):
            for n in range(4):
                if 0 <= column - n + num < board_size and 0 <= row < board_size:
                    if self.items[column - n + num][row] == player:
                        count_points += 1
            if count_points == 4:
                num_new_points += 1
            count_points = 0

        #vertical check
        for num in range(4):
            for n in range(4):
                if 0 <= column < board_size and 0 <= row - n + num < board_size:
                    if self.items[column][row - n + num] == player:
                        count_points += 1
            if count_points == 4:
                num_new_points += 1
            count_points = 0
            
        return num_new_points
        
    def add(self, column, player):
        
        if (self.num_entries[column] >= self.size) or (column < 0 or column >= self.size):
            return False
        else:
            first_available_row = self.num_entries[column]
            self.items[column][first_available_row] = player
            self.num_entries[column] += 1
            self.points[player - 1] += self.num_new_points(column, first_available_row, player)
            return True
    
    def free_slots_as_close_to_middle_as_possible(self):
        
        middle = (0 + self.size - 1)/2
        list_free_slots = []
        
        for row in range(self.size):
            for column in range(len(self.items[row])):
                if self.items[column][row] == 0 and column not in list_free_slots:
                    list_free_slots.append(column)
        
        list_free_slots_tuple = [(abs(num - middle), num) for num in list_free_slots]
        sorted_list_free_slots_tuple = sorted(list_free_slots_tuple)
        sorted_list_free_slots = []
        
        for index in range(len(sorted_list_free_slots_tuple)):
            sorted_list_free_slots.append(sorted_list_free_slots_tuple[index][1])
                    
        return sorted_list_free_slots
    
    def column_resulting_in_max_points(self, player):
        list_columns = self.free_slots_as_close_to_middle_as_possible()
        list_columns_points = []
    
        for index in range(len(list_columns)):
            column = list_columns[index]
            first_row = self.items[list_columns[index]].index(0)
            self.items[column][first_row] = player
            points = self.num_new_points(column, first_row, player)
            points_tuple = (column, points)
            self.items[column][first_row] = 0
            list_columns_points.append(points_tuple)
        
        highest_number_of_points = -1
        highest_num_points_list = []
        
        for i in range(len(list_columns_points)):
            num_points = int(list_columns_points[i][1])
            if int(num_points) > highest_number_of_points:
                highest_number_of_points = num_points
                highest_num_points_list = [(list_columns_points[i][0], num_points)]
        
        return (highest_num_points_list[0])

class FourInARow:
    def __init__(self, size):
        self.board=GameBoard(size)
    def play(self):
        print("*****************NEW GAME*****************")
        self.board.display()
        player_number=0
        print()
        while not self.board.game_over():
            print("Player ",player_number+1,": ")
            if player_number==0:
                valid_input = False
                while not valid_input:
                    try:
                        column = int(input("Please input slot: "))       
                    except ValueError:
                        print("Input must be an integer in the range 0 to ", self.board.size)
                    else:
                        if column<0 or column>=self.board.size:
                            print("Input must be an integer in the range 0 to ", self.board.size)
                        else:
                            if self.board.add(column, player_number+1):
                                valid_input = True
                            else:
                                print("Column ", column, "is already full. Please choose another one.")
            else:
                # Choose move which maximises new points for computer player
                (best_column, max_points)=self.board.column_resulting_in_max_points(2)
                if max_points>0:
                    column=best_column
                else:
                    # if no move adds new points choose move which minimises points opponent player gets
                    (best_column, max_points)=self.board.column_resulting_in_max_points(1)
                    if max_points>0:
                        column=best_column
                    else:
                        # if no opponent move creates new points then choose column as close to middle as possible
                        column = self.board.free_slots_as_close_to_middle_as_possible()[0]
                self.board.add(column, player_number+1)
                print("The AI chooses column ", column)
            
            self.board.display()
           
            player_number=(player_number+1)%2
        if (self.board.points[0]>self.board.points[1]):
            print("Player 1 (circles) wins!")
        elif (self.board.points[0]<self.board.points[1]):    
            print("Player 2 (crosses) wins!")
        else:  
            print("It's a draw!")
            
game = FourInARow(6)
game.play()
    
