import time

from selenium.webdriver.common.by import By

from pages.base import Base

BOX = ((By.CSS_SELECTOR, "[data-test='contact-form']"),
       (By.CSS_SELECTOR, "form.contact-form"),
       (By.CSS_SELECTOR, "form.commentsblock"))

TRG = ((By.CSS_SELECTOR, ".popmake-674"),
       (By.ID, "formModal"),
       (By.ID, "form-modal"),
       (By.XPATH, "//*[self::button or self::a][contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'contact')]"),
       (By.XPATH, "//*[self::button or self::a][contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'form')]"))

NAM = ((By.CSS_SELECTOR, "[data-test='contact-form'] input[type='text']"),
       (By.CSS_SELECTOR, "input.grunion-field.name"),
       (By.CSS_SELECTOR, "form input[name$='-name']"))

MAL = ((By.CSS_SELECTOR, "[data-test='contact-form'] input[type='email']"),
       (By.CSS_SELECTOR, "input.grunion-field.email"),
       (By.CSS_SELECTOR, "form input[type='email']"))

MSG = ((By.CSS_SELECTOR, "[data-test='contact-form'] textarea"),
       (By.CSS_SELECTOR, "textarea.grunion-field"),
       (By.CSS_SELECTOR, "form textarea"))

SND = ((By.CSS_SELECTOR, ".contact-submit button"),
       (By.CSS_SELECTOR, "form button[type='submit']"),
       (By.CSS_SELECTOR, "button[type='submit']"),
       (By.XPATH, "//button[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'submit')]"))

OK = ((By.XPATH, "//*[contains(normalize-space(.),'Your message has been sent')]"),
      (By.XPATH, "//*[contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'thank you')]"),
      (By.XPATH, "//*[contains(normalize-space(.),'has been sent')]"),
      (By.XPATH, "//*[contains(normalize-space(.),'message sent')]"))

ER = ((By.CSS_SELECTOR, ".grunion-error"),
      (By.CSS_SELECTOR, ".form-error"),
      (By.CSS_SELECTOR, "[class*='error']"),
      (By.XPATH, "//*[contains(normalize-space(.),'Please fill')]"))


class Frm(Base):

    def open(self, p="/"):
        self.go(p)
        return self.shown()

    def shown(self, t=10):
        if self.has(BOX):
            return True
        if self.has(TRG):
            try:
                self.tap(TRG)
                time.sleep(.6)
            except Exception:
                pass
            if self.has(BOX):
                return True
        try:
            self.js("try{var k=Object.keys(window.pum.popups||{});"
                    "for(var i=0;i<k.length;i++){var p=window.pum.popups[k[i]];"
                    "if(/form|contact|modal/i.test(p.slug||'')){window.pum.openPopup(p.id);return 1}}return 0}"
                    "catch(e){return 0}")
        except Exception:
            pass
        if self.has(BOX):
            return True
        try:
            self.js("var c=document.querySelectorAll('.pum-container');"
                    "for(var i=0;i<c.length;i++){if(c[i].querySelector(\"[data-test='contact-form']\")){"
                    "c[i].style.display='block';c[i].style.visibility='visible';c[i].style.opacity='1';"
                    "var o=c[i].parentElement;if(o){o.style.display='block';o.style.visibility='visible';o.style.opacity='1'}"
                    "return 1}}return 0")
        except Exception:
            pass
        time.sleep(.3)
        return self.has(BOX)

    def nam(self):
        return self.put(NAM, "")

    def put_all(self, n="", m="", t=""):
        self.put(NAM, n)
        self.put(MAL, m)
        return self.put(MSG, t)

    def val_nam(self):
        return (self.at(self.find(NAM), "value") or "").strip()

    def val_msg(self):
        return self.at(self.find(MSG), "value") or ""

    def val_mal(self):
        return (self.at(self.find(MAL), "value") or "").strip()

    def snd(self):
        self.tap(SND)
        time.sleep(1)
        return self.d.current_url

    def ok(self, t=20):
        end = time.time() + t
        while time.time() < end:
            if self.has(OK):
                return True
            try:
                h = self.js("return (document.documentElement.innerHTML||'').toLowerCase()")
                if h and ("has been sent" in h or "thank you" in h):
                    return True
            except Exception:
                pass
            time.sleep(.3)
        return False

    def ok_txt(self, t=6):
        return self.rx(r"your message has been sent|thank you|has been sent", t)

    def err(self):
        return self.has(ER)
