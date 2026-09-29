import time

import allure

from pages.modals import NO, OK, POP, TXT, Mod


@allure.feature("Modals")
@allure.story("Позитивные тесты")
def test_modals_page_opens(pg):
    m = pg(Mod)
    with allure.step("открываю /modals/"):
        m.open()
        h = m.head()
    assert "modal" in h.lower()


@allure.feature("Modals")
@allure.story("Позитивные тесты")
def test_all_trigger_buttons_are_visible(pg):
    m = pg(Mod)
    m.open()
    with allure.step("ищу кнопки-триггеры"):
        k = m.trigs()
    for x in ("simple", "confirm", "image"):
        assert x in k, "нет триггера %s, найдено %s" % (x, k)


@allure.feature("Modals")
@allure.story("Позитивные тесты")
def test_simple_modal_opens_with_title(pg):
    m = pg(Mod)
    m.open()
    with allure.step("кликаю Simple Modal"):
        p = m.openk("simple")
        t = m.ttl(p)
    assert "simple" in t.lower()


@allure.feature("Modals")
@allure.story("Позитивные тесты")
def test_simple_modal_shows_its_text(pg):
    m = pg(Mod)
    m.open()
    with allure.step("читаю текст простой модалки"):
        p = m.openk("simple")
        b = m.body(p)
    assert "modal" in b.lower()


@allure.feature("Modals")
@allure.story("Позитивные тесты")
def test_simple_modal_closes_by_cross(pg):
    m = pg(Mod)
    m.open()
    with allure.step("открываю и закрываю крестиком"):
        m.openk("simple")
        m.kill()
    assert m.gone(POP, 8), "модалка не закрылась"


@allure.feature("Modals")
@allure.story("Позитивные тесты")
def test_confirm_modal_opens(pg):
    m = pg(Mod)
    m.open()
    with allure.step("кликаю Confirm Modal"):
        p = m.openk("confirm")
        t = m.ttl(p)
    assert "confirm" in t.lower()


@allure.feature("Modals")
@allure.story("Позитивные тесты")
def test_confirm_modal_closes_by_ok(pg):
    m = pg(Mod)
    m.open()
    with allure.step("жму OK"):
        p = m.openk("confirm")
        b = m.btn(OK, p)
        assert b is not None, "нет кнопки OK"
        m.js("arguments[0].click()", b)
    assert m.gone(POP, 8), "OK не закрыл модалку"


@allure.feature("Modals")
@allure.story("Позитивные тесты")
def test_confirm_modal_closes_by_cancel(pg):
    m = pg(Mod)
    m.open()
    with allure.step("жму Cancel"):
        p = m.openk("confirm")
        b = m.btn(NO, p)
        assert b is not None, "нет кнопки Cancel"
        m.js("arguments[0].click()", b)
    assert m.gone(POP, 8), "Cancel не закрыл модалку"


@allure.feature("Modals")
@allure.story("Позитивные тесты")
def test_image_modal_contains_picture(pg):
    m = pg(Mod)
    m.open()
    with allure.step("кликаю Image Modal"):
        p = m.openk("image")
        i = m.img(p)
    assert i is not None, "в модалке нет картинки"


@allure.feature("Modals")
@allure.story("Негативные тесты")
def test_no_modal_is_visible_on_page_load(pg):
    m = pg(Mod)
    m.open()
    with allure.step("смотрю страницу до кликов"):
        on = m.pop_on()
    assert not on


@allure.feature("Modals")
@allure.story("Негативные тесты")
def test_closed_modal_stays_hidden(pg):
    m = pg(Mod)
    m.open()
    with allure.step("открываю, закрываю и жду пару секунд"):
        m.openk("simple")
        m.kill()
        time.sleep(2)
    assert not m.pop_on(), "модалка вылезла снова"


@allure.feature("Modals")
@allure.story("Негативные тесты")
def test_click_inside_modal_does_not_close_it(pg):
    m = pg(Mod)
    m.open()
    with allure.step("открываю модалку и кликаю по её содержимому"):
        p = m.openk("simple")
        b = m.btn(TXT, p)
        assert b is not None, "нет содержимого модалки"
        m.js("arguments[0].click()", b)
    assert m.pop_on(), "клик по содержимому закрыл модалку"


@allure.feature("Modals")
@allure.story("Негативные тесты")
def test_repeated_clicks_open_single_popup(pg):
    m = pg(Mod)
    m.open()
    with allure.step("жму на триггер три раза"):
        m.t("simple")
        m.t("simple")
        m.t("simple")
        n = len(m.pops())
    assert n <= 1, "видно сразу %d окон" % n
