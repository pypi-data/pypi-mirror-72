# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

"""Boston city safety."""

from ._city_safety import CitySafety
from .dataaccess._blob_accessor import BlobAccessorDescriptor


class BostonSafety(CitySafety):
    """Represents the Boston Safety public dataset.

    This dataset contains 311 calls reported to the city of Boston.
    For more information about this dataset, including column descriptions, different ways to access the dataset,
    and examples, see `Boston Safety Data <https://azure.microsoft.com/services/open-datasets/catalog/
    boston-safety-data/>`_ in the Microsoft Azure Open Datasets catalog.

    :param start_data: The date at which to start loading data, inclusive. If None, the ``default_start_date``
        is used.
    :type start_data: datetime
    :param end_data: The date at which to end loading data, inclusive. If None, the ``default_end_date``
        is used.
    :type end_data: datetime
    :param cols: A list of columns names to load from the dataset. If None, all columns are loaded. For
        information on the available columns in this dataset, see `Boston Safety Data <https://azure.microsoft.com/
        services/open-datasets/catalog/boston-safety-data/>`__.
    :type cols: builtin.list[str]
    :param enable_telemetry: Whether to enable telemetry on this dataset.
    :type enable_telemetry: bool
    """

    """const instance of blob accessor."""
    _blob_accessor = BlobAccessorDescriptor("city_safety_boston")
