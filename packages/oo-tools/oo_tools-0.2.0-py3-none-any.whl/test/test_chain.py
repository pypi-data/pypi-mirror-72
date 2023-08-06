import unittest

from oo_tools.chain import *

class TestBaseChainComponent(unittest.TestCase):
    def test_process(self):
        # make sure it raises when the child class doesnt implement process
        class NewLink(BaseChainComponent):
            pass
        
        newlink = NewLink()
        
        with self.assertRaises(NotImplementedError):
            newlink.process()
    
    def test_name(self):
        x = BaseChainComponent()
        
        assert x.name == 'BaseChainComponent'

class TestLink(unittest.TestCase):
    def setUp(self):
        self.link = Link()
        
    def test_next(self):
        # make sure it raises if you don't supply a chain component
        with self.assertRaises(TypeError):
            self.link.next = 'wrong type'
        
        class FakeNext:
            pass
        
        with self.assertRaises(TypeError):
            self.link.next = FakeNext()
        
        # make sure you can set it if it is a chain component
        link2 = Link()
        self.link.next = link2
        assert self.link.next == link2
        
    def test_do_next(self):
        next_link = Link()
        
        # it'll raise if the next link doesn't implement a process() method
        with self.assertRaises(NotImplementedError):
            self.link = next_link
            self.link.do_next()
        
        # it works as expected
        class FirstLink(Link):
            def process(self):
                self.do_next(2)

        class NextLink(Link):
            catch_res = None
            
            def process(self, *args, **kwargs):
                self.catch_res = args[0]
        
        first_link = FirstLink()
        next_link = NextLink()
        
        first_link.next = next_link
        first_link.process()
        
        assert next_link.catch_res == 2
