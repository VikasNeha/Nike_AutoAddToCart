from webpageEvents import WebpageEvents
from Utilities.constants import IDMODE
from Utilities.myLogger import logger
import sys
import time


class NikeEvents(WebpageEvents):

    def __init__(self, ProxyIP):
        super(NikeEvents, self).__init__(ProxyIP)

    def destroy(self):
        super(NikeEvents, self).destroy()

    def loginToNike(self, Nike_Username, Nike_Password):
        self.enterText(IDMODE.ID, 'exp-login-email', Nike_Username)
        self.enterText(IDMODE.ID, 'exp-login-password', Nike_Password)
        self.clickElement(IDMODE.ID, 'exp-login-rememberMe')
        self.findElement(IDMODE.ID, 'exp-login-password').submit()

    def select_size_and_add_to_cart(self, size):
        sizeBox = self.findElement(IDMODE.CLASS, 'exp-pdp-size-and-quantity-container')
        select2 = sizeBox.find_element_by_tag_name('a')
        select2.click()
        time.sleep(2)
        lis = sizeBox.find_elements_by_tag_name('li')
        for li in lis:
            if li.text.strip() == size:
                li.click()
                break

        time.sleep(2)
        button = self.findElement(IDMODE.CLASS, 'exp-pdp-save-container')
        button.find_element_by_tag_name('button').click()

        time.sleep(5)
        try:
            span = self.driver.find_element_by_class_name("smart-cart-header")
            if "Out of Stock" in span.text:
                logger.info("Out of Stock")
                return False
        except:
            pass

        return True