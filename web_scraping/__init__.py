from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def extract_html(url,xpath_element_position,path_html,wait_second):
	driver = webdriver.Chrome()
	driver.get(url)
	position = driver.find_elements(By.XPATH, xpath_element_position)
	original_window = driver.current_window_handle
	wait = WebDriverWait(driver,wait_second)
	
	for element in position:
		# Perform actions on each element
		print(element.text)
		element.click()
		wait.until(EC.number_of_windows_to_be(2))
		# element.send_keys("some

		for window_handle in driver.window_handles:
			if window_handle != original_window:
				driver.switch_to.window(window_handle)
				break

		driver.quit()



