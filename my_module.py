#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, errno, sys, logging
import datetime
import pandas as pd
import numpy as np
import pprint

this  = sys.modules[__name__]
today = datetime.datetime.now().date()
data  = {}

def init(date_range):

    this.data = dict.fromkeys(pd.to_datetime(date_range), 'special day')
    '''
    this.log    = logging.getLogger(__name__)
    func_name   = sys._getframe().f_code.co_name
    '''
    print('-------------------')
    pprint.pprint(this.data)
    print('-------------------')


def test_index_value (row):
    key = pd.to_datetime(row.name)
    if key in this.data:
        #return datetime.datetime.now().date()
        return this.data[key]
    else:
        return row.name # get value of index
