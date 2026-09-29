import re
import time

import allure

from pages.ads import AD, X, Ads


@allure.feature("Ads")
@allure.story("Позитивные тесты")
def test_ads_page_opens(pg):
    a = pg(Ads)
    with allure.step("открываю /ads/"):
        a.open()
        h = a.head()
    assert "ad" in h.lower()


@allure.feature("Ads")
@allure.story("Позитивные тесты")
def test_countdown_message_is_shown(pg):
    a = pg(Ads)
    a.open()
    with allure.step("ищу текст с отсчётом"):
        t = a.tick()
    assert t, "текст отсчёта не найден"


@allure.feature("Ads")
@allure.story("Позитивные тесты")
def test_countdown_shows_whole_sequence(pg):
    a = pg(Ads)
    a.open()
    with allure.step("ищу последовательность 5-4-3-2-1"):
        t = a.tick()
    assert re.search(r"5\D*4\D*3\D*2\D*1", t or ""), "нет полного отсчёта: %r" % t


@allure.feature("Ads")
@allure.story("Позитивные тесты")
def test_ad_appears_after_countdown(pg):
    a = pg(Ads)
    a.open()
    with allure.step("жду появления рекламы"):
        e = a.wait_ad(30)
    assert e.is_displayed()


@allure.feature("Ads")
@allure.story("Позитивные тесты")
def test_ad_has_visible_content(pg):
    a = pg(Ads)
    a.open()
    with allure.step("проверяю, что реклама не пустая"):
        e = a.wait_ad(30)
        t = a.body(e)
    assert t, "в рекламном блоке нет текста"


@allure.feature("Ads")
@allure.story("Позитивные тесты")
def test_ad_close_button_is_inside_ad_block(pg):
    a = pg(Ads)
    a.open()
    with allure.step("ищу рекламу и её крестик"):
        e = a.wait_ad(30)
        x = a.find(X)
    assert a.js("return arguments[0].contains(arguments[1])", e, x), "крестик не внутри рекламного блока"


@allure.feature("Ads")
@allure.story("Позитивные тесты")
def test_ad_can_be_closed(pg):
    a = pg(Ads)
    a.open()
    with allure.step("закрываю рекламу крестиком"):
        a.wait_ad(30)
        a.kill()
    assert a.gone(AD, 10), "реклама не закрылась"


@allure.feature("Ads")
@allure.story("Позитивные тесты")
def test_page_usable_after_ad_closed(pg):
    a = pg(Ads)
    a.open()
    with allure.step("закрываю рекламу и кликаю по заголовку"):
        a.wait_ad(30)
        a.kill()
        h = a.head()
    assert h and "ad" in h.lower()


@allure.feature("Ads")
@allure.story("Позитивные тесты")
def test_ad_appears_again_after_reload(pg):
    a = pg(Ads)
    a.open()
    with allure.step("закрываю рекламу и перезагружаю страницу"):
        a.wait_ad(30)
        a.kill()
        a.reload()
        e = a.wait_ad(30)
    assert e.is_displayed()


@allure.feature("Ads")
@allure.story("Негативные тесты")
def test_ad_is_not_visible_right_after_load(pg):
    a = pg(Ads)
    a.open()
    with allure.step("сразу после загрузки смотрю на рекламу"):
        on = a.ad_on()
    assert not on, "реклама была сразу"


@allure.feature("Ads")
@allure.story("Негативные тесты")
def test_ad_is_not_visible_before_countdown_ends(pg):
    a = pg(Ads)
    a.open()
    with allure.step("жду 3 секунды и проверяю рекламу"):
        time.sleep(3)
        on = a.ad_on()
    assert not on, "реклама слишком рано"


@allure.feature("Ads")
@allure.story("Негативные тесты")
def test_ad_does_not_return_after_close(pg):
    a = pg(Ads)
    a.open()
    with allure.step("закрываю и жду 6 секунд"):
        a.wait_ad(30)
        a.kill()
        time.sleep(6)
    assert not a.ad_on(), "закрытая реклама вылезла снова"


@allure.feature("Ads")
@allure.story("Негативные тесты")
def test_only_one_ad_block_visible(pg):
    a = pg(Ads)
    a.open()
    with allure.step("считаю видимые рекламные блоки"):
        a.wait_ad(30)
        n = len(a.ads())
    assert n == 1, "видно %d рекламных блоков" % n
