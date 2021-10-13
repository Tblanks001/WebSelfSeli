from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
# from requests_html import HTML
import pandas as pd
from bs4 import BeautifulSoup
import re
import time
import keyboard
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty

class MyGrid(Widget):
    smid = ObjectProperty(None)
    passw = ObjectProperty(None)
    fdl = ObjectProperty(None)
    tdl = ObjectProperty(None)
    tm = ObjectProperty(None)
    nm = ObjectProperty(None)

    def btn(self):
        lst = [self.smid.text, self.passw.text, self.fdl.text, self.tdl.text, self.tm.text, self.nm.text]
        opencolws(lst[0], lst[1], lst[2], lst[3])
        lis = copycontacts()
        messenger(lis, lst[4])
        opencolws(lst[0], lst[1], lst[2], lst[3])
        postnotes(lst[5])

class MyApp(App):
    def build(self):
        return MyGrid()

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
#driver.implicitly_wait(30)


def opencolws(smid, passw, fdal, tdal):
    driver.get("https://www.webselfstorage.com/SignIn")

    username = driver.find_element_by_name("LoginOrSmid")
    username.send_keys(smid)

    password = driver.find_element_by_name("Password")
    password.send_keys(passw)

    password.send_keys(Keys.RETURN)

    link = driver.find_element_by_link_text("Reports")
    link.click()

    coll = driver.find_element_by_link_text("Collection Worksheet")
    coll.click()



    time.sleep(1)

    driver.switch_to.window("Collection Worksheet")

    fdl = driver.find_element_by_id("ReportArguments_FromDaysLate")
    fdl.clear()
    fdl.send_keys(fdal)

    tdl = driver.find_element_by_id("ReportArguments_ToDaysLate")
    tdl.clear()
    tdl.send_keys(tdal)

    gen = driver.find_element_by_tag_name("Button")
    gen.click()

    time.sleep(2)


def copycontacts():

    results = []
    update = []
    content = driver.page_source
    soup = BeautifulSoup(content)


    for element in soup.findAll('td'):
        name = element.find(string=re.compile('Home :'))
        if name not in results:
            results.append(name)

    for i in results[1:]:
        update.append(i[8:22])

    while("              " in update):
        update.remove("              ")
    while("(000) 000-0000" in update):
        update.remove("(000) 000-0000")

    print(update)
    return update


def messenger(up, tm):
    driver.get('https://pos.uhaul.net/secure/POSLogin/Login.aspx?AppName=Console')
    username2 = driver.find_element_by_name("loginUser$UserName")
    username2.send_keys("1263448")

    password2 = driver.find_element_by_name("loginUser$Password")
    password2.send_keys("gokuUhoku678")

    password2.send_keys(Keys.RETURN)

    #time.sleep(5)

    #This thing breaks without even clicking anything. Figure out how to fix this
    while True:
        try:
            mess = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "messengerIcon"))
            )
            mess.click()
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "uhi-footer-messages")))
            break
        except TimeoutException:
            pass
        except ElementClickInterceptedException:
            print("It appears an error has occured(mess. icon)! Hit Enter to retry.")
            a = keyboard.read_key()
            if a == "Enter":
                pass
            continue

        break


    driver.switch_to.frame('frmMessenger')

    while True:
        try:
            texts = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "uhi-footer-messages"))
            )
            texts.click()
        except:
            print("It appears an error has occured(uhi footer messages)! Hit Enter to retry.")
            a = keyboard.read_key()
            if a == "Enter":
                continue
        break

    while True:
        try:
            nt = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "uhi-button-addmessage"))
            )
            nt.click()
        except:
            print("It appears an error has occured(add message)! Hit Enter to retry.")
            a = keyboard.read_key()
            if a == "Enter":
                continue
        break


    #time.sleep(3)

    for con in up:

        while True:

            #pb = driver.find_element_by_class_name('uhi-button-addfromphonebook')
            #if len(pb) > 0:
            try:
                pb = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "uhi-button-addfromphonebook"))
                )
                pb.click()
                WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.ID, "uhi-header-search"))
                )
                break

            except NoSuchElementException:
                print("It appears an error has occured(addfromphonebook1)! Hit Enter to retry.")
                a = keyboard.read_key()
                if a == "Enter":
                    continue

            except IndexError:
                print("It appears an error has occured(addfromphonebook2)! Hit Enter to retry.")
                a = keyboard.read_key()
                if a == "Enter":
                    continue
            except TimeoutException:
                pass
            except StaleElementReferenceException:
                pass
            except ElementClickInterceptedException:
                print("It appears an error has occured(addfromphonebook3)! Hit Enter to retry.")
                a = keyboard.read_key()
                if a == "Enter":
                    pass
                continue



        while True:
            #add = driver.find_elements_by_id('uhi-textmessage-addrecipients')
            #if len(add) > 0:

            try:
                search = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.ID, "uhi-header-search"))
                )
                search.clear()
                search.send_keys(con)
                add = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.ID, "uhi-textmessage-addrecipients"))
                )
                add.click()
                WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "uhi-button-addfromphonebook"))
                )
                break

            except TimeoutException:
                pass
            except ElementClickInterceptedException:
                print("It appears an error has occured(addrecipients)! Hit Enter to retry.")
                a = keyboard.read_key()
                if a == "Enter":
                    pass
                continue

    message = driver.find_element_by_id('uhi-newtextmessage-message')
    message.send_keys(tm)

    #send = driver.find_element_by_id('uhi-newtextmessage-send')
    #send.click()

                #search.clear()
            #onc = br.find_element_by_link_text("uhm.addPhoneNumbersToText()")
'''
        while True:
            try:

                add = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "uhi-textmessage-addrecipients"))
                )
                #add = driver.find_element_by_id("uhi-textmessage-addrecipients")
                add.click()
                #onc.click()


            except:
                print("It appears an error has occured(add recipients)! Hit Enter to retry.")
                a = keyboard.read_key()
                if a == "Enter":
                    continue
            finally:
                break
'''



'''
                #time.sleep(1)
            else:
                break


        #add.click().until(EC.element_to_be_clickable((By.CLASS_NAME, "uhi-button-addfromphonebook")))

        time.sleep(3)
        
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "uhi-button-addfromphonebook"))).click()
        except TimeoutException:
            break

        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "uhi-header-search"))).send_keys(con)
        except TimeoutException:
            break

        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "uhi-textmessage-addrecipients"))).click()
        except TimeoutException:
            break
        
        
        pb = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "uhi-button-addfromphonebook"))
        )
        pb.click().until()

        search = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "uhi-header-search"))
        )
        search.send_keys(con)

        add = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "uhi-textmessage-addrecipients"))
        )
        add.click()
        


'''




def postnotes(nm):

    posts1 = driver.find_elements_by_xpath("//*[contains(text(), 'Post Note')]")
    for i in range(len(posts1[:-1])):
        posts2 = driver.find_elements_by_xpath("//*[contains(text(), 'Post Note')]")
        cancel = driver.find_element_by_id('btnCancelNote')
        #save = driver.find_element_by_xpath("//*[contains(text(), 'Save')]")
        txtarea = driver.find_elements_by_tag_name('textarea')
        posts2[i].click()
        time.sleep(.5)
        txtarea[1].send_keys(nm)
        cancel.click()
        time.sleep(3)
        curr = driver.current_url
        driver.get(curr)

'''
def main():
    opencolws()
    lis = copycontacts()
    messenger(lis)
    opencolws()
    postnotes()
'''

# driver.switch_to.window("Collection Worksheet") Go to the part of the code where you are accessing the collection
# worksheet Comment out the part of the code where you are grabbing the contacts Create a loop that opens every Post
# Note on the page, places some text, then cancels every time Create an if statement that skips(or cancels. Which one
# is easier?) a Post Note when there is no number associated with a contact (This will only be used when we are
# dealing with work numbers, because as far as I know, there will always be home numbers. I will probably deal with
# this in the future if need be.)
