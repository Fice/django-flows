
import unittest
from django.conf.urls import include, patterns
from flows.components import Action, Scaffold
from flows.handler import FlowHandler

class Action1(Action):
    url = '/1$'

class Action2(Action):
    url = '/2$'

class Scaffold1(Scaffold):
    url = '/scaff1'
    action_set = [Action1, 'Action2']


class NonAtomicAction(Action):
    url = '/nonatomic$'
    non_atomic_requests = True


class LazyActionSetTest(unittest.TestCase):
    
    def test_get_by_name(self):
        a1, a2 = Scaffold1().action_set
        self.assertEqual( Action1, a1 )
        self.assertEqual( Action2, a2 )
    
    def test_index_of(self):
        actions = Scaffold1().action_set
        self.assertEqual( 0, actions.index(Action1) )
        self.assertEqual( 1, actions.index(Action2) )


class NonAtomicRequestsTest(unittest.TestCase):

    def test_non_atomic_requests(self):
        handler = FlowHandler('non_atomic')
        handler.register_entry_point(NonAtomicAction)
        urlpatterns = patterns('',
            (r'', include(handler.urls)),
        )
        view_function = urlpatterns[0].resolve('/nonatomic').func
        # If view function was annotated with
        # django.db.transaction.non_atomic_requests, then the view function 
        # should have a _non_atomic_requests attribute
        self.assertTrue(hasattr(view_function, '_non_atomic_requests'))
