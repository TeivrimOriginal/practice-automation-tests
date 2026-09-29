import re
import time

from selenium.common.exceptions import (ElementClickInterceptedException,
                                        ElementNotInteractableException,
                                        NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.common.by import By

W = 12.0

CK = ((By.ID, "cookie_action_close_header"),
      (By.CSS_SELECTOR, "#cookie-accept-all-yes"),
      (By.CSS_SELECTOR, "button#cookie-accept-all-yes"),
      (By.XPATH, "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'accept')]"))


class Ui(Exception):
    pass


class Base:

    def __init__(self, d, base="https://practice-automation.com", w=W):
        self.d = d
        self.base = base.rstrip("/")
        self.w = w

    def go(self, p):
        self.d.get(self.base + p)
        self.ck()
        try:
            self.d.execute_script("window.scrollTo(0,0)")
        except Exception:
            pass
        return self

    def url(self):
        return self.d.current_url

    def ck(self):
        for l in CK:
            try:
                for e in self.d.find_elements(*l):
                    if e.is_displayed():
                        e.click()
                        time.sleep(.2)
                        return True
            except Exception:
                pass
        return False

    def find(self, ls, t=None, vis=True):
        end = time.time() + (self.w if t is None else t)
        while True:
            for l in ls:
                try:
                    for e in self.d.find_elements(*l):
                        if not vis or e.is_displayed():
                            return e
                except (NoSuchElementException, StaleElementReferenceException):
                    pass
                except Exception:
                    pass
            if time.time() >= end:
                raise Ui("нет: %s" % (ls,))
            time.sleep(.1)

    def find0(self, ls):
        for l in ls:
            try:
                for e in self.d.find_elements(*l):
                    if e.is_displayed():
                        return e
            except Exception:
                pass
        return None

    def has(self, ls):
        return self.find0(ls) is not None

    def gone(self, ls, t=None):
        end = time.time() + (self.w if t is None else t)
        while time.time() < end:
            if not self.has(ls):
                return True
            time.sleep(.2)
        return not self.has(ls)

    def tap(self, ls, t=None):
        e = self.find(ls, t)
        for _ in range(3):
            try:
                self.d.execute_script("arguments[0].scrollIntoView({block:'center'});", e)
                time.sleep(.1)
                e.click()
                return e
            except (StaleElementReferenceException, ElementClickInterceptedException,
                    ElementNotInteractableException, NoSuchElementException):
                time.sleep(.3)
                e = self.find(ls, 1)
        self.d.execute_script("arguments[0].click();", e)
        return e

    def put(self, ls, s, t=None):
        e = self.find(ls, t)
        try:
            e.clear()
        except Exception:
            pass
        e.send_keys(s)
        return e

    def txt(self, ls, t=None):
        return (self.find(ls, t).text or "").strip()

    def txts(self, ls):
        out = []
        for l in ls:
            try:
                for e in self.d.find_elements(*l):
                    s = (e.text or "").strip()
                    if e.is_displayed() and s and s not in out:
                        out.append(s)
            except Exception:
                pass
            if out:
                break
        return out

    def rx(self, p, t=None):
        end = time.time() + (self.w if t is None else t)
        r = re.compile(p, re.I)
        while True:
            best = None
            for e in self.d.find_elements(By.CSS_SELECTOR, "h1,h2,h3,h4,p,span,li,a,strong,div"):
                try:
                    if not e.is_displayed():
                        continue
                    s = (e.text or "").strip()
                except Exception:
                    continue
                if s and r.search(s) and (best is None or len(s) < len(best)):
                    best = s
            if best:
                return best
            if time.time() >= end:
                return None
            time.sleep(.2)

    def js(self, s, *a):
        return self.d.execute_script(s, *a)

    def vmsg(self, e):
        try:
            return e.get_attribute("validationMessage") or ""
        except Exception:
            return ""

    def at(self, e, a):
        try:
            return e.get_attribute(a)
        except Exception:
            return None
