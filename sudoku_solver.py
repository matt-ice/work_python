# sudoku solver test

board = [
	[7, 8, 0, 4, 0, 0, 1, 2, 0],
	[6, 0, 0, 0, 7, 5, 0, 0, 9],
	[0, 0, 0, 6, 0, 1, 0, 7, 8],
	[0, 0, 7, 0, 4, 0, 2, 6, 0],
	[0, 0, 1, 0, 5, 0, 9, 3, 0],
	[9, 0, 4, 0, 6, 0, 0, 0, 5],
	[0, 7, 0, 3, 0, 0, 0, 1, 2],
	[1, 2, 0, 0, 0, 7, 4, 0, 0],
	[0, 4, 9, 2, 0, 6, 0, 0, 7]
]


def get_possible_board_with_empty_lists():
	output_list = board.copy()
	for row in range(9):
		for column in range(9):
			if output_list[row][column] == 0:
				output_list[row][column] = []
	return output_list


def get_available_numbers(row, column):
	result = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	# check column and row for existing numbers
	for i in range(0, 9):
		if board[row][i] in result:
			result.remove(board[row][i])
		if board[i][column] in result:
			result.remove(board[i][column])
		if len(result) == 1:
			return result

	# check square for existing numbers
	topCornerOfSquareRow = (row // 3) * 3
	topCornerOfSquareColumn = (column // 3) * 3
	for r in range(topCornerOfSquareRow, topCornerOfSquareRow + 3):
		for c in range(topCornerOfSquareColumn, topCornerOfSquareColumn + 3):
			if board[r][c] in result:
				result.remove(board[r][c])
			if len(result) == 1:
				return result
	return result

def get_tuple_in_list(full_list):
	duplicates_present = False
	shortlist = []
	result = []
	for i in full_list:
		if isinstance(i, list) and len(i) == 2:
			shortlist.append(i)

	for i in shortlist:
		if shortlist.count(i) > 1:
			duplicates_present = True
			break

	if duplicates_present:
		for i in shortlist:
			if shortlist.count(i)>1 and i not in result:
				result.append(i)
	return result

def get_coumn_list(column):
	result = []
	for row in range(9):
		result.append(possible_numbers[row][column])
	return result

def remove_tuples(possible_numbers):
	result = possible_numbers
	# remove tuple elements in rows
	for dimension in range(9):
		# iterate over rows
		tuple_list = get_tuple_in_list(result[dimension])
		tuple_count = len(tuple_list)
		if tuple_count > 0:
			for column in range(9):
				active_cell = result[dimension][column]
				for tup in tuple_list:
					if active_cell != tup and isinstance(active_cell,list):
						if tup[0] in active_cell:
							active_cell.remove(tup[0])
						if tup[1] in active_cell:
							active_cell.remove(tup[1])
		# iterate over columns
		tuple_list = get_tuple_in_list(get_coumn_list(dimension))
		tuple_count = len(tuple_list)
		if tuple_count > 0:
			for row in range(9):
				active_cell = result[row][dimension]
				for tup in tuple_list:
					if active_cell != tup and isinstance(active_cell, list):
						if tup[0] in active_cell:
							active_cell.remove(tup[0])
						if tup[1] in active_cell:
							active_cell.remove(tup[1])
	return result


def populate_possibles(possible_numbers):
	# where the board is an empty list (not solved yet), populate with potential numbers
	for row in range(9):
		for column in range(9):
			if isinstance(possible_numbers[row][column], list):
				possible_numbers[row][column] = get_available_numbers(row, column)
	return possible_numbers


def update_board(possible_numbers, board):
	# update board when there is only one possible answer
	for y in range(9):
		for x in range(9):
			if isinstance(possible_numbers[y][x], list) and len(possible_numbers[y][x]) == 1:
				board[y][x] = possible_numbers[y][x][0]
	return board


def isUnsolved():
	# check if the board still has unsolved spots
	for row in range(9):
		for column in range(9):
			if isinstance(board[row][column], list) or board[row][column] == 0:
				return True
	return False


iteration_count = 0

while isUnsolved():
	possible_numbers = get_possible_board_with_empty_lists()
	possible_numbers = populate_possibles(possible_numbers)
	possible_numbers = remove_tuples(possible_numbers)
	board = update_board(possible_numbers, board)
	iteration_count += 1

for row in board:
	print(row)
print("Done in {} iterations".format(iteration_count))
