"""LICENSE
Copyright 2015 Hermann Krumrey <hermann@krumreyh.com>

This file is part of manga-dl.

manga-dl is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

manga-dl is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with manga-dl.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""

import logging
import requests
import cfscrape


logger = logging.getLogger(__name__)


def download_image(
        image_url: str,
        file_path: str,
        max_retry: int = 3,
        ignore_ssl_errors: bool = True,
        use_cfscrape: bool = False
):
    """
    Downloads an image file
    :param image_url: The URL to the image
    :param file_path: THe path in which to store the image
    :param max_retry: Maximum number of retries
    :param ignore_ssl_errors: Whether or not to ignore SSL errors
    :param use_cfscrape: Whether or not the site is Cloudflare-protected
    :return: None
    """
    retry_count = 0
    while retry_count < max_retry:
        retry_count += 1

        try:
            if use_cfscrape:
                scraper = cfscrape.create_scraper()
                resp = scraper.get(image_url)
            else:
                resp = requests.get(
                    image_url,
                    headers={"User-Agent": "Mozilla/5.0"}
                )

            if resp.status_code >= 300:
                logger.warning(f"Couldn't download image file {file_path}")
            else:
                with open(file_path, "wb") as f:
                    f.write(resp.content)

                if retry_count > 1:
                    logger.info("Retrying download successful")

                retry_count = max_retry

        except Exception as e:
            logger.warning(f"Failed downloading {image_url}")
            if retry_count >= max_retry:
                logger.error(f"Failed to download {image_url}")
                raise e
