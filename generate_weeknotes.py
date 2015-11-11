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

#import basic_config
#import secure_config
import tweet_notes
import jira_notes
#import blog_builder

def prettify_html(html):
    return bs(html).prettify()


def generate_weeknotes():
    tweets = tweet_notes.html_weeknotes()
    jira = jira_notes.html_weeknotes()

    weeknotes = prettify_html(tweets+jira)
    
    return weeknotes

if __name__ == "__main__":
    print generate_weeknotes()



