import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

'''Steps We Will Follow:-
1. We will read an incomplete sudoku from a website.
2. Create a function for  displaying the sudoku from a website.
3. Start solving sudoku and when found a cell to be filled with appropriate number, display the updated sudoku.
4. Once solved display the final sudoku.'''


# To display sudoku
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


# read sudoku from web and return in the form of list.(fill 0 on all the empty cells)
def create_sudoku():
	sudo = [[[[0 for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]
	driverLocation = "D:/Tools/Selenium/chromedriver.exe"
	driver = webdriver.Chrome(executable_path=driverLocation)
	driver.maximize_window()
	driver.implicitly_wait(3)
	url = "https://www.websudoku.com/"
	driver.get(url)
	driver.switch_to.frame(0)
	cells_elements = driver.find_elements(By.XPATH, "//table[@id='puzzle_grid']//tr//td//input")
	values = []
	for cell in cells_elements:
		try:
			values.append(int(cell.get_attribute('value')))
		except:
			values.append(0)
	index = 0
	for i in range(3):
		for k in range(3):
			for j in range(3):
				for l in range(3):
					if sudo[i][j][k][l] != values[index]:
						sudo[i][j][k][l] = values[index]
					index += 1

	return sudo


# Check if sudoku has any cell with zero >> used to continue/stop solving the sudoku
def zeroAvailable(lst):
	for i in range(3):
		for k in range(3):
			for j in range(3):
				for l in range(3):
					if lst[i][j][k][l] == 0:
						return True
	return False


# Check if sudoku has any cell with zero within a block(considering 3*3 a block) >> used in level2 solution
def zeroAvailableInBlock(lst, i, j):
	for k in range(3):
		for l in range(3):
			if lst[i][j][k][l] == 0:
				return True
	return False


# for each cell check other values(horizontal/vertical/in the block)
# Check if there can be only one solution(number) for that cell seeing above values
# Used as a level1 solution
def checkOtherValues(sudo_sample2, i, j, k, l):
	expected_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
	found = 0
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
		found = expected_list[0]

	return sudo_sample2, found


# In a block(3*3) check how many numbers are missing from 1-9 and which cells are empty
# now check each number at each empty cells
# If there is any number which is possible only at one empty place in that block, update the sudoku
# Level2 solution
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


# Used in level2 solution
# Called by function checkBlock
# for a particular cell in a block check if that number can be filled in that cell or not
# Check if that number exist in that column or row
# if Yes return False else return True.
def checkPossibility(lst, i, j, position, item):
	k = position[0]
	l = position[1]
	# check in vertical values:
	for o_row in range(3):
		for i_row in range(3):
			# print(lst[o_row][j][i_row][l], end=" ")
			if lst[o_row][j][i_row][l] == item:
				return False

	# check in horizontal values:
	for o_col in range(3):
		for i_col in range(3):
			# print(lst[i][o_col][k][i_col], end=" ")
			if lst[i][o_col][k][i_col] == item:
				return False

	return True


# Level2 Solution
# To iterate over each block
# It is called when sudoku can't be solved after level1 solution
def solve_game_level2(sudo_sample):
	# go in each block and check if we can fill any values
	change = False
	fill = False
	for i in range(3):
		for j in range(3):
			if zeroAvailableInBlock(sudo_sample, i, j):
				sudo_sample, change = checkBlock(sudo_sample, i, j)
			if change:
				fill = True
				os.system('cls')
				display_sudo(sudo_sample)
	return sudo_sample, fill


# Level1 Solution, it iterates over each cell and try to solve sudoku
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
					if found != 0:
						fill = True
						os.system('cls')
						display_sudo(result)

	return result, fill


# start solving the sudoku and provide the final result
def start_game(sudo_sample):
	check = True
	while check:
		sudo_sample, fill = solve_game_level1(sudo_sample)
		if not fill:
			check = False
		else:
			check = zeroAvailable(sudo_sample)
	if zeroAvailable(sudo_sample):
		os.system('cls')
		print("Your Level1 Solved sudoku is.. ")
		time.sleep(.5)
		display_sudo(sudo_sample)
		time.sleep(1)
	while zeroAvailable(sudo_sample):
		sudo_sample, fill = solve_game_level2(sudo_sample)
		if not fill:
			break

	time.sleep(1)
	os.system('cls')
	print("Your Final Solved sudoku is.. ")
	time.sleep(.5)
	display_sudo(sudo_sample)


if __name__ == '__main__':
	print("Let's start the Sudoku Game...")
	time.sleep(.5)
	print("Coming in few seconds..")
	sudo_sample = create_sudoku()
	print("Please Solve this Sudoku...")
	time.sleep(.5)
	os.system('cls')
	display_sudo(sudo_sample)
	print()
	time.sleep(1)
	print("Let's start solving the sudoku")
	start_game(sudo_sample)


