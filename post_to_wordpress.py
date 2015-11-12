#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2015 bolster <bolster@milo>
#
# Distributed under terms of the MIT license.

"""
Post Draft Blog post to Wordpress using the XML-RPC API
"""

from basic_config import config_keys
from secure_config import wordpress_keys

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts, users

wp = Client(config_keys['wordpress_baseurl']+'xmlrpc.php', wordpress_keys['username'], wordpress_keys['password'])


def build_draft_post(title, content):
    post = WordPressPost()
    post.title = title
    post.content = content
    post.terms_names = {
        'post_tag': config_keys['wordpress_tags'],
        'category': config_keys['wordpress_categories']
    }

    # Don't duplicate same year / week no; reuse
    current_posts = wp.call(posts.GetPosts())
    dup_posts = filter(lambda p: p.title.split(':') == post.title.split(':'), current_posts)
    if dup_posts:
        # lets assume this returns in a sensible order
        dup_id = dup_posts[0].id
        wp.call(posts.EditPost(dup_id, post))
        post.id = dup_id
    else:
        post.id = wp.call(posts.NewPost(post))
    return post

