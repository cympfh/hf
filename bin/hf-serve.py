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
    @streamlit.cache(suppress_st_warning=True, allow_output_mutation=True)
    def tags(cls) -> List[str]:
        """All tags"""
        cmd = ["hf", "tags"]
        logger.info("Hf.tags: %s", cmd)
        stdout = subprocess.run(cmd, capture_output=True).stdout.decode()
        return ["null"] + stdout.strip().split()

    @classmethod
    @streamlit.cache(suppress_st_warning=True)
    def images_by_tags(cls, tags: str, rand: bool) -> List[str]:
        """hf grep"""
        cmd = ["hf", "grep"] + tags.split()
        logger.info("Hf.images_by_tags: %s", cmd)
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
        logger.info("Hf.show: %s", cmd)
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
        logger.info("Hf.add_tags: %s", cmd)
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
        logger.info("Hf.del_tags: %s", cmd)
        subprocess.run(cmd)

    @classmethod
    @streamlit.cache(suppress_st_warning=True)
    def images_random(cls) -> List[str]:
        """Random"""
        cmd = ["hf", "cat"]
        stdout = subprocess.run(cmd, capture_output=True).stdout.decode()
        images = stdout.split("\n")
        random.shuffle(images)
        return images

    @classmethod
    def delete(cls, img: str):
        cmd = ["hf", "del", img]
        logger.info("Hf.delete: %s", cmd)
        subprocess.run(cmd, capture_output=True).stdout.decode()


sidetag = streamlit.sidebar.selectbox("Select Tags", [""] + Hf.tags())
filtertags = streamlit.sidebar.text_input("Filtering by Tags")
rand = streamlit.sidebar.checkbox("Random")
logger.info(f"{sidetag=}, {filtertags=}, {rand=}")

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

logger.info("%s images found", len(images))

left, right = streamlit.columns(2)

# Search result
if len(images) == 0:
    left.error(f"No Images for `{target}`")
    streamlit.stop()

left.write(f"{len(images)} Images for `{target}`")

# Preview
idx = left.number_input("index", min_value=1, max_value=len(images), step=1)
img = images[idx - 1]
left.text_input("img", img, disabled=True)
try:
    left.image(img)
except Exception as err:
    left.warning(err)
    left.image(img, output_format="JPEG")

logger.info("Fetching medata for %s", img)
detail = Hf.show(img)
detail["tags"] = [str(t) for t in detail.get("tags", [])]
logger.info(f"{detail=}")

# Tag Editing
updated = False
img_tags = detail["tags"]
user_tags = right.multiselect(
    "tags", options=Hf.tags(), default=img_tags, key=f"{img}_a"
)
new_tags = list(set(right.text_input("new tags", value="", key=f"{img}_b").split()))
Hf.tags().extend(new_tags)
user_tags += new_tags
logger.info(f"{user_tags=}")
tags_add = set(user_tags) - set(img_tags)
tags_del = set(img_tags) - set(user_tags)

if len(tags_add) > 0:
    Hf.add_tags(detail["id"], tags_add)
    right.info(f"add {tags_add}")
    updated = True

if len(tags_del) > 0:
    Hf.del_tags(detail["id"], tags_del)
    right.info(f"del {tags_del}")
    updated = True

detail["tags"] = user_tags  # update

# Image Detail
right.write(detail)

if right.button("Delete this"):
    Hf.delete(img)
    updated = True

if updated:
    logger.info("Re-Run")
    streamlit.experimental_rerun()
