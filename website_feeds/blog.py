# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014 ThinkOpen Solutions(<http://thinkopen.solutions>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.addons.website.models.website import slug
from openerp.addons.website_blog.controllers.main import WebsiteBlog

from feedgen.feed import FeedGenerator
import logging

from core import feed

class BlogFeed(http.Controller):
    @feed(WebsiteBlog.blog)
    def blog_feed(self, values):
        domain = request.httprequest.host_url.rstrip('/')
        blog = values['blog']
        fg = FeedGenerator()
        fg.id(domain + values['pager']['page']['url'])
        fg.title(blog.name)
        fg.subtitle(blog.subtitle)
        for post in values['blog_posts']:
            fe = fg.add_entry()
            fe.id(domain + '/blog/{}/post/{}'.format(slug(blog), slug(post)))
            fe.title(post.name)
            fe.content(post.content)
        return fg
