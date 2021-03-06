import unittest

from src.utils.scraping import get_article_text, get_driver

# Before running these tests make sure you have a firefox selenium driver container running
# sudo docker run -d --rm --name standalone-firefox -p 4444:4444 -p 5900:5900 --shm-size 2g selenium/standalone-firefox-debug:3.141.59

class Test_get_articles(unittest.TestCase):
    
    def setUp(self):
        self.driver = get_driver()
        self.links_correct = ['https://statcore.co.uk/']
        self.links_broken = ['https://statcore.co.uk/', 'hfdakfndaf']

    def test_one_correct(self):
        result = get_article_text(self.links_correct, self.driver, pause_time = 4)
        self.assertTrue(result['links_worked'][0] == self.links_correct[0])
        self.assertTrue('We provide innovative ways to help you use your data more effectively' in result['articles'][0])
        self.assertTrue(len(result['links_failed']) == 0)

    def test_one_correct_one_broken(self):
        result = get_article_text(self.links_broken, self.driver, pause_time = 4)
        self.assertTrue(result['links_worked'][0] == 'https://statcore.co.uk/')
        self.assertTrue('We provide innovative ways to help you use your data more effectively' in result['articles'][0])
        self.assertTrue(result['links_failed'][0] == 'hfdakfndaf')

    def test_article_limit(self):
        result = get_article_text(self.links_broken, self.driver, pause_time = 4, article_limit = 1)
        self.assertTrue(len(result['links_worked']) == 1)
        self.assertTrue(len(result['links_failed']) == 0)

    def tearDown(self):
        self.driver.close()

if __name__ == '__main__':
    unittest.main()