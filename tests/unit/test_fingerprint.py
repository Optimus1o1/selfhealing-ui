import pytest
from selfheal.baseline.fingerprint import ElementFingerprint, BoundingBox


def test_fingerprint_sanitizes_passwords():
    raw_attrs = {
        "id": "pwdField",
        "name": "password",
        "type": "password",
        "value": "super_secret_password_123",
        "auth_token": "bearer_xyz_789",
        "placeholder": "Enter secret",
        "data-testid": "login-pwd"
    }

    sanitized = ElementFingerprint.sanitize_attributes(raw_attrs)

    # Password value and token must be stripped!
    assert "value" not in sanitized
    assert "auth_token" not in sanitized
    # type="password" is safe and informative
    assert sanitized.get("type") == "password"
    assert sanitized.get("data-testid") == "login-pwd"


def test_fingerprint_db_roundtrip():
    fp = ElementFingerprint(
        target_key="auth.submit",
        version=1,
        status="active",
        tag_name="button",
        element_id="loginBtn",
        class_list=["btn", "btn-primary"],
        inner_text="Sign In",
        aria_role="button",
        accessible_name="Sign In",
        input_type="submit",
        attributes={"name": "submitBtn", "data-testid": "auth-btn"},
        parent_tag="form",
        parent_id="loginForm",
        parent_classes=["form-horizontal"],
        children_count=1,
        children_tags=["span"],
        bounding_box=BoundingBox(x=150.0, y=250.0, width=120.0, height=45.0),
        page_url="/login",
        original_selector="#loginBtn"
    )

    row = fp.to_db_row()
    restored = ElementFingerprint.from_db_row(row)

    assert restored.target_key == fp.target_key
    assert restored.tag_name == fp.tag_name
    assert restored.element_id == fp.element_id
    assert restored.class_list == ["btn", "btn-primary"]
    assert restored.bounding_box.x == 150.0
    assert restored.bounding_box.width == 120.0
    assert restored.attributes["data-testid"] == "auth-btn"
