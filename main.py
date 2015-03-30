#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import jinja2
import webapp2

from models import Project
from google.appengine.ext import ndb
from google.appengine.api import users

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_env.get_template('templates/index.jinja2')
        portfolio = Project.query().order(-Project.last_touch_date_time)
        self.response.write(template.render({'portfolio':portfolio}))

class ProjectHandler(webapp2.RequestHandler):
    def get(self, project_key):
        template = jinja_env.get_template('templates/single-project.jinja2')
        key = ndb.Key(urlsafe=project_key)
        self.response.write(template.render({'project': key.get()}))

class ProjectAction(webapp2.RequestHandler):
    def post(self):
        if users.is_current_user_admin():
            new_project = Project()
            properties = {}
            for key, value in self.request.POST.items():
                properties[key] = value
            new_project.populate(**properties)
            new_project.put()
            self.response.write(str(new_project))
        else:
            self.abort(404)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    (r'/projects/([\w-]+)', ProjectHandler),
    ('/projects', ProjectAction)
], debug=True)
