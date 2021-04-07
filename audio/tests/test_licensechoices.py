from django.test import SimpleTestCase
from audio.choices import LICENSE_CHOICES, get_license_info

TEST_LICENSE_CHOICES = (
    (1, 'Public Domain'),
    (2, 'Unknown'),
    (3, 'CC BY-SA 2.5'),
    (4, 'CC BY-SA 3.0'),
    (5, 'CC BY 3.0'),
    (6, 'CC BY 1.0'),
    (7, 'CC0 1.0')
)

TEST_LICENSE_INFO = (
    ('Public Domain', 'https://en.wikipedia.org/wiki/Public_domain'),
    ('Unknown', 'https://example.com'),
    ('CC BY-SA 2.5', 'https://creativecommons.org/licenses/by-sa/2.5'),
    ('CC BY-SA 3.0', 'https://creativecommons.org/licenses/by-sa/3.0'),
    ('CC BY 3.0', 'https://creativecommons.org/licenses/by/3.0'),
    ('CC BY 1.0', 'https://creativecommons.org/licenses/by/1.0'),
    ('CC0 1.0', 'https://creativecommons.org/publicdomain/zero/1.0')
)


class LicenseChoicesTestCase(SimpleTestCase):

    def test_license_choices(self):
        self.assertEqual(len(LICENSE_CHOICES), 7)
        for i, x in enumerate(TEST_LICENSE_CHOICES):
            self.assertEqual(TEST_LICENSE_CHOICES[i], LICENSE_CHOICES[i])

    def test_license_info(self):
        for i in range(len(LICENSE_CHOICES)):
            self.assertEqual(get_license_info(i + 1), TEST_LICENSE_INFO[i])
