#Developer: Bryan Lor
#Date: 12/1/2020
#Program: A Modular Program that will constantly refresh websites and notify/buy the item if available
# ---------------------------------------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from threading import Thread
import time, os, winsound


#Global Variables ---------------------------------------
ProgramName = "PurchaseBot"
ProgramVersion = "v0.9"

#Settings ----------
SettingsDict = {
    "DEBUGGING": False,
    "LoadPersonalChromeAccount": False,
    "LoadBotChromeAccount": True,
    "WaitUntilReady": False,
    "HideDuringRun": False,
    "CheckOut": True,
    "ProceedToOrder": True,
    "FillOutInfo": True,
    "ConfirmOrder": False,
    "CustomSounds": False,
    "DisableSounds": False,
    }

#Text Attributes ----------
class color:
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"
   
#Paths ----------
DRIVERPATH = os.getcwd() + "\chromedriver"
CHROMEPATH = "C:\\Users\\<NAME>\AppData\\Local\\Google\\Chrome\\User Data"

#Sounds ----------
INITIALALERT_SFX = "sfx\InitialAlert.wav"
ALERT_SFX = "sfx\Alert.wav"
NOTIFICATION_SFX = "sfx\\Notification.wav"
ERROR_SFX = "sfx\\Error.wav"

#################### PRINT FUNCTIONS ###################       
#-------------------------------------------------------
def printProgramName():
    print(color.BOLD + color.BLUE + ProgramName + " " + ProgramVersion + color.END + " - Created by " + color.UNDERLINE + "Bryan Lor" + color.END)
    print("Currently In Early Beta")
    print("\n" * 2)
    
#-------------------------------------------------------
def printAlert(string, character = "!", defaultSpacing = 2):
    print(("\n" * defaultSpacing) + (str(character) * 64 + "\n") * 2)
    print(str(string))
    print(("\n" * 1) + (str(character) * 64 + "\n") * 2)

#-------------------------------------------------------
def playSound(Name, playASYNC = True):
    if SettingsDict.get("DisableSounds") == True : return None
    playDefault = False
    if SettingsDict.get("CustomSounds") == True:
        try:
            if playASYNC == True : winsound.PlaySound(str(Name), winsound.SND_ASYNC) #No Wait Till Sound Finish
            else: winsound.PlaySound(str(Name), winsound.SND_ALIAS) #Wait Till Sound Finish
        except: playDefault = True
    else: playDefault = True
    if playDefault == True : winsound.PlaySound("!", winsound.SND_ASYNC)
    
#-------------------------------------------------------  
def promptQuit():
    inputVal = input("Press " + color.UNDERLINE + color.YELLOW+ "Enter" + color.END + " To Quit")
    quit()
    
################## GENERAL FUNCTIONS ##################        
#-------------------------------------------------------   
def loadSettings():
    giveError = False
    try:
        with open("Settings.txt", "r") as f:
            count = 0
            for line in f: 
                splitLine = line.split()
                if "true" in str(splitLine[1:]).lower() : value = True
                elif "false" in str(splitLine[1:]).lower() : value = False
                try:
                    SettingsDict[list(SettingsDict)[count]] = value
                    count += 1
                except: giveError = True
            f.close()
    except:
        os.system("CLS")
        printProgramName()
        playSound(ERROR_SFX)
        print(color.BOLD + color.RED + "Error:" + color.END + color.RED + " Could Not Find/Read " + color.END + color.YELLOW + "'Settings.txt'" + color.END + color.RED + " File.\nPlease Make Sure It Exists And Is Formatted properly\n" + color.END)
        promptQuit()
    if giveError == True:
        os.system("CLS")
        printProgramName()
        playSound(ERROR_SFX)
        print(color.BOLD + color.RED + "Error:" + color.END + color.RED + " In Order To Proceed \nPlease Remove All Unidentified Text In The " + color.END + color.YELLOW + "'Settings.txt'\n" + color.END)
        print("-Unknown Definition ''" + color.RED + line + color.END + "'' at Line " + str(count) + ", in " + color.YELLOW + ProgramName + "\Settings.txt" + color.END + "\n")
        promptQuit()
            
#-------------------------------------------------------
def setUpProgram(websiteList):
    print("Setting Up The Website(s)...")
    print("Please " + color.YELLOW + "Wait A Moment" + color.END + ",")
    print("\n" * 10)
    try: readWebsites(websiteList)
    except:
        os.system("CLS")
        printProgramName()
        playSound(ERROR_SFX)
        print(color.BOLD + color.RED + "ERROR:" + color.END + color.RED + " Your 'Websites.txt' is missing!\n" + color.END)
        promptQuit()
    try:
        options = webdriver.ChromeOptions()
        if SettingsDict.get("LoadPersonalChromeAccount") == True : options.add_argument("user-data-dir=" + str(CHROMEPATH))
        elif SettingsDict.get("LoadBotChromeAccount") == True : options.add_argument("user-data-dir=" + str(CHROMEPATH) + ProgramName + " Profile")
##        if SettingsDict.get("HideDuringRun") == True : options.headless = True
        driver = webdriver.Chrome(executable_path=DRIVERPATH, options=options)
        driver.set_window_position(-100000, 0)
    except:
        os.system("CLS")
        printProgramName()
        playSound(ERROR_SFX)
        if SettingsDict.get("LoadPersonalChromeAccount") == True : print(color.BOLD + color.RED + "ERROR:" + color.END + color.RED + " Could Not Properly Load Your " + color.END + color.YELLOW + "<user-data-dir>" + color.END + color.RED + " Chrome Profile\n" + color.END)
        elif SettingsDict.get("LoadBotChromeAccount") == True : print(color.BOLD + color.RED + "ERROR:" + color.END + color.RED + " Could Not Properly Load " + color.END + color.BLUE + ProgramName + color.END + color.YELLOW + "<user-data-dir>" + color.END + color.RED + " Chrome Profile\n" + color.END)
        if SettingsDict.get("LoadPersonalChromeAccount") == True: print("Please make sure all browsers are " + color.BOLD + "CLOSED!" + color.END + "\n")
        else: print("Please make sure all browsers ran by " + color.BLUE + ProgramName + color.END + " is " + color.BOLD + "CLOSED!" + color.END + "\n")
        promptQuit()
    try: openWebsites(websiteList, driver)
    except:
        os.system("CLS")
        printProgramName()
        playSound(ERROR_SFX)
        print(color.BOLD + color.RED + "ERROR:" + color.END + color.RED + " Something went wrong while opening websites!\n" + color.END)
        promptQuit()
    return driver
    
#-------------------------------------------------------
def readWebsites(websiteList):
    f = open("Websites.txt", "r")
    Lines = f.readlines() 
    for line in Lines:
        websiteLink = cleanUpString(line, isWebsite = True)
        websiteList.append(websiteLink)
    f.close()
    
#-------------------------------------------------------
def openWebsites(websiteList, driver):
    for link in websiteList:
        driver.get(link)
        if len(websiteList) > 1 and websiteList.index(link) < (len(websiteList) - 1) : driver.execute_script('''window.open("''' + link + ''' ", "_blank");''')
    return True

#-------------------------------------------------------
def waitUntilReady(driver):
    driver.set_window_position(0, 0)
    os.system("CLS")
    printProgramName()
    playSound(NOTIFICATION_SFX)
    print(color.BOLD + color.YELLOW + ("!" * 25) + " Please Make Sure You Are Logged In On All Websites " + ("!" * 25) + color.END)
    print("Now Is a Good Time To Get Rid Of Any Queries or Cacha's That May Have Appeared")
    print("To disable this waiting feature, change the value of " + color.GREEN + "'WaitUntilReady'" + color.END+ " in the " + color.YELLOW+ "'Settings.txt'" + color.END)
    print("\n" * 2)    
    while True:
        time.sleep(2.75)
        inputVal = input("When You Are Ready, Press " + color.UNDERLINE + color.YELLOW + "Enter" + color.END)
        print("\n" * 10)
        return None


#-------------------------------------------------------
def loadWebsiteDataFile(driver):
    failCount = 0
    fileCount = 0
    for file in os.listdir(os.getcwd() + "\data"):
        fileName = os.path.splitext(file)[0]
        if str(fileName) in str(driver.current_url):
            if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " File '" + str(fileName) + "' Has Been Located")
            elementClassDict = loadWebsiteDataInfo(fileName)
            return elementClassDict
        elif str(fileName) not in str(driver.current_url) and fileName != "ExampleTemplateData" : failCount += 1
        fileCount += 1
    if failCount >= fileCount - 1:
        print("\n" + ("-" * 32) + color.BOLD + color.YELLOW + "\n*WARNING:" + color.END + color.YELLOW + " Could Not Find The .txt Data File For The Website:\n" + color.END + driver.current_url)
        print("\nMake Sure The File Exists And Is Properly Named In " + color.YELLOW + "'" + ProgramName + "\data'" + color.END)
        print(color.BLUE + ProgramName + color.END + color.YELLOW + " Will NOT Be Able To Recognize What To Do!!! The Page Will Be Ignored." + color.END + "\n" + ("-" * 32) + "\n")
        
#-------------------------------------------------------
def loadWebsiteDataInfo(websiteData):
    elementClassDict = {
        "AddToCartButton": "",
        "HasAddToCartPopUp": False,
        "AddToCartPopUpButtonClass": "",
        "PopUpCheckOutButton": "",
        "CheckOutButton": "",
        "ShoppingCartURL": "",
        "OrderFormURL": "",
        "OrderButtonClass": "",
        "CanFillInfo": False,
        "FirstNameInput": "",
        "LastNameInput": "",
        "EmailInput": "",
        "CreditCardInput": "",
        "CreditCardExpireMonth": "",
        "CreditCardExpireYear": "",
        "CreditCardCVV": "",
        "PhoneNumberInput": "",
        "StreetAddressInput": "",
        "CityInput": "",
        "ZipCodeInput": "",
        "SelectCountry": "",
        "SelectState": "",
        "ConfirmOrderButton": ""
        }

    giveError = False
    try:
        with open("data\\" + str(websiteData) + ".txt", "r") as f:
            count = 0
            for line in f:
                splitLine = line.split(" ", 1)
                if "https://" in splitLine[1:] : value = cleanUpString(str(splitLine[1:]), isWebsite = True)
                else: value = cleanUpString(str(splitLine[1:]))
                try: #Bool Data ----------
                    if "true" in value.lower() :
                        elementClassDict[list(elementClassDict)[count]] = True
                        giveError = False
                        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " elementClassDict Bool Data Convertion Success")
                        count += 1
                        continue
                    if "false" in value.lower() :
                        elementClassDict[list(elementClassDict)[count]] = False
                        giveError = False
                        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " elementClassDict Bool Data Convertion Success")
                        count += 1
                        continue
                except: giveError = True
                try: #String Data ----------
                    elementClassDict[list(elementClassDict)[count]] = value
                    giveError = False
                    if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " elementClassDict String Data Convertion Success")
                    count += 1
                    continue
                except:
                    if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " elementClassDict String Data Convertion Failure")
                    giveError = True
            f.close()
    except: giveError = True
    if giveError == True:
        playSound(ERROR_SFX)
        print(("\n" * 2) + color.BOLD + color.YELLOW + "*Warning:" + color.END + color.YELLOW + " Failed To Open/Read '" + color.END + color.GREEN + websiteData +
              color.END + color.YELLOW + "' txt File In The Directory, '" + color.END + color.GREEN + ProgramName + "\data' \n" + color.END)
        print("The Website '" + color.GREEN + websiteData.capitalize().replace(".com", "") + color.END+ "' Will Not Work Properly. Please Check Your " + color.YELLOW + "'" + websiteData + "'" + color.END + " File")
    return elementClassDict

#-------------------------------------------------------
def readPI():
    piDict = {
        "FirstName": "",
        "LastName": "",
        "Email": "",
        "PhoneNumber": "",
        "Country": "",
        "State": "",
        "City": "",
        "Street": "",
        "ZipCode": "",
        "CreditCardNumber": "",
        "CreditCardExpireMonth": "",
        "CreditCardExpireYear": "",
        "CreditCardCVV": "",
        }
    giveError = False
    try:
        with open("pi.txt", "r") as f:
            count = 0
            for line in f:
                splitLine = line.split(" ", 1)
                value = cleanUpString(str(splitLine[1:]))
                value = value.replace("'", "")
                try: #String Data
                    piDict[list(piDict)[count]] = value
                    giveError = False
                    if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " piDict String Data Convertion Success")
                    count += 1
                    continue
                except:
                    if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " piDict String Data Convertion Failure")
                    giveError = True
            f.close()
    except:
        giveError = True
    if giveError == True:
        playSound(ERROR_SFX)
        print(("\n" * 2) + color.BOLD + color.YELLOW + "*Warning:" + color.END + color.YELLOW + " Failed To Open/Read "
              + color.END + color.GREEN + "'pi.txt'" + color.END + color.YELLOW + " File In The Directory, " + color.END + color.YELLOW + "'" + ProgramName + "\data' \n" + color.END)
        print("Please Check If The File Exists And Is Formatted Properly!!!" + color.END)
    return piDict

#-------------------------------------------------------
def cleanUpString(string, isWebsite = False):
    if isWebsite == True : removeList = ["\\n", "\n", "'"]
    else: removeList = ["[", "\\n", "]", "\n"]
    for i in range(len(removeList)):
        string = string.replace(str(removeList[i]), "")
    return string

#-------------------------------------------------------
def foundItemAlert(driver):
    printAlert(color.BOLD + color.PURPLE + "An Item Has Been Found!" + color.END, "*")
    driver.set_window_position(0, 0)
    playSound(INITIALALERT_SFX)
    
#-------------------------------------------------------  
def clickElement(element):
    try: element.click()
    except: None
                
################### SEARCH FUNCTIONS ################### 
#-------------------------------------------------------   
def findElementByXPath(stringName, driver):
    try:
        element = driver.find_element_by_xpath(stringName)
        if element != None : return element
    except: return None

#-------------------------------------------------------   
##def findElementsByXPath(stringName, driver):
##    try:
##        element = driver.find_elements_by_xpath(stringName)
##        if element != None : return element
##    except: return None
    
#-------------------------------------------------------
def lookForButtonElement(elementType, elementClassDict, driver):
    try: elementClassName = str(elementClassDict.get(elementType))
    except: None
    try:
        element = findElementByXPath("//button[@class=" + elementClassName + " and not(@disabled)]", driver)
        if element != None : return element
    except: None

#-------------------------------------------------------
def lookForInputElementName(elementName, elementClassDict, driver):
    try: elementClassName = str(elementClassDict.get(elementName))
    except: None
    try:
        element = findElementByXPath("//input[@name=" + elementClassName + " and not(@disabled)]", driver)
        if element != None : return element
    except: None

#-------------------------------------------------------
def lookForSelectElementName(elementName, elementOption, elementClassDict, driver):
    try: elementClassName = str(elementClassDict.get(elementName))
    except: None
    try:
        element = findElementByXPath("//select[@name=" + elementClassName + " and not(@disabled)]/option[text()='" + elementOption + "'", driver)
        if element != None : return element
    except: None
    
#-------------------------------------------------------
def findAndClickElement(elementClassDictType,elementClassDict, driver, waitASec = False):
    if waitASec == True : driver.implicitly_wait(1)
    else: driver.implicitly_wait(0)
    element = lookForButtonElement(elementClassDictType, elementClassDict, driver)
    if element == None : element = lookForInputElementName(elementClassDictType, elementClassDict, driver)
    if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Looking For '" + str(elementClassDictType) + "' Element")
    if element != None:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Successfully Found '" + str(elementClassDictType) + "' Element Found")
        try:
            clickElement(element)
            if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Successfully Clicked On '" + str(elementClassDictType) + "' Element!")
            return elementClassDict
        except:
            if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Click On '" + str(elementClassDictType) + "' Element")
        try:
##            element.send_keys(elementClassDict.get(elementClassDictType))
            element.send_keys(Keys.RETURN)
        except:
            if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Send Keys To '" + str(elementClassDictType) + "' Element")
    else:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed Find '" + str(elementClassDictType) + "' Element")
    if waitASec == True: return False
    else: return None
    
##################### LOOP FUNCIONS ####################
#-------------------------------------------------------   
def alertLoop(string, waitTime = 0):
    if string != None : printAlert(string)
    time.sleep(waitTime)
    while True:
        playSound(ALERT_SFX, playASYNC = False)
        time.sleep(1.5)
        
#-------------------------------------------------------
def searchLoop(driver):
    while True:
        for i in driver.window_handles:
            elementClassDict = loadWebsiteDataFile(driver)
            foundItem = findAndClickElement("AddToCartButton", elementClassDict, driver)
            if foundItem != None: return elementClassDict
            driver.switch_to.window(i)
            driver.refresh()

#-------------------------------------------------------
def fillOutInfo(pInfo, elementClassDict, driver):
    firstNameInput = lookForInputElementName("FirstNameInput", elementClassDict, driver)
    lastNameInput = lookForInputElementName("LastNameInput", elementClassDict, driver)
    emailInput = lookForInputElementName("EmailInput", elementClassDict, driver)
    creditCardInput = lookForInputElementName("CreditCardInput", elementClassDict, driver)
    creditCardExpireMonthInput = lookForInputElementName("CreditCardExpireMonth", elementClassDict, driver)
    creditCardExpireYearInput = lookForInputElementName("CreditCardExpireYear", elementClassDict, driver)
    creditCardCVVInput = lookForInputElementName("CreditCardCVV", elementClassDict, driver)
    phoneNumberInput = lookForInputElementName("PhoneNumberInput", elementClassDict, driver)
    streetAddressinput = lookForInputElementName("StreetAddressInput", elementClassDict, driver)
    cityInput = lookForInputElementName("CityInput", elementClassDict, driver)
    zipCodeInput = lookForInputElementName("ZipCodeInput", elementClassDict, driver)
    selectCountry = lookForSelectElementName("SelectCountry", pInfo.get("Country"), elementClassDict, driver)
    selectState = lookForSelectElementName("SelectState", pInfo.get("State"), elementClassDict, driver)
    
    #FirstName Input----------
    try: firstNameInput.send_keys(pInfo.get("FirstName")), firstNameInput.send_keys(Keys.RETURN)
    except:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Find/Send Keys To 'FirstNameInput' Element")
        
    #LastName Input   ----------
    try: lastNameInput.send_keys(pInfo.get("LastName")), lastNameInput.send_keys(Keys.RETURN)
    except:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Find/Send Keys To 'LastNameInput' Element")
        
    #Email Input----------
    try: emailInput.send_keys(pInfo.get("Email")), emailInput.send_keys(Keys.RETURN)
    except:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Find/Send Keys To 'EmailInput' Element")
        
    #CreditCard Input----------
    try:  creditCardInput.send_keys(pInfo.get("CreditCardNumber")), creditCardInput.send_keys(Keys.RETURN)
    except:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Find/Send Keys To 'CreditCardInput' Element")
        
    #CreditCardExpireMonth Input----------
    try: creditCardExpireMonth.send_keys(pInfo.get("CreditCardExpireMonth")), creditCardExpireMonth.send_keys(Keys.RETURN)
    except:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Find/Send Keys To 'CreditCardExpireMonth' Element")
        
    #CreditCardExpireYear Input----------
    try: creditCardExpireYear.send_keys(pInfo.get("CreditCardExpireYear")), creditCardExpireYear.send_keys(Keys.RETURN)
    except:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Find/Send Keys To 'CreditCardExpireYear' Element")

    #CreditCardCVV Input----------
    try: creditCardCVVInput.send_keys(pInfo.get("CreditCardCVV")), creditCardCVVInput.send_keys(Keys.RETURN)
    except:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Find/Send Keys To 'CreditCardCVV' Element")

    #PhoneNumber Input ----------
    try: phoneNumberInput.send_keys(pInfo.get("PhoneNumber")), phoneNumberInput.send_keys(Keys.RETURN)
    except:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Find/Send Keys To 'PhoneNumberInput' Element")

    #StreetAddress Input ----------
    try:  streetAddressinput.send_keys(pInfo.get("Street")), streetAddressinput.send_keys(Keys.RETURN)
    except:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Find/Send Keys To 'StreetAddressInput' Element")

    #City Input  ----------
    try: cityInput.send_keys(pInfo.get("City")), cityInput.send_keys(Keys.RETURN)
    except:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Find/Send Keys To 'CityInput' Element")

    #ZipCode Input ----------
    try: zipCodeInput.send_keys(pInfo.get("ZipCode")), zipCodeInput.send_keys(Keys.RETURN)
    except:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Find/Send Keys To 'ZipCodeInput' Element")
        
    #SelectCountry Input ----------
    try: clickElement(selectCountry)
    except:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Find/Send Keys To 'SelectCountry' Element")
        
    #SelectState Input ----------
    try: clickElement(selectState)
    except:
        if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Find/Send Keys To 'SelectState' Element")

######################### MAIN ######################### 
#-------------------------------------------------------
def main():
    websiteList = []
    
    #Start Program ----------
    os.system("CLS")
    printProgramName()
    loadSettings()
    time.sleep(0.1)
    driver = setUpProgram(websiteList)
    if SettingsDict.get("DEBUGGING") == False: os.system("CLS")
    printProgramName()

    #Wait Until Ready ----------
    if SettingsDict.get("WaitUntilReady") == True and SettingsDict.get("DEBUGGING") == False : waitUntilReady(driver)
    elif SettingsDict.get("WaitUntilReady") == True and SettingsDict.get("DEBUGGING") == True :
        print("\n" + ("-" * 32) + color.BOLD + color.YELLOW + "\n*WARNING: " + color.END + color.GREEN + "'DebugMode'" +
              color.END + color.YELLOW + " Is Enabled, " + color.END + color.GREEN + "'WaitUntilReady'" + color.END + color.YELLOW
              + " Will Be Ignored" + color.END + "\n" + ("-" * 32) + "\n")

    #Main Search Loop ----------
    if SettingsDict.get("DEBUGGING") == False: os.system("CLS"), printProgramName()
    print(color.GREEN + "Search In Progress..." + color.END)
    if SettingsDict.get("HideDuringRun") == True : driver.set_window_position(-100000, 0)
    else: driver.set_window_position(0,0)
##    if SettingsDict.get("HideDuringRun") == True :
##        currentURL = driver.current_url
##        driver.quit()
##        options = webdriver.ChromeOptions()
##        if SettingsDict.get("LoadPersonalChromeAccount") == True : options.add_argument("user-data-dir=" + str(CHROMEPATH))
##        elif SettingsDict.get("LoadBotChromeAccount") == True : options.add_argument("user-data-dir=" + str(CHROMEPATH) + ProgramName + " Profile")
##        options.headless = True
##        driver = webdriver.Chrome(executable_path=DRIVERPATH, options=options)
##        driver.get(currentURL)
        
    elementClassDict = searchLoop(driver)

    #Found Item Alert ----------
    threadA = Thread(target = foundItemAlert(driver))
    threadA.start()
    
    #Attempt To Proceed To Checkout ----------
    if SettingsDict.get("CheckOut") and elementClassDict.get("HasAddToCartPopUp") :
        try:
            findAndClickElement("AddToCartPopUpButtonClass", elementClassDict, driver, waitASec = True)
            isSuccessful = findAndClickElement("PopUpCheckOutButton", elementClassDict, driver)
            if isSuccesful == False:
                isSuccessful = findAndClickElement("CheckOutButton", elementClassDict, driver)
        except: isSuccessful = False
        if isSuccessful == False:
            try:
                driver.get(str(elementClassDict.get("ShoppingCartURL"))[1:-1])
                if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Check Out via Button, Manually Heading To Url Instead")
            except:
                if SettingsDict.get("DEBUGGING") == False: os.system("CLS")
                if SettingsDict.get("DEBUGGING") == False: printProgramName()
                threadB = Thread(target = alertLoop(color.BOLD + color.GREEN +"An Item Is In Stock!," + color.END + " But " + color.RED + "Failed" + color.END + " To Proceed To " + color.YELLOW + "'CheckOut' Form" + color.END, 3))
                threadB.start()

    #Attempt To Proceed To Order ----------
    if SettingsDict.get("ProceedToOrder") == True : isSuccessful = findAndClickElement("OrderButtonClass", elementClassDict, driver, waitASec = True)
    else:
        threadB = Thread(target = alertLoop("An Item Is In Stock!", 4.5))
        threadB.start()    
    if isSuccessful == False :
        try:
            driver.get(str(elementClassDict.get("OrderFormURL"))[1:-1])
            if SettingsDict.get("DEBUGGING") == True : print(color.BOLD + color.YELLOW + "DEBUG:" + color.END + " Failed To Proceed To Order Form, Manually Heading To Url Instead")
        except:
            if SettingsDict.get("DEBUGGING") == False: os.system("CLS"), printProgramName()
            threadB = Thread(target = alertLoop(color.BOLD + color.GREEN + "An Item Is In Stock!," + color.END + " But " + color.RED + "Failed" + color.END + " To Proceed To " + color.YELLOW + "'Order' Form" + color.END, 3))
            threadB.start()
    
    #Attempt To Fill Out Info ----------
    if SettingsDict.get("FillOutInfo") == True and elementClassDict.get("CanFillInfo") == True:
        pInfo = readPI()
        try: fillOutInfo(pInfo, elementClassDict, driver)
        except:
            threadB = Thread(target = alertLoop(color.BOLD + color.GREEN + "An Item Is In Stock!," + color.END + " But " + color.RED + "Failed" + color.END + " To " + color.YELLOW + "Fill Out" + color.END + " Information" + color.END, 3))
            threadB.start()
    else:
        if SettingsDict.get("DEBUGGING") == False: os.system("CLS"), printProgramName()
        if elementClassDict.get("CanFillInfo") == False:
            threadB = Thread(target = alertLoop(color.BOLD + color.GREEN + "An Item Is In Stock!," + color.END + " But Can't " + color.YELLOW + "Fill Out" + color.END + " Information" + color.END, 3))
            threadB.start()
        else:
            threadB = Thread(target = alertLoop(color.BOLD + color.GREEN + "An Item Is In Stock!," + color.END + " But " + color.RED + "Failed" + color.END + " To " + color.YELLOW + "Fill Out" + color.END + " Information" + color.END, 3))
            threadB.start()
        
    #Confirm Order ----------
    if SettingsDict.get("ConfirmOrder") == True :
        try: confirmButton = findAndClickElement("ConfirmOrderButton", elementClassDict, driver, waitASec = True)
        except:
            threadB = Thread(target = alertLoop(color.BOLD + color.GREEN + "An Item Is In Stock!," + color.END + " But " + color.RED + "Failed" + color.END + " To Confirm Purchase", 3))
            print("Please " + color.BOLD + color.RED + "exit" + color.END + " out of this program when you are done.")
            threadB.start()
    else:
        if SettingsDict.get("DEBUGGING") == False: os.system("CLS"), printProgramName()
        threadB = Thread(target = alertLoop(color.BOLD + color.GREEN + "An Item Is In Stock!," + color.END + " But " + color.YELLOW +
                                            "ConfirmOrder" + color.END + " Is " + color.RED + "Disabled" + color.END + " in the " + color.YELLOW + "'Settings.txt'" + color.END, 3))
        print("Please " + color.BOLD + color.RED + "exit" + color.END + " out of this program when you are done.")
        threadB.start()

    #Congratulations ----------
    if SettingsDict.get("DEBUGGING") == False: os.system("CLS"), printProgramName()
    else: print()
    printAlert(color.BOLD + color.GREEN + "Congratulations!!\n" + color.END + color.BLUE + ProgramName + color.END + 
               " has successfully found and purchased an item.\nIt is recommended that you still " + color.UNDERLINE +
               color.YELLOW + "review" + color.END + " and " + color.UNDERLINE + color.YELLOW + "confirm" + color.END + " the purchase information.\n\n~Thank You!", "*", 0)
    print("Please " + color.BOLD + color.RED + "exit" + color.END + " out of this program.")
    threadB = Thread(target = alertLoop(None, 3))
    threadB.start()
        
main()
