# This is a sample Python script.
import math
import os
import pickle
import time
from time import sleep

from crontab import CronTab
# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


driver = webdriver.Chrome()
driver.set_window_size(1000, 1200)

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

def goToServer():
    body_server = driver.find_elements(By.CLASS_NAME, "rt-tbody")
    for servers in body_server:
        for server in servers.find_elements(By.CLASS_NAME, "rt-tr-group"):
            if (server.text == "Mathilde"):
                server.click()
                btn_play_mathilde = server.find_element(By.CLASS_NAME, "btn-primary")
                btn_play_mathilde.click()
                sleep(1)

def goToOverview():
    try:
        driver.get("https://s191-fr.ogame.gameforge.com/game/index.php?page=ingame&component=overview")
        sleep(1)
        return True
    except Exception as e:
        print(e)
        return False

def goToFleetDispatch():
    try:
        driver.get("https://s191-fr.ogame.gameforge.com/game/index.php?page=ingame&component=fleetdispatch")
        sleep(1)
        return True
    except Exception as e:
        print(e)
        return False

def goToShipyard():
    try:
        driver.get("https://s191-fr.ogame.gameforge.com/game/index.php?page=ingame&component=shipyard")
        sleep(1)
        return True
    except Exception as e:
        print(e)
        return False

def goToMovement():
    try:
        driver.get("https://s191-fr.ogame.gameforge.com/game/index.php?page=ingame&component=movement")
        sleep(1)
        return True
    except Exception as e:
        print(e)
        return False

#PLANET
def getAllPlanet():
    planetList = driver.find_elements(By.ID, "planetList")
    OutputplanetList = []

    for planets in planetList:
        for planet in planets.find_elements(By.CLASS_NAME, "smallplanet"):
            value = {}
            value["name"] = planet.find_element(By.CLASS_NAME, "planet-name").text
            value["koords"] = planet.find_element(By.CLASS_NAME, "planet-koords").text[1: -1]
            OutputplanetList.append(value)
    return OutputplanetList

def getPlanet(planet_name):
    planetList = driver.find_elements(By.ID, "planetList")
    Outputplanet= {}

    for planets in planetList:
        for planet in planets.find_elements(By.CLASS_NAME, "smallplanet"):
            if planet_name == planet.find_element(By.CLASS_NAME, "planet-name").text:
                Outputplanet["name"] = planet.find_element(By.CLASS_NAME, "planet-name").text
                Outputplanet["koords"] = planet.find_element(By.CLASS_NAME, "planet-koords").text[1: -1]
    return Outputplanet

def goToPlanet(planet_name):
    planetList = driver.find_elements(By.ID, "planetList")

    for planets in planetList:
        for planet in planets.find_elements(By.CLASS_NAME, "smallplanet"):
            if planet_name == planet.find_element(By.CLASS_NAME, "planet-name").text:
                planet.find_element(By.CLASS_NAME, "planetlink").click()
                sleep(1)
                return True

def goToLune(planet_name):
    planetList = driver.find_elements(By.ID, "planetList")

    for planets in planetList:
        for planet in planets.find_elements(By.CLASS_NAME, "smallplanet"):
            if planet_name == planet.find_element(By.CLASS_NAME, "planet-name").text:
                planet.find_element(By.CLASS_NAME, "moonlink").click()
                sleep(1)
                return True

#RESSOURCE
def getAllRessources():
    ressources = {}
    list_ressources = ["metal", "crystal", "deuterium"]
    for ressource in list_ressources:
        if driver.find_element(By.CLASS_NAME, ressource).text[-1::] == "M":
            list_nb = driver.find_element(By.CLASS_NAME, ressource).text[0: -1].split(",")
            million = list_nb[0]
            millier  = list_nb[1] + "000000"[0: -len(list_nb[1])]
            ressources[ressource] = int(million+millier)
        else:
            list_nb = driver.find_element(By.CLASS_NAME, ressource).text.split(".")
            millier = list_nb[0]
            nb  = list_nb[1] + "000"[0: -len(list_nb[1])]
            ressources[ressource] = int(millier+nb)
    return ressources

def getTotalRessourceInPlanet():
    ressources_total = {}
    for planet in getAllPlanet():
        goToPlanet(planet.get("name"))
        goToOverview()
        ressources = getAllRessources()
        ressources_total["metal"] = ressources_total["metal"] + ressources["metal"]
        ressources_total["crystal"] = ressources_total["crystal"] + ressources["crystal"]
        ressources_total["deuterium"] = ressources_total["deuterium"] + ressources["deuterium"]
    return ressources_total

#FLOAT
def getAllFloatCivil():
    goToFleetDispatch()
    float_name_list = ["transporterLarge", "transporterSmall", "recycler", "espionageProbe"]
    float_list = {}

    for float in float_name_list:
        try:
            driver.find_element(By.ID, "warning")
            float_list[float] = 0
        except:
            float_list[float] = int(driver.find_element(By.CLASS_NAME, float).text.replace(".", ""))

    return float_list

def getFloatCivil(float):
    goToFleetDispatch()
    float_list = {}
    try:
        driver.find_element(By.ID, "warning")
        float_list[float] = 0
    except:
        float_list[float] = int(driver.find_element(By.CLASS_NAME, float).text.replace(".", ""))
    return float_list


#FRET
def updateNbAllFret():
    goToShipyard()
    float_list = {}
    float_name_list = ["transporterLarge", "transporterSmall", "recycler", "espionageProbe"]
    for float in float_name_list:
        driver.find_element(By.CLASS_NAME, float).click()
        sleep(0.5)
        driver.find_element(By.CLASS_NAME, "details").click()
        sleep(0.5)
        float_list[float] = int(driver.find_element(By.CLASS_NAME, "cargo_capacity").find_element(By.CLASS_NAME, "tooltipHTML").text.replace(".", ""))
    return float_list

def updateNbFret(float):
    goToShipyard()
    driver.find_element(By.CLASS_NAME, float).click()
    sleep(0.5)
    driver.find_element(By.CLASS_NAME, "details").click()
    sleep(0.5)
    return int(driver.find_element(By.CLASS_NAME, "cargo_capacity").find_element(By.CLASS_NAME, "tooltipHTML").text.replace(".", ""))

def getNbGtForTotalRessource(float):
    fret = updateNbFret(float)
    ressouce = getAllRessources()
    return math.ceil((ressouce["metal"] + ressouce["crystal"] + ressouce["deuterium"]) / fret)

def sendAllRessource(dest, float):
    try:
        nbgt = getNbGtForTotalRessource(float)
        goToFleetDispatch()
        driver.find_element(By.NAME, float).send_keys(nbgt)
        driver.find_element(By.CLASS_NAME, "colonyShip").click()
        button = driver.find_element(By.ID, "continueToFleet2")
        ActionChains(driver).move_to_element(button)
        sleep(1)
        button.click()
        sleep(1)
        koords = getPlanet(dest).get("koords").split(":")
        driver.find_element(By.ID, "galaxy").send_keys(koords[0])
        driver.find_element(By.ID, "system").send_keys(koords[1])
        driver.find_element(By.ID, "position").send_keys(koords[2])
        button = driver.find_element(By.ID, "button3")
        ActionChains(driver).move_to_element(button)
        sleep(1)
        button.click()
        sleep(1)
        driver.find_element(By.ID, "selectMaxMetal").click()
        driver.find_element(By.ID, "selectMaxCrystal").click()
        driver.find_element(By.ID, "selectMaxDeuterium").click()
        driver.find_element(By.ID, "sendFleet").click()
        sleep(1)
        return True
    except:
        return False

def sendExp(planet, floats):
    goToLune(planet)
    goToFleetDispatch()
    floats = {
        'transporterLarge':
        {
            "nb": 2000,
            "Obligatory": True,
        },
        'transporterSmall':
        {
            "nb": 200,
            "Obligatory": False,
        },
        'espionageProbe':
        {
        'nb': 1,
        'Obligatory': True,
        }     ,
        'explorer':
        {
        'nb': 50,
        'Obligatory': False,
        },
        'reaper':
        {
        'nb': 50,
        'Obligatory': False,
        }
    }
    #gonogo pour le bouton suivant fin des envoie expé
    go_nogo = True
    nb_exp = 0
    while(go_nogo):
        for key, value in floats.items():
            float_selecter = driver.find_element(By.CLASS_NAME, key)
            float = int(float_selecter.find_element(By.CLASS_NAME, "amount").text.replace(".", ""))

            if not (float - value.get("nb") > 0 or not bool(value.get("Obligatory"))):
                go_nogo = False
            elif float == 0:
                continue
            else:
                float_selecter.find_element(By.NAME, key).send_keys(value.get("nb"))


        exp_in_progress = driver.find_element(By.ID, "slots").find_elements(By.CLASS_NAME, "fleft")[1].text.split(":")[1].split("/")
        if int(exp_in_progress[0] < exp_in_progress[1]):
            if go_nogo:
                driver.find_element(By.CLASS_NAME, "colonyShip").click()
                button = driver.find_element(By.ID, "continueToFleet2")
                ActionChains(driver).move_to_element(button)
                sleep(1)
                button.click()
                sleep(1)

                driver.find_element(By.ID, "position").send_keys(16)
                button = driver.find_element(By.ID, "button15")
                ActionChains(driver).move_to_element(button)
                sleep(1)
                button.click()
                sleep(1)
                driver.find_element(By.ID, "sendFleet").click()
                sleep(1)
                nb_exp = nb_exp + 1
    return nb_exp

def getExpInProgress():
    goToMovement()
    fleetDetails = driver.find_elements(By.XPATH, '//div[@data-mission-type="15"]')
    cron = []
    for fleetDetail in fleetDetails:
        timer = fleetDetail.find_element(By.CLASS_NAME, "nextabsTime").text.split(":")
        cron.append(str(int(timer[1])) + " " + timer[0] + " * * *")
    return cron

def addCronTab(crontab):
    os.system("echo \"\" > /var/spool/cron/crontabs/waggo")
    for cron in crontab:
        for compare in crontab:
            if cron == compare:
                crontab.remove(cron)
    for cron in crontab:
        os.system("echo \"" + str(cron) + " python3.9 " + os.getcwd() + "/main.py\"" + " > /var/spool/cron/crontabs/waggo")
    return crontab

getUrlAuth()
ogameAuth()
getLinkAccount()
goToServer()
goToOverview()
print("nb_exp", sendExp('Ood', {}))
print(addCronTab(getExpInProgress()))
print(getAllPlanet())


"""for planet in getAllPlanet():
    if (planet.get("name") != 'Alie'):
        print("got to=", planet.get("name"))
        goToPlanet(planet.get("name"))
        goToOverview()
        print(getAllFloatCivil())

        bool = False
        while(not bool):
            bool = sendAllRessource("Alie", "transporterLarge")
            if(not bool):
                sleep(300)"""




sleep(1)
driver.quit()

"""
import os
from selenium import webdriver
from pyvirtualdisplay import Display
display = Display(visible=0, size=(800, 600))
display.start()
driver = webdriver.Chrome()
driver.get("http://www.google.com")
print(driver.page_source.encode('utf-8'))
driver.quit()
display.stop()"""

