from splinter import Browser
from time import sleep


def get_image_urls(url):
    img_urls = []

    def add_new_image_urls(images):
        new_urls = [image['src'] for image in images]
        cleaned_urls = [
            url for url in new_urls
            if url not in img_urls
        ]
        img_urls.extend(cleaned_urls)

    with Browser() as browser:
        def get_current_page():
            return browser.find_by_css('.currentpage').first.text

        browser.visit(url)
        next_page_button = browser.find_by_css('.book_right').first
        prev_page = 'Page -1'
        current_page = get_current_page()
        print('Processing score')
        while current_page != prev_page:
            # Get the score images
            img_elements = browser.find_by_css('img.BRpageimage.BRnoselect')
            # Order left and right pages correctly
            img_elements.sort(key=lambda img: 'left' in img['style'])

            # Add new URLs to master URL list
            add_new_image_urls(img_elements)
            print(current_page)

            next_page_button.click()  # Go to the next page
            sleep(1)  # Allow time for the transition
            # Update pages
            prev_page, current_page = current_page, get_current_page()
    return img_urls
