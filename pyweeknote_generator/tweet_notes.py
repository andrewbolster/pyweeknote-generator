#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 bolster <bolster@milo>
#
# Distributed under terms of the MIT license.

"""
Twitter Integrations for Weeknotes
"""

from datetime import date, timedelta

import twitter

from dateutil import parser

from basic_config import usernames, config_keys, text_fields
from secure_config import twitter_keys

api = twitter.Api(**twitter_keys)

user = api.VerifyCredentials()


def get_list_timeline_since_date(list_id, target_date):
    _statuses = []
    last_date = date.today()
    last_id = None
    assert isinstance(target_date, date)
    while last_date >= target_date:
        intermediate_list = api.GetListTimeline(list_id=list_id, max_id=last_id, slug='')
        _statuses.extend(intermediate_list)
        last_status = intermediate_list[-1].AsDict()
        last_date = parser.parse(last_status['created_at']).date()
        last_id = last_status['id']
    return _statuses


def get_notes_statuses():
    user_lists = api.GetLists(user.GetId())
    relevant_lists = filter(
        lambda l: l.GetFull_name() == '@{}/{}'.format(usernames['twitter'], config_keys['twitter_list']), user_lists)
    assert len(relevant_lists) == 1, "Invalid Number of Relevant Twitter Lists"
    relevant_list = relevant_lists[0]

    tweet_notes = filter(lambda s: '#{}'.format(config_keys['weeknotes_str']) in s.text,
                         get_list_timeline_since_date(relevant_list.GetId(), date.today() - timedelta(days=7)))
    return tweet_notes


def make_html_embeddable(tweets):
    return map(lambda s: api.GetStatusOembed(s.GetId())['html'], tweets)


def make_url_list_text(tweets):
    urls = []
    for tweet in tweets:
        tweet_d = tweet.AsDict()
        urls.append("\nhttps://twitter.com/{}/status/{}\n".format(tweet_d['user']['screen_name'], tweet_d['id']))

    return urls


def html_weeknotes():
    header = '<div id="tweet_notes"><h2>{}</h2>'.format(text_fields['twitter_header'])
    content = "\n".join(make_url_list_text(get_notes_statuses()))
    footer = "These tweets are automatically selected from tweets from registered members who are listed in the @{}/{} twitter list using the #{} hashtag</div>".format(
        usernames['twitter'], config_keys['twitter_list'], config_keys['weeknotes_str'])

    return "\n".join([header, content, footer])


if __name__ == '__main__':
    print html_weeknotes()
