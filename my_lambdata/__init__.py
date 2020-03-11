from sklearn.model_selection import train_test_split
from pandas import to_datetime
class DataFrameHelper:
    def split_dates(dataframe, columns=None):
        df = dataframe.copy()
        if columns is None:
            columns = df.columns.tolist()
        for column in columns:
            df[column] = to_datetime(df[column], errors='ignore')
            for time in ('day', 'month', 'year'):
                df[f'{column}_{time}'] = getattr(df[column].dt, time)
        return df
    def tvt_split(*arrays, set_sizes=(0.8, 0.1, 0.1), **options):
        """
        Split arrays or matrices into random train,
        validation, and test subsets

        Wrapper of scikit-learn's train_test_split
        to have proportioned splitting with validation subset included.

        setsizes: list-like of ints or floats representing proportion of train,
        validation, and test subsets, respectively.
        If floats, must sum up to 1.
        If ints, must sum up to total observations in dataset.

        Otherwise, all other parameters are passed to train_test_split.
        I'm not sure what happens if you give train_size or test_size,
        so programmer beware.

        I'm also not sure if I'm legally allowed to copy and paste
        the documentation from train_test_split,
        so you get no information here about it.
        """
        first_split = set_sizes[0] + set_sizes[1]
        
        second_split = set_sizes[1]
        if sum(set_sizes) <= 1:
            second_split /= first_split

        train_and_val, test = train_test_split(*arrays,
                                               test_size = set_sizes[2],
                                               **options)
        train, val = train_test_split(train_and_val,
                                      test_size = second_split,
                                      **options)
        return train, val, test