from google.appengine.ext import ndb


class Project(ndb.Expando):
    image = ndb.StringProperty()
    title = ndb.StringProperty()
    last_touch_date_time = ndb.DateTimeProperty(auto_now_add=True)