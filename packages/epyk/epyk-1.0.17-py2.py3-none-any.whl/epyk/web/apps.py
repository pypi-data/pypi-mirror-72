
import sys
import os

from epyk.web import angular


class AppRoute(object):

  def __init__(self, page):
    self.page = page

  def angular(self, server, app, selector=None, name=None):
    """

    :param server:
    :param app:
    :param selector:
    :param name:
    """
    name = name or os.path.split(sys.argv[0])[1][:-3]
    selector = selector or os.path.split(sys.argv[0])[1][:-3]
    return angular.Angular(server, app).page(selector, name, report=self.page)
