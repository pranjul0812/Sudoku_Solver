import os
import time


def display_sudo(sudo_sample):

	for i in range(3):
		print("_ " * 12)
		for k in range(3):
			for j in range(3):
				for l in range(3):
					if sudo_sample[i][j][k][l] == 0:
						print(" ", end=" ")
					else:
						print(str(sudo_sample[i][j][k][l]), end=" ")
					if l == 2:
						print("|", end=" ")
			print()


def create_sudoku():
	easy = [[[[0 for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]

	# easy[0][0][0][0] = 5
	# easy[0][0][0][1] = 3
	easy[0][0][0][2] = 6
	# easy[0][0][1][0] = 6
	easy[0][0][1][1] = 3
	easy[0][0][1][2] = 9
	easy[0][0][2][0] = 5
	# easy[0][0][2][1] = 9
	# easy[0][0][2][2] = 8

	easy[0][1][0][0] = 1
	# easy[0][1][0][1] = 7
	easy[0][1][0][2] = 2
	# easy[0][1][1][0] = 1
	easy[0][1][1][1] = 5
	# easy[0][1][1][2] = 5
	# easy[0][1][2][0] = 8
	easy[0][1][2][1] = 4
	easy[0][1][2][2] = 9

	easy[0][2][0][0] = 5
	# easy[0][2][0][1] = 7
	# easy[0][2][0][2] = 2
	easy[0][2][1][0] = 1
	easy[0][2][1][1] = 4
	easy[0][2][1][2] = 2
	# easy[0][2][2][0] = 8
	# easy[0][2][2][1] = 4
	# easy[0][2][2][2] = 8

	easy[1][0][0][0] = 9
	# easy[1][0][0][1] = 7
	easy[1][0][0][2] = 2
	# easy[1][0][1][0] = 4
	easy[1][0][1][1] = 8
	# easy[1][0][1][2] = 4
	easy[1][0][2][0] = 1
	# easy[1][0][2][1] = 7
	easy[1][0][2][2] = 3

	# easy[1][1][0][0] = 6
	easy[1][1][0][1] = 3
	# easy[1][1][0][2] = 7
	# easy[1][1][1][0] = 8
	# easy[1][1][1][1] = 8
	# easy[1][1][1][2] = 3
	# easy[1][1][2][0] = 7
	easy[1][1][2][1] = 6
	# easy[1][1][2][2] = 2

	easy[1][2][0][0] = 4
	# easy[1][2][0][1] = 3
	easy[1][2][0][2] = 1
	# easy[1][2][1][0] = 1
	easy[1][2][1][1] = 7
	# easy[1][2][1][2] = 1
	easy[1][2][2][0] = 8
	# easy[1][2][2][1] = 1
	easy[1][2][2][2] = 9

	# easy[2][0][0][1] = 6
	# easy[2][0][0][1] = 6
	# easy[2][0][0][1] = 6
	# easy[2][0][1][0] = 4
	easy[2][0][1][1] = 5
	easy[2][0][1][2] = 4
	# easy[2][0][2][0] = 1
	# # easy[2][0][2][1] = 7
	easy[2][0][2][2] = 7

	# easy[2][1][0][0] = 2
	easy[2][1][0][1] = 1
	# easy[2][1][0][2] = 4
	# easy[2][1][1][0] = 4
	# easy[2][1][1][1] = 1
	# easy[2][1][1][2] = 9
	easy[2][1][2][0] = 5
	# easy[2][1][2][1] = 8
	easy[2][1][2][2] = 3

	# easy[2][2][0][0] = 2
	# easy[2][2][0][1] = 8
	easy[2][2][0][2] = 5
	easy[2][2][1][0] = 9
	easy[2][2][1][1] = 1
	# easy[2][2][1][2] = 5
	easy[2][2][2][0] = 2
	# easy[2][2][2][1] = 7
	# easy[2][2][2][2] = 9

	return easy


def zeroAvailable(lst):
	for i in range(3):
		for k in range(3):
			for j in range(3):
				for l in range(3):
					if lst[i][j][k][l] == 0:
						return True
	return False


def checkOtherValues(sudo_sample2, i, j, k, l):
	expected_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	found = False
    # Check horizontal values
	for outer_col in range(3):
		for inner_col in range(3):
			if sudo_sample2[i][outer_col][k][inner_col] in expected_list:
				expected_list.remove(sudo_sample2[i][outer_col][k][inner_col])

	# check Vertical values
	for outer_row in range(3):
		for inner_row in range(3):
			if sudo_sample2[outer_row][j][inner_row][l] in expected_list:
				expected_list.remove(sudo_sample2[outer_row][j][inner_row][l])

	# check block values
	for row in range(3):
		for col in range(3):
			if sudo_sample2[i][j][row][col] in expected_list:
				expected_list.remove(sudo_sample2[i][j][row][col])

	if len(expected_list) == 1:
		sudo_sample2[i][j][k][l] = expected_list[0]
		found = True

	return sudo_sample2, found


def checkBlock(lst, i, j):
	expected_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	zero_positions = []
	change = False
	for k in range(3):
		for l in range(3):
			if lst[i][j][k][l] != 0:
				expected_list.remove(lst[i][j][k][l])
			else:
				zero_positions.append([k, l])
	# print(expected_list)
	# print(zero_positions)
	for item in expected_list:
		possible_positions = []
		for position in zero_positions:
			if checkPossibility(lst, i, j, position, item):
				possible_positions.append(position)
			if len(possible_positions) > 1:
				break
		# print(possible_positions)
		if len(possible_positions) == 1:
			change = True
			lst[i][j][possible_positions[0][0]][possible_positions[0][1]] = item
			zero_positions.remove(possible_positions[0])

	return lst, change


def checkPossibility(lst, i, j, position, item):
	k = position[0]
	l = position[1]
	# check in vertical values:
	for o_row in range(3):
		for i_row in range(3):
			# print(lst[o_row][j][i_row][l], end=" ")
			if lst[o_row][j][i_row][l] == item:
				return False
	# print()
	# check in horizontal values:
	for o_col in range(3):
		for i_col in range(3):
			# print(lst[i][o_col][k][i_col], end=" ")
			if lst[i][o_col][k][i_col] == item:
				return False

	return True


def solve_game_level2(sudo_sample):
	# go in each block and check if we can fill any values
	fill = False
	for i in range(3):
		for j in range(3):
			sudo_sample, change = checkBlock(sudo_sample, i, j)
			time.sleep(3)
			if change:
				fill = True
				# os.system('cls')
				# display_sudo(sudo_sample)
	return sudo_sample, fill


def solve_game_level1(sudo_sample1):
	result = sudo_sample1
	found = False
	fill = False
	# go one by one in each row
	for i in range(3):
		for k in range(3):
			for j in range(3):
				for l in range(3):
					if sudo_sample1[i][j][k][l] == 0:
						result, found = checkOtherValues(sudo_sample1, i, j, k, l)
					if found:
						fill = True
						# os.system('cls')
						# display_sudo(result)

	return result, fill


def start_game():
	print("Let's start the Sudoku Game...")
	time.sleep(.5)
	sudo_sample = create_sudoku()
	print("Please Solve this Sudoku...")
	time.sleep(.5)
	print("Coming in few seconds..")
	time.sleep(2)
	os.system('cls')
	display_sudo(sudo_sample)
	print()
	time.sleep(1)
	print("Let's start solving the sudoku")
	check = True
	while check:
		sudo_sample, fill = solve_game_level1(sudo_sample)
		if not fill:
			check = False
		else:
			check = zeroAvailable(sudo_sample)
	# os.system('cls')
	# print("Your Level1 Solved sudoku is coming in few seconds.. ")
	# time.sleep(.5)
	# display_sudo(sudo_sample)
	# time.sleep(1)
	while not check:
		sudo_sample, fill = solve_game_level2(sudo_sample)
		if not fill:
			check = True
		else:
			check = not zeroAvailable(sudo_sample)
	time.sleep(1)
	os.system('cls')
	print("Your Final Solved sudoku is coming in few seconds.. ")
	time.sleep(2)
	display_sudo(sudo_sample)


if __name__ == '__main__':
	# sudo_sample = create_sudoku()
	# print("Please Solve this Sudoku...")
	# time.sleep(1)
	# print("Coming in few seconds..")
	# time.sleep(3)
	# os.system('cls')
	# display_sudo(sudo_sample)
	start_game()


