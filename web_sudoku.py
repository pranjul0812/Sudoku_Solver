from selenium import webdriver
import time



class WebSudoku:
	driverLocation = "D:/Tools/Selenium/chromedriver.exe"
	driver = webdriver.Chrome(executable_path=driverLocation)
	driver.maximize_window()
	driver.implicitly_wait(3)
	url = "https://www.websudoku.com/"
	driver.get(url)
	driver.maximize_window()
	driver.implicitly_wait(3)
	time.sleep(3)

	# elements locator
	webtable = "//table[@id='puzzle_grid']/tbody"
	rows = "//table[@id='puzzle_grid']/tbody//tr"  # 9 rows
	cells = "//table[@id='puzzle_grid']/tbody//tr//td"  # 81 cells

	# create 81 cells array