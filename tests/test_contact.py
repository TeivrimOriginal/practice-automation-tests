import allure

from pages.contact import BOX, Frm
from pages.home import Hm

MAIL = "qa@example.com"


@allure.feature("Contact form")
@allure.story("Позитивные тесты")
@allure.title("Поле Message заполняется списком из раздела Automation Tools")
def test_message_field_gets_automation_tools_list(pg):
    h = pg(Hm)
    f = pg(Frm)
    with allure.step("открываю главную и собираю список раздела Automation Tools"):
        h.open()
        tools = h.tools()
        assert tools, "раздел Automation Tools не найден"
        line = ", ".join(tools)
    with allure.step("открываю форму обратной связи"):
        assert f.open("/"), "форма не открылась"
    with allure.step("заполняю Name, Email и Message списком через запятую"):
        f.put_all("QA Bot", MAIL, line)
        v = f.val_msg()
    assert v == line, "в Message не тот список"
    assert "," in v and len(tools) > 1


@allure.feature("Contact form")
@allure.story("Позитивные тесты")
def test_form_is_reachable_from_modals_page(pg):
    f = pg(Frm)
    with allure.step("открываю /modals/ и ищу форму"):
        f.open("/modals/")
    assert f.has(BOX), "формы на странице модалок нет"


@allure.feature("Contact form")
@allure.story("Позитивные тесты")
def test_form_sends_and_shows_confirmation(pg):
    f = pg(Frm)
    with allure.step("заполняю и отправляю форму"):
        assert f.open(), "форма не открылась"
        f.put_all("QA Bot", MAIL, "Проверка отправки сообщения")
        f.snd()
    with allure.step("жду подтверждение отправки"):
        ok = f.ok(25)
    assert ok, "сообщение об успешной отправке не появилось"


@allure.feature("Contact form")
@allure.story("Позитивные тесты")
def test_long_message_is_accepted(pg):
    f = pg(Frm)
    s = "A" * 900
    with allure.step("вставляю длинный текст в Message"):
        assert f.open(), "форма не открылась"
        f.put_all("QA Bot", MAIL, s)
        v = f.val_msg()
    assert len(v) == 900


@allure.feature("Contact form")
@allure.story("Негативные тесты")
def test_empty_required_name_blocks_submission(pg):
    f = pg(Frm)
    with allure.step("отправляю форму с пустым Name"):
        assert f.open(), "форма не открылась"
        f.put_all("", MAIL, "Пустое имя")
        f.snd()
    with allure.step("проверяю, что успеха нет"):
        ok = f.ok(6)
    assert not ok, "форма отправилась без обязательного Name"


@allure.feature("Contact form")
@allure.story("Негативные тесты")
def test_empty_form_does_not_send_anything(pg):
    f = pg(Frm)
    with allure.step("жму Submit на пустой форме"):
        assert f.open(), "форма не открылась"
        f.snd()
        ok = f.ok(6)
    assert not ok, "пустая форма отправилась"
