from selenium import webdriver

class Session1688(object):
    cookies = {}
    driver = webdriver.Chrome()

    # 登陆
    def login(self):
        self.driver.get("https://login.1688.com/member/signin.htm")
        input('pls login')
        self.setCookies()

    def setCookies(self):
        for c in self.driver.get_cookies():
            self.cookies[c["name"]] = c["value"]