#Pygmy Browser By James Alexander Glynn 2022-2022
#Followed tutorial by GeeksforGeeks 'PyQt5 Tabbed Browser'
#and followed https://www.youtube.com/watch?v=z-5bZ8EoKu4
#then added, rickroll, custom icons, shortcuts, google search 
#from url bar. Custom settings page coming soon.

import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from  PyQt5.QtGui import QIcon
from PyQt5.QtGui import QKeySequence
import pygame
from pynput.keyboard import Key, Controller
import time
from win32api import GetSystemMetrics

pygame.mixer.init()

link = ''
history = []
home_page_url = 'file:///C:/Users/James/Desktop/Home-Page/Home%20Page%20-%20Pygmy.html'

keyboard = Controller()

def play(string, vol):
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.load(string)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    
def playNo(string, vol):
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.load(string)
    pygame.mixer.music.play()

def stop():
    pygame.mixer.music.stop()

def keyword(keywords, statement):
    for i in keywords:
        if i.lower() in statement:
            return True
    return False


class MainWindow(QMainWindow):
    def __init__(self):
        global link
        super(MainWindow, self).__init__()
        self.browser = QWebEngineView()
        self.showMaximized()

        #Adding tabs!
        self.tabs = QTabWidget()

        self.tabs.setDocumentMode = True
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)

        #Adding status bar
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        #Navigation bar: url, forward, backward, reload etc.
        navigation_bar = QToolBar()
        self.addToolBar(navigation_bar)

        #Back button
        back_button = QAction('Back', self)
        back_button.triggered.connect(lambda: self.tabs.currentWidget().back())
        back_button.setIcon(QIcon('Backward.png'))
        navigation_bar.addAction(back_button)

        #Forward button
        forward_button = QAction('Forward', self)
        forward_button.triggered.connect(lambda: self.tabs.currentWidget().forward())
        forward_button.setIcon(QIcon('Forward.png'))
        navigation_bar.addAction(forward_button)
        
        #Reload button
        reload_button = QAction("Reload", self)
        reload_button.triggered.connect(lambda: self.tabs.currentWidget().reload())
        reload_button.setIcon(QIcon('Refresh.png'))
        navigation_bar.addAction(reload_button)

        #URL bar e.g. https://google.com
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        navigation_bar.addWidget(self.url_bar)
        self.browser.urlChanged.connect(self.update_url)

        #Set current tab to google
        google_button = QAction("Google", self)
        google_button.triggered.connect(self.go_to_google)
        google_button.setIcon(QIcon('google.png'))
        navigation_bar.addAction(google_button)

        #Haha secret rickroll! Looks like a home button!
        secret_rickroll_button = QAction("Ricrkroll", self)
        secret_rickroll_button.triggered.connect(self.go_to_rickroll)
        secret_rickroll_button.setIcon(QIcon('Logo_Draft_1.svg'))
        navigation_bar.addAction(secret_rickroll_button)

        #Shortcut keyboard bindings

        #Reload shortuct: CTRL + R
        self.reload_shortuct = QShortcut(QKeySequence('Ctrl+R'), self)
        self.reload_shortuct.activated.connect(self.browser.reload)

        #Open new tab
        self.new_tab_shortcut = QShortcut(QKeySequence('Ctrl+T'), self)
        self.new_tab_shortcut.activated.connect(self.add_new_tab)

        #Delete current tab
        self.delete_shortcut = QShortcut(QKeySequence('Ctrl+W'), self)
        self.delete_shortcut.activated.connect(self.close_current_tab)
        
        #Open recently closed tab
        self.open_old_tab_shortcut = QShortcut(QKeySequence('Ctrl+Shift+T'), self)
        self.open_old_tab_shortcut.activated.connect(self.open_recently_closed_tab)

        #Back shortcut: CTRL + SHIFT + Left Arrow
        self.back_shortuct = QShortcut(QKeySequence('CTRL+SHIFT+Left'), self)
        self.back_shortuct.activated.connect(self.browser.back)

        #Forward shortcut: CTRL + SHIFT + Right Arrow
        self.forward_shortuct = QShortcut(QKeySequence('CTRL+SHIFT+Right'), self)
        self.forward_shortuct.activated.connect(self.browser.forward)

        #Haha rickroll shortcut! CTRL + SHIFT + R
        self.rickroll_shortuct = QShortcut(QKeySequence('CTRL+SHIFT+R'), self)
        self.rickroll_shortuct.activated.connect(self.go_to_rickroll)

        #And to stop the rickroll if triggered accidentally: CTRL + SHIFT + N
        self.rickroll_shortuct = QShortcut(QKeySequence('CTRL+SHIFT+N'), self)
        self.rickroll_shortuct.activated.connect(self.stop_rickroll)

        # Make the first tab
        self.add_new_tab(QUrl(home_page_url), 'Homepage')
 
        # showing all the components
        self.show()

        #self.setFixedSize(self.sizeHint())
        self.setMinimumSize(GetSystemMetrics(0), GetSystemMetrics(1))

    def navigate_to_url(self):
        #Get the URL bar text and convert it to hyperlink
        if not keyword([' '], self.url_bar.text()):
            q = QUrl(self.url_bar.text())
        else:
            q = QUrl('https://google.com/search?q=' + self.url_bar.text().replace(' ', '+'))
 
        #If the hyper-text-transfer-protocols is blank
        if q.scheme() == "":
            #Set it to hyper-text-transfer-protocol-secure
            q.setScheme("http")
 
        #Then set the url
        self.tabs.currentWidget().setUrl(q)
    
    def add_new_tab(self, qurl = None, label ="Home"):
 
        #If no one added a url in url bar
        if qurl is None:
            #Go to home page
            qurl = QUrl('https://www.google.com')
 
        #Make a place to see home page or url open
        browser = QWebEngineView()
 
        #Set url in navbar
        browser.setUrl(qurl)
 
        #Set tab index
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
 
        #When the url is changed, update it!
        browser.urlChanged.connect(lambda qurl, browser = browser: self.update_url(qurl, browser))
 
        #When you've finished loading the website, go ahead and add that fancy title to the tab
        browser.loadFinished.connect(lambda _, i = i, browser = browser: self.tabs.setTabText(i, browser.page().title()))

    def open_recently_closed_tab(self):
        self.add_new_tab(QUrl(history[-1]))

    def tab_open_doubleclick(self, i):
 
        # checking index i.e
        # No tab under the click
        #if i == -1:
            # creating a new tab
        self.add_new_tab()
        return

    def close_current_tab(self):
        global history
 
        #If there's one tab left, don't close it!
        if self.tabs.count() < 2:
            # do nothing
            return

        #Add url to history
        self.tabs.setCurrentWidget(self.tabs.currentIndex)
        history.append(str(self.tabs.currentWidget().url()))

        #Otherwise, make like a tree and get out of here!
        i = self.tabs.currentIndex()
        self.tabs.removeTab(i)

    def current_tab_changed(self):
 
        #Get the current URL
        qurl = self.tabs.currentWidget().url()
 
        #Update the URL
        self.update_url(qurl, self.tabs.currentWidget())
 
        #Update the fancy-schmansy tab title
        self.update_title(self.tabs.currentWidget())

    def update_title(self, browser):
 
        # If it's not from the current tab:
        if browser != self.tabs.currentWidget():
            #Do nothing!!!
            return
 
        #Otherwse get the fancy-schmansy tab title
        title = self.tabs.currentWidget().page().title()

    def go_to_rickroll(self):
        playNo('Rickroll.mp3', 1)
        time.sleep(1)
        with keyboard.pressed(Key.cmd_l):
            keyboard.press('r')
            keyboard.release('r')
        time.sleep(.3)
        keyboard.type('notepad')
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        time.sleep(1)
        rickroll = open('Rickroll.txt', 'r')
        rickroll_word_list = rickroll.read().split()

        for i in rickroll_word_list:
            keyboard.type(i + " ")
            time.sleep(.2)
        rickroll.close()

    def stop_rickroll(self):
        stop()

    def go_to_google(self):
        self.tabs.currentWidget().setUrl(QUrl('https://www.google.com'))

    def update_url(self, q, browser = None):
        #If this signal is not from the current tab then ignore it
        if browser != self.tabs.currentWidget():
            return
        
        #Otherwise, set the text in the url bar to match the real url
        self.url_bar.setText(q.toString())


app = QApplication(sys.argv)
QApplication.setApplicationName('Pygmy')
QApplication.setWindowIcon(QIcon("Logo_Draft_1.svg"))
window = MainWindow()
app.exec_()