#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from utils import any2utf8

import logging
logger = logging.getLogger('topogram.processor')

class Processor:
    """
    Interface (abstract base class) for Processor 
    This class should be instantiated to describe a specific action (regexps, NLP, etc.)

    """

    def __init__(self): 
        logger.info("init Processor class")

    def save(self):
        raise NotImplementedError('Not available for abstract base class. You should instantiate this class for a specific language')

    def load(self):
        raise NotImplementedError('Not available for abstract base class. You should instantiate this class for a specific language')
