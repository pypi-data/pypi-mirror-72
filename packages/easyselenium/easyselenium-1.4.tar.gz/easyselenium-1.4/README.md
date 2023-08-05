easyselenium 

*Let us handle the boring stuff!*

* [Step2success](https://step2success.in)

====================


<a href="https://selenium.dev"><img src="https://selenium.dev/images/selenium_logo_square_green.png" width="180" alt="Selenium"/></a>
Now Automate your browser based projects in easily and faster.

easyselenium is write on the top of selenium to make selenium easier for beginers for ready built in funtions only they need to call the functions and pass the arguments.All extra thing time delay and webdriver wait select findping xpath will do in backend.
Get rid of using time delays

By Ankit Kothari [Apache 2.0 license](https://github.com/SeleniumHQ/selenium/blob/master/LICENSE).


## Advantage

* 1.Simple easy syntax, Dont need to  remeber the whole selenium syntax and google it.It will call the required code acc to your need.ie: (browser=ie/chrome/firefox)
* 2.Dont need to download drivers for chrmoe/firefox/it it automatically download accc to your version in cache/your desired path.
* 3.All commands are with explicit wait so dont need to use time sleep and slow your code or element not found error. It will wait untill element/page found.
* 4.select your option with partial text
* 5.Manage Window/Javascript alerts also.
* 6.Debug will print line by line what going inside.
* 7.Read element/elements its text and value automatically and print in debug mode and retun in packed list.


## Documentation
* www.step2success.in/easyselenium
* https://pypi.org/project/easyselenium/

* [examples](https://github.com/ankitk29kothari/Step2success/tree/master/Selenium-Web%20Automation/easy_selenium/Examples)

## from easy selenium import *


## 1. open_browser()
```sh
with optional arguments

open_browser(browser='chrome/firefox/ie',headless=True/False,debug=True/False)

By default
by default time: Explicit wait is 50 sec for every function
Change from passing(timeout=1)
## open_browser(headless=False,,browser='chrome',debug=False,path=cache memory to download drivers/or your customised path)
```



## 2.connect_exisitng_browser(url,session_id)
```sh
pass url nad seesion id from your existing browser which is printed when you call browser.
```



## 3.open_url(url='https://step2success.in')
```sh
with optional arguments
open_url(url='https://step2success.in',new_tab=False)
new_tab = True/False (open in new tab or same)

```


## 4.window_handle(no=1)
window_handle(title='google')
```sh
To switch to your popup or another tab window ()


```

## 5.switch_frame (no=1 or name='mainframe')
```sh
To switch to iframe or frame with no or name
switch_frame(no=1 / name='mainframe'/id='name'/css='btn-danger'/ xpath='class=btn-pop'/xpath='//[div[3]/article/div[1]]')
```


## 6.click_on (text='submit'or image='imagepath' or id='submit' or css='send' or xpath='this')
To Click on buton based on iamge/Text or xpath

```sh
with optional arguments
click_on(no=1 / name='mainframe'/id='name'/css='btn-danger'/ xpath='class=btn-pop'/xpath='//[div[3]/article/div[1]]')

repeat=True/False (True- To double click on item)
```


## 7.mosue_hover (text='submit'or image='imagepath' or id='submit' or css='send' or xpath='this')
```sh
To hover mouse on avascript element instead of click
```



## 8.send_text (text='your text' with  id='submit' or css='send' or xpath='this')
```shTo send text to block

```sh
with optional arguments
send_text(no=1 / name='mainframe'/id='name'/css='btn-danger'/ xpath='class=btn-pop'/xpath='//[div[3]/article/div[1]]')

with_enter=True/False (True-To enter after type text)
```

## 9.select_dropdown (option ='option to select' with  id='submit' or css='send' or xpath='this')
```sh
To select option in dropdown with partial text
select_dropdown(no=1 / name='mainframe'/id='name'/css='btn-danger'/ xpath='class=btn-pop'/xpath='//[div[3]/article/div[1]]')
```


## 10.read_text (id='submit' or css='send' or xpath='this')
```sh
To read text from element/multiple elements
It is samrt enough to automatically detect if single or multiple element is present
Value/Text is present

Then return you a packed list of elemnts  containing text,value and session_id
read_text(no=1 / name='mainframe'/id='name'/css='btn-danger'/ xpath='class=btn-pop'/xpath='//[div[3]/article/div[1]]')
```



## 11.close_window (no=1 or name='yahoo')
```sh
To switch and close the provided window
optional switch_to=0
to switch to this window after closing
```



## 12.windows_alert (text='NA',with_enter=False)
```sh
To send text or enter to accept to windows authentication
```


## 13.alerts (text='yes'/'no'/'custom'/blank to read it text)
```sh
To accept/decline/send text/read text from alert box
```


## 14.page_source ()
```sh
To print raw HTML
```



Example :

```sh
import time

from easyselenium import *
import time
open_browser(path="chromedriver.exe",browser='chrome',debug=True)
#open_broswer(browser='firefox')
#open_broswer(browser='ie')
#open_broswer(browser='chrome',headless=True)

open_url(url="https://step2success.in/registration-page-demo/")
open_url(url="https://step2success.in/iframe-demo/",new_tab=True)
window_handle(no=0)
send_text(text='Ankit',id='first_name')
send_text(text='Kothari',id='last_name',with_enter=True)
select_dropdown(option='What is your Birthdate?',id='dropdown')
#click_on(text='REGISTER')
#click_on(id='register')


time.sleep(3)

window_handle(no=1)
switch_frame(no=0)
read_text(href ='#')
click_on(text='Follow On Twitter')

window_handle(no=2)

#close_window(no=2)

```


