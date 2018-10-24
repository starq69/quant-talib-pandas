#!/usr/bin/env python
# -*- coding: utf-8 -*-

import my_module
import pandas as pd
import numpy as np
import datetime

def main():

    todays_date = datetime.datetime.now().date()
    date_range  = pd.date_range(todays_date - datetime.timedelta(6), periods=6, freq='D')
    df      = pd.DataFrame(index=date_range, columns=['x','y']).fillna(0)
    print (date_range)

    my_module.init(date_range)

    df['test_column'] = df.apply(my_module.test_index_value, axis=1)
    print(df)
    print(df.info())

if __name__ == '__main__':
    main()
