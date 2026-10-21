def pytest_addoption(parser):
    parser.addoption(
        "--headless", action="store_true", help="Run UI tests without a browser window"
    )
    parser.addoption("--browser", choices=["chrome", "edge"], default="chrome")
    parser.addoption(
        "--screenshot-on-failure", action="store_true", help="Save failed UI screenshots locally"
    )
