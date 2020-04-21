# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 14:29:40 2020

@author: user
"""

class Way:
    """
    A direction of movement.
    """
    
    def __init__(self, name, stack):
        """
        Creates a new direction.
        @param name: The direction's name.
        @param delta: The coordinate modification needed for moving in the specified direction.
        """
        self.name = name
        self.stack = stack
    
    def stack(self):
        """
        The hash method must be implemented for actions to be inserted into sets 
        and dictionaries.
        @return: The hash value of the action.
        """
        return self.stack
    
    def __str__(self):
        """
        @return: The string representation of this object when *str* is called.
        """
        return str(self.name)
    
    def go(self, position):
        """
        @return: Moving from the given location in this direction will result in the returned location.
        """
        return (position[0] + self.stack[0], position[1] + self.stack[1])
