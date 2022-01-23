from selenium.webdriver.support.ui import Select
from .base_selenium_tests import BaseSeleniumTestData


class AccountsTest(BaseSeleniumTestData):

    def do_login(self, username, password):
        # Helper function to log in user.
        self.browser.get(f'{self.live_server_url}/login/')
        self.browser.find_element_by_name('username').send_keys(username)
        self.browser.find_element_by_name('password').send_keys(password)
        self.browser.find_element_by_id('btn-submit').click()

        alert = self.browser.find_element_by_class_name('alert')
        self.assertEqual(alert.text, 'Logged in')

    def test_user_logs_in(self):
        # The user logs in.
        self.do_login('user', 'test4321')

    def test_user_creates_new_account(self):
        # The user creates new account.
        self.browser.get(f'{self.live_server_url}/register/')
        self.browser.find_element_by_name('username').send_keys('testuser')
        self.browser.find_element_by_name('email').send_keys('test@user.asd')
        self.browser.find_element_by_name('password1').send_keys('test4321')
        self.browser.find_element_by_name('password2').send_keys('test4321')
        self.browser.find_element_by_name('submit').click()

        alert = self.browser.find_element_by_class_name('alert')
        self.assertEqual(alert.text, 'Added new account for testuser.')

    def test_user_changes_password(self):
        # The user logs in.
        self.do_login('user', 'test4321')

        # The user navigates to change password page.
        self.browser.find_element_by_id('nav-account').click()
        self.browser.find_element_by_id('btn-change-password').click()

        # The user changes password.
        self.browser.find_element_by_name('old_password').send_keys('test4321')
        self.browser.find_element_by_name(
            'new_password1').send_keys('changed4321')
        self.browser.find_element_by_name(
            'new_password2').send_keys('changed4321')
        self.browser.find_element_by_name('btn-submit').click()

        alert = self.browser.find_element_by_class_name('alert')
        self.assertEqual(alert.text, 'Password changed')

    def test_user_requests_book(self):

        # The user logs in.
        self.do_login('user', 'test4321')

        # The user navigates to book detail page and requests book loan. Then is redirected to book list page.
        self.browser.get(f'{self.live_server_url}')
        self.browser.find_element_by_id('book-title-1').click()
        Select(self.browser.find_element_by_id('site')).select_by_visible_text('secondary')
        self.browser.find_element_by_id('btn-submit').click()

        alert = self.browser.find_element_by_class_name('alert')
        self.assertEqual(alert.text, 'Book requested')

        # The user navigates to book detail page again to check if the book is marked as reserved.
        self.browser.find_element_by_id('book-title-1').click()

        reserved = self.browser.page_source.__contains__(
            'This copy is reserved at the moment.')
        self.assertTrue(reserved)
