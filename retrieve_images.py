from urllib.request import urlretrieve


def retrieve_images(img_urls, dir='/tmp'):
    print('Retrieving images')
    image_dirs = []
    for i, img_src in enumerate(img_urls[1:-1]):
        image_dir = '{}/page-{}.jpg'.format(dir, i)
        urlretrieve(img_src, image_dir)
        print(image_dir)
        image_dirs.append(image_dir)
    return image_dirs
