import time

from selenium.webdriver.common.by import By

from pages.base import Base

TG = {"simple": ((By.ID, "simple-modal"), (By.ID, "simpleModal"),
                 (By.XPATH, "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'simple')]")),
      "confirm": ((By.ID, "confirm-modal"), (By.ID, "confirmModal"),
                  (By.XPATH, "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'confirm')]")),
      "image": ((By.ID, "image-modal"), (By.ID, "imageModal"),
                (By.XPATH, "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'image')]")),
      "form": ((By.ID, "form-modal"), (By.ID, "formModal"),
               (By.XPATH, "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'form')]"),
               (By.XPATH, "//a[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'contact')]"))}

POP = ((By.CSS_SELECTOR, "div.pum-container"),
       (By.CSS_SELECTOR, "div.modal.show"),
       (By.CSS_SELECTOR, "div[role='dialog']"),
       (By.CSS_SELECTOR, "div.modal"))

TTL = ((By.CSS_SELECTOR, ".pum-title"),
       (By.CSS_SELECTOR, ".modal-title"),
       (By.CSS_SELECTOR, "h2"),
       (By.CSS_SELECTOR, "h1"))

TXT = ((By.CSS_SELECTOR, ".pum-content"),
       (By.CSS_SELECTOR, ".modal-body"),
       (By.CSS_SELECTOR, "div[role='dialog']"))

X = ((By.ID, "btn-close-modal"),
     (By.CSS_SELECTOR, "button.pum-close"),
     (By.CSS_SELECTOR, ".pum-close"),
     (By.CSS_SELECTOR, "button[aria-label='Close']"),
     (By.CSS_SELECTOR, "button.close"),
     (By.XPATH, "//button[normalize-space(.)='×' or normalize-space(.)='x' or normalize-space(.)='X']"))

OK = ((By.ID, "btn-ok"),
      (By.CSS_SELECTOR, "button.btn-ok"),
      (By.XPATH, "//button[normalize-space(.)='OK']"),
      (By.XPATH, "//button[contains(normalize-space(.),'OK')]"))

NO = ((By.ID, "btn-cancel"),
      (By.CSS_SELECTOR, "button.btn-cancel"),
      (By.XPATH, "//button[normalize-space(.)='Cancel']"),
      (By.XPATH, "//button[contains(normalize-space(.),'Cancel')]"))

IM = ((By.CSS_SELECTOR, "img"),
      (By.CSS_SELECTOR, "picture img"),
      (By.CSS_SELECTOR, "figure img"))


class Mod(Base):

    def open(self):
        return self.go("/modals/")

    def head(self):
        return self.txt(((By.CSS_SELECTOR, "h1"),))

    def trigs(self):
        return [k for k in ("simple", "confirm", "image", "form") if self.has(TG[k])]

    def t(self, k):
        return self.tap(TG[k])

    def pops(self):
        out = []
        for l in POP:
            try:
                for e in self.d.find_elements(*l):
                    if e.is_displayed():
                        out.append(e)
            except Exception:
                pass
            if out:
                break
        return out

    def pop(self, t=None):
        end = time.time() + (self.w if t is None else t)
        while time.time() < end:
            p = self.pops()
            if p:
                return p[0]
            time.sleep(.2)
        raise AssertionError("модалка не открылась")

    def pop_on(self):
        return len(self.pops()) > 0

    def openk(self, k, t=None):
        self.t(k)
        return self.pop(t)

    def kill(self):
        e = self.find(X, 6)
        self.js("arguments[0].click()", e)
        time.sleep(.4)
        return e

    def ttl(self, p=None):
        p = p or self.pop()
        for l in TTL:
            for e in p.find_elements(*l):
                s = (e.text or "").strip()
                if s:
                    return s
        return (p.text or "").strip()[:40]

    def body(self, p=None):
        p = p or self.pop()
        for l in TXT:
            for e in p.find_elements(*l):
                s = (e.text or "").strip()
                if s:
                    return s
        return (p.text or "").strip()[:120]

    def img(self, p=None):
        p = p or self.pop()
        for l in IM:
            for e in p.find_elements(*l):
                if e.is_displayed():
                    return e
        return None

    def esc(self):
        from selenium.webdriver.common.keys import Keys
        self.d.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
        time.sleep(.4)

    def btn(self, ls, p=None):
        p = p or self.pop()
        for l in ls:
            for e in p.find_elements(*l):
                if e.is_displayed():
                    return e
        return None
