#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 bolster <bolster@milo>
# 
# Distributed under terms of the MIT license.

"""
slack_notify, part of pyweeknote-generator
"""

from slacker import Slacker
from basic_config import config_keys
from secure_config import slack_token

api = Slacker(slack_token)


def notify(message):
    api.chat.post_message(config_keys['slack_notify_channel'], message, username=config_keys['slack_username'])
