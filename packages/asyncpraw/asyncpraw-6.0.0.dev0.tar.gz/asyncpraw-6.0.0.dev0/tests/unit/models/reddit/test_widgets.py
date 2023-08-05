from json import dumps

from asyncpraw.models import (SubredditWidgets, SubredditWidgetsModeration,
                         Widget, WidgetModeration)
from asyncpraw.models.reddit.widgets import WidgetEncoder
from asyncpraw.models.base import PRAWBase

from ... import UnitTest


class TestWidgetEncoder(UnitTest):
    def test_bad_encode(self):
        data = [1, 'two', SubredditWidgetsModeration(
            self.reddit.subreddit('subreddit'), self.reddit)]
        try:
            dumps(data, cls=WidgetEncoder)  # should throw TypeError
        except TypeError:
            pass  # success
        else:
            assert False

    def test_good_encode(self):
        data = [1, 'two',
                PRAWBase(self.reddit, _data={'_secret': 'no', '3': 3})]
        assert '[1, "two", {"3": 3}]' == dumps(data, cls=WidgetEncoder)


class TestWidgets(UnitTest):
    def test_subredditwidgets_mod(self):
        sw = SubredditWidgets(self.reddit.subreddit('fake_subreddit'))
        assert isinstance(sw.mod, SubredditWidgetsModeration)

    def test_widget_mod(self):
        w = Widget(self.reddit, {})
        assert isinstance(w.mod, WidgetModeration)
        assert w.mod.widget == w
