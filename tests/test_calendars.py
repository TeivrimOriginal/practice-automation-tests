import re

import allure

from pages.calendars import FD, IN, PAN, SB, Cal

DT = re.compile(r"(\d{1,2}[/\-.]\d{1,2}[/\-.]\d{2,4})|(\d{4}-\d{2}-\d{2})")


@allure.feature("Calendars")
@allure.story("Позитивные тесты")
def test_page_opens_and_shows_three_date_inputs(pg):
    c = pg(Cal)
    with allure.step("открываю /calendars/"):
        c.open()
        h = c.head()
    assert "calendar" in h.lower()
    with allure.step("ищу три поля даты"):
        n = c.ins()
    assert n == [1, 2, 3]


@allure.feature("Calendars")
@allure.story("Позитивные тесты")
def test_top_form_date_field_is_empty(pg):
    c = pg(Cal)
    c.open()
    with allure.step("беру поле формы выбора даты"):
        e = c.find(FD)
    assert (c.at(e, "value") or "").strip() == ""


@allure.feature("Calendars")
@allure.story("Позитивные тесты")
def test_datepicker1_opens_after_click(pg):
    c = pg(Cal)
    c.open()
    with allure.step("кликаю по первому полю"):
        p = c.op(1)
    assert p.is_displayed()
    assert c.pan_on()


@allure.feature("Calendars")
@allure.story("Позитивные тесты")
def test_datepicker1_day_click_fills_the_input(pg):
    c = pg(Cal)
    c.open()
    with allure.step("выбираю день 15 в первом календаре"):
        v = c.setd(1, 15)
    assert v != ""


@allure.feature("Calendars")
@allure.story("Позитивные тесты")
def test_datepicker1_value_contains_selected_day(pg):
    c = pg(Cal)
    c.open()
    with allure.step("выбираю день 15 и проверяю формат значения"):
        v = c.setd(1, 15)
    assert "15" in v
    assert DT.search(v), "значение не похоже на дату: %r" % v


@allure.feature("Calendars")
@allure.story("Позитивные тесты")
def test_datepicker1_next_arrow_switches_month(pg):
    c = pg(Cal)
    c.open()
    with allure.step("открываю календарь и запоминаю заголовок"):
        c.op(1)
        a = c.cap()
        c.nx(1)
        b = c.cap()
    assert a and b and a != b, "заголовок не сменился: %r" % a


@allure.feature("Calendars")
@allure.story("Позитивные тесты")
def test_datepicker1_prev_arrow_returns_to_start_month(pg):
    c = pg(Cal)
    c.open()
    with allure.step("листаю вперёд и назад"):
        c.op(1)
        a = c.cap()
        c.nx(1)
        c.nx(-1)
        b = c.cap()
    assert a == b


@allure.feature("Calendars")
@allure.story("Позитивные тесты")
def test_datepicker2_opens_after_click(pg):
    c = pg(Cal)
    c.open()
    with allure.step("кликаю по второму полю"):
        p = c.op(2)
    assert p.is_displayed()


@allure.feature("Calendars")
@allure.story("Позитивные тесты")
def test_datepicker2_close_button_hides_picker(pg):
    c = pg(Cal)
    c.open()
    with allure.step("открываю второй календарь"):
        c.op(2)
        b = c.close_b()
        assert b is not None, "нет кнопки закрытия"
        c.js("arguments[0].click()", b)
    assert c.gone(PAN, 8), "пикер не скрылся"


@allure.feature("Calendars")
@allure.story("Позитивные тесты")
def test_datepicker3_day_click_fills_the_input(pg):
    c = pg(Cal)
    c.open()
    with allure.step("выбираю день 20 в третьем календаре"):
        v = c.setd(3, 20)
    assert v != ""
    assert "20" in v


@allure.feature("Calendars")
@allure.story("Негативные тесты")
def test_no_picker_is_visible_before_click(pg):
    c = pg(Cal)
    c.open()
    with allure.step("смотрю на страницу до клика"):
        on = c.pan_on()
    assert not on


@allure.feature("Calendars")
@allure.story("Негативные тесты")
def test_empty_form_cannot_be_submitted(pg):
    c = pg(Cal)
    c.open()
    with allure.step("жму Submit с пустой датой"):
        e = c.find(FD)
        assert (c.at(e, "value") or "").strip() == ""
        c.tap(SB)
    with allure.step("смотрю, что сервер не сказал «отправлено»"):
        ok = c.sent(5)
        why = c.vmsg(e) or ("ошибка на странице" if c.err() else "пусто")
    assert not ok, "пустая форма принята сервером (%s)" % why


@allure.feature("Calendars")
@allure.story("Негативные тесты")
def test_month_navigation_without_pick_keeps_field_empty(pg):
    c = pg(Cal)
    c.open()
    with allure.step("листаю месяцы, ничего не выбирая"):
        c.op(1)
        c.nx(1)
        c.nx(1)
        c.nx(-1)
        v = c.val(1)
    assert v == ""


@allure.feature("Calendars")
@allure.story("Негативные тесты")
def test_unselectable_day_does_not_fill_the_input(pg):
    c = pg(Cal)
    c.open()
    with allure.step("открываю календарь и ищу заблокированные дни"):
        c.op(1)
        d = c.dead()
        if d:
            c.js("arguments[0].click()", d[0])
            v = c.val(1)
            assert v == "", "заблокированный день записался в поле: %r" % v
        else:
            assert c.val(1) == ""


@allure.feature("Calendars")
@allure.story("Негативные тесты")
def test_garbage_text_is_not_turned_into_a_date(pg):
    c = pg(Cal)
    c.open()
    s = "не дата"
    with allure.step("ввожу мусор в поле и убираю фокус"):
        c.put(IN[1], s)
        c.js("document.body.click()")
    v = c.val(1)
    assert not DT.search(v), "из мусора получилась дата: %r" % v
