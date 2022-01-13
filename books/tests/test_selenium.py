from selenium import webdriver
import selenium
from selenium.webdriver.common.keys import Keys
from django.urls import reverse
from time import sleep
from library.models import Book
from django.contrib.auth.models import User

from .base_selenium_tests import BaseSeleniumTestData


class AccountsTest(BaseSeleniumTestData):

    def test_user_logs_in(self):
        self.browser.get(f'{self.live_server_url}/list/')
        self.browser.find_element_by_id('nav-login').click()
        
        self.browser.find_element_by_name('username').send_keys('user')
        self.browser.find_element_by_name('password').send_keys('test4321')
        self.browser.find_element_by_id('btn-submit').click()
        alert = self.browser.find_element_by_class_name('alert')
        self.assertEqual(alert.text, 'Logged in')

    def test_user_creates_new_account(self):
        self.browser.get(f'{self.live_server_url}/register/')
        self.browser.find_element_by_name('username').send_keys('testuser')
        self.browser.find_element_by_name('email').send_keys('test@user.asd')
        self.browser.find_element_by_name('password1').send_keys('test4321')
        self.browser.find_element_by_name('password2').send_keys('test4321')
        self.browser.find_element_by_name('submit').click()
        
        alert = self.browser.find_element_by_class_name('alert')
        self.assertEqual(alert.text, 'Added new account for testuser.')
    
    def test_user_changes_password(self):
        self.browser.get(f'{self.live_server_url}/login/')
        self.browser.find_element_by_name('username').send_keys('user')
        self.browser.find_element_by_name('password').send_keys('test4321')
        self.browser.find_element_by_id('btn-submit').click()

        self.browser.find_element_by_id('nav-account').click()
        self.browser.find_element_by_id('btn-change-password').click()

        self.browser.find_element_by_name('old_password').send_keys('test4321')
        self.browser.find_element_by_name('new_password1').send_keys('changed4321')
        self.browser.find_element_by_name('new_password2').send_keys('changed4321')
        self.browser.find_element_by_name('btn-submit').click()

        alert = self.browser.find_element_by_class_name('alert')
        self.assertEqual(alert.text, 'Password changed')