import re
import time

from selenium.webdriver.common.by import By

from pages.base import Base

AD = ((By.CSS_SELECTOR, "div.pum-container"),
      (By.CSS_SELECTOR, "div[id^='ad-']"),
      (By.CSS_SELECTOR, "div[class*='adsbox']"),
      (By.CSS_SELECTOR, "div[class*='ad-container']"),
      (By.CSS_SELECTOR, "iframe[id*='ad']"),
      (By.CSS_SELECTOR, "ins.adsbygoogle"))

X = ((By.CSS_SELECTOR, "button.pum-close"),
     (By.CSS_SELECTOR, ".pum-close"),
     (By.CSS_SELECTOR, "button[aria-label='Close']"),
     (By.CSS_SELECTOR, "button.close"),
     (By.ID, "close-ad"),
     (By.XPATH, "//button[normalize-space(.)='×' or normalize-space(.)='x' or normalize-space(.)='X']"))

CD = r"(?s)ad will appear|appear in\s*5|\b5\s*[.·…]*\s*4\s*[.·…]*\s*3"

BODY = re.compile(r"ad\b|advert", re.I)


class Ads(Base):

    def open(self):
        return self.go("/ads/")

    def reload(self):
        self.d.refresh()
        self.ck()
        time.sleep(.3)

    def head(self):
        return self.txt(((By.CSS_SELECTOR, "h1"),))

    def tick(self):
        return self.rx(CD, 6)

    def ads(self):
        out = []
        for l in AD:
            try:
                for e in self.d.find_elements(*l):
                    if e.is_displayed() and e.size["width"] > 0 and e.size["height"] > 0:
                        out.append(e)
            except Exception:
                pass
            if out:
                break
        return out

    def ad(self, t=None):
        end = time.time() + (self.w if t is None else t)
        while time.time() < end:
            a = self.ads()
            if a:
                return a[0]
            time.sleep(.2)
        raise AssertionError("реклама не появилась")

    def ad_on(self):
        return len(self.ads()) > 0

    def wait_ad(self, t=25):
        return self.ad(t)

    def kill(self):
        e = self.find(X, 8)
        self.js("arguments[0].click()", e)
        time.sleep(.4)
        return e

    def body(self, a=None):
        a = a or self.ad()
        s = (a.text or "").strip()
        if s:
            return s
        return (a.get_attribute("innerText") or "").strip()[:120]
