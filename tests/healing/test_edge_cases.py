import pytest
from selfheal.engine.page import SelfHealingPage
from selfheal.detection.exceptions import UnhealableFailureError
from demo_app.app import DemoServer


def test_hidden_element_rejected_without_healing(
    healed_page: SelfHealingPage,
    demo_server: DemoServer
):
    base_url = f"http://{demo_server.host}:{demo_server.port}"
    healed_page.goto(f"{base_url}/edge_cases")

    # Element exists in DOM but is display: none.
    # Framework must NOT attempt healing. It must escalate as actionability failure.
    with pytest.raises(UnhealableFailureError) as exc_info:
        healed_page.healed_locator("#hiddenButton", key="edge.hidden").click(timeout=1000)

    assert "ELEMENT_HIDDEN" in str(exc_info.value)


def test_disabled_element_rejected_without_healing(
    healed_page: SelfHealingPage,
    demo_server: DemoServer
):
    base_url = f"http://{demo_server.host}:{demo_server.port}"
    healed_page.goto(f"{base_url}/edge_cases")

    # Element exists in DOM but is disabled.
    # Framework must NOT attempt healing. It must escalate as actionability failure.
    with pytest.raises(UnhealableFailureError) as exc_info:
        healed_page.healed_locator("#disabledButton", key="edge.disabled").click(timeout=1000)

    assert "ELEMENT_DISABLED" in str(exc_info.value)


def test_ambiguous_locator_rejected_without_healing(
    healed_page: SelfHealingPage,
    demo_server: DemoServer
):
    base_url = f"http://{demo_server.host}:{demo_server.port}"
    healed_page.goto(f"{base_url}/edge_cases")

    # Locator matches multiple elements (2 duplicate buttons)
    with pytest.raises(UnhealableFailureError) as exc_info:
        healed_page.healed_locator(".ambiguous-btn", key="edge.ambiguous").click(timeout=1000)

    assert "AMBIGUOUS_LOCATOR" in str(exc_info.value)

