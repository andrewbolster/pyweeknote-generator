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
Pending:
    Calendar Integration
    Instagram Integration?
    Facebook Integration?
    Slack Integration?
"""

from BeautifulSoup import BeautifulSoup as bs
from datetime import date

import basic_config
#import secure_config
import tweet_notes
import jira_notes
#import blog_builder

def prettify_html(html):
    return bs(html).prettify()


def generate_weeknotes():
    header = "<div id='weeknotes'><h1>Weeknotes {}-{}</h1>".format(*date.today().isocalendar()[0:2])
    intro = basic_config.text_fields['intro']
    
    tweets = tweet_notes.html_weeknotes()
    jira = jira_notes.html_weeknotes()

    footer = basic_config.text_fields['footer'] 

    content_l = [header, intro, tweets, jira, footer]
    content = u'\n'.join(content_l)

    weeknotes = prettify_html(content)
    
    return weeknotes

if __name__ == "__main__":
    print generate_weeknotes()



