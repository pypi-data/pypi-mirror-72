# MIT License. This file is part of telegram_me.
#
# Copyright (c) 2020 Hearot
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from typing import Optional

import attr
import requests
from lxml import html


TELEGRAM_BIO_XPATH = "//div[starts-with(@class, 'tgme_page_description')]"
TELEGRAM_LINK_TEMPLATE = "https://t.me/{username}"
TELEGRAM_NAME_XPATH = "//div[@class='tgme_page_title']/span"
TELEGRAM_PHOTO_XPATH = "//img[@class='tgme_page_photo_image']/@src"


@attr.s(auto_attribs=True)
class Link:
    bio: Optional[str]
    image: Optional[str]
    name: Optional[str]
    username: str

    @classmethod
    def from_username(cls, username: str) -> "Link":
        username = username.strip("@")

        page = requests.get(TELEGRAM_LINK_TEMPLATE.format(username=username))
        tree = html.fromstring(page.text)

        bio = tree.xpath(TELEGRAM_BIO_XPATH)
        bio = bio[0].text_content().strip() if bio else None

        image = tree.xpath(TELEGRAM_PHOTO_XPATH)
        image = image[0].strip() if image else None

        name = tree.xpath(TELEGRAM_NAME_XPATH)
        name = name[0].text_content().strip() if name else None

        return cls(bio, image, name, username)
