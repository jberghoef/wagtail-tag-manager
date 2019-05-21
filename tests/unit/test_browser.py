import pytest
import re
import time
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from wagtail_tag_manager.utils import parse_consent_state

from tests.factories.tag import (
    tag_lazy_delayed,
    tag_lazy_traceable,
    tag_instant_delayed,
    tag_lazy_analytical,
    tag_lazy_functional,
    tag_instant_traceable,
    tag_instant_analytical,
    tag_instant_functional,
)


def get_messages_for_log(driver, amount, iterations=5):
    log = driver.get_log("browser")
    while len(log) < amount and iterations > 0:
        log = driver.get_log("browser")
        iterations = iterations - 1
        time.sleep(1)

    messages = []
    for item in log:
        search = re.search(r"\"(.+)\"", item.get("message"))
        if search:
            messages.append(search.group(1))

    assert len(messages) == amount
    return messages

def get_consent_state(driver, iterations=5):
    while True and iterations > 0:
        cookies = driver.get_cookies()
        for cookie in driver.get_cookies():
            if cookie.get("name") == "wtm":
                return parse_consent_state(cookie.get("value", ""))
        iterations = iterations - 1
        time.sleep(1)

@pytest.mark.django_db
def test_default_functionality(driver, site, live_server):
    tag_instant_analytical()
    tag_instant_delayed()
    tag_instant_functional()
    tag_instant_traceable()
    tag_lazy_analytical()
    tag_lazy_delayed()
    tag_lazy_functional()
    tag_lazy_traceable()

    driver.get(live_server.url)
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    messages = get_messages_for_log(driver, 4)
    consent_state = get_consent_state(driver)
    assert consent_state.get("functional") == "true"
    assert consent_state.get("analytical") == "unset"
    assert consent_state.get("delayed") == "true"
    assert consent_state.get("traceable") == "false"

    driver.refresh()
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    messages = get_messages_for_log(driver, 6)
    consent_state = get_consent_state(driver)
    assert consent_state.get("functional") == "true"
    assert consent_state.get("analytical") == "unset"
    assert consent_state.get("delayed") == "true"
    assert consent_state.get("traceable") == "false"

    checkbox = driver.find_element_by_id("id_traceable")
    checkbox.click()
    submit = driver.find_element_by_css_selector("input[type=submit]")
    submit.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    messages = get_messages_for_log(driver, 8)
    consent_state = get_consent_state(driver)
    assert consent_state.get("functional") == "true"
    assert consent_state.get("analytical") == "true"
    assert consent_state.get("delayed") == "true"
    assert consent_state.get("traceable") == "true"


@pytest.mark.django_db
def test_functional_only(driver, site, live_server):
    tag_instant_analytical()
    tag_instant_delayed()
    tag_instant_functional()
    tag_instant_traceable()
    tag_lazy_analytical()
    tag_lazy_delayed()
    tag_lazy_functional()
    tag_lazy_traceable()

    driver.get(live_server.url)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    link = driver.find_element_by_css_selector("li.manage-link a")
    link.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    check_analytical = driver.find_element_by_css_selector(".container #id_analytical")
    check_analytical.click()

    check_delayed = driver.find_element_by_css_selector(".container #id_delayed")
    check_delayed.click()

    # check_traceable = driver.find_element_by_css_selector(".container #id_traceable")
    # check_traceable.click()

    submit = driver.find_element_by_css_selector(".container input[type=submit]")
    submit.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    consent_state = get_consent_state(driver)
    assert consent_state.get("functional") == "true"
    assert consent_state.get("analytical") == "false"
    assert consent_state.get("delayed") == "false"
    assert consent_state.get("traceable") == "false"

@pytest.mark.django_db
def test_analytical_only(driver, site, live_server):
    tag_instant_analytical()
    tag_instant_delayed()
    tag_instant_functional()
    tag_instant_traceable()
    tag_lazy_analytical()
    tag_lazy_delayed()
    tag_lazy_functional()
    tag_lazy_traceable()

    driver.get(live_server.url)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    link = driver.find_element_by_css_selector("li.manage-link a")
    link.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    # check_analytical = driver.find_element_by_css_selector(".container #id_analytical")
    # check_analytical.click()

    check_delayed = driver.find_element_by_css_selector(".container #id_delayed")
    check_delayed.click()

    # check_traceable = driver.find_element_by_css_selector(".container #id_traceable")
    # check_traceable.click()

    submit = driver.find_element_by_css_selector(".container input[type=submit]")
    submit.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    consent_state = get_consent_state(driver)
    assert consent_state.get("functional") == "true"
    assert consent_state.get("analytical") == "true"
    assert consent_state.get("delayed") == "false"
    assert consent_state.get("traceable") == "false"

@pytest.mark.django_db
def test_delayed_only(driver, site, live_server):
    tag_instant_analytical()
    tag_instant_delayed()
    tag_instant_functional()
    tag_instant_traceable()
    tag_lazy_analytical()
    tag_lazy_delayed()
    tag_lazy_functional()
    tag_lazy_traceable()

    driver.get(live_server.url)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    link = driver.find_element_by_css_selector("li.manage-link a")
    link.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    check_analytical = driver.find_element_by_css_selector(".container #id_analytical")
    check_analytical.click()

    # check_delayed = driver.find_element_by_css_selector(".container #id_delayed")
    # check_delayed.click()

    # check_traceable = driver.find_element_by_css_selector(".container #id_traceable")
    # check_traceable.click()

    submit = driver.find_element_by_css_selector(".container input[type=submit]")
    submit.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    consent_state = get_consent_state(driver)
    assert consent_state.get("functional") == "true"
    assert consent_state.get("analytical") == "false"
    assert consent_state.get("delayed") == "true"
    assert consent_state.get("traceable") == "false"


@pytest.mark.django_db
def test_traceable_only(driver, site, live_server):
    tag_instant_analytical()
    tag_instant_delayed()
    tag_instant_functional()
    tag_instant_traceable()
    tag_lazy_analytical()
    tag_lazy_delayed()
    tag_lazy_functional()
    tag_lazy_traceable()

    driver.get(live_server.url)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    link = driver.find_element_by_css_selector("li.manage-link a")
    link.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    check_analytical = driver.find_element_by_css_selector(".container #id_analytical")
    check_analytical.click()

    check_delayed = driver.find_element_by_css_selector(".container #id_delayed")
    check_delayed.click()

    check_traceable = driver.find_element_by_css_selector(".container #id_traceable")
    check_traceable.click()

    submit = driver.find_element_by_css_selector(".container input[type=submit]")
    submit.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    consent_state = get_consent_state(driver)
    assert consent_state.get("functional") == "true"
    assert consent_state.get("analytical") == "false"
    assert consent_state.get("delayed") == "false"
    assert consent_state.get("traceable") == "true"
