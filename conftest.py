import pytest
import allure
from pathlib import Path
from playwright.sync_api import sync_playwright

# ========================================================================
# PYTEST + PLAYWRIGHT TEST CONFIGURATION FILE
# ========================================================================
# Options such as --browser, --headed, --base-url, --video, --screenshot
# and --tracing are provided by the pytest-playwright plugin, so they are
# NOT registered here again. Set their values in pytest.ini.
# ========================================================================

REPORTS_DIR = Path("reports")
VIDEOS_DIR = REPORTS_DIR / "videos"
TRACES_DIR = REPORTS_DIR / "traces"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"


def pytest_addoption(parser):
    """No custom options needed; pytest-playwright already provides them."""
    pass


def get_config_value(config, option_name, default=None):
    """Read an option registered by a plugin; return default if it is None."""
    value = config.getoption(option_name, default=default)
    return default if value is None else value


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Stores the result of each phase and attaches a screenshot when a test fails."""
    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    # Attach a screenshot to the test body as soon as the test fails
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            try:
                allure.attach(
                    page.screenshot(full_page=True),
                    name="Failure screenshot",
                    attachment_type=allure.attachment_type.PNG,
                )
            except Exception as e:
                print(f"[WARN] Could not capture screenshot: {e}")


# ----------------------------------------------------------------------------
# FIXTURE 1 - BROWSER CONTEXT
# ----------------------------------------------------------------------------
@pytest.fixture(scope="function")
def browser_context(request, browser_name):
    """
    Starts Playwright, launches the browser and creates a context.
    `browser_name` comes from pytest-playwright (a plain string, e.g. 'chromium').
    """
    headed_flag = get_config_value(request.config, "headed", False)
    video_option = get_config_value(request.config, "video", "off")

    print(f"[OK] Starting browser: {browser_name}")
    print(f"[OK] Headless mode: {not headed_flag} (headed={headed_flag})")

    playwright = sync_playwright().start()

    browser_type = getattr(playwright, browser_name.lower(), None)
    if browser_type is None:
        playwright.stop()
        raise ValueError(f"[FAIL] Unsupported browser: {browser_name}")

    browser = browser_type.launch(headless=not headed_flag)

    context_args = {}
    if video_option in ["on", "retain-on-failure"]:
        VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
        context_args["record_video_dir"] = str(VIDEOS_DIR)

    context = browser.new_context(**context_args)

    yield context

    print("[CLEANUP] Closing browser context and stopping Playwright...")
    context.close()
    browser.close()
    playwright.stop()


# ----------------------------------------------------------------------------
# FIXTURE 2 - PAGE + ARTIFACT HANDLING
# ----------------------------------------------------------------------------
@pytest.fixture(scope="function")
def page(request, browser_context):
    """
    Creates a page, opens the base URL, and handles trace / screenshot /
    video artifacts after the test.
    """
    base_url = get_config_value(request.config, "--base-url")
    screenshot_option = get_config_value(request.config, "screenshot", "off")
    tracing_option = get_config_value(request.config, "tracing", "off")
    video_option = get_config_value(request.config, "video", "off")

    print(f"[INFO] Navigating to: {base_url}")

    if tracing_option in ["on", "retain-on-failure"]:
        print("[TRACE] Tracing enabled - capturing screenshots and actions")
        browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = browser_context.new_page()
    if base_url:
        page.goto(base_url)

    yield page

    # ------------------------------------------------------------------------
    # After the test
    # ------------------------------------------------------------------------
    test_name = request.node.name.replace("[", "_").replace("]", "")
    test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed

    print(f"[RESULT] Test '{test_name}' result: {'[FAIL]' if test_failed else '[PASS]'}")

    # Screenshot saved to disk (the Allure attachment is done in the hook above)
    if screenshot_option == "on" or (test_failed and screenshot_option == "only-on-failure"):
        SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
        screenshot_path = SCREENSHOTS_DIR / f"{test_name}.png"
        page.screenshot(path=str(screenshot_path))
        print(f"[SAVE] Screenshot saved: {screenshot_path}")

    # Trace: save only when requested, otherwise discard
    if tracing_option in ["on", "retain-on-failure"]:
        if tracing_option == "on" or test_failed:
            TRACES_DIR.mkdir(parents=True, exist_ok=True)
            trace_path = TRACES_DIR / f"{test_name}_trace.zip"
            browser_context.tracing.stop(path=str(trace_path))
            print(f"[SAVE] Trace saved: {trace_path}")
        else:
            browser_context.tracing.stop()

    # Video: the file is only complete after the page is closed
    video = page.video
    try:
        page.close()
    except Exception as e:
        print(f"[WARN] Could not close page cleanly: {e}")
        video = None

    if video:
        try:
            video_path = Path(video.path())
            if video_option == "on" or (test_failed and video_option == "retain-on-failure"):
                if video_path.exists():
                    allure.attach.file(
                        str(video_path),
                        name=f"{test_name}_video",
                        attachment_type=allure.attachment_type.WEBM,
                    )
                    print("[ATTACH] Video attached to Allure report")
            else:
                # Passed test with retain-on-failure: remove the recording
                video_path.unlink(missing_ok=True)
        except Exception as e:
            print(f"[WARN] Could not process video: {e}")