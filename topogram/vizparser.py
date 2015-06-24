#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger('topogram.visualizer')

class Visualizer:
    """
    Interface (abstract base class) for Visualizer 
    This class should be instantiated to describe a specific action (regexps, NLP, etc.)

    """

    def __init__(self): 
        logger.info("init Visualizer class")
        self.test = "test"
        
