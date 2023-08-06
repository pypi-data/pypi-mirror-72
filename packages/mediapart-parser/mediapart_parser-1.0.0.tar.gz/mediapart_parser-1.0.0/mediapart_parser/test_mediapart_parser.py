import os
import unittest
from .mediapart_parser import MediapartParser
import tempfile
import shutil
import PyPDF2

mediapart_user_name = os.environ['MEDIAPART_USER_NAME']
mediapart_user_password = os.environ['MEDIAPART_USER_PASSWORD']

class MediapartParserTest(unittest.TestCase):

    def test_instanciation(self):
        parser = MediapartParser(mediapart_user_name, mediapart_user_password)

    def test_get_last_articles_titles(self):
        parser = MediapartParser(mediapart_user_name, mediapart_user_password)
        last_articles_titles = parser.get_last_articles_titles()
        self.assertEqual(10,len(last_articles_titles))

    def test_get_last_articles_categories(self):
        parser = MediapartParser(mediapart_user_name, mediapart_user_password)
        last_articles_categories = parser.get_last_articles_categories()
        self.assertEqual(10,len(last_articles_categories))

    def test_get_last_articles_links(self):
        parser = MediapartParser(mediapart_user_name, mediapart_user_password)
        last_articles_links = parser.get_last_articles_links()
        self.assertEqual(10,len(last_articles_links))

    def test_get_article_id(self):
        parser = MediapartParser(mediapart_user_name, mediapart_user_password)
        article_url = parser.get_last_articles_links()[0]
        identifier = parser.get_article_id(article_url)
        self.assertRegex(identifier,"^[-+]?\d+$")

    def test_download_article(self):
        tests_tmp_folder = tempfile.gettempdir() + "/python_tests"
        parser = MediapartParser(mediapart_user_name, mediapart_user_password)
        article_url = parser.get_last_articles_links()[0]
        article_id = parser.get_article_id(article_url)
        article_path = tests_tmp_folder+"article_"+article_id+".pdf"
        parser.download_article(article_id,article_path)
        self.assertTrue(os.path.exists(article_path))
        try:
            doc = PyPDF2.PdfFileReader(open(article_path, "rb"))
        except PyPDF2.utils.PdfReadError:
            self.fail("test_download_article failed.")

    @classmethod
    def setUpClass(cls):
        tests_tmp_folder = tempfile.gettempdir() + "/python_tests"

        if not os.path.exists(tests_tmp_folder):
            os.makedirs(tests_tmp_folder)
    
    @classmethod
    def tearDownClass(cls):
        tests_tmp_folder = tempfile.gettempdir() + "/python_tests"

        for filename in os.listdir(tests_tmp_folder):
            file_path = os.path.join(tests_tmp_folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print("Failed to delete %s. Reason: %s" % (file_path, e))
    

