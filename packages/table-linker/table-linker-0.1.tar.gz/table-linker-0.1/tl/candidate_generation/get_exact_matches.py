import pandas as pd
from tl.candidate_generation.es_search import Search
from tl.candidate_generation.utility import Utility
from tl.exceptions import RequiredInputParameterMissingException


class ExactMatches(object):
    def __init__(self, es_url, es_index, es_user=None, es_pass=None):
        self.es = Search(es_url, es_index, es_user=es_user, es_pass=es_pass)
        self.utility = Utility(self.es)

    def get_exact_matches(self, column, properties="labels,aliases", lower_case=False, size=50, file_path=None,
                          df=None):
        """
        retrieves the identifiers of KG entities whose label or aliases match the input values exactly.

        Args:
            column: the column used for retrieving candidates.
            properties: a comma separated names of properties in the KG to search for exact match query: default is labels,aliases
            lower_case: case insensitive retrieval, default is case sensitive.
            size: maximum number of candidates to retrieve, default is 50.
            file_path: input file in canonical format
            df: input dataframe in canonical format

        Returns: a dataframe in candidates format

        """
        if file_path is None and df is None:
            raise RequiredInputParameterMissingException(
                'One of the input parameters is required: {} or {}'.format("file_path", "df"))

        if file_path:
            df = pd.read_csv(file_path, dtype=object)

        df.fillna(value="", inplace=True)

        return self.utility.create_candidates_df(df, column, size, properties, 'exact-match', lower_case=lower_case)
