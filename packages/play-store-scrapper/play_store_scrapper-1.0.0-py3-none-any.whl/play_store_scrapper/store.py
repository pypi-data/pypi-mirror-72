import os
from os import path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
import time
import re
import json
from .internals import *
import requests

class PlayStore:
    def __init__(self, web_driver=None):
        self.BASE_URL = "https://play.google.com"
        self.STORE_URL = self.BASE_URL + "/store"
        self.CATEGORY_DETAIL_PAGE_URL = self.STORE_URL + "/apps/category/"
        self.APP_DETAIL_PAGE_URL = self.STORE_URL + "/apps/details?id="
        self.DEV_PAGE_URL = self.STORE_URL + "/apps/dev?id="
        self.TOP_CHARTS_URL = self.STORE_URL + "/apps/top"
        webdriver_path = ""
        if web_driver is None:
            if "GECKO_DRIVER_PATH" in os.environ:
                if path.exists(os.environ["GECKO_DRIVER_PATH"]):
                    webdriver_path = os.environ["GECKO_DRIVER_PATH"]
                else:
                    raise FileNotFoundError(
                        "Speicifed path in GECKO_DRIVER_PATH does not exists."
                    )
            else:
                raise KeyError(
                    "GECKO_DRIVER_PATH is not defined in Environment Variables"
                )
        else:
            if path.exists(web_driver):
                webdriver_path = web_driver
            else:
                raise FileNotFoundError(
                    "Specified path for Web Driver does not exists."
                )
        options = Options()
        options.add_argument("--headless")
        self.webdriver = webdriver.Firefox(
            executable_path=webdriver_path, options=options
        )
        self.webdriver.get(self.STORE_URL)
        self.app_categories = []
        self.game_categories = []
        self.top_charts = {}

    def get_categories(self):

        self.webdriver.get(self.STORE_URL)
        categories_button = self.webdriver.find_element_by_id(
            "action-dropdown-parent-Categories"
        )
        ActionChains(self.webdriver).click(categories_button).perform()
        self.webdriver.implicitly_wait(2)
        categories_divs = self.webdriver.find_elements_by_css_selector(
            "#action-dropdown-children-Categories > div > ul > li > ul"
        )
        apps_cats_links = categories_divs[0].find_elements_by_css_selector("li > a")
        games_cats_links = categories_divs[1].find_elements_by_css_selector("li > a")
        apps_categories = []
        for category in apps_cats_links:
            href = category.get_attribute("href")
            if "/category/" not in str(href):
                continue
            slug_index = href.rindex("/") + 1
            slug = href[slug_index:]
            label = category.text
            apps_categories.append({"slug": slug, "name": label})
        games_categories = []
        for category in games_cats_links:
            href = category.get_attribute("href")
            slug_index = href.rindex("/") + 1
            slug = href[slug_index:]
            label = category.text
            games_categories.append({"slug": slug, "name": label})
        self.game_categories = games_categories
        self.app_categories = apps_categories
        return {"apps": self.app_categories, "games": self.game_categories}

    def get_apps_in_category(self, category_slug, max_apps=100):
        apps = self._get_apps_from_page(self.CATEGORY_DETAIL_PAGE_URL + category_slug)
        return apps

    def get_app_detail(self, app_id):
        APP_URL = self.APP_DETAIL_PAGE_URL + app_id + "&hl=en&gl=us"
        self.webdriver.get(APP_URL)
        page_source = self.webdriver.page_source
        matches = HelperRegex.SCRIPT.findall(page_source)
        res = {}
        for match in matches:
            key_match = HelperRegex.KEY.findall(match)
            value_match = HelperRegex.VALUE.findall(match)
            if key_match and value_match:
                key = key_match[0]
                value = json.loads(value_match[0])

                res[key] = value
        self.webdriver.execute_script("console.log(" + json.dumps(res) + ")")
        result = {}
        for k, spec in ElementSpecs.Detail.items():
            content = spec.extract_content(res)
            if type(content) == str:
                content = str(content).replace('\n', "\\n") \
                                      .replace('\&', "\\&") \
                                      .replace('\r', "\\r") \
                                      .replace('\t', "\\t") \
                                      .replace('\b', "\\b") \
                                      .replace('\f', "\\f")
            result[k] = content

        result["appId"] = app_id
        result["url"] = APP_URL
        result["permissions"] = self.get_app_permissions(app_id)

        self.webdriver.execute_script("console.log(" + json.dumps(result) + ")")
        return result
    
    def get_top_charts(self):
        self.webdriver.get(self.TOP_CHARTS_URL)
        top_h2s = self.webdriver.find_elements_by_css_selector("a[href^='/store/apps/collection/cluster'] > h2")
        top_chart_links = {}
        top_charts = {}
        for h2 in top_h2s:
            if h2.text[:3] == "Top":
                top_link = h2.find_element_by_xpath("./..")
                top_page_link = top_link.get_attribute('href')
                top_chart_links[h2.text] = top_page_link
        for top_chart, link in top_chart_links.items():
            top_charts[top_chart] = self._get_apps_from_page(link)
        self.top_charts = top_charts
        return top_charts
    
    def get_app_permissions(self, appId):
        body = r"f.req=%5B%5B%5B%22xdSrCf%22%2C%22%5B%5Bnull%2C%5B%5C%22"+ appId + r"%5C%22%2C7%5D%2C%5B%5D%5D%5D%22%2Cnull%2C%221%22%5D%5D%5D"
        url = self.BASE_URL + '/_/PlayStoreUi/data/batchexecute?rpcids=qnKhOb&f.sid=-697906427155521722&bl=boq_playuiserver_20190903.08_p0&hl=en&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=1065213'
        response = requests.post(url, data=body, headers={'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'})
        data_input = json.loads(response.text[5:])
        data = json.loads(data_input[0][2])
        common_permission = data[0]
        common = {}
        others = {}
        if len(common_permission) > 0:
            valid_permissions = []
            for permission in common_permission:
                if len(permission) > 0:
                    valid_permissions.append(permission)
            permissions = {}
            for permission in valid_permissions:
                perm_type = permission[3][0]
                name = permission[0]
                perms = []
                for perm in permission[2]:
                    perms.append(perm[1])
                permissions[perm_type] = {'details': perms, 'description': name}
            common = permissions
        other_permission = data[1]
        if len(other_permission) > 0:
            valid_permissions = []
            for permission in other_permission:
                if len(permission) > 0:
                    valid_permissions.append(permission)
            permissions = {}
            for permission in valid_permissions:
                perm_type = permission[3][0]
                name = permission[0]
                perms = []
                for perm in permission[2]:
                    perms.append(perm[1])
                permissions[perm_type] = {'details': perms, 'description': name}
            others = permissions
        return {"common": common, "other": others}

    def done(self):
        self.webdriver.quit()

    def _scroll_to_page_end(self):
        """A method for scrolling the page to the end."""

        # Get scroll height.
        last_height = self.webdriver.execute_script("return document.body.scrollHeight")

        while True:

            # Scroll down to the bottom.
            self.webdriver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )

            # Wait to load the page.
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height.
            new_height = self.webdriver.execute_script(
                "return document.body.scrollHeight"
            )

            if new_height == last_height:

                break

            last_height = new_height

    def _get_apps_from_page(self, page_url):
        self.webdriver.get(page_url)
        self._scroll_to_page_end()
        app_links = self.webdriver.find_elements_by_css_selector(
            "a[href^='/store/apps/details?id=']"
        )
        app_ids = []
        for link in app_links:
            app_id = str(link.get_attribute("href"))[
                46:
            ]  # Strip this part ("https://play.google.com/store/apps/details?id=") of url
            if link.is_displayed() and app_id not in app_ids:
                app_ids.append(app_id)
        return app_ids

