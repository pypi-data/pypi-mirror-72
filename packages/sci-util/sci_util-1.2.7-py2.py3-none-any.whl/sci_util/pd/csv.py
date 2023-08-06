#!/usr/bin/python
# -*- coding: utf-8 -*-
# Author: violinsolo
# Created on 2020/7/1
import traceback
from typing import Union

import pandas as pd
import numpy as np


def combine_csv_files(from_files: list, to_file: str, wanted_cols: Union[list, str, None] = None, *args, **kwargs) -> pd.DataFrame:
    """
    Covert several csv files to ONE csv file with specified columns.

    :param na_vals:
    :param sep:
    :param from_files: a list of csv file paths which represent the source files to combine, <br>
        eg. ['path/to/source_file_1.csv', 'path/to/source_file_2.csv'] <br> <br>
    :param to_file: the csv file path which designate the destinate location to store the result, <br>
        eg. 'path/to/save_file.csv' <br> <br>
    :param wanted_cols: the filter columns, which will be the result csv columns, <br>
        no data in this column and this column will be empty, <br>
        no wanted_cols provided (None), all columns will be preserved. <br>

    :return: pd.DataFrame which is the data content store in the "to_file" csv file.
    """
    if from_files is None:
        raise ValueError('from_files cannot be None')
    elif type(from_files) is not list:
        raise ValueError('from_files must be <type: list>')
    elif len(from_files) == 0:
        raise ValueError('from_files cannot be empty')

    if to_file is None:
        raise ValueError('to_file cannot be None')
    elif type(to_file) is not str:
        raise ValueError('to_file must be <type: str>')
    elif len(to_file) == 0:
        raise ValueError('to_file cannot be empty')

    dfs = []
    for _from_file in from_files:
        try:
            _df = pd.read_csv(_from_file, *args, **kwargs)
            dfs.append(_df)
        except:
            print('*'*32)
            print(f'- pd.read_csv error with input file: "{_from_file}"')
            traceback.print_exc()
            print('*'*32)
            continue

    # combine all dfs with concat 'outer' join,
    # ignore_index will allow concat directly and add columns automatically,
    # axis=0 means concat follow vertical direction.
    final_combined_df = pd.concat(dfs, axis=0, ignore_index=True, sort=False)

    if wanted_cols is None \
            or (type(wanted_cols) is list and len(wanted_cols) == 0) \
            or (type(wanted_cols) is not list and type(wanted_cols) is not str):
        final_combined_df = final_combined_df
    else:
        current_cols = final_combined_df.columns.to_list()
        if type(wanted_cols) is list:
            for _col in wanted_cols:
                if _col not in current_cols:
                    final_combined_df[_col] = np.nan
        elif type(wanted_cols) is str:
            if wanted_cols not in current_cols:
                final_combined_df[wanted_cols] = np.nan

        final_combined_df = final_combined_df[wanted_cols]

    final_combined_df.to_csv(to_file, header=True)
    return final_combined_df


if __name__ == '__main__':
    d1 = {'A': [2, 3, 4], 'B': ['a', 'b', 'c'], 'C': ['10002', 'sss', 'msc23d']}
    d2 = {'A': [12, 13, 4, 15], 'B': ['1a', 'b', 'c', '1Z'], 'Z': ['333', '444', '555', 'ZZZ']}

    df1 = pd.DataFrame(d1)
    df2 = pd.DataFrame(d2)

    df1_pth = 'df1_test.csv'
    df2_pth = 'df2_test.csv'

    df1.to_csv(df1_pth, index=False)
    df2.to_csv(df2_pth, index=False)

    # dfNone = combine_csv_files(from_files=[df1_pth, df2_pth], to_file='dfcombine_test_None.csv', wanted_cols=None)
    # dfAZC = combine_csv_files(from_files=[df1_pth, df2_pth], to_file='dfcombine_test_AZC.csv', wanted_cols=['A', 'Z', 'C'])
    dfNone = combine_csv_files([df1_pth, df2_pth], 'dfcombine_test_None.csv', None)
    dfAZC = combine_csv_files([df1_pth, df2_pth], 'dfcombine_test_AZC.csv', ['A', 'Z', 'C'])
    dfZ = combine_csv_files([df1_pth, df2_pth], 'dfcombine_test_Z.csv', 'Z')
    dfZZZ = combine_csv_files([df1_pth, df2_pth], 'dfcombine_test_ZZZ.csv', 'ZZZ')

    print('df1 === \n', df1)
    print('df2 === \n', df2)
    print('dfNone === \n', dfNone)
    print('dfAZC === \n', dfAZC)
    print('dfZ === \n', dfZ)
    print('dfZZZ === \n', dfZZZ)
