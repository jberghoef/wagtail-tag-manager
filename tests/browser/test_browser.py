import re
import time

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from tests.factories.tag import (
    tag_lazy_marketing,
    tag_lazy_necessary,
    tag_lazy_statistics,
    tag_lazy_preferences,
    tag_instant_marketing,
    tag_instant_necessary,
    tag_instant_statistics,
    tag_instant_preferences,
)
from wagtail_tag_manager.utils import parse_consent_state


def get_messages_for_log(driver, amount, iterations=5):
    time.sleep(iterations)
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
    time.sleep(iterations)
    while True and iterations > 0:
        for cookie in driver.get_cookies():
            if cookie.get("name") == "wtm":
                return parse_consent_state(cookie.get("value", ""))
        iterations = iterations - 1
        time.sleep(1)


@pytest.mark.django_db
def test_default_necessaryity(driver, site, live_server):
    tag_instant_preferences()
    tag_instant_statistics()
    tag_instant_necessary()
    tag_instant_marketing()
    tag_lazy_preferences()
    tag_lazy_statistics()
    tag_lazy_necessary()
    tag_lazy_marketing()

    driver.get(live_server.url)
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    get_messages_for_log(driver, 4)
    consent_state = get_consent_state(driver)
    assert consent_state.get("necessary") == "true"
    assert consent_state.get("preferences") == "unset"
    assert consent_state.get("statistics") == "true"
    assert consent_state.get("marketing") == "false"

    driver.refresh()
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    get_messages_for_log(driver, 6)
    consent_state = get_consent_state(driver)
    assert consent_state.get("necessary") == "true"
    assert consent_state.get("preferences") == "unset"
    assert consent_state.get("statistics") == "true"
    assert consent_state.get("marketing") == "false"

    checkbox = driver.find_element_by_id("id_marketing")
    checkbox.click()
    submit = driver.find_element_by_css_selector("input[type=submit]")
    submit.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    get_messages_for_log(driver, 8)
    consent_state = get_consent_state(driver)
    assert consent_state.get("necessary") == "true"
    assert consent_state.get("preferences") == "true"
    assert consent_state.get("statistics") == "true"
    assert consent_state.get("marketing") == "true"


@pytest.mark.django_db
def test_necessary_only(driver, site, live_server):
    tag_instant_preferences()
    tag_instant_statistics()
    tag_instant_necessary()
    tag_instant_marketing()
    tag_lazy_preferences()
    tag_lazy_statistics()
    tag_lazy_necessary()
    tag_lazy_marketing()

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

    check_preferences = driver.find_element_by_css_selector(
        ".container #id_preferences"
    )
    check_preferences.click()

    check_statistics = driver.find_element_by_css_selector(".container #id_statistics")
    check_statistics.click()

    # check_marketing = driver.find_element_by_css_selector(".container #id_marketing")
    # check_marketing.click()

    submit = driver.find_element_by_css_selector(".container input[type=submit]")
    submit.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    consent_state = get_consent_state(driver)
    assert consent_state.get("necessary") == "true"
    assert consent_state.get("preferences") == "false"
    assert consent_state.get("statistics") == "false"
    assert consent_state.get("marketing") == "false"


@pytest.mark.django_db
def test_preferences_only(driver, site, live_server):
    tag_instant_preferences()
    tag_instant_statistics()
    tag_instant_necessary()
    tag_instant_marketing()
    tag_lazy_preferences()
    tag_lazy_statistics()
    tag_lazy_necessary()
    tag_lazy_marketing()

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

    # check_preferences = driver.find_element_by_css_selector(".container #id_preferences")
    # check_preferences.click()

    check_statistics = driver.find_element_by_css_selector(".container #id_statistics")
    check_statistics.click()

    # check_marketing = driver.find_element_by_css_selector(".container #id_marketing")
    # check_marketing.click()

    submit = driver.find_element_by_css_selector(".container input[type=submit]")
    submit.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    consent_state = get_consent_state(driver)
    assert consent_state.get("necessary") == "true"
    assert consent_state.get("preferences") == "true"
    assert consent_state.get("statistics") == "false"
    assert consent_state.get("marketing") == "false"


@pytest.mark.django_db
def test_statistics_only(driver, site, live_server):
    tag_instant_preferences()
    tag_instant_statistics()
    tag_instant_necessary()
    tag_instant_marketing()
    tag_lazy_preferences()
    tag_lazy_statistics()
    tag_lazy_necessary()
    tag_lazy_marketing()

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

    check_preferences = driver.find_element_by_css_selector(
        ".container #id_preferences"
    )
    check_preferences.click()

    # check_statistics = driver.find_element_by_css_selector(".container #id_statistics")
    # check_statistics.click()

    # check_marketing = driver.find_element_by_css_selector(".container #id_marketing")
    # check_marketing.click()

    submit = driver.find_element_by_css_selector(".container input[type=submit]")
    submit.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    consent_state = get_consent_state(driver)
    assert consent_state.get("necessary") == "true"
    assert consent_state.get("preferences") == "false"
    assert consent_state.get("statistics") == "true"
    assert consent_state.get("marketing") == "false"


@pytest.mark.django_db
def test_marketing_only(driver, site, live_server):
    tag_instant_preferences()
    tag_instant_statistics()
    tag_instant_necessary()
    tag_instant_marketing()
    tag_lazy_preferences()
    tag_lazy_statistics()
    tag_lazy_necessary()
    tag_lazy_marketing()

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

    check_preferences = driver.find_element_by_css_selector(
        ".container #id_preferences"
    )
    check_preferences.click()

    check_statistics = driver.find_element_by_css_selector(".container #id_statistics")
    check_statistics.click()

    check_marketing = driver.find_element_by_css_selector(".container #id_marketing")
    check_marketing.click()

    submit = driver.find_element_by_css_selector(".container input[type=submit]")
    submit.click()
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "wtm_cookie_bar"))
        )
    except TimeoutException:
        pass

    consent_state = get_consent_state(driver)
    assert consent_state.get("necessary") == "true"
    assert consent_state.get("preferences") == "false"
    assert consent_state.get("statistics") == "false"
    assert consent_state.get("marketing") == "true"
