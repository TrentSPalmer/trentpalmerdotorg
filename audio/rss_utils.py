from tp.settings import IMAGES_URL


def get_rss_item_desc(item):
    a = f'<h1>{item}</h1>'
    b = f'<img src="{IMAGES_URL}{item.image.name}">'
    c = f'<p>{item.description}</p>'

    d = f'<p>Photo <a href="{item.feed.original_image_url}">{item.feed.image_title}</a> by '
    if item.feed.image_attribution_url == '':
        e = f'{item.feed.image_attribution}'
    else:
        e = f'<a href="{item.feed.image_attribution_url}">{item.feed.image_attribution}</a>'
    f = f' is licensed <a href="{item.feed.image_license_url}">{item.feed.image_license_name}</a>'
    g = f' {item.feed.image_license_jurisdiction}.</p>'

    h = f'<p>Photo <a href="{item.original_image_url}">{item.image_title}</a> by '
    if item.image_attribution_url == '':
        i = f'{item.image_attribution}'
    else:
        i = f'<a href="{item.image_attribution_url}">{item.feed.image_attribution}</a>'
    j = f' is licensed <a href="{item.image_license_url}">{item.image_license_name}</a>'
    k = f' {item.image_license_jurisdiction}.</p>'

    m = f'<p><a href="{item.feed.ebook_url}">{item.feed.ebook_title}</a> by '
    n = f'<a href="{item.feed.author_url}">{item.feed.author}</a> '
    o = f'is licensed <a href="{item.feed.license_url}">{item.feed.license_name}</a>'

    if item.feed.translator == '':
        p = ''
    else:
        p = f' Translated by <a href="{item.feed.translator_url}">{item.feed.translator}</a>.'

    if item.feed.intro_author == '':
        q = ''
    else:
        q = f' Intro by <a href="{item.feed.intro_author_url}">{item.feed.intro_author}</a>.'

    r = f' {item.feed.license_jurisdiction}.{p}{q}</p>'

    return f'{a}{b}{c}{d}{e}{f}{g}{h}{i}{j}{k}{m}{n}{o}{r}'
