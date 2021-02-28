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
    @streamlit.cache
    def tags(cls) -> List[str]:
        """All tags"""
        cmd = ["hf", "tags"]
        logger.info(cmd)
        stdout = subprocess.run(cmd, capture_output=True).stdout.decode()
        return stdout.strip().split()

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


sidetag = streamlit.sidebar.selectbox("Select Tags", [""] + Hf.tags())
tags = streamlit.sidebar.text_input("Filtering by Tags")

if not tags:
    tags = sidetag

if tags:
    images = Hf.images_by_tags(tags)
    if len(images) == 0:
        streamlit.error(f"No Images for `{tags}`")
    else:
        # preview
        streamlit.write(f"{len(images)} Images for `{tags}`")
        idx = streamlit.number_input("index", min_value=1, step=1)
        if idx > len(images):
            streamlit.warning("Out of Index")
            idx = len(images)
        img = images[idx - 1]
        streamlit.text(img)
        streamlit.image(img)

        detail = Hf.show(img)

        # tag editing
        img_tags = detail["tags"]
        user_tags = streamlit.text_input(
            "tags", value=" ".join(img_tags), key=img
        ).split()
        tags_add = set(user_tags) - set(img_tags)
        tags_del = set(img_tags) - set(user_tags)
        if len(tags_add) > 0:
            Hf.add_tags(detail["id"], tags_add)
            streamlit.info(f"add {tags_add}")
        if len(tags_del) > 0:
            Hf.del_tags(detail["id"], tags_del)
            streamlit.info(f"del {tags_del}")

        # show detail for debugging
        if img_tags != user_tags:
            detail = Hf.show(img)
        streamlit.write(detail)
