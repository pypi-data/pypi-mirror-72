import json
import os
import time
from io import BytesIO
from os.path import dirname, exists
from sys import platform
from urllib.parse import urlparse, parse_qs
from zipfile import ZipFile

import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options

import requests

with open(f"{dirname(__file__)}/chrome.json") as _:
    urls = json.load(_)


STATUS_CODES = {
    '400': "UNKOWN ERROR",
    '404': "RESULTS NOT FOUND",
    '100': "ALREADY DONE",
    '101': "DECIDED NOT TO",
    '500': "TIME OUT",
    '200': "OK",
}


def CheckChrome():
    """
    Checks if there is a portable version of chrome and it's driver downloaded to the folder this package is in.

    :return: A tuple of booleans denoting what's downloaded - (chrome, chromedriver)
    """
    if platform == "win32":
        return (
            exists(f"{dirname(__file__)}/chrome-win/chrome.exe"),
            exists(f"{dirname(__file__)}/chromedriver_win32/chromedriver.exe")
        )
    elif platform == "linux":
        return (
            exists(f"{dirname(__file__)}/chrome-linux/chrome"),
            exists(f"{dirname(__file__)}/chromedriver_linux64/chromedriver")
        )
    elif platform == "darwin":
        return (
            exists(f"{dirname(__file__)}/chrome-mac/Chromium.app/Contents/MacOS/Chromium"),
            exists(f"{dirname(__file__)}/chromedriver_mac64/chromedriver")
        )


def RecChmod(path, mode):
    """
    Simple wrapper for os.chmod that runs it in recursive mode.

    :param path: File or directory to change the permissions for.
    :param mode: Permissions to set in octal form - eg. 0o777 (the 0o tells Python it's an octal number)
    :return:
    """
    os.chmod(path, mode)
    for dirpath, dirnames, filenames in os.walk(path):
        for dirname in dirnames:
            os.chmod("/".join([dirpath, dirname]), mode)
        for filename in filenames:
            os.chmod("/".join([dirpath, filename]), mode)


def DownloadExtractZip(url, path):
    """
    Downloads a zip file and extracts it's contents to the specified path.

    :param url: Link to the file to download
    :param path: Location to extract the contents to
    :return:
    """
    response = requests.get(url)
    response.raise_for_status()
    zip_file = ZipFile(BytesIO(response.content))
    zip_file.extractall(path)


def InstallWin():
    """
    NOTE: Use this if you're using Windows
    Runs CheckChrome() and downloads a build of chromium and it's driver if needed.

    The location it downloads the software from is defined in chrome.json

    :return:
    """
    chrome, chromium = CheckChrome()

    if not chrome:
        print("Downloading Chrome")
        DownloadExtractZip(urls["win32"]["chrome"], f"{dirname(__file__)}")
    if not chromium:
        print("Downloading ChromeDriver")
        DownloadExtractZip(urls["win32"]["chromedriver"], f"{dirname(__file__)}")


def InstallMac():
    """
    NOTE: Use this if you're using MacOS
    Runs CheckChrome() and downloads a build of chromium and it's driver if needed.

    The location it downloads the software from is defined in chrome.json

    :return:
    """
    chrome, chromium = CheckChrome()
    if not chrome:
        print("Downloading Chrome")
        DownloadExtractZip(urls["mac"]["chrome"], f"{dirname(__file__)}")
        RecChmod(f"{dirname(__file__)}/chrome-mac/Chromium.app/Contents/MacOS/Chromium", 0o777)
    if not chromium:
        print("Downloading ChromeDriver")
        DownloadExtractZip(urls["mac"]["chromedriver"], f"{dirname(__file__)}")
        RecChmod(f"{dirname(__file__)}/chromedriver_mac64/chromedriver", 0o777)


def InstallLinux():
    """
    NOTE: Use this if you're using Linux
    Runs CheckChrome() and downloads a build of chromium and it's driver if needed.

    The location it downloads the software from is defined in chrome.json

    :return:
    """
    chrome, chromium = CheckChrome()
    if not chrome:
        print("Downloading Chrome")
        DownloadExtractZip(urls["linux"]["chrome"], f"{dirname(__file__)}")
        RecChmod(f"{dirname(__file__)}/chrome-linux/chrome", 0o777)
    if not chromium:
        print("Downloading ChromeDriver")
        DownloadExtractZip(urls["linux"]["chromedriver"], f"{dirname(__file__)}")
        try:
            RecChmod(f"{dirname(__file__)}/chromedriver_linux64/chromedriver", 0o777)
        except:
            pass


def Install():
    """
    Runs CheckChrome() and downloads a build of chromium and it's driver if needed.

    The location it downloads the software from is defined in chrome.json

    :return:
    """
    if platform == "win32":
        InstallWin()
    elif platform == "linux":
        InstallLinux()
    elif platform == "darwin":
        InstallLinux()


def OpenBrowser(options: selenium.webdriver.chrome.options.Options = None, cookie_path=None):
    """
    Opens a Selenium connected browser with the designated options and path to the cookies.

    Makes a check and downloads chrome if necessary.

    :param options:
    :param cookie_path:
    :return:
    """
    if options is None:
        options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-logging')
    if cookie_path:
        os.makedirs(cookie_path, exist_ok=True)
        options.add_argument(f'--user-data-dir={cookie_path}')

    if platform == "win32":
        InstallWin()
        options.binary_location = f"{dirname(__file__)}/chrome-win/chrome.exe"
        chromedriver = f"{dirname(__file__)}/chromedriver_win32/chromedriver.exe"
    elif platform == "linux":
        InstallLinux()
        options.binary_location = f"{dirname(__file__)}/chrome-linux/chrome"
        chromedriver = f"{dirname(__file__)}/chromedriver_linux64/chromedriver"
    elif platform == "darwin":
        InstallMac()
        options.binary_location = f"{dirname(__file__)}/chrome-mac/Chromium.app/Contents/MacOS/Chromium"
        chromedriver = f"{dirname(__file__)}/chromedriver_mac64/chromedriver"
    else:
        raise RuntimeError("Unknown platform")
    driver = webdriver.Chrome(chromedriver, options=options)
    driver.set_page_load_timeout(15)
    return driver


def WaitForLoad(element, timeout=5.):
    """
    Waits until an element has been fully loaded (both enabled and displayed).

    :param element: Element to wait for
    :param timeout: How long to wait before raising an error
    :return:
    """
    start = time.time()
    while not element.is_displayed() or not element.is_enabled():
        assert (time.time() - start) < timeout


def WaitForFind(source, by, value, timeout=5.):
    """
    Looks for an element using the source.find_element(by, value) method.

    Waits until it actually finds an element

    :param source: Element or driver to look into
    :param by: How to look for it (see the documentation for selenium's webdriver.find_element())
    :param value: The value of the thing you want to find
    :param timeout: How long to wait before raising an error
    :return: The element it finds
    """
    start = time.time()
    while True:
        assert (time.time() - start) < timeout
        try:
            return source.find_element(by, value)
        except NoSuchElementException:
            pass


def WaitForFindLoad(source, by, value, timeout=5.):
    """
    Combines WaitForLoad() and WaitForFind() to one function.

    Looks for an element using the source.find_element(by, value) method.
    Then
    Waits until that element has been fully loaded (both enabled and displayed).

    :param source: Element or driver to look into
    :param by: How to look for it (see the documentation for selenium's webdriver.find_element())
    :param value: The value of the thing you want to find
    :param timeout: How long to wait before raising an error
    :return: The element it finds
    """
    start = time.time()
    while True:
        assert (time.time() - start) < timeout
        try:
            element = source.find_element(by, value)
            break
        except NoSuchElementException:
            pass
    WaitForLoad(element, timeout + start - time.time())
    return element


def CloseOtherTabs(driver, keep_tab=0):
    """
    Closes all tabs but the specified tab (default 0)

    :param keep_tab: The index of the tab to keep (default 0)
    :param driver: The selenium driver
    :return:
    """
    for tab in driver.window_handles[:keep_tab] + driver.window_handles[(keep_tab + 1):]:
        driver.switch_to.window(tab)
        driver.close()
    driver.switch_to.window(driver.window_handles[0])


def SolveCaptcha(api_key, site_key, url):
    """
    Uses the 2Captcha service to solve Captcha's for you.

    Captcha's are held in iframes; to solve the captcha, you need a part of the url of the iframe. The iframe is usually
    inside a div with id=gRecaptcha. The part of the url we need is the query parameter k, this is called the site_key:

    www.google.com/recaptcha/api2/anchor?ar=1&k=6LcleDIUAAAAANqkex-vX88sMHw8FXuJQ3A4JKK9&co=aHR0cHM6Ly93d3cuZGljZS5jb206NDQz&hl=en&v=oqtdXEs9TE9ZUAIhXNz5JBt_&size=normal&cb=rpcg9w84syix
                                              k=6LcleDIUAAAAANqkex-vX88sMHw8FXuJQ3A4JKK9

    Here the site_key is 6LcleDIUAAAAANqkex-vX88sMHw8FXuJQ3A4JKK9

    You also need to supply the url of the current page you're on.

    This function will return a string with the response key from captcha validating the test. This needs to be inserted
    into an input field with the id=g-recaptcha-response.

    :param api_key: The 2Captcha API key.
    :param site_key: The site_key extracted from the Captcha iframe url
    :param url: url of the site you're on
    :return: the response from captcha validating the test
    """
    print("Solving Captcha...")
    print("Sending Request...")
    request_response = requests.get("https://2captcha.com/in.php?", params={
        "googlekey": site_key,
        "method": "userrecaptcha",
        "pageurl": url,
        "key": api_key,
        "json": 1,
        "invisible": 0,
    })
    request_response.raise_for_status()
    print("Waiting for Response...")
    time.sleep(30)
    answer_response_json = {'status': 0, 'request': 'CAPCHA_NOT_READY'}
    while answer_response_json['request'] == 'CAPCHA_NOT_READY':
        answer_response = requests.get("https://2captcha.com/res.php", params={
            "key": api_key,
            "action": "get",
            "id": request_response.json()['request'],
            "json": 1
        })
        answer_response_json = answer_response.json()
        print(answer_response_json)
        time.sleep(5)
    if answer_response_json['status'] == 1:
        print("Solved!")
        return answer_response_json['request']
    elif answer_response_json['request'] == 'ERROR_CAPTCHA_UNSOLVABLE':
        raise TimeoutError("ERROR_CAPTCHA_UNSOLVABLE")
    else:
        raise Exception(answer_response_json['request'])


def FindSolveCaptcha(api_key, driver, form):
    """
    Finds and solves Captchas using the 2Captcha service. When this function is done running, the captcha will be solved
    (not visibly), and you can submit the form.

    Handles errors if there is no captcha present.

    Captcha's are generally tied to a form, to solve the captcha, we nee the form that it's inside.

    The webdriver is also required to finish solving the captcha.

    :param api_key: The 2Captcha API key.
    :param driver: The webdriver controlling the browser
    :param form: The form that houses the captcha
    :return:
    """
    try:
        captcha_div = form.find_element_by_id("gRecaptcha")
        assert captcha_div.is_displayed(), '102'
        captcha_iframe = captcha_div.find_element_by_tag_name("iframe")
        assert captcha_iframe.is_displayed(), '102'
        captcha_src = urlparse(captcha_iframe.get_attribute("src"))
        assert captcha_src, '102'
        captcha_query = parse_qs(captcha_src.query)
        assert captcha_query, '102'
        captcha_sitekey = captcha_query['k'][0]
    except NoSuchElementException:
        return '102'
    except AssertionError as x:
        return x.args[0]
    else:
        solution = SolveCaptcha(api_key, captcha_sitekey, driver.current_url)
        captcha_answer = captcha_div.find_element_by_id("g-recaptcha-response")
        driver.execute_script(f"arguments[0].innerText = '{solution}'", captcha_answer)


def QueryEncode(q: dict):
    """

    :param q:
    :return:
    """
    return "?" + "&".join(["=".join(entry) for entry in q.items()])



