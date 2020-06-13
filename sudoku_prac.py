import os
import time


def display_sudo(sudo_sample):
	for i in range(3):
		print("_ "*11)
		for k in range(3):
			for j in range(3):
				for l in range(3):
					if sudo_sample[i][j][k][l] == 0:
						print(" ", end=" ")
					else:
						print(str(sudo_sample[i][j][k][l]), end=" ")
					if l == 2:
						print("|", end="")
			print()
	print("_ "*11)


def create_sudoku():
	easy = [[[[0 for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]

	easy[0][0][1][0] = 6
	easy[0][0][1][1] = 8
	easy[0][0][2][0] = 1
	easy[0][0][2][1] = 9

	easy[0][1][0][0] = 2
	easy[0][1][0][1] = 6
	easy[0][1][1][1] = 7
	easy[0][1][2][2] = 4

	easy[0][2][0][0] = 7
	easy[0][2][0][2] = 1
	easy[0][2][1][1] = 9
	easy[0][2][2][0] = 5

	easy[1][0][0][0] = 8
	easy[1][0][0][1] = 2
	easy[1][0][1][2] = 4
	easy[1][0][2][1] = 5

	easy[1][1][0][0] = 1
	easy[1][1][1][0] = 6
	easy[1][1][1][2] = 2
	easy[1][1][2][2] = 3

	easy[1][2][0][1] = 4
	easy[1][2][1][0] = 9
	easy[1][2][2][1] = 2
	easy[1][2][2][2] = 8

	easy[2][0][0][2] = 9
	easy[2][0][1][1] = 4
	easy[2][0][2][0] = 7
	easy[2][0][2][2] = 3

	easy[2][1][0][0] = 3
	easy[2][1][1][1] = 5
	easy[2][1][2][1] = 1
	easy[2][1][2][2] = 8

	easy[2][2][0][1] = 7
	easy[2][2][0][2] = 4
	easy[2][2][1][1] = 3
	easy[2][2][1][2] = 6

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


def solve_game(sudo_sample1):
	result = sudo_sample1
	found = False
	# go one by one in each row
	for i in range(3):
		for k in range(3):
			for j in range(3):
				for l in range(3):
					if sudo_sample1[i][j][k][l] == 0:
						result, found = checkOtherValues(sudo_sample1, i, j, k, l)
					if found:
						os.system('cls')
						display_sudo(result)

	return result


def start_game():
	print("Let's start the Sudoku Game...")
	time.sleep(2)
	sudo_sample = create_sudoku()
	print("Please Solve this Sudoku...")
	time.sleep(1)
	print("Coming in few seconds..")
	time.sleep(3)
	os.system('cls')
	display_sudo(sudo_sample)
	print()
	time.sleep(1)
	print("Let's start solving the sudoku")
	check = True
	while check:
		sudo_sample = solve_game(sudo_sample)
		check = zeroAvailable(sudo_sample)
	time.sleep(1)
	os.system('cls')
	print("Your Final Solved sudoku is coming in few seconds.. ")
	time.sleep(2)
	display_sudo(sudo_sample)


if __name__ == '__main__':
	start_game()