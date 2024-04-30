from conftest import APP_URL
from playwright.sync_api import Page, expect


def test_startup(page: Page):
    page.goto(APP_URL)
    expect(page).not_to_have_title("404")
