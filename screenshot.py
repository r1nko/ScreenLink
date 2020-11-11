from time import sleep

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class WebScreenshot():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("window-size=1980,1080")
    path = '/Users/retwish/Downloads/chromedriver'
    link = ''

    def get_screenshot(self, link, static='on', file_name='image'):
        driver = webdriver.Chrome(executable_path=self.path, chrome_options=self.options)
        if 'https://' not in link:
            link = 'https://' + link
        driver.get(link)
        sleep(5)

        if static == 'off':
            driver.execute_script("""
            let a = document.querySelectorAll('body *')
            a.forEach(function(item){
                let styless = getComputedStyle(item);
                if (styless.position === 'fixed') {
                    item.remove();
            };
            });
            """)
        driver.find_element_by_tag_name('body').screenshot('screenshots/' + str(file_name) + '.png')
        driver.quit()
        print('Captured!')


