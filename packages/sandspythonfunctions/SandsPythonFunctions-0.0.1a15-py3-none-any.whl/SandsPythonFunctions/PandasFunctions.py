# --------------------------------------------------------------------------------------
# File: "PandasFunctions.py"
# Dir: "/mnt/f/GithubRepos/SandsPythonFunctions/src/SandsPythonFunctions"
# Created: 2020-06-26
# --------------------------------------------------------------------------------------

"""
this file contains useful functions that manipulate pandas dataframes

display_full_dataframe
"""

# def sample_dataframe(dta, sample_number=100):
#     import pandas as pd

#     dta.sample


def display_full_dataframe(dta):
    """displays a dataframe without cutting anything off for being too long

    Arguments:
        dta {dataframe} -- a dataframe you wish to display
    """
    import pandas as pd

    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(dta)
