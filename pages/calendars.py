import time

from selenium.webdriver.common.by import By

from pages.base import Base, Ui

IN = {1: ((By.ID, "datepicker1"), (By.CSS_SELECTOR, "input[id*='datepicker1' i]"),
         (By.XPATH, "(//input[starts-with(@id,'datepicker')])[1]")),
      2: ((By.ID, "datepicker2"), (By.CSS_SELECTOR, "input[id*='datepicker2' i]"),
         (By.XPATH, "(//input[starts-with(@id,'datepicker')])[2]")),
      3: ((By.ID, "datepicker3"), (By.CSS_SELECTOR, "input[id*='datepicker3' i]"),
         (By.XPATH, "(//input[starts-with(@id,'datepicker')])[3]"))}

PAN = ((By.CSS_SELECTOR, "div.ui-datepicker[style*='display: block']"),
       (By.CSS_SELECTOR, "div.ui-datepicker[style*='display:block']"),
       (By.CSS_SELECTOR, "div.ui-datepicker"),
       (By.ID, "ui-datepicker-div"))

CAP = ((By.CSS_SELECTOR, ".ui-datepicker-title"),
       (By.CSS_SELECTOR, ".ui-datepicker-month"),
       (By.CSS_SELECTOR, ".ui-datepicker-year"))

FD = ((By.CSS_SELECTOR, "input[placeholder*='YYYY']"),
      (By.CSS_SELECTOR, "input[type='date']"),
      (By.CSS_SELECTOR, ".entry-content input[type='text']:not([id^='datepicker'])"),
      (By.CSS_SELECTOR, "form input:not([id^='datepicker'])"))

SB = ((By.CSS_SELECTOR, "form button[type='submit']"),
      (By.CSS_SELECTOR, "button[type='submit']"),
      (By.CSS_SELECTOR, "input[type='submit']"),
      (By.XPATH, "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'submit')]"))

ER = ((By.CSS_SELECTOR, ".grunion-error"),
      (By.CSS_SELECTOR, ".jp-contact-form-error"),
      (By.XPATH, "//*[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'problem with your submission')]"),
      (By.XPATH, "//*[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'please fill')]"))


class Cal(Base):

    def open(self):
        return self.go("/calendars/")

    def head(self):
        return self.txt(((By.CSS_SELECTOR, "h1"),))

    def ins(self):
        return [n for n in (1, 2, 3) if self.has(IN[n])]

    def fld(self, n, t=None):
        return self.find(IN[n], t)

    def val(self, n):
        return (self.at(self.fld(n), "value") or "").strip()

    def pan(self, t=None):
        return self.find(PAN, t)

    def pan_on(self):
        return self.has(PAN)

    def op(self, n, t=None):
        self.tap(IN[n])
        return self.pan(t)

    def cap(self):
        p = self.pan()
        for l in CAP:
            for e in p.find_elements(*l):
                s = (e.text or "").strip()
                if s:
                    return s
        return (p.text or "").strip()[:40]

    def nx(self, d):
        p = self.pan()
        n = "ui-datepicker-next" if d > 0 else "ui-datepicker-prev"
        for e in p.find_elements(By.CSS_SELECTOR, "a.%s, span.%s, .%s" % (n, n, n)):
            self.js("arguments[0].click()", e)
            time.sleep(.4)
            return True
        return False

    def day(self, d):
        p = self.pan()
        for x in (".//td[not(contains(@class,'ui-datepicker-unselectable'))]/a[normalize-space(text())=%d]",
                  ".//a[normalize-space(text())=%d]",
                  ".//td[not(contains(@class,'ui-datepicker-unselectable'))][normalize-space(text())=%d]"):
            for e in p.find_elements(By.XPATH, x % d):
                return e
        raise Ui("нет дня %s" % d)

    def dead(self):
        p = self.pan()
        return p.find_elements(By.CSS_SELECTOR,
                               "td.ui-datepicker-unselectable a, a.ui-datepicker-unselectable")

    def setd(self, n, d):
        self.op(n)
        self.js("arguments[0].click()", self.day(d))
        time.sleep(.3)
        return self.val(n)

    def sent(self, t=6):
        return self.rx(r"your message has been sent|thank you|has been sent|message sent", t)

    def err(self):
        return self.has(ER)

    def close_b(self):
        p = self.pan()
        for x in (".//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'close')]",
                  ".//a[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'close')]",
                  ".//*[contains(@class,'datepicker-close')]"):
            for e in p.find_elements(By.XPATH, x):
                return e
        return None
