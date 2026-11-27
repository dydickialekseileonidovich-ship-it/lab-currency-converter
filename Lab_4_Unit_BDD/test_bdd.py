import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from main import work_session, short_break, long_break

scenarios('features/pomodoro_breaks.feature')


@pytest.fixture
def context():
    return {}


@given("используются стандартные настройки таймера")
def default_settings(context):
    context.clear()


@when("запрашивается рабочая сессия и короткий перерыв по умолчанию")
def request_defaults(context):
    context["work"] = work_session()
    context["short"] = short_break()


@then(parsers.parse("рабочая сессия длится {work_min:d} минут, а короткий перерыв {short_min:d} минут"))
def verify_defaults(context, work_min, short_min):
    assert context["work"] == work_min
    assert context["short"] == short_min


@given(parsers.parse("номер текущего цикла равен {cycle:d}"))
def set_cycle(context, cycle):
    context["cycle"] = cycle


@when(parsers.parse("запрашивается перерыв с периодичностью {every:d} и длинным интервалом {minutes:d} минут"))
def request_break(context, every, minutes):
    context["result"] = long_break(cycle=context["cycle"], every=every, minutes=minutes)


@then(parsers.parse("длительность перерыва должна составлять {expected_minutes:d} минут"))
def verify_break(context, expected_minutes):
    assert context["result"] == expected_minutes


@when("запрашивается перерыв с обработкой ошибки")
def request_break_expecting_error(context):
    try:
        long_break(cycle=context["cycle"])
        context["error"] = None
    except Exception as exc:
        context["error"] = exc


@then("возникает ошибка валидации ValueError")
def verify_value_error(context):
    assert isinstance(context["error"], ValueError)
