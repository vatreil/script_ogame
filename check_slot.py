
import pickle
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display

display = Display(visible=0, size=(800, 800))
display.start()

driver = webdriver.Chrome()
driver.set_window_size(800, 800)


#AUTH
def getUrlAuth():
    try:
        driver.get("https://lobby.ogame.gameforge.com/fr_FR/")
        sleep(1)
        return True;
    except Exception as e:
        print(e)
        return False

def ogameAuth():
    try:
        print("load cookie")
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        sleep(1)
        return True
    except:
        print("erreur load cookie")
        sleep(30) # A REFAIRE POUR Généré le cookie plus proprement (auth fb)
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
        print("load cookie")
        return True


#LINK
def getLinkAccount():
    try:
        driver.get("https://lobby.ogame.gameforge.com/fr_FR/accounts")
        sleep(1)
        return True;
    except Exception as e:
        print(e)
        return False


def goToGalaxie():
    try:
        driver.get("https://s191-fr.ogame.gameforge.com/game/index.php?page=ingame&component=galaxy")
        sleep(1)
        return True
    except Exception as e:
        print(e)
        return False

def goToServer():
    body_server = driver.find_elements(By.CLASS_NAME, "rt-tbody")
    for servers in body_server:
        for server in servers.find_elements(By.CLASS_NAME, "rt-tr-group"):
            if (server.text == "Mathilde"):
                server.click()
                btn_play_mathilde = server.find_element(By.CLASS_NAME, "btn-primary")
                btn_play_mathilde.click()
                sleep(1)


def checkSlot(galaxie, systeme):
	sleep(1)
	driver.find_element(By.ID, "galaxy_input").send_keys(galaxie)
	driver.find_element(By.ID, "system_input").send_keys(systeme)
	galaxyHeader = driver.find_element(By.ID, "galaxyHeader")
	sleep(1)
	galaxyHeader.find_elements(By.CLASS_NAME, "btn_blue")[0].click()
	sleep(2)
	body = {}
	for i in "galaxyRow6", "galaxyRow7", "galaxyRow8", "galaxyRow9":
		print(driver.find_element(By.ID, i).find_element(By.CLASS_NAME, "cellPlanet").text)
		slot = driver.find_element(By.ID, i).find_element(By.CLASS_NAME, "cellPlanet")
		try:
			slot.find_element(By.CLASS_NAME, "microplanet")
			body[i] = str(galaxie) + ":" + str(systeme)
		except:
			continue

	print(body)

getUrlAuth()
ogameAuth()
getLinkAccount()
goToServer()
goToGalaxie()
checkSlot(2, 203)