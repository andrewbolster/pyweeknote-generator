#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 bolster <bolster@milo>
#
# Distributed under terms of the MIT license.

"""
Jira integration for Weeknotes
"""

import jira

from collections import OrderedDict
from cgi import escape

from basic_config import usernames, config_keys, text_fields


def format_issue(i):
    issue_details = {
            'title' : escape(i.fields.summary),
            'description' : escape(i.fields.description),
            'link' : i.permalink(),
            'status' : escape(i.fields.status.name)
    }

    inner_string = issue_details['title']

    if issue_details['status'] == "Closed":
        inner_string = "<strike>{}</strike>".format(inner_string)

    issue_details['inner_string'] = inner_string

    content = """<li class="{status}"><a href="{link}" title="{description}">{inner_string}</a></li>""".format(**issue_details)
    
    return content


def format_issue_group(issues, title="Issues"):
    formatted_issues = map(format_issue, issues)
    header = "<h3>{}</h3><ul>".format(title)
    footer = "</ul>"
    content = ""
    for issue_html in formatted_issues:
        content+=issue_html
    return header+content+footer

api = jira.JIRA(config_keys['jira_baseurl'], options={'verify':False})

# Currently one cares about public issues anyway, so no authentication needed

closed_issues = api.search_issues("status changed to Closed after -1w")
changed_issues = api.search_issues('status changed to ("In Progress", Reopened, "To Do", "Waiting for Support", "Waiting for Customer", "Waiting for Review") after -1w')
waiting_issues = api.search_issues('status in ("Waiting for Support", "Waiting for Customer", "Waiting for Review")')

issues = [
    closed_issues,
    changed_issues,
    waiting_issues
]
titles = [
    "Closed Issues",
    "Actioned Issues",
    "Waiting Issues"
]

def html_weeknotes():
    header = '<div id="jira"><h2>{}</h2>'.format(text_fields['jira_header'])
    content = ""
    footer = "</div>"

    content += header
    for _issues,_title in zip(issues, titles):
        content+= format_issue_group(_issues, title=_title)
    content += footer

    return content


if __name__ == '__main__':
    print html_weeknotes()
