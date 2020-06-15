from selenium import webdriver
import time
from Phase2_prac.sudoku import sudoku_prac as sp
from selenium.webdriver.common.by import By


class WebSudoku:
	# elements locator
	# webtable = "//table[@id='puzzle_grid']"
	# rows = "//table[@id='puzzle_grid']//tr"  # 9 rows
	cells = "//table[@id='puzzle_grid']//tr//td//input"  # 81 cells
	verify = "//input[@name='submit']"

	def __init__(self, driver):
		self.driver = driver
		self.driver.maximize_window()
		self.driver.implicitly_wait(3)
		url = "https://www.websudoku.com/"
		self.driver.get(url)

	def create(self):
		# create 81 cells array
		sudo = [[[[0 for i in range(3)] for i in range(3)] for i in range(3)] for i in range(3)]

		# get the values available in the sudoku
		self.driver.switch_to.frame(0)
		cells_elements = self.driver.find_elements(By.XPATH, self.cells)
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
						if sudo[i][j][k][l]!= values[index]:
							sudo[i][j][k][l] = values[index]
						index +=1
		return sudo, cells_elements

	def solve_sudo(self, sudo, cells):
		found = False
		fill = False
		index = 0
		for i in range(3):
			for k in range(3):
				for j in range(3):
					for l in range(3):
						if sudo[i][j][k][l] == 0:
							sudo, found = sp.checkOtherValues(sudo, i, j, k, l)
						if found != 0:
							fill = True
							cells[index].send_keys(str(found))
						index += 1

		return sudo, fill

	def game(self):
		sudo, cells = self.create()
		while sp.zeroAvailable(sudo):
			sudo, fill = self.solve_sudo(sudo, cells)
			if not fill:
				break
			time.sleep(2)
		self.driver.find_element(By.XPATH, self.verify).click()
		sp.display_sudo(sudo)


driverLocation = "D:/Tools/Selenium/chromedriver.exe"
driver = webdriver.Chrome(executable_path=driverLocation)
web_sudo = WebSudoku(driver)
web_sudo.game()
