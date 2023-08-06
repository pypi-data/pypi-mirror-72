import feedparser
import requests
import time
import os
from .mediapart_constants import Global
from .mediapart_constants import Login
from bs4 import BeautifulSoup
from requests import Session


class MediapartParser:

    mediapart_user = ""
    mediapart_pwd = ""

    def __init__(self, user, pwd):
        self.mediapart_user = user
        self.mediapart_pwd = pwd

    def __get_rss_entries(self):
        mediapart_parsed_rss = feedparser.parse(
            "https://www.mediapart.fr/articles/feed")
        last_articles = mediapart_parsed_rss.entries
        return last_articles

    def __load_article_page(self, url):
        s = Session()
        login_data = {
            Login.CONNECTION_USER_NAME: self.mediapart_user,
            Login.CONNECTION_USER_PASSWORD: self.mediapart_pwd,
            "op": Login.OP_STRING_FRENCH
            }
        s.post(Login.LOGIN_PAGE_FRENCH, login_data)
        page = s.get(url)
        return page

    def __write_page_content_in_file(self, final_file_path, page):
        f = open(final_file_path, 'wb')
        f.write(page.content)
        f.close()

        while not os.path.exists(final_file_path):
            time.sleep(1)

    def get_last_articles_links(self):
        """Returns a list containing all articles
        links available from the RSS feed."""

        all_links = []
        last_articles = self.__get_rss_entries()
        for article in last_articles:
            for link in article.links:
                all_links.append(link.href)
        return all_links

    def get_last_articles_titles(self):
        """Return a list containing all articles
        titles available from the RSS feed."""

        titles = []
        last_articles = self.__get_rss_entries()
        for article in last_articles:
            titles.append(article.title)
        return titles

    def get_last_articles_categories(self):
        """Returns a list containing all articles
        categories available from the RSS feed."""

        categories = []
        last_articles = self.__get_rss_entries()
        for article in last_articles:
            categories.append(article.tags[0].term)
        return categories

    def get_article_id(self, article_url):
        """Resolves the article's unique identifier.

        Parameters:
            article_url -- the url of the article

        Returns:
            article's unique identifier
        """
        page = requests.get(
            article_url,
            auth=(self.mediapart_user, self.mediapart_pwd))
        soup = BeautifulSoup(page.text, "html.parser")
        result = soup.find("div", {"class": "sub-header accur8-desktop accur8-tablet accurWidth-desktop accurWidth-tablet"})
        return result["data-nid"]

    def download_article(self, article_id, file_path):
        """Resolves the article's PDF url and download it on the disk.

        Parameters:
            article_id -- the unique identifier of the article
            (can be retrieved using get_article_id)
            file_path -- the path on the disk where
            you want the article to be written
        
        Returns:
            None
        """

        # resolve article pdf complete url
        url = Global.PDF_ARTICLE_BASE_URL + str(article_id)

        # load the page
        page = self.__load_article_page(url)

        # finaly write page content in a file
        self.__write_page_content_in_file(file_path, page)
