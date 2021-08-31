# About
This is the source code for [trentpalmer.org](https://trentpalmer.org),
a [Django](https://www.djangoproject.com/) web app for hosting podcasts
or audiobooks serialized as podcasts.
Inspired by [David Collins-Rivera](https://hackerpublicradio.org/eps.php?id=1933),
who serializes his audiobooks as [podcasts](https://stardrifter.podbean.com/).

# Listening
Using a podcast client is strongly encouraged because of the obvious limitations
of trying to listen in the web browser. Although I do at some point intend to include
a [PWA](https://en.wikipedia.org/wiki/Progressive_web_application),
in the future, probably using either [flutter-web](https://flutter.dev/web)
or [react](https://reactjs.org/).

**Paste the rss link into a podcast client application.**

Every podcast (or audiobook) has an associated rss feed which you can paste into
a podcast client. My personal preference is [AntennaPod](https://antennapod.org/).

Django has a built-in syndication app for generating the rss feeds, which I find
delightful to work with once you get the hang of it.

# Recording
I record to [Audacity](https://www.audacityteam.org/) on a refurbished
[Dell Optiplex 3010](https://www.amazon.com/Dell-3010-Performance-Certified-Refurbished/dp/B07C3H4KSX/0),
which has an [Ivy Bridge](https://en.wikipedia.org/wiki/Ivy_Bridge_(microarchitecture))
Core i5 cpu, running [Gentoo Linux](https://www.gentoo.org/), 
with the [XFCE Desktop Environment](https://www.xfce.org/), using a
[Samson Meteor](https://www.amazon.com/Samson-Meteor-Studio-Condenser-Microphone/dp/B004MF39YS)
usb condensor microphone.

It would certainly be possible to configure the website to allow additional contributors, and/or
build the rss feeds such that they could be listed in iTunes, or Google Podcasts, or Spotify.

# Additional Django Apps
* [django-bootstrap](https://pypi.org/project/django-bootstrap4/)
* [django-crispyforms](https://pypi.org/project/django-crispy-forms/)
* [django-storages](https://pypi.org/project/django-storages/)

# Hosting
For now, the website is deployed on [Arch Linux](https://archlinux.org/),
using Arch Linux python packages,
with the static assets in
[minio](https://min.io/), which is an
[s3-compatible object store](https://en.wikipedia.org/wiki/Amazon_S3).

# Logging
I have added a
[custom logging handler](https://github.com/TrentSPalmer/trentpalmerdotorg/blob/master/tp/sendxmpp_handler.py)
using [sendxmpp](https://sendxmpp.hostname.sk/),
because [Prosody](https://prosody.im/) is far easier to setup than in comparison to
an email server. The relevant settings are in
[tp/logging_settings.py](https://github.com/TrentSPalmer/trentpalmerdotorg/blob/master/tp/logging_settings.py),
called from [tp/settings.py](https://github.com/TrentSPalmer/trentpalmerdotorg/blob/master/tp/settings.py).
