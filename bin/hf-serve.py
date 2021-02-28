#!/usr/bin/env python

import json
import logging
import random
import subprocess
from typing import List, Set

import streamlit

logger = logging.getLogger("hf-serve")
streamlit.set_page_config(layout="wide")


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
    @streamlit.cache
    def images_by_tags(cls, tags: str, rand: bool) -> List[str]:
        """hf grep"""
        cmd = ["hf", "grep"] + tags.split()
        logger.info(cmd)
        stdout = subprocess.run(cmd, capture_output=True).stdout.decode().strip()
        if not stdout:
            return []
        images = stdout.strip().split("\n")
        if rand:
            random.shuffle(images)
        return images

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

    @classmethod
    @streamlit.cache
    def images_random(cls) -> List[str]:
        """Random"""
        cmd = ["hf", "cat"]
        stdout = subprocess.run(cmd, capture_output=True).stdout.decode()
        images = stdout.split("\n")
        random.shuffle(images)
        return images


sidetag = streamlit.sidebar.selectbox("Select Tags", [""] + Hf.tags())
filtertags = streamlit.sidebar.text_input("Filtering by Tags")
rand = streamlit.sidebar.checkbox("Random")

images = []

if filtertags:
    images = Hf.images_by_tags(filtertags, rand)
    target = filtertags
elif sidetag:
    images = Hf.images_by_tags(sidetag, rand)
    target = sidetag
elif rand:
    images = Hf.images_random()
    target = "random"
else:
    streamlit.stop()


left, right = streamlit.beta_columns(2)

# Search result
if len(images) == 0:
    left.error(f"No Images for `{target}`")
    streamlit.stop()

left.write(f"{len(images)} Images for `{target}`")

# Preview
idx = left.number_input("index", min_value=1, max_value=len(images), step=1)
img = images[idx - 1]
left.text(img)
logger.info(img)
try:
    left.image(img)
except Exception as err:
    left.warning(err)
    left.image(img, output_format="JPEG")

detail = Hf.show(img)
logger.info(detail)
detail["tags"] = [str(t) for t in detail["tags"]]

# Tag Editing
img_tags = detail["tags"]
user_tags = right.text_input("tags", value=" ".join(img_tags), key=img).split()
tags_add = set(user_tags) - set(img_tags)
tags_del = set(img_tags) - set(user_tags)

if len(tags_add) > 0:
    Hf.add_tags(detail["id"], tags_add)
    right.info(f"add {tags_add}")

if len(tags_del) > 0:
    Hf.del_tags(detail["id"], tags_del)
    right.info(f"del {tags_del}")

detail["tags"] = user_tags  # update

# Image Detail
right.write(detail)
