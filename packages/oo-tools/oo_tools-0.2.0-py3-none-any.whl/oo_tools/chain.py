"""Use this module to implement the 'Chain of Responsibility' pattern"""

class BaseChainComponent:

    @property
    def name(self):
        return type(self).__name__

    def process(self):
        raise NotImplementedError('You must implement a process() method')

class Link(BaseChainComponent):
    
    """
    a start or intermediate chain component
    """

    @property
    def next(self):
        """The next component in the chain of responsibility
        
        Raises:
            NotImplementedError: 
        
        Returns:
            BaseChainComponent -- next component in the chain
        """
        try:
            return self._next
        except:
            raise NotImplementedError('You must supply a next component first')
        
    @next.setter
    def next(self, next_chain_component: BaseChainComponent):
        """
        Next component in the chain
        
        Raises:
            TypeError: is not a subclass of BaseChainComponent
        """
        try:
            if not isinstance(next_chain_component, BaseChainComponent):
                raise TypeError
            
            self._next = next_chain_component
        except TypeError:
            raise TypeError(f'next_chain_component must be a BaseChainComponent subclass, not = {type(next_chain_component)}')

    def do_next(self, *args, **kwargs):
        """
        Call the next component in the chain
        """
        self.next.process(*args, **kwargs)
