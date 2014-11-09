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

from werkzeug.wrappers import Response
import functools
import logging

def feed(controller_func):
    logging.info("Controller func is %s", controller_func)
    def decorator(f):
        logging.info("f is %s", f)
        @functools.wraps(f)
        def feed_wrap(self, *a, **k):
            logging.info("args: %s, %s", a, k)
            obj = controller_func.im_class()
            bound_method = getattr(obj, controller_func.original_func.__name__)
            original_response = bound_method(*a, **k)
            values = original_response.qcontext
            logging.info("values is %s", values)
            generated = f(self, values)
            encoded = generated.atom_str(pretty=True)
            logging.info("encoded is %s", encoded)
            return Response(encoded)
        original_routes = controller_func.routing['routes']
        new_routes = [r + '/atom' for r in original_routes]
        logging.info("routes are %s", new_routes)
        feed_wrap.routing = dict(routes=new_routes, type='http', auth="public", website=True)
	feed_wrap.original_func = f
        return feed_wrap
    return decorator

