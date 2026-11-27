import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from main import long_break

scenarios('features/pomodoro_breaks.feature')


@pytest.fixture
def context():
    return {}


@given(parsers.parse("номер текущего цикла равен {cycle:d}"))
def set_cycle(context, cycle):
    context["cycle"] = cycle


@when(parsers.parse("запрашивается перерыв с периодичностью {every:d} и длинным интервалом {minutes:d} минут"))
def request_break(context, every, minutes):
    context["result"] = long_break(cycle=context["cycle"], every=every, minutes=minutes)


@then(parsers.parse("длительность перерыва должна составлять {expected_minutes:d} минут"))
def verify_break(context, expected_minutes):
    assert context["result"] == expected_minutes
