#!/usr/bin/env bash
set +xe

uv run ./fetch_blogs.py
git add .
git commit -am "Update Blogs"
git push origin

