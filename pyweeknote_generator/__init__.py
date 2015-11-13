#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 bolster <bolster@milo>
#
# Distributed under terms of the MIT license.

"""
Pythonic ish Version of the DoES Liverpool-based Weeknotes generator (for Farset Labs)

Includes:
    Twitter #weeknotes hashtag
    Public JIRA tasks opened or marked as complete this week
    Calendar Integration
Pending:
    Wordpress Integration
    Instagram Integration?
    Facebook Integration?
    Slack Integration?
"""

from datetime import date
import argparse
import os
import sys
import subprocess
import warnings
import traceback
import importlib
from BeautifulSoup import BeautifulSoup as bs

import basic_config
from post_to_wordpress import build_draft_post


def try_to_open(filename):
    try:
        if sys.platform == 'linux2':
            subprocess.call(["xdg-open", filename])
        else:
            os.startfile(filename)
    except Exception as err:
        warnings.warn(traceback.format_exc())


def prettify_html(html):
    return bs(html).prettify()


def generate_weeknotes(for_wordpress=False):
    intro = basic_config.text_fields['intro']

    weeknotes_l = []
    for module_name in basic_config.modules:
        try:
            module = importlib.import_module('.'+module_name, package='pyweeknote_generator')
            weeknotes_l.append(module.html_weeknotes())
        except ImportError:
            warnings.warn("Could not import {}; skipping".format(module_name))
        except:
            print("Exception in {}".format(module_name))
            raise

    weeknotes = u'\n<hr>\n'.join(weeknotes_l)

    footer = basic_config.text_fields['footer']

    content_l = [intro, weeknotes, footer]
    content = u'\n<hr>\n'.join(content_l)

    if not for_wordpress:
        # Wordpress doesn't like pretty code, especially newlines
        content = prettify_html(content)

    return content


def generate_and_post_draft_to_wordpress(title, content):
    post = build_draft_post(title, content)
    post_edit_url = "{baseurl}/wp-admin/post.php?post={id}&action=edit".format(
        baseurl=basic_config.config_keys['wordpress_baseurl'],
        id=post.id
    )
    print("If everything has gone well, an editor should be able to update and publish this weeknote at: {}".format(
        post_edit_url))
    return {'outputs': [post_edit_url]}


def main():
    parser = argparse.ArgumentParser(
        description="pyweeknotes"
    )
    parser.add_argument('-p', "--publish", action='store_true', help="Publish notes", default=False)
    parser.add_argument('-o', "--open", action='store_true', help="Attempt to launch generated outputs", default=False)
    parser.add_argument('-t', "--title", action='store', help="Set title afterword", default="CHANGEME")

    args = parser.parse_args()

    title = "Weeknotes {}-{}:".format(*date.today().isocalendar()[0:2])
    title += args.title
    content = generate_weeknotes(for_wordpress='wordpress' in basic_config.post_to)
    outputs = []

    if args.publish:
        outputs.extend(generate_and_post_draft_to_wordpress(title, content)['outputs'])
    else:
        with open('sample_output.html', 'r+') as f:
            f.write(content.encode("UTF-8"))
        outputs.append("sample_output.html")
        print("HTML Content dumped to sample_output.html")
    if args.open:
        map(try_to_open, outputs)
