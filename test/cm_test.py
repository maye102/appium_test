import json

from appium import webdriver
import unittest
import time
import os
import allure


timeout = 30
poll = 2

@allure.feature('IAppium')
class IAppium(unittest.TestCase):

    def setUp(self):
        data = json.load(open("iAppium_python.json"))
        desired_caps = dict()
        appium_server_url = data['appium_server_url']
        desired_caps['platformName'] = data['desired_caps']['platformName']
        desired_caps['deviceName'] = data['desired_caps']['deviceName']
        desired_caps['appPackage'] = data['desired_caps']['appPackage']
        desired_caps['appActivity'] = data['desired_caps']['appActivity']
        desired_caps['automationName'] = data['desired_caps']['automationName']
        desired_caps['noReset'] = data['desired_caps']['noReset']
        desired_caps['app'] = f'{os.path.dirname(os.path.abspath("."))}\\app\\ContactManager.apk'

        self.driver = webdriver.Remote(appium_server_url, desired_caps)

    def tearDown(self):
        self.driver.quit()


    @allure.story('Test Contact')
    def test_contact(self):
        """  """

        # 单击contact按钮
        self._click_add_contact_btn()
        # contact输入名字
        self._input_contact_name('zhang')
        # 输入email
        self._input_email('zhang@example.com')
        time.sleep(2)
        # 点击save
        self._click_save_btn()

        time.sleep(2)

    def _click_add_contact_btn(self):
        elem = self._find_elem_by_xpath('//android.widget.Button[contains(@resource-id,"addContactButton")]')
        print(f'Click add contact button')
        elem.click()

    def _input_contact_name(self, txt_name):
        elem = self._find_elem_by_xpath('//android.widget.EditText[contains(@resource-id, "contactNameEditText")]')
        print(f'Input contact name {txt_name}')
        elem.send_keys(txt_name)

    def _input_email(self, txt_email):
        elem = self._find_elem_by_xpath('//android.widget.EditText[contains(@resource-id, "contactEmailEditText")]')
        print(f'Input email {txt_email}')
        elem.send_keys(txt_email)

    def _click_save_btn(self):
        elem = self._find_elem_by_xpath('//android.widget.Button[contains(@resource-id, "contactSaveButton")]')
        print('Click the save button')
        elem.click()



    def _find_elem_by_xpath(self, elem_xpath, time_out=timeout, raise_exception=True):
        start = time.time()
        elem = None
        while time.time() - start < time_out and elem is None:
            time.sleep(poll)
            try:
                elem = self.driver.find_element_by_xpath(elem_xpath)
            except Exception:
                print('by pass the element not found')

        if elem is None and raise_exception:
            raise LookupError(f'The element which xpath is {elem_xpath} could not be found')

        return elem
