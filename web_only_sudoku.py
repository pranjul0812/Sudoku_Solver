from selenium import webdriver
import time
from selenium.webdriver.common.by import By


class WebSudoku:
	cells = "//tr//td"
	startbtn = "//div[contains(text(), 'Start Sudoku')]"

	def __init__(self, driver):
		self.driver = driver
		self.driver.maximize_window()
		self.driver.implicitly_wait(3)
		url = "https://en.sudoku-online.net/sudoku-easy/"
		self.driver.get(url)
		self.driver.execute_script('window.scrollBy(0, 300);')
		self.driver.find_element(By.XPATH, self.startbtn).click()

	def create(self):
		# get the values available in the sudoku in a list(1-D)
		cells_elements = self.driver.find_elements(By.XPATH, self.cells)
		values = []
		count = 0
		for cell in cells_elements:
			try:
				values.append(int(cell.text))
			except:
				count+=1
				values.append(0)
		return values, cells_elements, count

	def getCol(self, index, values):
		j = index%9
		data = []
		while j < 81:
			data.append(values[j])
			j+=9
		return data

	def getRow(self, index, values):
		start = 9*(index//9)
		data = []
		for i in range(start, start+9):
			data.append(values[i])
		return data

	def blocks(self, index, values):
		col = index%9
		row = index//9
		blocks = [[[0, 1, 2, 9, 10, 11, 18, 19, 20], [3, 4, 5, 12, 13, 14, 21, 22, 23], [6, 7, 8, 15, 16, 17, 24, 25, 26]],
				  [[27, 28, 29, 36, 37, 38, 45, 46, 47], [30, 31, 32, 39, 40, 41, 48, 49, 50], [33, 34, 35, 42, 43, 44, 51, 52, 53]],
				  [[54, 55, 56, 63, 64, 65, 72, 73, 74], [57, 58, 59, 66, 67, 68, 75, 76, 77], [60, 61, 62, 69, 70, 71, 78, 79, 80]]]
		i = row//3
		j = col//3
		data = []
		for i in blocks[i][j]:
			data.append(values[i])
		return data

	def checkOtherValues(self, sudo, index):
		expected_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
		found = 0
		# Check horizontal values
		data = self.getRow(index, sudo)
		for item in data:
			if item in expected_list:
				expected_list.remove(item)

		# check Vertical values
		data = self.getCol(index, sudo)
		for item in data:
			if item in expected_list:
				expected_list.remove(item)

		# check block values
		data = self.blocks(index, sudo)
		for item in data:
			if item in expected_list:
				expected_list.remove(item)

		if len(expected_list) == 1:
			found = expected_list[0]
			sudo[index] = found
		return found

	def solve_sudo(self, sudo, cells):
		count = 0
		fill = False
		for index in range(81):
			if sudo[index] == 0:
				found = self.checkOtherValues(sudo, index)
				if found != 0:
					fill = True
					cells[index].send_keys(str(found))
					count+=1
		return sudo, count, fill

	def game(self):
		sudo, cells, countOfZeroes = self.create()
		while countOfZeroes!=0:
			sudo, filled_count, fill = self.solve_sudo(sudo, cells)
			if not fill:
				break
			countOfZeroes -= filled_count
		time.sleep(2)
		self.driver.close()


driverLocation = "D:/Tools/Selenium/chromedriver.exe"
driver = webdriver.Chrome(executable_path=driverLocation)
web_sudo = WebSudoku(driver)
web_sudo.game()
