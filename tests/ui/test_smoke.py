import re

import pytest
from playwright.sync_api import expect

from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.contact_page import ContactPage

@pytest.mark.smoke
def test_smoke_search_pliers(page):
    """Goal: verify product search.
    Precondition: none.
    Expected: every displayed product name contains pliers."""
    home = HomePage(page).open().search("pliers")

    expect(home.search_completed).to_be_visible()

    names = home.product_names.all_inner_texts()

    assert names, "Search returned no products"
    assert all("pliers" in name.lower() for name in names), names

@pytest.mark.smoke
def test_smoke_add_product_to_cart(page):
    """Goal: verify add-to-cart.
    Precondition: Claw Hammer exists.
    Expected: cart badge displays 3."""
    product = (
        HomePage(page)
        .open()
        .open_product("Claw Hammer")
        .add_to_cart(quantity=3)
    )

    expect(product.cart_quantity).to_have_text("3")

@pytest.mark.smoke
def test_smoke_login_invalid_credentials(page):
    """Goal: verify invalid login is rejected.
    Precondition: the email does not belong to an account.
    Expected: error message appears and URL remains at login."""
    login = (
        LoginPage(page)
        .open()
        .login(
            "nobody-here@example.com",
            "Wrong-Password-123"
        )
    )

    expect(login.error).to_contain_text(
        "Invalid email or password"
    )

    expect(page).to_have_url(
        re.compile(r"/auth/login$")
    )

@pytest.mark.smoke
def test_smoke_contact_form_empty_validation(page):
    """Goal: verify empty contact form validation.
    Precondition: none.
    Expected: subject and message required errors appear."""
    contact = ContactPage(page).open().submit()

    expect(
        contact.errors.filter(has_text="Subject is required")
    ).to_be_visible()

    expect(
        contact.errors.filter(has_text="Message is required")
    ).to_be_visible()

