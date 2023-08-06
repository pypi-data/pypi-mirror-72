import os
import csv

class Form:
    """
    Abstract Data Type for SEC forms
    """
    def __init__(self, df):
        self.df = Form.source_format(df)


    @staticmethod
    def source_format(df):
        """
        adds a column designating which source column dataframe values came from

        :param df (df): the dataframe
        :return (dF): the dataframe in source format
        """
        df["source_column"] = df.groupby(["tag", "fy"]).cumcount().add(1)
        df = df.set_index(["tag", "source_column"])
        return df


    @staticmethod
    def pivot(df, columns):
        """
        turns the dataframe into a pivot table

        :param df (df): the dataframe
        :param columns (str or list of str): the columns which values will be in the pivot table
        :return (df): the pivot table
        """
        return df.reset_index().pivot_table(index=["tag", "source_column", "uom"], columns=columns, values="value")


    def raw(self):
        """
        getter method for the source format

        :return (df): the source format dataframe
        """
        return self.df.copy()


    def form(self):
        """
        MAIN GETTER METHOD
        getter method for the nicely formatted dataframe

        :return (df): the formatted dataframe
        """
        return self.df.groupby(["tag", "uom"]).first().copy()


    def filter(self, regex, axis="index"):
        """
        generates a data sheet based on a keyword regex

        :param regex (str): the keyword regular expression
        :param axis (int or str): 0 or "index", 1 or "column"
        :return (df): a subset of the whole dataframe filtered by the regex
        """
        form = self.form()
        # return form[form.tag.str.contains(regex)].reset_index(drop=True)
        # return self.form().filter(regex=regex, axis=axis)
        return form[form.index.get_level_values("tag").str.contains(regex)]


    def asset_sheet(self):
        """
        generates a data sheet of "Asset" values

        :return (df): a subset of the whole dataframe filtered by assets
        """
        return self.filter("Asset|Assets")


    def liability_sheet(self):
        """
        generates a data sheet of "Liability" values

        :return (df): a subset of the whole dataframe filtered by liabilities
        """
        return self.filter("Liability|Liabilities")


    def debt_sheet(self):
        """
        generates a data sheet of "Debt" values

        :return (df): a subset of the whole dataframe filtered by debts
        """
        return self.filter("Debt|Debts")



    # def to_csv(
    #         self,
    #         path_or_buf=None,
    #         sep=",",
    #         na_rep="",
    #         float_format=None,
    #         columns=None,
    #         header=True,
    #         index=True,
    #         index_label=None,
    #         mode="w",
    #         encoding="utf-8",
    #         compression="infer",
    #         quoting=csv.QUOTE_MINIMAL,
    #         quotechar='"',
    #         line_terminator=os.linesep,
    #         chunksize=None,
    #         date_format=None,
    #         doublequote=True,
    #         escapechar=None,
    #         decimal="."
    #     ):
    #     """
    #     saves form as a csv according to: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html
    #
    #     :param path_or_buf (str or file handle): File path or object
    #     :param sep (str length 1): field delimiter
    #     :param na_rep (str): missing data representation
    #     :param float_format (str): format for floating point numbers
    #     :param columns (sequence): columns to write
    #     :param header (bool or list of str): write out the column names
    #     :param index (bool): write row names
    #     :param index_label (str or sequence, or False): column label for index columns if desired
    #     :param mode (str): python write mode
    #     :param encoding (str): encoding to use
    #     :param compression (str or dict): compression mode
    #     :param quoting (constance from csv module): csv value handling of numerics
    #     :param quotechar (str): character used to quote fields
    #     :param line_terminator (str): newline character
    #     :param chunksize (int or None): rows to write at a time
    #     :param date_format (str): format string for datetime objects
    #     :param doublequote (bool): control quoting of quotechar inside a field
    #     :param escapechar (str): character used to escape sep and quotechar
    #     :param decimal (str): character recognized as decimal separator
    #     :return: string of df if path_or_buf is None
    #     """
    #
    #     return self.form().to_csv(
    #         path_or_buf,
    #         sep,
    #         na_rep,
    #         float_format,
    #         columns,
    #         header,
    #         index,
    #         index_label,
    #         mode,
    #         encoding,
    #         compression,
    #         quoting,
    #         quotechar,
    #         line_terminator,
    #         chunksize,
    #         date_format,
    #         doublequote,
    #         escapechar,
    #         decimal
    #     )


    def __str__(self):
        return str(self.form())



class Form10K(Form):
    """
    Abstract Data Type for the SEC Form 10-K
    """
    def __init__(self, df):
        super().__init__(df)
        self.df = Form.pivot(self.df, columns="fy")



    # def calc_ROA(self):
    #     """
    #     calculates ROA = net income / average total assets
    #
    #     :return (df): the ROA values
    #     """
    #     # self.df.groupby(["tag", "uom"]).first().reset_index()
    #     return

    def calc_ROE(self):
        """
        calculates ROE = net income / total stockholders equity

        :return (df): the ROE values
        """
        net_income =  self.filter("^NetIncomeLoss$")
        stockholders_equity = self.filter("^StockholdersEquity$")
        years = net_income.columns.to_list()
        df = net_income.reindex([("ROE", "ratio")])

        for year in years:
            df[year] = net_income[year][0] / stockholders_equity[year][0]

        return df


    def calc_CurrentRatio(self):
        """
        calculates the current ratio = current assets / current liabilities

        :return (df): the current ratio values
        """
        current_assets = self.filter("^AssetsCurrent$")
        current_liabilities = self.filter("^LiabilitiesCurrent$")
        years = current_assets.columns.to_list()
        df = current_assets.reindex([("CurrentRatio", "ratio")])

        for year in years:
            df[year] = current_assets[year][0] / current_liabilities[year][0]

        return df


    def calc_DebtToEquity(self):
        """
        calculates the debt-to-equity ratio = total liabilities / total stockholders equity

        :return (df): the debt-to-equity ratio
        """
        total_liabilities = self.filter("^Liabilities$")
        stockholders_equity = self.filter("^StockholdersEquity$")
        years = total_liabilities.columns.to_list()
        df = total_liabilities.reindex([("DebtToEquity", "ratio")])

        for year in years:
            df[year] = total_liabilities[year][0] / stockholders_equity[year][0]

        return df


    def calc_BookValue(self):
        """
        calculates the book value = total assets - total liabilities

        :return (df): the book value
        """
        assets = self.filter("^Assets$")
        liabilities = self.filter("^Liabilities$")
        years = assets.columns.to_list()
        df = assets.reindex([("BookValue", "USD")])

        for year in years:
            df[year] = assets[year][0] - liabilities[year][0]

        return df




class Form10Q(Form):
    """
    Abstract Data Type for the SEC Form 10-Q
    """
    def __init__(self, df):
        super().__init__(df)
        self.df = Form.pivot(self.df, columns=["fy", "fp"])


