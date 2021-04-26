from tp.settings import IMAGES_URL


def get_ep_a_description(feed_x, episode_x):
    a = f'<h1>{episode_x}</h1>'
    b = f'<img src="{IMAGES_URL}{episode_x.image.name}">'
    c = f'<p>{episode_x.description}</p>'
    d = f'<p>Photo <a href="{feed_x.original_image_url}">'
    e = f'{feed_x.image_title}</a> by <a href="{feed_x.image_attribution_url}">'
    f = f'{feed_x.image_attribution}</a> is licensed <a href="{feed_x.image_license_url}">'
    g = f'{feed_x.image_license_name}</a> {feed_x.image_license_jurisdiction}.</p>'
    h = f'<p>Photo <a href="{episode_x.original_image_url}">'
    i = f'{episode_x.image_title}</a> by <a href="{episode_x.image_attribution_url}">'
    j = f'{episode_x.image_attribution}</a> is licensed <a href="{episode_x.image_license_url}">'
    k = f'{episode_x.image_license_name}</a> {episode_x.image_license_jurisdiction}.</p><p>'
    m = f'<a href="{feed_x.ebook_url}">{feed_x.ebook_title}</a> by '
    o = f'<a href="{feed_x.author_url}">{feed_x.author}</a> '
    p = f'is licensed <a href="{feed_x.license_url}">{feed_x.license_name}</a> '
    q = f'{feed_x.license_jurisdiction}. Translated by <a href="{feed_x.translator_url}">'
    r = f'{feed_x.translator}</a>. '
    s = f'Intro by <a href="{feed_x.intro_author_url}">{feed_x.intro_author}</a>.</p>'
    return f'{a}{b}{c}{d}{e}{f}{g}{h}{i}{j}{k}{m}{o}{p}{q}{r}{s}'
