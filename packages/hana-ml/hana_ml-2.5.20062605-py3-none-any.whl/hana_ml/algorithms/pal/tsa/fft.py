"""
This module contains Python wrapper for PAL Fast-Fourier-Transform(FFT) algorithm.

The following class is available:

    * :class:`FFT`
    * :func:`fft`
"""

# pylint:disable=line-too-long, too-few-public-methods
import logging
import uuid
from hdbcli import dbapi
from hana_ml.algorithms.pal.pal_base import (
    PALBase,
    #Table,
    ParameterTable,
    #INTEGER,
    #DOUBLE,
    try_drop,
    require_pal_usable,
    call_pal_auto
)
logger = logging.getLogger(__name__)#pylint: disable=invalid-name

class FFT(PALBase):
    r"""
    Fast Fourier Transform is applied to discrete data sequence.

    Parameters
    ----------

    None

    Attributes
    ----------

    None

    Examples
    --------

    Training data df:

    >>> df.collect()
       ID  RE   IM
    0   1  2.0  9.0
    1   2  3.0 -3.0
    2   3  5.0  0.0
    3   4  0.0  0.0
    4   5 -2.0 -2.0
    5   6 -9.0 -7.0
    6   7  7.0  0.0

    Create a FFT instance:

    >>> fft = FFT()

    Call apply() on given data sequence:

    >>> result = fft.apply(data=df, inverse=False)
    >>> result.collect()
       ID   REAL        IMAG
    0   1   6.000000   -3.000000
    1   2   16.273688  -0.900317
    2   3  -5.393946    26.265112
    3   4  -13.883222   18.514840
    4   5  -4.233990   -2.947800
    5   6   9.657319    3.189618
    6   7   5.580151    21.878547

    """

    number_type_map = {'real':1, 'imag':2}
    def apply(self, data, num_type=None, inverse=None):
        """
        Apply Fast-Fourier-Transfrom to the input data, and return the transformed data.

        Parameters
        ----------

        data : DataFrame
            The DataFrame contains at most 3 columns. The first column is ID, which indicates order of sequence.
            The second column is the real part of the sequenc. The third column indicates imaginary part of the sequence which is optional.

        num_type : {'real', 'imag'}, optional
            Number type for the second column of the input data.
            Valid only when the input data contains 3 columns.

            Defaults to 'real'.
        inverse : bool, optional
            If False, forward FFT is applied; otherwise inverse FFT is applied.

            Defaults to False.

        Returns
        -------

        DataFrame
            Dataframe containing the transformed sequence, structured as follows:

                - 1st column: ID, with same name and type as input data.
                - 2nd column: REAL, type DOUBLE, representing real part of the transformed sequence.
                - 3rd column: IMAG, type DOUBLE, represneting imaginary part of the transformed sequence.

        """
        conn = data.connection_context
        require_pal_usable(conn)
        inverse = self._arg('inverse', inverse, bool)
        num_type = self._arg('num_type', num_type, self.number_type_map)

        unique_id = str(uuid.uuid1()).replace('-', '_').upper()

        #tables = ['DATA', 'PARAM', 'RESULT']
        result_tbl = '#PAL_FFT_RESULT_TBL_{}_{}'.format(self.id, unique_id)
        #data_tbl, param_tbl, result_tbl = tables

        param_rows = [
            ('INVERSE', None if inverse is None else int(inverse), None, None),
            ('NUMBER_TYPE',
             None if num_type is None else int(num_type),
             None, None)
            ]
        #result_spec = [
        #    ("ID", INTEGER),
        #    ("REAL", DOUBLE),
        #    ("IMAG", DOUBLE)
        #    ]
        try:
            #self._materialize(data_tbl, data)
            #self._create(ParameterTable(param_tbl).with_data(param_rows))
            #self._create(Table(result_tbl, result_spec))

            call_pal_auto(conn,
                          "PAL_FFT",
                          data,
                          ParameterTable().with_data(param_rows),
                          result_tbl)
        except dbapi.Error as db_err:
            #msg = ('HANA error while attempting to apply FFT.')
            logger.exception(str(db_err))
            try_drop(conn, result_tbl)
            raise

        return conn.table(result_tbl)

def fft(data, num_type=None, inverse=None):
    """
    Apply Fast-Fourier-Transfrom to the input data, and return the transformed data.

    Parameters
    ----------
    data : DataFrame
        The DataFrame contains at most 3 columns. The first column is ID, which indicates order of sequence.
        The second column is the real part of the sequenc. The third column indicates imaginary part of the sequence which is optional.

    num_type : {'real', 'imag'}, optional
        Number type for the second column of the input data.
        Valid only when the input data contains 3 columns.

        Defaults to 'real'.
    inverse : bool, optional
        If False, forward FFT is applied; otherwise inverse FFT is applied.

        Defaults to False.

    Returns
    -------

    DataFrame
        Dataframe containing the transformed sequence, structured as follows:

            - 1st column: ID, with same name and type as input data.
            - 2nd column: REAL, type DOUBLE, representing real part of the transformed sequence.
            - 3rd column: IMAG, type DOUBLE, represneting imaginary part of the transformed sequence.
    Examples
    --------

    Training data df:

    >>> df.collect()
       ID  RE   IM
    0   1  2.0  9.0
    1   2  3.0 -3.0
    2   3  5.0  0.0
    3   4  0.0  0.0
    4   5 -2.0 -2.0
    5   6 -9.0 -7.0
    6   7  7.0  0.0

    >>> result = fft(data=df, inverse=False)
    >>> result.collect()
       ID   REAL        IMAG
    0   1   6.000000   -3.000000
    1   2   16.273688  -0.900317
    2   3  -5.393946    26.265112
    3   4  -13.883222   18.514840
    4   5  -4.233990   -2.947800
    5   6   9.657319    3.189618
    6   7   5.580151    21.878547
    """
    fft_instance = FFT()
    return fft_instance.apply(data, num_type, inverse)
