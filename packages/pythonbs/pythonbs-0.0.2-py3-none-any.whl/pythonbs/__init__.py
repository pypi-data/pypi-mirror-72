from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def get_webdriver(username=None,accesskey=None,desired_cap=None,is_mobile=False):
    try :
        command_executor = 'https://%s:%s@hub-cloud.browserstack.com/wd/hub'%(username,accesskey)
        driver = webdriver.Remote(command_executor=command_executor,desired_capabilities=desired_cap)
        return driver
    except:
        print('Creating session failed ,Try again with valid credentials')
        driver.quit()