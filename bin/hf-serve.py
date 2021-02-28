#!/usr/bin/env python

import json
import logging
import subprocess
from typing import List, Set

import streamlit

logger = logging.getLogger("hf-serve")


class Hf:
    """Wrapper for hf command"""

    @classmethod
    def images_by_tags(cls, tags: str) -> List[str]:
        """hf grep"""
        cmd = ["hf", "grep"] + tags.split()
        logger.info(cmd)
        stdout = subprocess.run(cmd, capture_output=True).stdout.decode()
        return stdout.strip().split()

    @classmethod
    def show(cls, object: str) -> dict:
        """hf show --json"""
        cmd = ["hf", "show", "--json", object]
        logger.info(cmd)
        stdout = subprocess.run(cmd, capture_output=True).stdout.decode()
        return json.loads(stdout)

    @classmethod
    def add_tags(cls, id: int, tags: Set[str]):
        """hf tags add ..."""
        if len(tags) == 0:
            logger.info("Skip add_tags")
            return
        cmd = ["hf", "tags", "add", str(id)]
        for t in tags:
            cmd += ["-t", t]
        logger.info(cmd)
        subprocess.run(cmd)

    @classmethod
    def del_tags(cls, id: int, tags: Set[str]):
        """hf tags add ..."""
        if len(tags) == 0:
            logger.info("Skip del_tags")
            return
        cmd = ["hf", "tags", "del", str(id)]
        for t in tags:
            cmd += ["-t", t]
        logger.info(cmd)
        subprocess.run(cmd)


tags = streamlit.text_input("Filtering by Tags")
if tags:
    images = Hf.images_by_tags(tags)
    if len(images) == 0:
        streamlit.error(f"No Images for `{tags}`")
    else:
        # preview
        streamlit.write(f"{len(images)} Images for `{tags}`")
        idx = streamlit.number_input(
            "index", min_value=1, max_value=len(images), step=1
        )
        img = images[idx - 1]
        streamlit.image(img)

        detail = Hf.show(img)

        # tag editing
        tags = detail["tags"]
        tags_user = streamlit.text_input("tags", value=" ".join(tags)).split()
        tags_add = set(tags_user) - set(tags)
        tags_del = set(tags) - set(tags_user)
        Hf.add_tags(detail["id"], tags_add)
        Hf.del_tags(detail["id"], tags_del)

        # show detail for debugging
        streamlit.write(detail)
