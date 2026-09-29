import os
import re
import time

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as CO
from selenium.webdriver.chrome.service import Service as CS
from selenium.webdriver.firefox.options import Options as FO
from selenium.webdriver.firefox.service import Service as FS

ROOT = os.path.dirname(os.path.abspath(__file__))
SHOTS = os.path.join(ROOT, "shots")
NAME = os.path.join(ROOT, "allure-results")


def pytest_addoption(parser):
    parser.addoption("--br", action="store", default="chrome", help="chrome|firefox|edge")
    parser.addoption("--headful", action="store_true", default=False)
    parser.addoption("--base", action="store", default="https://practice-automation.com")
    parser.addoption("--w", action="store", type=float, default=12.0)


@pytest.fixture(scope="session")
def cfg(request):
    return request.config


def mk(br, head):
    if br == "firefox":
        o = FO()
        o.add_argument("--width=1600")
        o.add_argument("--height=1200")
        o.set_preference("dom.webnotifications.enabled", False)
        o.set_preference("toolkit.testing.slowMo", 0)
        if not head:
            o.add_argument("-headless")
        d = webdriver.Firefox(options=o, service=FS(log_output=os.devnull))
    else:
        o = CO()
        o.add_argument("--window-size=1600,1200")
        o.add_argument("--lang=en-US")
        o.add_argument("--no-sandbox")
        o.add_argument("--disable-gpu")
        o.add_argument("--disable-dev-shm-usage")
        o.add_argument("--disable-search-engine-choice-screen")
        o.add_argument("--disable-notifications")
        o.add_argument("--disable-popup-blocking")
        o.add_argument("--remote-allow-origins=*")
        o.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36")
        if not head:
            o.add_argument("--headless=new")
        if br == "edge":
            d = webdriver.Edge(options=o, service=CS(log_output=os.devnull))
        else:
            d = webdriver.Chrome(options=o, service=CS(log_output=os.devnull))
    d.set_page_load_timeout(90)
    d.implicitly_wait(0)
    return d


@pytest.fixture
def d(request):
    c = request.config
    drv = mk(c.getoption("--br"), c.getoption("--headful"))
    drv.base = c.getoption("--base")
    drv.w = c.getoption("--w")
    yield drv
    try:
        drv.quit()
    except Exception:
        pass


@pytest.fixture
def pg(d):
    def mk_(cls, *a, **kw):
        return cls(d, d.base, d.w, *a, **kw)
    return mk_


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    r = yield
    rep = r.get_result()
    setattr(item, "rep", rep)
    drv = item.funcargs.get("d")
    if drv is None or rep.when != "call":
        return
    try:
        allure.attach((drv.title + "  |  " + drv.current_url).encode("utf-8", "replace"),
                      name="page", attachment_type=allure.attachment_type.TEXT, extension="txt")
    except Exception:
        pass
    if not rep.failed:
        return
    n = re.sub(r"[^A-Za-z0-9_.-]", "_", item.nodeid)[-110:]
    p = os.path.join(SHOTS, time.strftime("%H%M%S") + "_" + n + ".png")
    try:
        os.makedirs(SHOTS, exist_ok=True)
        drv.save_screenshot(p)
        with open(p, "rb") as f:
            allure.attach(f.read(), name=os.path.basename(p),
                          attachment_type=allure.attachment_type.PNG, extension="png")
    except Exception:
        pass
    try:
        allure.attach(drv.page_source.encode("utf-8", "replace"), name="page.html",
                      attachment_type=allure.attachment_type.TEXT, extension="html")
    except Exception:
        pass
