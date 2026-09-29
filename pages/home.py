from selenium.webdriver.common.by import By

from pages.base import Base

SEC = ((By.XPATH, "//*[self::h1 or self::h2 or self::h3 or self::h4][contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'automation tool')]"),
       (By.XPATH, "//*[self::h1 or self::h2 or self::h3 or self::h4][contains(translate(normalize-space(.),'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'),'tool')]"))

GRID = ((By.CSS_SELECTOR, ".entry-content a.wp-block-button__link"),
        (By.CSS_SELECTOR, ".entry-content .wp-block-button a"),
        (By.CSS_SELECTOR, "main a[href*='practice-automation.com']"),
        (By.CSS_SELECTOR, "main a"),
        (By.CSS_SELECTOR, ".entry-content a"))


class Hm(Base):

    def open(self):
        return self.go("/")

    def tools(self):
        for l in SEC:
            h = self.find0(l)
            if h:
                for x in ("./ancestor::*[.//ul or .//ol][1]", "./ancestor::div[1]", "./parent::*"):
                    try:
                        box = h.find_element(By.XPATH, x)
                    except Exception:
                        continue
                    out = self._t(box.find_elements(By.CSS_SELECTOR, "li,a"))
                    if len(out) > 2:
                        return out
        return self._t(self.d.find_elements(*GRID[0])) or self._t(self.d.find_elements(*GRID[1]))

    def _t(self, els):
        out = []
        for e in els:
            try:
                if not e.is_displayed():
                    continue
                s = " ".join((e.text or "").split())
            except Exception:
                continue
            if s and s not in out:
                out.append(s)
        return out

    def line(self):
        return ", ".join(self.tools())
