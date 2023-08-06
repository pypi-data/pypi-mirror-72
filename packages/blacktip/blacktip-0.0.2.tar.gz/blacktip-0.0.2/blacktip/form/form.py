
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
        return self.df.reset_index()


    def form(self):
        """
        MAIN GETTER METHOD
        getter method for the nicely formatted dataframe

        :return (df): the formatted dataframe
        """
        return self.df.groupby(["tag", "uom"]).first().reset_index()


    def generate_sheet(self, regex):
        """
        generates a data sheet based on a keyword regex

        :param regex (str): the keyword regular expression
        :return (df): a subset of the whole dataframe filtered by the regex
        """
        form = self.form()
        return form[form.tag.str.contains(regex)].reset_index(drop=True)


    def asset_sheet(self):
        """
        generates a data sheet of "Asset" values

        :return (df): a subset of the whole dataframe filtered by assets
        """
        return self.generate_sheet("Asset|Assets")


    def liability_sheet(self):
        """
        generates a data sheet of "Liability" values

        :return (df): a subset of the whole dataframe filtered by liabilities
        """
        return self.generate_sheet("Liability|Liabilities")


    def debt_sheet(self):
        """
        generates a data sheet of "Debt" values

        :return (df): a subset of the whole dataframe filtered by debts
        """
        return self.generate_sheet("Debt|Debts")




class Form10K(Form):
    """
    Abstract Data Type for the SEC Form 10-K
    """
    def __init__(self, df):
        super().__init__(df)
        self.df = Form.pivot(self.df, columns="fy")




class Form10Q(Form):
    """
    Abstract Data Type for the SEC Form 10-Q
    """
    def __init__(self, df):
        super().__init__(df)
        self.df = Form.pivot(self.df, columns=["fy", "fp"])


