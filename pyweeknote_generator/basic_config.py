#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 bolster <bolster@milo

usernames = {'twitter': 'FarsetLabs'}

modules = ['tweet_notes', 'jira_notes', 'gcal_notes']

post_to = ['wordpress']

config_keys = {'twitter_list': 'members',
               'jira_baseurl': 'https://jira.farsetlabs.org.uk',
               'weeknotes_str': 'weeknotes',
               'google_calendar_id': 'farsetlabs.org.uk_srmqnkn373auq51u00s2nijrq8@group.calendar.google.com',
               'google_calendar_lookahead': 14,
               'wordpress_baseurl': 'https://blog.farsetlabs.org.uk/wordpress/',
               'wordpress_categories': ['News', 'Weeknotes'],
               'wordpress_tags': ['weeknotes', 'automated']}

text_fields = {
    'intro': "Each week we'll endeavour to publish some details of the interesting things that members have been up to over the past seven days.",
    'footer': "Farset exists to support the community that uses it. If you use Farset Labs or attend events at the labs, then you are part of that community. If you would like to publicise something related to Farset, you can email info@farsetlabs.org.uk with the formatted content for us to use as a new blog post. Tell us what you're up to, and we'll show the world what madness happens at the Labs!",
    'twitter_header': "Things of Note",
    'jira_header': "Done, Doing, Waiting"
}


def cleanup_text_dict(d):
    for k, v in d.items():
        try:
            d[k] = v.decode('utf-8', 'ignore')
        except UnicodeDecodeError:
            print("Borked on {}:{}".format(k, v))
            raise


cleanup_text_dict(text_fields)
