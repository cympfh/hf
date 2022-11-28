#!/usr/bin/env python

import json
import logging
import subprocess
from typing import List, Set

import streamlit

logger = logging.getLogger("hf-serve")
streamlit.set_page_config(
    layout="wide",
    page_title="hf",
)


class Hf:
    """Wrapper for hf command"""

    @classmethod
    @streamlit.cache(suppress_st_warning=True)
    def tags(cls) -> List[str]:
        """All tags"""
        cmd = ["hf", "tags"]
        logger.info("Hf.tags: %s", cmd)
        stdout = subprocess.run(cmd, capture_output=True).stdout.decode()
        return ["null"] + stdout.strip().split()

    @classmethod
    @streamlit.cache(suppress_st_warning=True)
    def images_by_tags(cls, tags: str) -> List[str]:
        """hf grep"""
        cmd = ["hf", "grep"] + tags.split()
        logger.info("Hf.images_by_tags: %s", cmd)
        stdout = subprocess.run(cmd, capture_output=True).stdout.decode().strip()
        if not stdout:
            return []
        images = stdout.strip().split("\n")
        return images

    @classmethod
    def show(cls, object: str) -> dict:
        """hf show --json"""
        cmd = ["hf", "show", "--json", object]
        logger.info("Hf.show: %s", cmd)
        stdout = subprocess.run(cmd, capture_output=True).stdout.decode()
        if not stdout:
            return {}
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
    def delete(cls, img: str):
        cmd = ["hf", "del", img]
        logger.info("Hf.delete: %s", cmd)
        subprocess.run(cmd, capture_output=True).stdout.decode()


hftags = Hf.tags()

tags = streamlit.sidebar.multiselect("Tags", options=[""] + hftags)
shuffle = streamlit.sidebar.checkbox("Shuffle")
logger.info(f"Filter by {tags=}, {shuffle=}")

images = []

if tags:
    target = " ".join(tags)
    images = Hf.images_by_tags(target)
else:
    streamlit.info("Select tags from left Panel")
    streamlit.stop()

logger.info("%s images found", len(images))

left, right = streamlit.columns(2)

# Search result
if len(images) == 0:
    left.error(f"No Images for `{target}`")
    streamlit.stop()

left.write(f"{len(images)} Images for `{target}`")

# Preview
idx = int(left.number_input("index", min_value=1, max_value=len(images), step=1))
img = images[idx - 1] if not shuffle else images[(idx + len(images) // 2) % len(images)]
if ".mp4" in img:
    left.video(img)
elif ".jpg" in img or ".jpeg" in img:
    left.image(img, output_format="JPEG")
else:
    left.image(img)

logger.info("Fetching medata for %s", img)
detail = Hf.show(img)

if not detail:
    streamlit.error(f"Not found: {img}")
    streamlit.stop()
else:
    right.caption(detail["value"])
    right.caption(img)

detail["tags"] = [str(t) for t in detail.get("tags", [])]
logger.info(f"{detail=}")

# Tag Editing
img_tags = detail["tags"]


def update(tags_old: set[str], tags_new: set[str]):
    tags_add = tags_new - tags_old
    tags_del = tags_old - tags_new
    if len(tags_add) > 0:
        Hf.add_tags(detail["id"], tags_add)
        right.info(f"add {tags_add}")
    if len(tags_del) > 0:
        Hf.del_tags(detail["id"], tags_del)
        right.info(f"del {tags_del}")


with right.form("tag_editor"):
    user_tags = streamlit.multiselect(
        "tags",
        options=(set(hftags) | set(img_tags)),
        default=img_tags,
        key=f"{img}_a",
    )
    new_tags = list(
        set(streamlit.text_input("new tags", value="", key=f"{img}_b").split())
    )
    user_tags += new_tags
    submit = streamlit.form_submit_button("Update")
    if submit:
        update(set(img_tags), set(user_tags))

detail = Hf.show(img)
right.write(detail)

if right.button("Remove"):
    user_tags = ["removed"]
    update(set(img_tags), set(user_tags))

if right.button("Delete this (permanently)", type="primary"):
    Hf.delete(img)
