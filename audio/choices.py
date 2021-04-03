LICENSE_CHOICES = [
    (1, 'Public Domain'),
    (2, 'Unknown'),
    (3, 'CC BY-SA 2.5'),
    (4, 'CC BY-SA 3.0'),
    (5, 'CC BY 3.0'),
    (6, 'CC BY 1.0'),
    (7, 'CC0 1.0')
]


def get_license_info(x):
    if x == 1:
        return ('Public Domain', 'https://en.wikipedia.org/wiki/Public_domain')
    if x == 2:
        return ('Unknown', 'https://example.com')
    if x == 3:
        return ('CC BY-SA 2.5', 'https://creativecommons.org/licenses/by-sa/2.5')
    if x == 4:
        return ('CC BY-SA 3.0', 'https://creativecommons.org/licenses/by-sa/3.0')
    if x == 5:
        return ('CC BY 3.0', 'https://creativecommons.org/licenses/by/3.0')
    if x == 6:
        return ('CC BY 1.0', 'https://creativecommons.org/licenses/by/1.0')
    if x == 7:
        return ('CC0 1.0', 'https://creativecommons.org/publicdomain/zero/1.0')
