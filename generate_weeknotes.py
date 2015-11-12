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

from BeautifulSoup import BeautifulSoup as bs
from datetime import date

import basic_config
#import secure_config
from post_to_wordpress import build_draft_post

def prettify_html(html):
    return bs(html).prettify()


def generate_weeknotes(for_wordpress=False):
    intro = basic_config.text_fields['intro']

    weeknotes_l = []
    for module_name in basic_config.modules:
        try:
            module = __import__(module_name)
            weeknotes_l.append(module.html_weeknotes())
        except ImportError:
            print("Could not import {}; skipping".format(module_name))
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

if __name__ == "__main__":
    title = "Weeknotes {}-{}:CHANGEME".format(*date.today().isocalendar()[0:2])
    content = generate_weeknotes(for_wordpress=True)
    with open('/dev/shm/test.html','r+') as f:
        f.write(content.encode("UTF-8"))

    post = build_draft_post(title, content)
    post_edit_url = "{baseurl}/wp-admin/post.php?post={id}&action=edit".format(
            baseurl = basic_config.config_keys['wordpress_baseurl'],
            id = post.id
    )
    print("If everything has gone well, an editor should be able to update and publish this weeknote at: {}".format(post_edit_url))



