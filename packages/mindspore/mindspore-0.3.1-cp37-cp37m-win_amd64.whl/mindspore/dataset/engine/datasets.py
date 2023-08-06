# Copyright 2019 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""
datasets.py supports various formats of datasets, including ImageNet, TFData,
MNIST, Cifar10/100, Manifest, MindRecord, etc. This module could load data in
high performance and parse data precisely. It also provides the following
operations for users to preprocess data: shuffle, batch, repeat, map, and zip.
"""
import glob
import json
import math
import os
import uuid
import multiprocessing
import queue
from enum import Enum
from importlib import import_module
import threading

import copy
import numpy as np

from mindspore._c_dataengine import DataType, TFReaderOp, ImageFolderOp, CifarOp, MnistOp, ManifestOp, \
    MindRecordOp, TextFileOp, VOCOp, CBatchInfo
from mindspore._c_expression import typing

from mindspore import log as logger
from . import samplers
from .iterators import DictIterator, TupleIterator
from .validators import check_batch, check_shuffle, check_map, check_filter, check_repeat, check_skip, check_zip, \
    check_rename, \
    check_take, check_project, check_imagefolderdatasetv2, check_mnist_cifar_dataset, check_manifestdataset, \
    check_tfrecorddataset, check_vocdataset, check_celebadataset, check_minddataset, check_generatordataset, \
    check_sync_wait, check_zip_dataset, check_add_column, check_textfiledataset, check_concat, check_split
from ..core.datatypes import mstype_to_detype, mstypelist_to_detypelist

try:
    context = import_module("mindspore.context")
except ModuleNotFoundError:
    context = None


class Shuffle(str, Enum):
    GLOBAL: str = "global"
    FILES: str = "file"


@check_zip
def zip(datasets):
    """
    Zips the datasets in the input tuple of datasets.

    Args:
        datasets (tuple of class Dataset): A tuple of datasets to be zipped together.
            The number of datasets should be more than 1.

    Returns:
        DatasetOp, ZipDataset.

    Raises:
        ValueError: If the number of datasets is 1.
        TypeError: If datasets is not a tuple.

    Examples:
            >>> import mindspore.dataset as ds
            >>>
            >>> dataset_dir1 = "path/to/imagefolder_directory1"
            >>> dataset_dir2 = "path/to/imagefolder_directory2"
            >>> ds1 = ds.ImageFolderDatasetV2(dataset_dir1, num_parallel_workers=8)
            >>> ds2 = ds.ImageFolderDatasetV2(dataset_dir2, num_parallel_workers=8)
            >>>
            >>> # creates a dataset which is the combination of ds1 and ds2
            >>> data = ds.zip((ds1, ds2))
    """
    if len(datasets) <= 1:
        raise ValueError(
            "Can't zip empty or just one dataset!")
    return ZipDataset(datasets)


def get_num_rows(num_rows, num_shards):
    """
    Get the number rows of the dataset according to the shards.

    Args:
        num_rows (int): The number rows of the dataset should be more than 0.
            The number rows of the dataset should be more than 0.
        num_shards (int or None): Number of shards that the dataset should be divided into.
            The number of shards should be None or more than 1.

    Returns:
        Int, number of rows.

    Raises:
        ValueError: If num_rows is invalid (< 0).
        ValueError: If num_shards is invalid (<= 0).
    """
    if num_rows < 0:
        raise ValueError("num_rows is invalid (< 0)")

    if num_shards is not None:
        if num_shards <= 0:
            raise ValueError("num_shards is invalid (<= 0)")
        if num_rows % num_shards == 0:
            num_rows = num_rows // num_shards
        else:
            num_rows = num_rows // num_shards + 1
    return num_rows


class Dataset:
    """
    Abstract class to represent a dataset in DataEngine's data pipeline.

    This class is the base class of SourceDataset and DatasetOp, and represents
    a node in the data flow graph.

    Args:
        num_parallel_workers (int, optional): Number of workers to process the Dataset in parallel
            (default=None).
    """

    def __init__(self, num_parallel_workers=None):
        self.input = []
        self.output = []
        self.num_parallel_workers = num_parallel_workers
        self._device_iter = 0
        self._input_indexs = ()
        self._output_types = None
        self._output_shapes = None
        self._dataset_size = None
        self._batch_size = None
        self._num_classes = None
        self._repeat_count = None
        self._sync = False

    def __add__(self, datasets):
        return self.concat(datasets)

    def get_args(self):
        """
        Returns attributes (member variables) related to the current class.

        Must include all arguments passed to the __init__() of the current class, excluding 'input_dataset'.

        Args:

        Returns:
            Python dictionary.
        """
        args = dict()
        args["num_parallel_workers"] = self.num_parallel_workers
        return args

    @check_batch
    def batch(self, batch_size, drop_remainder=False, num_parallel_workers=None, per_batch_map=None,
              input_columns=None, pad_info=None):
        """
        Combines batch_size number of consecutive rows into batches.

        For any child node, a batch is treated as a single row.
        For any column, all the elements within that column must have the same shape.
        If a per_batch_map callable is provided, it will be applied to the batches of tensors.

        Note:
            The order of using repeat and batch reflects the number of batches. Recommend that
            repeat operation should be used after batch operation.

        Args:
            batch_size (int or function): The number of rows each batch is created with. An
                int or callable which takes exactly 1 parameter, BatchInfo.
            drop_remainder (bool, optional): Determines whether or not to drop the last
                possibly incomplete batch (default=False). If True, and if there are less
                than batch_size rows available to make the last batch, then those rows will
                be dropped and not propagated to the child node.
            num_parallel_workers (int, optional): Number of workers to process the Dataset in parallel (default=None).
            per_batch_map (callable, optional): Per batch map callable. A callable which takes
                (list[Tensor], list[Tensor], ..., BatchInfo) as input parameters. Each list[Tensor] represent a batch of
                Tensors on a given column. The number of lists should match with number of entries in input_columns. The
                last parameter of the callable should always be a BatchInfo object.
            input_columns (list of string, optional): List of names of the input columns. The size of the list should
                match with signature of per_batch_map callable.
            pad_info (dict, optional): Whether to perform padding on selected columns. pad_info={"col1":([224,224],0)}
                would pad column with name "col1" to a tensor of size [224,224] and fill the missing with 0.

        Returns:
            BatchDataset, dataset batched.

        Examples:
            >>> import mindspore.dataset as ds
            >>> # data is an instance of Dataset object.
            >>> # creates a dataset where every 100 rows is combined into a batch
            >>> # and drops the last incomplete batch if there is one.
            >>> data = data.batch(100, True)
        """
        return BatchDataset(self, batch_size, drop_remainder, num_parallel_workers, per_batch_map, input_columns,
                            pad_info)

    @check_sync_wait
    def sync_wait(self, condition_name, num_batch=1, callback=None):
        '''
        Add a blocking condition to the input Dataset.

        Args:
            num_batch (int): the number of batches without blocking at the start of each epoch.
            condition_name (str): The condition name that is used to toggle sending next row.
            callback (function): The callback funciton that will be invoked when sync_update is called.

        Raises:
            RuntimeError: If condition name already exists.

        Examples:
            >>> import mindspore.dataset as ds
            >>> # data is an instance of Dataset object.
            >>> data = data.sync_wait("callback1")
            >>> data = data.batch(batch_size)
            >>> for batch_data in data.create_dict_iterator():
            >>>     data = data.sync_update("callback1")
        '''
        return SyncWaitDataset(self, condition_name, num_batch, callback)

    @check_shuffle
    def shuffle(self, buffer_size):
        """
        Randomly shuffles the rows of this dataset using the following algorithm:

        1. Make a shuffle buffer that contains the first buffer_size rows.
        2. Randomly select an element from the shuffle buffer to be the next row
           propogated to the child node.
        3. Get the next row (if any) from the parent node and put it in the shuffle buffer.
        4. Repeat steps 2 and 3 until there are no more rows left in the shuffle buffer.

        A seed can be provided to be used on the first epoch. In every subsequent
        epoch, the seed is changed to a new one, randomly generated value.

        Args:
            buffer_size (int): The size of the buffer (must be larger than 1) for
                shuffling. Setting buffer_size equal to the number of rows in the entire
                dataset will result in a global shuffle.

        Returns:
            ShuffleDataset, dataset shuffled.

        Raises:
            RuntimeError: If exist sync operators before shuffle.

        Examples:
            >>> import mindspore.dataset as ds
            >>> # data is an instance of Dataset object
            >>> # optionally set the seed for the first epoch
            >>> ds.config.set_seed(58)
            >>>
            >>> # creates a shuffled dataset using a shuffle buffer of size 4
            >>> data = data.shuffle(4)
        """
        return ShuffleDataset(self, buffer_size)

    def flat_map(self, func):
        """
        Maps `func` to each row in dataset and flatten the result.

        The specified `func` is a function that must take one 'Ndarray' as input
        and return a 'Dataset'.

        Args:
            func (function): A function that must take one 'Ndarray' as an argument and
                return a 'Dataset'.

        Returns:
            Dataset, applied by the function.

        Examples:
            >>> import mindspore.dataset as ds
            >>> import mindspore.dataset.text as text
            >>> # declare a function which returns a Dataset object
            >>> def flat_map_func(x):
            >>>     data_dir = text.to_str(x[0])
            >>>     d = ds.ImageFolderDatasetV2(data_dir)
            >>>     return d
            >>> # data is a Dataset object
            >>> data = ds.TextFileDataset(DATA_FILE)
            >>> data = data.flat_map(flat_map_func)

        Raises:
            TypeError: If `func` is not a function.
            TypeError: If `func` doesn't return a Dataset.
        """
        dataset = None
        if not hasattr(func, '__call__'):
            raise TypeError("func must be a function.")

        for row_data in self:
            if dataset is None:
                dataset = func(row_data)
            else:
                dataset += func(row_data)

        if not isinstance(dataset, Dataset):
            raise TypeError("flat_map must return a Dataset object.")
        return dataset

    @check_map
    def map(self, input_columns=None, operations=None, output_columns=None, columns_order=None,
            num_parallel_workers=None, python_multiprocessing=False):
        """
        Applies each operation in operations to this dataset.

        The order of operations is determined by the position of each operation in operations.
        operations[0] will be applied first, then operations[1], then operations[2], etc.

        Each operation will be passed one or more columns from the dataset as input, and zero or
        more columns will be outputted. The first operation will be passed the columns specified
        in input_columns as input. If there is more than one operator in operations, the outputted
        columns of the previous operation are used as the input columns for the next operation.
        The columns outputted by the very last operation will be assigned names specified by
        output_columns.

        Only the columns specified in columns_order will be propagated to the child node. These
        columns will be in the same order as specified in columns_order.

        Args:
            input_columns (list[str]): List of the names of the columns that will be passed to
                the first operation as input. The size of this list must match the number of
                input columns expected by the first operator. (default=None, the first
                operation will be passed however many columns that is required, starting from
                the first column).
            operations (list[TensorOp] or Python list[functions]): List of operations to be
                applied on the dataset. Operations are applied in the order they appear in this list.
            output_columns (list[str], optional): List of names assigned to the columns outputted by
                the last operation. This parameter is mandatory if len(input_columns) !=
                len(output_columns). The size of this list must match the number of output
                columns of the last operation. (default=None, output columns will have the same
                name as the input columns, i.e., the columns will be replaced).
            columns_order (list[str], optional): list of all the desired columns to propagate to the
                child node. This list must be a subset of all the columns in the dataset after
                all operations are applied. The order of the columns in each row propagated to the
                child node follow the order they appear in this list. The parameter is mandatory
                if the len(input_columns) != len(output_columns). (default=None, all columns
                will be propagated to the child node, the order of the columns will remain the
                same).
            num_parallel_workers (int, optional): Number of threads used to process the dataset in
                parallel (default=None, the value from the config will be used).
            python_multiprocessing (bool, optional): Parallelize python operations with multiple worker process. This
                option could be beneficial if the python operation is computational heavy (default=False).

        Returns:
            MapDataset, dataset after mapping operation.

        Examples:
            >>> import mindspore.dataset as ds
            >>> import mindspore.dataset.transforms.vision.c_transforms as c_transforms
            >>>
            >>> # data is an instance of Dataset which has 2 columns, "image" and "label".
            >>> # ds_pyfunc is an instance of Dataset which has 3 columns, "col0", "col1", and "col2". Each column is
            >>> # a 2d array of integers.
            >>>
            >>> # This config is a global setting, meaning that all future operations which
            >>> # uses this config value will use 2 worker threads, unless if specified
            >>> # otherwise in their constructor. set_num_parallel_workers can be called
            >>> # again later if a different number of worker threads are needed.
            >>> ds.config.set_num_parallel_workers(2)
            >>>
            >>> # Two operations, which takes 1 column for input and outputs 1 column.
            >>> decode_op = c_transforms.Decode(rgb_format=True)
            >>> random_jitter_op = c_transforms.RandomColorAdjust((0.8, 0.8), (1, 1), (1, 1), (0, 0))
            >>>
            >>> # 1) Simple map example
            >>>
            >>> operations = [decode_op]
            >>> input_columns = ["image"]
            >>>
            >>> # Applies decode_op on column "image". This column will be replaced by the outputed
            >>> # column of decode_op. Since columns_order is not provided, both columns "image"
            >>> # and "label" will be propagated to the child node in their original order.
            >>> ds_decoded = data.map(input_columns, operations)
            >>>
            >>> # Rename column "image" to "decoded_image"
            >>> output_columns = ["decoded_image"]
            >>> ds_decoded = data.map(input_columns, operations, output_columns)
            >>>
            >>> # Specify the order of the columns.
            >>> columns_order ["label", "image"]
            >>> ds_decoded = data.map(input_columns, operations, None, columns_order)
            >>>
            >>> # Rename column "image" to "decoded_image" and also specify the order of the columns.
            >>> columns_order ["label", "decoded_image"]
            >>> output_columns = ["decoded_image"]
            >>> ds_decoded = data.map(input_columns, operations, output_columns, columns_order)
            >>>
            >>> # Rename column "image" to "decoded_image" and keep only this column.
            >>> columns_order ["decoded_image"]
            >>> output_columns = ["decoded_image"]
            >>> ds_decoded = data.map(input_columns, operations, output_columns, columns_order)
            >>>
            >>> # Simple example using pyfunc. Renaming columns and specifying column order
            >>> # work in the same way as the previous examples.
            >>> input_columns = ["col0"]
            >>> operations = [(lambda x: x + 1)]
            >>> ds_mapped = ds_pyfunc.map(input_columns, operations)
            >>>
            >>> # 2) Map example with more than one operation
            >>>
            >>> # If this list of operations is used with map, decode_op will be applied
            >>> # first, then random_jitter_op will be applied.
            >>> operations = [decode_op, random_jitter_op]
            >>>
            >>> input_columns = ["image"]
            >>>
            >>> # Creates a dataset where the images are decoded, then randomly color jittered.
            >>> # decode_op takes column "image" as input and outputs one column. The column
            >>> # outputted by decode_op is passed as input to random_jitter_op.
            >>> # random_jitter_op will output one column. Column "image" will be replaced by
            >>> # the column outputted by random_jitter_op (the very last operation). All other
            >>> # columns are unchanged. Since columns_order is not specified, the order of the
            >>> # columns will remain the same.
            >>> ds_mapped = data.map(input_columns, operations)
            >>>
            >>> # Creates a dataset that is identical to ds_mapped, except the column "image"
            >>> # that is outputted by random_jitter_op is renamed to "image_transformed".
            >>> # Specifying column order works in the same way as examples in 1).
            >>> output_columns = ["image_transformed"]
            >>> ds_mapped_and_renamed = data.map(input_columns, operation, output_columns)
            >>>
            >>> # Multiple operations using pyfunc. Renaming columns and specifying column order
            >>> # work in the same way as examples in 1).
            >>> input_columns = ["col0"]
            >>> operations = [(lambda x: x + x), (lambda x: x - 1)]
            >>> output_columns = ["col0_mapped"]
            >>> ds_mapped = ds_pyfunc.map(input_columns, operations, output_columns)
            >>>
            >>> # 3) Example where number of input columns is not equal to number of output columns
            >>>
            >>> # operations[0] is a lambda that takes 2 columns as input and outputs 3 columns.
            >>> # operations[1] is a lambda that takes 3 columns as input and outputs 1 column.
            >>> # operations[1] is a lambda that takes 1 column as input and outputs 4 columns.
            >>> #
            >>> # Note: the number of output columns of operation[i] must equal the number of
            >>> # input columns of operation[i+1]. Otherwise, this map call will also result
            >>> # in an error.
            >>> operations = [(lambda x y: (x, x + y, x + y + 1)),
            >>>               (lambda x y z: x * y * z),
            >>>               (lambda x: (x % 2, x % 3, x % 5, x % 7))]
            >>>
            >>> # Note: because the number of input columns is not the same as the number of
            >>> # output columns, the output_columns and columns_order parameter must be
            >>> # specified. Otherwise, this map call will also result in an error.
            >>> input_columns = ["col2", "col0"]
            >>> output_columns = ["mod2", "mod3", "mod5", "mod7"]
            >>>
            >>> # Propagate all columns to the child node in this order:
            >>> columns_order = ["col0", "col2", "mod2", "mod3", "mod5", "mod7", "col1"]
            >>> ds_mapped = ds_pyfunc.map(input_columns, operations, output_columns, columns_order)
            >>>
            >>> # Propagate some columns to the child node in this order:
            >>> columns_order = ["mod7", "mod3", "col1"]
            >>> ds_mapped = ds_pyfunc.map(input_columns, operations, output_columns, columns_order)
        """
        return MapDataset(self, input_columns, operations, output_columns, columns_order, num_parallel_workers,
                          python_multiprocessing)

    @check_filter
    def filter(self, predicate, input_columns=None, num_parallel_workers=1):
        """
        Filter dataset by predicate.

        Note:
             If input_columns not provided or empty, all columns will be used.

        Args:
            predicate(callable): python callable which returns a boolean value, if False then filter the element.
            input_columns: (list[str], optional): List of names of the input columns, when
                default=None, the predicate will be applied on all columns in the dataset.
            num_parallel_workers (int, optional): Number of workers to process the Dataset
                in parallel (default=None).

        Returns:
            FilterDataset, dataset filter.

        Examples:
            >>> import mindspore.dataset as ds
            >>> # generator data(0 ~ 63)
            >>> # filter the data that greater than or equal to 11
            >>> dataset_f = dataset.filter(predicate=lambda data: data < 11, input_columns = ["data"])
        """
        return FilterDataset(self, predicate, input_columns, num_parallel_workers)

    @check_repeat
    def repeat(self, count=None):
        """
        Repeats this dataset count times. Repeat indefinitely if the count is None or -1.

        Note:
            The order of using repeat and batch reflects the number of batches. Recommend that
            repeat operation should be used after batch operation.
            If dataset_sink_mode is False, here repeat operation is invalid.
            If dataset_sink_mode is True, repeat count should be equal to the epoch of training. Otherwise,
            errors could occur since the amount of data is not the amount training requires.

        Args:
            count (int): Number of times the dataset should be repeated (default=None).

        Returns:
            RepeatDataset, dataset repeated.

        Examples:
            >>> import mindspore.dataset as ds
            >>> # data is an instance of Dataset object.
            >>> # creates a dataset where the dataset is repeated for 50 epochs
            >>> repeated = data.repeat(50)
            >>>
            >>> # creates a dataset where each epoch is shuffled individually
            >>> shuffled_and_repeated = data.shuffle(10)
            >>> shuffled_and_repeated = shuffled_and_repeated.repeat(50)
            >>>
            >>> # creates a dataset where the dataset is first repeated for
            >>> # 50 epochs before shuffling. the shuffle operator will treat
            >>> # the entire 50 epochs as one big dataset.
            >>> repeat_and_shuffle = data.repeat(50)
            >>> repeat_and_shuffle = repeat_and_shuffle.shuffle(10)
        """
        if count == 1:
            return self
        return RepeatDataset(self, count)

    @check_skip
    def skip(self, count):
        """
        Skip the first N elements of this dataset.

        Args:
            count (int): Number of elements the dataset should be skipped.

        Returns:
            SkipDataset, dataset skipped.

        Examples:
            >>> import mindspore.dataset as ds
            >>> # data is an instance of Dataset object.
            >>> # creates a dataset which skips first 3 elements from data
            >>> data = data.skip(3)
        """
        return SkipDataset(self, count)

    @check_take
    def take(self, count=-1):
        """
        Takes at most given numbers of elements from the dataset.

        Note:
            1. If count is greater than the number of element in dataset or equal to -1,
               all the element in dataset will be taken.
            2. The order of using take and batch effects. If take before batch operation,
               then taken given number of rows, otherwise take given number of batches.

        Args:
            count (int, optional): Number of elements to be taken from the dataset (default=-1).

        Returns:
            TakeDataset, dataset taken.

        Examples:
            >>> import mindspore.dataset as ds
            >>> # data is an instance of Dataset object.
            >>> # creates a dataset where the dataset including 50 elements.
            >>> data = data.take(50)
        """
        if count == -1:
            return self
        return TakeDataset(self, count)

    def _get_absolute_split_sizes(self, sizes):
        """
        Internal method called by split to calculate absolute split sizes and to
        do some error checking after calculating absolute split sizes.
        """
        # call get_dataset_size here and check input here because
        # dont want to call this once in check_split and another time in
        # here again
        dataset_size = self.get_dataset_size()

        if dataset_size is None or dataset_size <= 0:
            raise RuntimeError("dataset size unknown, unable to split.")

        all_int = all(isinstance(item, int) for item in sizes)
        if all_int:
            sizes_sum = sum(sizes)
            if sizes_sum != dataset_size:
                raise RuntimeError("sum of split sizes {} is not equal to dataset size {}."
                                   .format(sizes_sum, dataset_size))
            return sizes

        absolute_sizes = []
        for item in sizes:
            absolute_size = int(round(item * dataset_size))
            if absolute_size == 0:
                raise RuntimeError("split percentage {} is too small.".format(item))
            absolute_sizes.append(absolute_size)

        absolute_sizes_sum = sum(absolute_sizes)
        if absolute_sizes_sum != dataset_size:
            raise RuntimeError("sum of calculated split sizes {} is not equal to dataset size {}."
                               .format(absolute_sizes_sum, dataset_size))

        return absolute_sizes

    @check_split
    def split(self, sizes, randomize=True):
        """
        Splits the dataset into smaller, non-overlapping datasets.

        This is a general purpose split function which can be called from any operator in the pipeline.
        There is another, optimized split function, which will be called automatically if ds.split is
        called where ds is a MappableDataset.

        Args:
            sizes (list of int or list of float): If a list of integers [s1, s2, …, sn] is
                provided, the dataset will be split into n datasets of size s1, size s2, …, size sn
                respectively. If the sum of all sizes does not equal the original dataset size, an
                an error will occur.
                If a list of floats [f1, f2, …, fn] is provided, the dataset will be split into n
                Datasets of size f1*K, f2*K, …, fn*K (rounded to nearest integer) where K is the size
                of the original dataset. If after rounding, any size equals 0, an error will occur.
                All floats must be between 0 and 1 and must sum to 1, otherwise an error will occur.
            randomize (bool, optional): determines whether or not to split the data randomly (default=True).
                If true, the data will be randomly split. Otherwise, each split will be created with
                consecutive rows from the dataset.

        Note:
            1. Dataset cannot be sharded if split is going to be called.
            2. It is strongly recommended to not shuffle the dataset, but use randomize=True instead.
               Shuffling the dataset may not be deterministic, which means the data in each split
               will be different in each epoch.

        Raises:
            RuntimeError: If get_dataset_size returns None or is not supported for this dataset.
            RuntimeError: If sizes is list of integers and sum of all elements in sizes does not
                equal the dataset size.
            RuntimeError: If sizes is list of float and there is a split with size 0 after calculations.
            RuntimeError: If the dataset is sharded prior to calling split.
            ValueError: If sizes is list of float and not all floats are between 0 and 1, or if the
                floats don’t sum to 1.

        Returns
            tuple(Dataset), a tuple of datasets that have been split.

        Examples:
            >>> import mindspore.dataset as ds
            >>>
            >>> dataset_dir = "/path/to/text_file.txt"
            >>>
            >>> # TextFileDataset is not a mappable dataset, so this non optimized split will be called.
            >>> # many datasets have shuffle on by default, set shuffle to False if split will be called!
            >>> data = ds.TextFileDataset(dataset_dir, shuffle=False)
            >>> train, test = data.split([0.9, 0.1])
        """
        if self.is_shuffled():
            logger.warning("dataset is shuffled before split.")

        if self.is_sharded():
            raise RuntimeError("dataset should not be sharded before split.")

        absolute_sizes = self._get_absolute_split_sizes(sizes)
        splits = []
        rows_to_skip = 0
        for size in absolute_sizes:
            ds = copy.deepcopy(self)
            if randomize:
                # want to shuffle the same way every epoch before split
                # in alter_tree, shuffle buffer is minimum 10000, so use 10000 here
                ds = ds.shuffle(10000)
                ds.reshuffle_each_epoch = False

            if rows_to_skip > 0:
                ds = ds.skip(rows_to_skip)

            ds = ds.take(size)
            splits.append(ds)

            rows_to_skip += size

        return tuple(splits)

    @check_zip_dataset
    def zip(self, datasets):
        """
        Zips the datasets in the input tuple of datasets. Columns in the input datasets must not have the same name.

        Args:
            datasets (tuple or class Dataset): A tuple of datasets or a single class Dataset
                to be zipped together with this dataset.

        Returns:
            ZipDataset, dataset zipped.

        Examples:
            >>> import mindspore.dataset as ds
            >>> # ds1 and ds2 are instances of Dataset object
            >>> # creates a dataset which is the combination of ds1 and ds2
            >>> data = ds1.zip(ds2)
        """
        if isinstance(datasets, tuple):
            datasets = (self, *datasets)
        elif isinstance(datasets, Dataset):
            datasets = (self, datasets)
        else:
            raise TypeError("The zip function %s type error!" % (datasets))
        return ZipDataset(datasets)

    @check_concat
    def concat(self, datasets):
        """
        Concat the datasets in the input list of datasets, supported using "+" to reload concat operation.

        Note:
            The column name，column data type and rank of column data should be the same in input datasets.

        Args:
            datasets (list or class Dataset): A list of datasets or a single class Dataset
                to be concatenated together with this dataset.

        Returns:
            ConcatDataset, dataset concatenated.

        Examples:
            >>> import mindspore.dataset as ds
            >>> # ds1 and ds2 are instances of Dataset object
            >>> # creates a dataset by concating ds1 and ds2 with "+" operation
            >>> data1 = ds1 + ds2
            >>> # creates a dataset by concating ds1 and ds2 with concat operation
            >>> data1 = ds1.concat(ds2)
        """
        if isinstance(datasets, Dataset):
            datasets = [self] + [datasets]
        elif isinstance(datasets, list):
            datasets = [self] + datasets
        else:
            raise TypeError("The concat_dataset function %s type error!" % (datasets))
        return ConcatDataset(datasets)

    @check_rename
    def rename(self, input_columns, output_columns):
        """
        Renames the columns in input datasets.

        Args:
            input_columns (list[str]): list of names of the input columns.
            output_columns (list[str]): list of names of the output columns.

        Returns:
            RenameDataset, dataset renamed.

        Examples:
            >>> import mindspore.dataset as ds
            >>> # data is an instance of Dataset object.
            >>> input_columns = ["input_col1", "input_col2", "input_col3"]
            >>> output_columns = ["output_col1", "output_col2", "output_col3"]
            >>>
            >>> # creates a dataset where input_col1 is renamed to output_col1, and
            >>> # input_col2 is renamed to output_col2, and input_col3 is renamed
            >>> # to output_col3.
            >>> data = data.rename(input_columns=input_columns, output_columns=output_columns)
        """

        return RenameDataset(self, input_columns, output_columns)

    @check_project
    def project(self, columns):
        """
        Projects certain columns in input datasets.

        The specified columns will be selected from the dataset and passed down
        the pipeline in the order specified. The other columns are discarded.

        Args:
            columns(list[str]): list of names of the columns to project.

        Returns:
            ProjectDataset, dataset projected.

        Examples:
            >>> import mindspore.dataset as ds
            >>> # data is an instance of Dataset object
            >>> columns_to_project = ["column3", "column1", "column2"]
            >>>
            >>> # creates a dataset that consist of column3, column1, column2
            >>> # in that order, regardless of the original order of columns.
            >>> data = data.project(columns=columns_to_project)
        """

        return ProjectDataset(self, columns)

    def apply(self, apply_func):
        """
        Apply a function in this dataset.

        The specified apply_func is a function that must take one 'Dataset' as an argument
        and return a preprogressing 'Dataset'.

        Args:
            apply_func (function): A function that must take one 'Dataset' as an argument and
                                   return a preprogressing 'Dataset'.

        Returns:
            Dataset, applied by the function.

        Examples:
            >>> import mindspore.dataset as ds
            >>> # data is an instance of Dataset object
            >>> # declare an apply_func function which returns a Dataset object
            >>> def apply_func(ds):
            >>>     ds = ds.batch(2)
            >>>     return ds
            >>> # use apply to call apply_func
            >>> data = data.apply(apply_func)

        Raises:
            TypeError: If apply_func is not a function.
            TypeError: If apply_func doesn't return a Dataset.
        """

        if not hasattr(apply_func, '__call__'):
            raise TypeError("apply_func must be a function.")

        dataset = apply_func(self)
        if not isinstance(dataset, Dataset):
            raise TypeError("apply_func must return a dataset.")
        return dataset

    def device_que(self, prefetch_size=None):
        """
        Returns a transferredDataset that transfer data through device.

        Args:
            prefetch_size (int, optional): prefetch number of records ahead of the
                user's request (default=None).

        Note:
            If device is Ascend, features of data will be transferred one by one. The limitation
            of data transmission per time is 256M.

        Return:
            TransferDataset, dataset for transferring.
        """
        return self.to_device()

    def to_device(self, num_batch=None):
        """
        Transfers data through CPU, GPU or Ascend devices.

        Args:
            num_batch (int, optional): limit the number of batch to be sent to device (default=None).

        Note:
            If device is Ascend, features of data will be transferred one by one. The limitation
            of data transmission per time is 256M.

        Returns:
            TransferDataset, dataset for transferring.

        Raises:
            TypeError: If device_type is empty.
            ValueError: If device_type is not 'Ascend', 'GPU' or 'CPU'.
            ValueError: If num_batch is None or 0 or larger than int_max.
            RuntimeError: If dataset is unknown.
            RuntimeError: If distribution file path is given but failed to read.
        """
        if num_batch is None:
            num_batch = self.get_dataset_size()
            repeat_count = self.get_repeat_count()
            num_batch = num_batch * repeat_count

        queue_name = str(uuid.uuid1())

        if context:
            device_type = context.get_context("device_target")
        else:
            device_type = "CPU"

        if device_type == "":
            raise TypeError("Please set device_type in context")

        if device_type not in ('Ascend', 'GPU', 'CPU'):
            raise ValueError("only support CPU, Ascend, GPU")

        if num_batch is None or num_batch == 0:
            raise ValueError("num_batch is None or 0.")

        def get_distribution(output_dataset):
            dev_id = 0
            if isinstance(output_dataset, (MindDataset)):
                return output_dataset.distribution, dev_id
            if isinstance(output_dataset, (Cifar10Dataset, Cifar100Dataset, GeneratorDataset, ImageFolderDatasetV2,
                                           ManifestDataset, MnistDataset, VOCDataset, CelebADataset)):
                sampler = output_dataset.sampler
                if isinstance(sampler, samplers.DistributedSampler):
                    dev_id = sampler.shard_id
                return "", dev_id
            if isinstance(output_dataset, TFRecordDataset):
                if output_dataset.shard_id is not None:
                    dev_id = output_dataset.shard_id
                return "", dev_id

            if not output_dataset.input:
                raise RuntimeError("Unknown output_dataset: {}".format(type(output_dataset)))
            input_dataset = output_dataset.input[0]
            return get_distribution(input_dataset)

        distribution_path, device_id = get_distribution(self)
        if distribution_path == "":
            return TransferDataset(self, queue_name, device_id, device_type, num_batch)
        try:
            with open(distribution_path, 'r') as distribution_f:
                dist = json.load(distribution_f)
                device_id = dist["deviceId"]
        except json.decoder.JSONDecodeError:
            raise RuntimeError("Json decode error when load distribution file")
        except Exception:
            raise RuntimeError("Distribution file failed to read")

        return TransferDataset(self, queue_name, device_id, device_type, num_batch)

    def create_tuple_iterator(self, columns=None):
        """
        Create an Iterator over the dataset. The data retrieved will be a list of ndarray of data.

        To specify which columns to list and the order needed, use columns_list. If columns_list
        is not provided, the order of the columns will not be changed.

        Args:
            columns (list[str], optional): List of columns to be used to specify the order of columns
                (defaults=None, means all columns).

        Returns:
            Iterator, list of ndarray.

        Examples:
            >>> import mindspore.dataset as ds
            >>> # data is an instance of Dataset object
            >>> # creates an iterator. The columns in the data obtained by the
            >>> # iterator will not be changed.
            >>> iterator = data.create_tuple_iterator()
            >>> for item in iterator:
            >>>     # convert the returned tuple to a list and print
            >>>     print(list(item))
        """
        return TupleIterator(self, columns)

    def create_dict_iterator(self):
        """
        Create an Iterator over the dataset.

        The data retrieved will be a dictionary. The order
        of the columns in the dictionary may not be the same as the original order.

        Returns:
            Iterator, dictionary of column_name-ndarray pair.

        Examples:
            >>> import mindspore.dataset as ds
            >>> # data is an instance of Dataset object
            >>> # creates an iterator. The columns in the data obtained by the
            >>> # iterator might be changed.
            >>> iterator = data.create_dict_iterator()
            >>> for item in iterator:
            >>>     # print the data in column1
            >>>     print(item["column1"])

        """
        return DictIterator(self)

    def __iter__(self):
        """Create an Iterator over the dataset."""
        return self.create_tuple_iterator()

    @property
    def input_indexs(self):
        return self._input_indexs

    @input_indexs.setter
    def input_indexs(self, value):
        self._input_indexs = value

    def _get_pipeline_info(self):
        """
        Gets pipeline information.
        """
        device_iter = TupleIterator(self)
        self._output_shapes = device_iter.get_output_shapes()
        self._output_types = device_iter.get_output_types()
        if self._dataset_size is None:
            self._dataset_size = device_iter.get_dataset_size()
        self._batch_size = device_iter.get_batch_size()
        self._num_classes = device_iter.num_classes()
        self._repeat_count = device_iter.get_repeat_count()
        device_iter.release()

    def output_shapes(self):
        """
        Get the shapes of output data.

        Return:
            List, list of shape of each column.
        """
        if self._output_shapes is None:
            self._get_pipeline_info()
        return self._output_shapes

    def output_types(self):
        """
        Get the types of output data.

        Return:
            List of data type.
        """
        if self._output_types is None:
            self._get_pipeline_info()
        return self._output_types

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        if self.input:
            return self.input[0].get_dataset_size()
        return None

    def num_classes(self):
        """
        Get the number of classes in a dataset.

        Return:
            Number, number of classes.
        """
        if self.input:
            return self.input[0].num_classes()
        return None

    def get_sync_notifiers(self):
        if self.input:
            return self.input[0].get_sync_notifiers()
        return {}

    def is_sync(self):
        if self.input:
            return self.input[0].is_sync()
        return False

    def sync_update(self, condition_name, num_batch=None, data=None):
        """
        Release a blocking condition and triger callback with given data.

        Args:
            condition_name (str): The condition name that is used to toggle sending next row.
            num_batch (int or None): The number of batches(rows) that are released.
                When num_batch is None, it will default to the number specified by the sync_wait operator.
            data (dict or None): The data passed to the callback.
        """
        notifiers_dict = self.get_sync_notifiers()
        if condition_name not in notifiers_dict:
            raise RuntimeError("Condition name not found")
        if num_batch is not None:
            num_batch *= self.get_batch_size()
        notifiers_dict[condition_name](num_batch, data)

    def get_batch_size(self):
        """
        Get the size of a batch.

        Return:
            Number, the number of data in a batch.
        """
        if self.input:
            return self.input[0].get_batch_size()
        return 1

    def get_repeat_count(self):
        """
        Get the replication times in RepeatDataset else 1.

        Return:
            Number, the count of repeat.
        """
        if self.input:
            return self.input[0].get_repeat_count()
        return 1

    def get_class_indexing(self):
        """
        Get the class index.

        Return:
            Dict, A str-to-int mapping from label name to index.
        """
        if self.input:
            return self.input[0].get_class_indexing()
        raise NotImplementedError("Dataset {} has not supported api get_class_indexing yet.".format(type(self)))

    def reset(self):
        """Reset the dataset for next epoch."""

    def is_shuffled(self):
        for input_dataset in self.input:
            if input_dataset.is_shuffled():
                return True

        return False

    def is_sharded(self):
        for input_dataset in self.input:
            if input_dataset.is_sharded():
                return True

        return False


class SourceDataset(Dataset):
    """
    Abstract class to represent a source dataset which produces content to the data pipeline.
    """

    # No need for __init__ since it is the same as the super's init

    @staticmethod
    def _find_files(patterns):
        """
        Utility function to search for files with the given glob patterns.

        Args:
            patterns (str or list[str]): string or list of patterns to be searched.

        Returns:
            List, files.
        """

        if not isinstance(patterns, list):
            patterns = [patterns]

        file_list = []
        unmatched_patterns = []
        for pattern in patterns:
            matches = [match for match in glob.glob(pattern, recursive=True) if os.path.isfile(match)]

            if matches:
                file_list.extend(matches)
            else:
                unmatched_patterns.append(pattern)

        if unmatched_patterns:
            raise ValueError("The following patterns did not match any files: ", unmatched_patterns)

        if file_list:  # not empty
            return file_list
        raise ValueError("The list of path names matching the patterns is empty.")

    def is_shuffled(self):
        raise NotImplementedError("SourceDataset must implement is_shuffled.")

    def is_sharded(self):
        raise NotImplementedError("SourceDataset must implement is_sharded.")


class MappableDataset(SourceDataset):
    """
    Abstract class to represent a source dataset which supports use of samplers.
    """

    def __init__(self, num_parallel_workers=None):
        # check if all subclasses use this name
        super().__init__(num_parallel_workers)
        self.sampler = None

    def add_sampler(self, new_sampler):
        # note: by adding a sampler, we mean that the sampled ids will flow to new_sampler
        # after first passing through the current samplers attached to this dataset.
        new_sampler.add_child(self.sampler)
        self.sampler = new_sampler

    def use_sampler(self, new_sampler):
        """
        Will make the current dataset use the new_sampler provided.

        Args:
            new_sampler (Sampler): the sampler to use for the current dataset.

        Returns:
            Dataset, that uses new_sampler.

        Examples:
            >>> import mindspore.dataset as ds
            >>>
            >>> dataset_dir = "/path/to/imagefolder_directory"
            >>> # a SequentialSampler is created by default
            >>> data = ds.ImageFolderDatasetV2(dataset_dir)
            >>>
            >>> # use a DistributedSampler instead of the SequentialSampler
            >>> new_sampler = ds.DistributedSampler(10, 2)
            >>> data.use_sampler(new_sampler)
        """
        if new_sampler is None:
            raise TypeError("Input sampler could not be None.")
        if not isinstance(new_sampler, (samplers.BuiltinSampler, samplers.Sampler)):
            raise TypeError("Input sampler is not an instance of a sampler.")

        self.sampler = self.sampler.child_sampler
        self.add_sampler(new_sampler)

    def is_shuffled(self):
        raise NotImplementedError("MappableDataset must implement is_shuffled.")

    def is_sharded(self):
        raise NotImplementedError("MappableDataset must implement is_sharded.")

    def _get_sampler_dataset_size(self):
        if self.sampler is not None:
            if hasattr(self.sampler, 'get_dataset_size'):
                return self.sampler.get_dataset_size()
            if hasattr(self.sampler, '__len__'):
                return len(self.sampler)

        return None

    @check_split
    def split(self, sizes, randomize=True):
        """
        Splits the dataset into smaller, non-overlapping datasets.

        There is the optimized split function, which will be called automatically when the dataset
        that calls this function is a MappableDataset.

        Args:
            sizes (list of int or list of float): If a list of integers [s1, s2, …, sn] is
                provided, the dataset will be split into n datasets of size s1, size s2, …, size sn
                respectively. If the sum of all sizes does not equal the original dataset size, an
                an error will occur.
                If a list of floats [f1, f2, …, fn] is provided, the dataset will be split into n
                Datasets of size f1*K, f2*K, …, fn*K (rounded to nearest integer) where K is the size
                of the original dataset. If after rounding, any size equals 0, an error will occur.
                All floats must be between 0 and 1 and must sum to 1, otherwise an error will occur.
            randomize (bool, optional): determines whether or not to split the data randomly (default=True).
                If true, the data will be randomly split. Otherwise, each split will be created with
                consecutive rows from the dataset.

        Note:
            1. Dataset should not be sharded if split is going to be called. Instead, create a
               DistributedSampler and specify a split to shard after splitting. If dataset is
               sharded after a split, it is strongly recommended to set the same seed in each instance
               of execution, otherwise each shard may not be part of the same split (see Examples).
            2. It is strongly recommended to not shuffle the dataset, but use randomize=True instead.
               Shuffling the dataset may not be deterministic, which means the data in each split
               will be different in each epoch. Furthermore, if sharding occurs after split, each
               shard may not be part of the same split.

        Raises:
            RuntimeError: If get_dataset_size returns None or is not supported for this dataset.
            RuntimeError: If sizes is list of integers and sum of all elements in sizes does not
                equal the dataset size.
            RuntimeError: If sizes is list of float and there is a split with size 0 after calculations.
            RuntimeError: If the dataset is sharded prior to calling split.
            ValueError: If sizes is list of float and not all floats are between 0 and 1, or if the
                floats don’t sum to 1.

        Returns
            tuple(Dataset), a tuple of datasets that have been split.

        Examples:
            >>> import mindspore.dataset as ds
            >>>
            >>> dataset_dir = "/path/to/imagefolder_directory"
            >>>
            >>> # many datasets have shuffle on by default, set shuffle to False if split will be called!
            >>> data = ds.ImageFolderDatasetV2(dataset_dir, shuffle=False)
            >>>
            >>> # sets the seed, and tells split to use this seed when randomizing. This
            >>> # is needed because we are sharding later
            >>> ds.config.set_seed(58)
            >>> train, test = data.split([0.9, 0.1])
            >>>
            >>> # if we want to shard the train dataset, we can use a DistributedSampler
            >>> train_sampler = ds.DistributedSampler(10, 2)
            >>> train.use_sampler(train_sampler)
        """
        if self.is_shuffled():
            logger.warning("dataset is shuffled before split.")

        if self.is_sharded():
            raise RuntimeError("dataset should not be sharded before split.")

        absolute_sizes = self._get_absolute_split_sizes(sizes)
        splits = []
        current_split_start_index = 0
        for size in absolute_sizes:
            ds = copy.deepcopy(self)
            if randomize:
                # want to shuffle the same way every epoch before split, we are assuming
                # that the user will call set_seed
                random_sampler = samplers.RandomSampler()
                random_sampler.reshuffle_each_epoch = False
                ds.add_sampler(random_sampler)

            subset_sampler = samplers.SubsetSampler(current_split_start_index, size)
            ds.add_sampler(subset_sampler)

            # add sequential sampler, so that if user calls use_sampler, we will
            # get rid of the sequential sampler instead of something we need
            ds.add_sampler(samplers.SequentialSampler())

            splits.append(ds)

            current_split_start_index += size

        return tuple(splits)


class DatasetOp(Dataset):
    """
    Abstract class to represent a operations on dataset.
    """

    # No need for __init__ since it is the same as the super's init


class BatchDataset(DatasetOp):
    """
    The result of applying Batch operator to the input dataset.

    Args:
        input_dataset (Dataset): Input Dataset to be batched.
        batch_size (int or function): The number of rows each batch is created with. An
            int or callable which takes exactly 1 parameter, BatchInfo.
        drop_remainder (bool, optional): Determines whether or not to drop the last
            possibly incomplete batch (default=False). If True, and if there are less
            than batch_size rows available to make the last batch, then those rows will
            be dropped and not propagated to the child node.
        num_parallel_workers (int, optional): Number of workers to process the Dataset in parallel (default=None).
        per_batch_map (callable, optional): Per batch map callable. A callable which takes
            (list[Tensor], list[Tensor], ..., BatchInfo) as input parameters. Each list[Tensor] represent a batch of
            Tensors on a given column. The number of lists should match with number of entries in input_columns. The
            last parameter of the callable should always be a BatchInfo object.
        input_columns (list of string, optional): List of names of the input columns. The size of the list should
            match with signature of per_batch_map callable.
        pad_info (dict, optional): Whether to perform padding on selected columns. pad_info={"col1":([224,224],0)}
            would pad column with name "col1" to a tensor of size [224,224] and fill the missing with 0.

    """

    def __init__(self, input_dataset, batch_size, drop_remainder=False, num_parallel_workers=None,
                 per_batch_map=None, input_columns=None, pad_info=None):
        super().__init__(num_parallel_workers)

        if BatchDataset._is_ancestor_of_repeat(input_dataset):
            logger.warning("Repeat is located before batch, data from two epochs can be batched together.")

        BatchDataset._update_batch_size_for_syncwait(input_dataset, batch_size)

        self.batch_size = batch_size
        self.drop_remainder = drop_remainder
        self.per_batch_map = per_batch_map
        self.input_columns = input_columns
        self.pad_info = pad_info
        self.input.append(input_dataset)
        input_dataset.output.append(self)
        self._input_indexs = input_dataset.input_indexs

    def get_args(self):
        args = super().get_args()
        args["batch_size"] = self.batch_size
        args["drop_remainder"] = self.drop_remainder
        args["per_batch_map"] = self.per_batch_map
        args["input_columns"] = self.input_columns
        args["pad_info"] = self.pad_info
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        child_size = self.input[0].get_dataset_size()
        if child_size is not None:
            if self.drop_remainder:
                return math.floor(child_size / self.batch_size)
            return math.ceil(child_size / self.batch_size)
        return None

    def get_batch_size(self):
        """
        Get the size of a batch.

        Return:
            Number, the number of data in a batch.
        """
        return self.batch_size

    @staticmethod
    def _is_ancestor_of_repeat(dataset):
        """
        Utility function to find the case where repeat is used before batch.

        Args:
             dataset (Dataset): dataset to be checked.
        Return:
            True or False.
        """
        if isinstance(dataset, RepeatDataset):
            return True
        flag = False
        for input_dataset in dataset.input:
            flag = flag | BatchDataset._is_ancestor_of_repeat(input_dataset)
        return flag

    @staticmethod
    def _update_batch_size_for_syncwait(dataset, batch_size):
        """
        Utility function to notify batch size to sync_wait.

        Args:
             dataset (Dataset): dataset to be checked.
             batchsize (int): batch size to notify.
        """
        if isinstance(dataset, SyncWaitDataset):
            dataset.update_sync_batch_size(batch_size)
        for input_dataset in dataset.input:
            BatchDataset._update_batch_size_for_syncwait(input_dataset, batch_size)


class BatchInfo(CBatchInfo):
    """
    The information object associates with the current batch of tensors.
    """

    def get_batch_num(self):
        """
        Return the batch number of the current batch.

        Return:
            Number, number of the current batch.
        """
        return

    def get_epoch_num(self):
        """
        Return the epoch number of the current batch.

        Return:
            Number, number of the current epoch.
        """
        return

class BlockReleasePair:
    """
    The blocking condition class used by SyncWaitDataset.

    Args:
        init_release_rows (int): Number of lines to allow through the pipeline.
        callback (function): The callback funciton that will be called when release is called.
    """
    def __init__(self, init_release_rows, callback=None):
        self.row_count = -init_release_rows
        self.cv = threading.Condition()
        self.callback = callback
        self.default_rows = init_release_rows

    def __deepcopy__(self, memodict):
        if id(self) in memodict:
            return memodict[id(self)]
        memodict[id(self)] = self
        # condition variable and callback are the same, but reset the counter
        self.reset()
        return self

    def reset(self):
        with self.cv:
            self.row_count = -self.default_rows
            self.cv.notify_all()

    def update_batched_size(self, batch_size):
        # should only use before the pipeline creates
        self.row_count *= batch_size
        self.default_rows *= batch_size

    def block_func(self):
        with self.cv:
            self.cv.wait_for(lambda: self.row_count < 0)
            self.row_count += 1
        return True

    def release_func(self, pass_rows=None, data=None):
        with self.cv:
            if pass_rows is None:
                pass_rows = self.default_rows
            self.row_count -= pass_rows
            if self.callback is not None:
                self.callback(data)
            self.cv.notify_all()

class SyncWaitDataset(DatasetOp):
    """
    The result of adding a blocking condition to the input Dataset.

    Args:
        input_dataset (Dataset): Input dataset to apply flow control.
        num_batch (int): the number of batches without blocking at the start of each epoch.
        condition_name (str): The condition name that is used to toggle sending next row.
        callback (function): The callback funciton that will be invoked when sync_update is called.

    Raises:
        RuntimeError: If condition name already exists.
    """

    def __init__(self, input_dataset, condition_name, num_batch, callback=None):
        super().__init__()
        self.input.append(input_dataset)
        input_dataset.output.append(self)
        # set to the default value, waiting for the batch to update it
        self._condition_name = condition_name
        self._pair = BlockReleasePair(num_batch, callback)
        if self._condition_name in self.input[0].get_sync_notifiers():
            raise RuntimeError("Condition name is already in use")
        logger.warning("Please remember to add dataset.sync_update(condition=%s), otherwise will result in hanging",
                       condition_name)

    def get_sync_notifiers(self):
        return {**self.input[0].get_sync_notifiers(), **{self._condition_name: self._pair.release_func}}

    def is_sync(self):
        return True

    def get_args(self):
        args = super().get_args()
        args["condition_name"] = self._condition_name
        args["condition_func"] = self._pair.block_func
        return args

    def update_sync_batch_size(self, batch_size):
        self._pair.update_batched_size(batch_size)

    @staticmethod
    def _is_ancestor_of_batch(dataset):
        """
        Utility function to find the case where sync_wait is used before batch.

        Args:
             dataset (Dataset): dataset to be checked.
        Return:
            True or False.
        """
        if isinstance(dataset, BatchDataset):
            return True
        flag = False
        for input_dataset in dataset.input:
            flag = flag | SyncWaitDataset._is_ancestor_of_batch(input_dataset)
        return flag


class ShuffleDataset(DatasetOp):
    """
    The result of applying Shuffle operator to the input Dataset.

    Args:
        input_dataset (Dataset): Input Dataset to be shuffled.
        buffer_size (int): The size of the buffer.

    Raises:
        RuntimeError: If exist sync operators before shuffle.
    """

    def __init__(self, input_dataset, buffer_size):
        super().__init__()
        self.buffer_size = buffer_size
        self.input.append(input_dataset)
        self.reshuffle_each_epoch = None
        input_dataset.output.append(self)
        self._input_indexs = input_dataset.input_indexs
        if self.is_sync():
            raise RuntimeError("No shuffle after sync operators")

    def get_args(self):
        args = super().get_args()
        args["buffer_size"] = self.buffer_size
        if self.reshuffle_each_epoch is not None:
            args["reshuffle_each_epoch"] = self.reshuffle_each_epoch

        return args

    def is_shuffled(self):
        return True


# Pyfunc collection for multiprocess pyfunc
# This global variable will only be used within subprocesses
_GLOBAL_PYFUNC_LIST = []


# Pyfunc worker init function
# Python multiprocessing library forbid sending lambda function through pipe.
# This init function allow us to add all python function to a global collection and then fork afterwards.
def _pyfunc_worker_init(pyfunc_list):
    global _GLOBAL_PYFUNC_LIST
    _GLOBAL_PYFUNC_LIST = pyfunc_list


# Pyfunc worker execution function
# All exceptions will be raised to main processes
def _pyfunc_worker_exec(index, *args):
    try:
        return _GLOBAL_PYFUNC_LIST[index](*args)
    except KeyboardInterrupt:
        raise Exception("Multiprocess MapOp worker receives KeyboardInterrupt")


# PythonCallable wrapper for multiprocess pyfunc
class _PythonCallable:
    """
    Internal python function wrapper for multiprocessing pyfunc.
    """
    def __init__(self, py_callable, idx, pool=None):
        # Original python callable from user.
        self.py_callable = py_callable
        # Process pool created for current iterator.
        self.pool = pool
        # Python callable index for subprocess _GLOBAL_PYFUNC_LIST
        self.idx = idx

    def __call__(self, *args):
        if self.pool is not None:
            try:
                # This call will send the tensors along with Python callable index to the process pool.
                # Block, yield GIL. Current thread will reacquire GIL once result is returned.
                return self.pool.apply(_pyfunc_worker_exec, [self.idx, *args])
            except KeyboardInterrupt:
                self.pool.terminate()
                self.pool.join()
                raise Exception("Multiprocess MapOp worker receives KeyboardInterrupt")
        # Invoke original python callable in master process in case the pool is gone.
        return self.py_callable(*args)


class MapDataset(DatasetOp):
    """
    The result of applying Map operator to the input Dataset.

    Args:
        input_dataset (Dataset): Input Dataset to be mapped.
        input_columns (list[str]): List of names of the input columns
            (default=None, the operations will be applied on the first columns in the dataset).
            The size of the list should match the number of inputs of the first operator.
        operations (TensorOp): A function mapping a nested structure of tensors
            to another nested structure of tensor (default=None).
        output_columns (list[str], optional): list of names of the output columns.
            The size of the list should match the number of outputs of the last operator
            (default=None, output columns will be the input columns, i.e., the columns will
            be replaced).
        columns_order (list[str], optional): list of all the desired columns of the dataset (default=None).
            The argument is mandatory if len(input_columns) != len(output_columns).
        num_parallel_workers (int, optional): Number of workers to process the Dataset
            in parallel (default=None).
        python_multiprocessing (bool, optional): Parallelize python operations with multiple worker process. This
            option could be beneficial if the python operation is computational heavy (default=False).

        Raises:
            ValueError: If len(input_columns) != len(output_columns) and columns_order is not specified.
    """

    def __init__(self, input_dataset, input_columns=None, operations=None, output_columns=None, columns_order=None,
                 num_parallel_workers=None, python_multiprocessing=False):
        super().__init__(num_parallel_workers)
        self.input.append(input_dataset)
        if input_columns is not None and not isinstance(input_columns, list):
            input_columns = [input_columns]
        self.input_columns = input_columns
        if operations is not None and not isinstance(operations, list):
            operations = [operations]
        self.operations = operations
        if output_columns is not None and not isinstance(output_columns, list):
            output_columns = [output_columns]
        self.output_columns = output_columns
        self.columns_order = columns_order

        if self.input_columns and self.output_columns \
                and len(self.input_columns) != len(self.output_columns) \
                and self.columns_order is None:
            raise ValueError("When (len(input_columns) != len(output_columns)), columns_order must be specified.")

        input_dataset.output.append(self)
        self._input_indexs = input_dataset.input_indexs
        self.python_multiprocessing = python_multiprocessing
        self.process_pool = None

    def get_args(self):
        args = super().get_args()
        args["input_columns"] = self.input_columns
        args["operations"] = self.operations
        args["output_columns"] = self.output_columns
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        return self.input[0].get_dataset_size()

    def __deepcopy__(self, memodict):
        if id(self) in memodict:
            return memodict[id(self)]
        cls = self.__class__
        new_op = cls.__new__(cls)
        memodict[id(self)] = new_op
        new_op.input = copy.deepcopy(self.input, memodict)
        new_op.input_columns = copy.deepcopy(self.input_columns, memodict)
        new_op.output_columns = copy.deepcopy(self.output_columns, memodict)
        new_op.columns_order = copy.deepcopy(self.columns_order, memodict)
        new_op.num_parallel_workers = copy.deepcopy(self.num_parallel_workers, memodict)
        new_op.output = copy.deepcopy(self.output, memodict)
        new_op.input_indexs = copy.deepcopy(self._input_indexs, memodict)
        new_op.python_multiprocessing = copy.deepcopy(self.python_multiprocessing, memodict)
        new_op.operations = self.operations
        return new_op

    # Iterator bootstrap will be called on iterator construction.
    # A deep copy of Dataset object is created prior of iterator_bootstrap.
    # This method will create per iterator process pool and bind pyfunc execution to the pool.
    def iterator_bootstrap(self):
        """
        Per iterator bootstrap callback.
        """
        if self.python_multiprocessing:
            iter_specific_operations = []
            callable_list = []

            # Pass #1, look for python callables and build list
            for op in self.operations:
                if callable(op):
                    callable_list.append(op)

            if callable_list:
                # Construct pool with the callable list
                # The callable list and _pyfunc_worker_init are used to pass lambda function in to subprocesses
                self.process_pool = multiprocessing.Pool(processes=self.num_parallel_workers,
                                                         initializer=_pyfunc_worker_init,
                                                         initargs=(callable_list,))
                # Pass #2
                idx = 0
                for op in self.operations:
                    if callable(op):
                        # Wrap python callable into _PythonCallable
                        iter_specific_operations.append(_PythonCallable(op, idx, self.process_pool))
                        idx += 1
                    else:
                        # CPP ops remain the same
                        iter_specific_operations.append(op)
                self.operations = iter_specific_operations

    def __del__(self):
        if hasattr(self, 'process_pool') and self.process_pool is not None:
            self.process_pool.terminate()


class FilterDataset(DatasetOp):
    """
    The result of applying filter predicate to the input Dataset.

    Args:
        input_dataset: Input Dataset to be mapped.
        predicate: python callable which returns a boolean value, if False then filter the element.
        input_columns: (list[str]): List of names of the input columns, when
        default=None, the predicate will be applied all columns in the dataset.
        num_parallel_workers (int, optional): Number of workers to process the Dataset
            in parallel (default=None).
    """

    def __init__(self, input_dataset, predicate, input_columns=None, num_parallel_workers=None):
        super().__init__(num_parallel_workers)
        self.predicate = lambda *args: bool(predicate(*args))
        self.input.append(input_dataset)
        input_dataset.output.append(self)
        if input_columns is not None and not isinstance(input_columns, list):
            input_columns = [input_columns]
        self.input_columns = input_columns

    def get_args(self):
        args = super().get_args()
        args["predicate"] = self.predicate
        args["input_columns"] = self.input_columns
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.
        the size cannot be determined before we run the pipeline.
        Return:
            0
        """
        return 0


class RepeatDataset(DatasetOp):
    """
    The result of applying Repeat operator to the input Dataset.

    Args:
        input_dataset (Dataset): Input Dataset to be repeated.
        count (int): Number of times the dataset should be repeated.
    """

    def __init__(self, input_dataset, count):
        super().__init__()
        if count is None:
            self.count = -1
        else:
            self.count = count
        self.input.append(input_dataset)
        input_dataset.output.append(self)
        self._input_indexs = input_dataset.input_indexs

    def get_args(self):
        args = super().get_args()
        args["count"] = self.count
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        child_size = self.input[0].get_dataset_size()
        if child_size is not None:
            return child_size
        return None

    def get_repeat_count(self):
        """
        Get the replication times in RepeatDataset.

        Return:
            Number, the count of repeat.
        """
        return self.count


class SkipDataset(DatasetOp):
    """
    The result of applying Skip operator to the input Dataset.

    Args:
        datasets (tuple): A tuple of datasets to be skipped.
        count (int): Number of rows the dataset should be skipped.
    """

    def __init__(self, input_dataset, count):
        super().__init__()
        self.count = count
        self.input.append(input_dataset)
        input_dataset.output.append(self)
        self._input_indexs = input_dataset.input_indexs

    def get_args(self):
        args = super().get_args()
        args["count"] = self.count
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        child_size = self.input[0].get_dataset_size()
        output_size = 0
        if self.count >= 0 and self.count < child_size:
            output_size = child_size - self.count
        return output_size


class TakeDataset(DatasetOp):
    """
    The result of applying Take operator to the input Dataset.

    Args:
        input_dataset (Dataset): Input Dataset to be taken element from.
        count (int): Number of elements to be taken from the dataset.
    """

    def __init__(self, input_dataset, count):
        super().__init__()
        self.count = count
        self.input.append(input_dataset)
        input_dataset.output.append(self)
        self._input_indexs = input_dataset.input_indexs

    def get_args(self):
        args = super().get_args()
        args["count"] = self.count
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        child_size = self.input[0].get_dataset_size()
        if child_size < self.count:
            return child_size
        return self.count


class ZipDataset(DatasetOp):
    """
    The result of applying Zip operator to the input Dataset.

    Args:
        datasets (tuple): A tuple of datasets to be zipped together.

    Raises:
        TypeError: If dataset is not an instance of Dataset.
    """

    def __init__(self, datasets):
        super().__init__()
        for dataset in datasets:
            if not isinstance(dataset, Dataset):
                raise TypeError("The parameter %s of zip has type error!" % (dataset))
        self.datasets = datasets
        for data in datasets:
            self.input.append(data)
            data.output.append(self)

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        children_sizes = [c.get_dataset_size() for c in self.input]
        if all(c is not None for c in children_sizes):
            return min(children_sizes)
        return None

    def num_classes(self):
        """
        Get the number of classes in a dataset.

        Return:
            Number, number of classes.
        """
        return None

    def is_sync(self):
        return any([c.is_sync() for c in self.input])

    def get_args(self):
        args = super().get_args()
        return args


class ConcatDataset(DatasetOp):
    """
    The result of applying concat dataset operator to the input Dataset.

    Args:
        datasets (list): A list of datasets to be concatenated together.

    Raises:
        TypeError: If dataset is not an instance of Dataset.
    """

    def __init__(self, datasets):
        super().__init__()
        for dataset in datasets:
            if not isinstance(dataset, Dataset):
                raise TypeError("The parameter %s of concat has type error!" % (dataset))
        self.datasets = datasets
        for data in datasets:
            self.input.append(data)
            data.output.append(self)

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        children_sizes = [c.get_dataset_size() for c in self.input]
        dataset_size = np.sum(children_sizes)
        return dataset_size


class RenameDataset(DatasetOp):
    """
    The result of applying Rename operator to the input Dataset.

    Args:
        input_dataset (Dataset): Input Dataset to be Renamed.
        input_column_names (list[str]): list of names of the input columns.
        output_column_names (list[str]): list of names of the output columns.
    """

    def __init__(self, input_dataset, input_columns, output_columns):
        super().__init__()
        if not isinstance(input_columns, list):
            input_columns = [input_columns]
        if not isinstance(output_columns, list):
            output_columns = [output_columns]
        self.input_column_names = input_columns
        self.output_column_names = output_columns
        self.input.append(input_dataset)
        input_dataset.output.append(self)
        self._input_indexs = input_dataset.input_indexs

    def get_args(self):
        args = super().get_args()
        args["input_columns"] = self.input_column_names
        args["output_columns"] = self.output_column_names
        return args


class ProjectDataset(DatasetOp):
    """
    The result of applying Project operator to the input Dataset.

    Args:
        input_dataset (Dataset): Input Dataset to be Project.
        columns (list[str]): List of names of the columns to project.
        prefetch_size (int, optional): Prefetch number of records ahead of the
            user's request (default=None).
    """

    def __init__(self, input_dataset, columns, prefetch_size=None):
        super().__init__()
        if not isinstance(columns, list):
            columns = [columns]
        self.columns = columns
        self.input.append(input_dataset)
        self.prefetch_size = prefetch_size

        input_dataset.output.append(self)
        self._input_indexs = input_dataset.input_indexs

    def get_args(self):
        args = super().get_args()
        args["columns"] = self.columns
        args["prefetch_size"] = self.prefetch_size
        return args


class TransferDataset(DatasetOp):
    """
    The result of applying TDT operator to the input Dataset.

    Args:
        input_dataset (Dataset): Input Dataset to be transferred.
        queue_name (str): Name of device queue.
        device_id (int): Id of device.
        device_type (str): Type of device, including "CPU", "GPU", and "Ascend".
        num_batch (int): limit the number of batch to be sent to device (default=None).
    """

    def __init__(self, input_dataset, queue_name, device_id, device_type, num_batch=None):
        super().__init__()
        self.input.append(input_dataset)
        input_dataset.output.append(self)
        self.queue_name = queue_name
        self._input_indexs = input_dataset.input_indexs
        self._device_type = device_type
        self._device_id = device_id
        self.__num_batch = num_batch
        self.iterator = None

    def get_args(self):
        args = super().get_args()
        args["queue_name"] = self.queue_name
        args["device_type"] = self._device_type
        args["device_id"] = self._device_id
        args["num_batch"] = self.__num_batch
        return args

    def create_dict_iterator(self):
        raise RuntimeError("TransferDataset is not iterable")

    def create_tuple_iterator(self, columns=None):
        raise RuntimeError("TransferDataset is not iterable")

    def __iter__(self):
        raise RuntimeError("TransferDataset is not iterable")

    def output_shapes(self):
        raise RuntimeError("TransferDataset does not support output_shapes")

    def output_types(self):
        raise RuntimeError("TransferDataset does not support output_types")

    def send(self):
        # need to keep iterator alive so the executionTree is not destroyed
        self.iterator = TupleIterator(self)


class RangeDataset(MappableDataset):
    """
    A source dataset that reads and parses datasets stored on disk in a range.

    Args:
        start (int): starting index.
        stop (int): ending index.
        step (int): step size in a range.
    """

    def __init__(self, start, stop, step):
        super().__init__()
        self.start = start
        self.stop = stop
        self.step = step

    def get_args(self):
        args = super().get_args()
        args["start"] = self.start
        args["stop"] = self.stop
        args["step"] = self.step
        return args

    def is_shuffled(self):
        return False

    def is_sharded(self):
        return False


def _select_sampler(num_samples, input_sampler, shuffle, num_shards, shard_id):
    """
    Create sampler based on user input.

    Args:
        num_samples (int): Number of samples.
        input_sampler (Iterable / Sampler): Sampler from user.
        shuffle (bool): Shuffle.
        num_shards (int): Number of shard for sharding.
        shard_id (int): Shard ID.
    """
    if shuffle is None:
        if input_sampler is not None:
            # If shuffle is not specified, user provided sampler, use user's sampler
            return input_sampler
        if num_shards is not None:
            # If shuffle is not specified, sharding enabled, use distributed random sampler
            shuffle = True
            return samplers.DistributedSampler(num_shards, shard_id, shuffle=shuffle)
        # If shuffle is not specified, sharding disabled, use random sampler
        if num_samples is not None:
            return samplers.RandomSampler(replacement=True, num_samples=num_samples)
        return samplers.RandomSampler()
    if shuffle is True:
        if num_shards is not None:
            # If shuffle enabled, sharding enabled, use distributed random sampler
            return samplers.DistributedSampler(num_shards, shard_id, shuffle=shuffle)
        # If shuffle enabled, sharding disabled, use random sampler
        if num_samples is not None:
            return samplers.RandomSampler(replacement=True, num_samples=num_samples)
        return samplers.RandomSampler()
    if num_shards is not None:
        # If shuffle disabled, sharding enabled, use distributed sequential sampler
        return samplers.DistributedSampler(num_shards, shard_id, shuffle=shuffle)
    # If shuffle disabled, sharding disabled, use sequential sampler
    return samplers.SequentialSampler()


class ImageFolderDatasetV2(MappableDataset):
    """
    A source dataset that reads images from a tree of directories.

    All images within one folder have the same label.
    The generated dataset has two columns ['image', 'label'].
    The shape of the image column is [image_size] if decode flag is False, or [H,W,C]
    otherwise.
    The type of the image tensor is uint8. The label is just a scalar uint64
    tensor.
    This dataset can take in a sampler. sampler and shuffle are mutually exclusive. Table
    below shows what input args are allowed and their expected behavior.

    .. list-table:: Expected Order Behavior of Using 'sampler' and 'shuffle'
       :widths: 25 25 50
       :header-rows: 1

       * - Parameter 'sampler'
         - Parameter 'shuffle'
         - Expected Order Behavior
       * - None
         - None
         - random order
       * - None
         - True
         - random order
       * - None
         - False
         - sequential order
       * - Sampler object
         - None
         - order defined by sampler
       * - Sampler object
         - True
         - not allowed
       * - Sampler object
         - False
         - not allowed

    Args:
        dataset_dir (str): Path to the root directory that contains the dataset.
        num_samples (int, optional): The number of images to be included in the dataset
            (default=None, all images).
        num_parallel_workers (int, optional): Number of workers to read the data
            (default=None, set in the config).
        shuffle (bool, optional): Whether or not to perform shuffle on the dataset
            (default=None, expected order behavior shown in the table).
        sampler (Sampler, optional): Object used to choose samples from the
            dataset (default=None, expected order behavior shown in the table).
        extensions (list[str], optional): List of file extensions to be
            included in the dataset (default=None).
        class_indexing (dict, optional): A str-to-int mapping from folder name to index
            (default=None, the folder names will be sorted
            alphabetically and each class will be given a
            unique index starting from 0).
        decode (bool, optional): decode the images after reading (default=False).
        num_shards (int, optional): Number of shards that the dataset should be divided
            into (default=None).
        shard_id (int, optional): The shard ID within num_shards (default=None). This
            argument should be specified only when num_shards is also specified.

    Raises:
        RuntimeError: If sampler and shuffle are specified at the same time.
        RuntimeError: If sampler and sharding are specified at the same time.
        RuntimeError: If num_shards is specified but shard_id is None.
        RuntimeError: If shard_id is specified but num_shards is None.
        RuntimeError: If class_indexing is not a dictionary.
        ValueError: If shard_id is invalid (< 0 or >= num_shards).

    Examples:
        >>> import mindspore.dataset as ds
        >>> # path to imagefolder directory. This directory needs to contain sub-directories which contain the images
        >>> dataset_dir = "/path/to/imagefolder_directory"
        >>> # 1) read all samples (image files) in dataset_dir with 8 threads
        >>> imagefolder_dataset = ds.ImageFolderDatasetV2(dataset_dir, num_parallel_workers=8)
        >>> # 2) read all samples (image files) from folder cat and folder dog with label 0 and 1
        >>> imagefolder_dataset = ds.ImageFolderDatasetV2(dataset_dir,class_indexing={"cat":0,"dog":1})
        >>> # 3) read all samples (image files) in dataset_dir with extensions .JPEG and .png (case sensitive)
        >>> imagefolder_dataset = ds.ImageFolderDatasetV2(dataset_dir, extensions={".JPEG",".png"})
    """

    @check_imagefolderdatasetv2
    def __init__(self, dataset_dir, num_samples=None, num_parallel_workers=None,
                 shuffle=None, sampler=None, extensions=None, class_indexing=None,
                 decode=False, num_shards=None, shard_id=None):
        super().__init__(num_parallel_workers)

        self.dataset_dir = dataset_dir
        self.sampler = _select_sampler(num_samples, sampler, shuffle, num_shards, shard_id)
        self.num_samples = num_samples
        self.shuffle_level = shuffle
        self.extensions = extensions
        self.class_indexing = class_indexing
        self.decode = decode
        self.num_shards = num_shards
        self.shard_id = shard_id
        self.cur_dataset_size = None

    def get_args(self):
        args = super().get_args()
        args["dataset_dir"] = self.dataset_dir
        args["num_samples"] = self.num_samples
        args["sampler"] = self.sampler
        args["shuffle"] = self.shuffle_level
        args["extensions"] = self.extensions
        args["class_indexing"] = self.class_indexing
        args["decode"] = self.decode
        args["num_shards"] = self.num_shards
        args["shard_id"] = self.shard_id
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        if self.cur_dataset_size is not None:
            return self.cur_dataset_size

        if self.num_samples is None:
            num_samples = 0
        else:
            num_samples = self.num_samples
        num_rows = ImageFolderOp.get_num_rows_and_classes(self.dataset_dir, num_samples)[0]
        rows_per_shard = get_num_rows(num_rows, self.num_shards)
        rows_from_sampler = self._get_sampler_dataset_size()

        if rows_from_sampler is None:
            self.cur_dataset_size = rows_per_shard
            return rows_per_shard

        self.cur_dataset_size = min(rows_from_sampler, rows_per_shard)
        return self.cur_dataset_size

    def num_classes(self):
        """
        Get the number of classes in dataset.

        Return:
            Number, number of classes.
        """
        if self.num_samples is None:
            num_samples = 0
        else:
            num_samples = self.num_samples
        return ImageFolderOp.get_num_rows_and_classes(self.dataset_dir, num_samples)[1]

    def is_shuffled(self):
        if self.shuffle_level is None:
            return True

        return self.shuffle_level or self.sampler.is_shuffled()

    def is_sharded(self):
        if self.num_shards is not None:
            return self.num_shards > 1

        return self.sampler.is_sharded()


class MnistDataset(MappableDataset):
    """
    A source dataset for reading and parsing the Mnist dataset.

    The generated dataset has two columns ['image', 'label'].
    The type of the image tensor is uint8. The label is just a scalar uint32 tensor.
    This dataset can take in a sampler. sampler and shuffle are mutually exclusive. Table
    below shows what input args are allowed and their expected behavior.

    .. list-table:: Expected Order Behavior of Using 'sampler' and 'shuffle'
       :widths: 25 25 50
       :header-rows: 1

       * - Parameter 'sampler'
         - Parameter 'shuffle'
         - Expected Order Behavior
       * - None
         - None
         - random order
       * - None
         - True
         - random order
       * - None
         - False
         - sequential order
       * - Sampler object
         - None
         - order defined by sampler
       * - Sampler object
         - True
         - not allowed
       * - Sampler object
         - False
         - not allowed

    Args:
        dataset_dir (str): Path to the root directory that contains the dataset.
        num_samples (int, optional): The number of images to be included in the dataset
            (default=None, all images).
        num_parallel_workers (int, optional): Number of workers to read the data
            (default=value, set in the config).
        shuffle (bool, optional): Whether or not to perform shuffle on the dataset
            (default=None, expected order behavior shown in the table).
        sampler (Sampler, optional): Object used to choose samples from the
            dataset (default=None, expected order behavior shown in the table).
        num_shards (int, optional): Number of shards that the dataset should be divided
            into (default=None).
        shard_id (int, optional): The shard ID within num_shards (default=None). This
            argument should be specified only when num_shards is also specified.

    Raises:
        RuntimeError: If sampler and shuffle are specified at the same time.
        RuntimeError: If sampler and sharding are specified at the same time.
        RuntimeError: If num_shards is specified but shard_id is None.
        RuntimeError: If shard_id is specified but num_shards is None.
        ValueError: If shard_id is invalid (< 0 or >= num_shards).

    Examples:
        >>> import mindspore.dataset as ds
        >>> dataset_dir = "/path/to/mnist_folder"
        >>> # 1) read 3 samples from mnist_dataset
        >>> mnist_dataset = ds.MnistDataset(dataset_dir=dataset_dir, num_samples=3)
        >>> # in mnist_dataset dataset, each dictionary has keys "image" and "label"
    """

    @check_mnist_cifar_dataset
    def __init__(self, dataset_dir, num_samples=None, num_parallel_workers=None,
                 shuffle=None, sampler=None, num_shards=None, shard_id=None):
        super().__init__(num_parallel_workers)

        self.dataset_dir = dataset_dir
        self.sampler = _select_sampler(num_samples, sampler, shuffle, num_shards, shard_id)
        self.num_samples = num_samples
        self.shuffle_level = shuffle
        self.num_shards = num_shards
        self.shard_id = shard_id

    def get_args(self):
        args = super().get_args()
        args["dataset_dir"] = self.dataset_dir
        args["num_samples"] = self.num_samples
        args["shuffle"] = self.shuffle_level
        args["sampler"] = self.sampler
        args["num_shards"] = self.num_shards
        args["shard_id"] = self.shard_id
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        if self.num_samples is None:
            num_samples = 0
        else:
            num_samples = self.num_samples

        num_rows = MnistOp.get_num_rows(self.dataset_dir, num_samples)
        rows_per_shard = get_num_rows(num_rows, self.num_shards)
        rows_from_sampler = self._get_sampler_dataset_size()

        if rows_from_sampler is None:
            return rows_per_shard

        return min(rows_from_sampler, rows_per_shard)

    def is_shuffled(self):
        if self.shuffle_level is None:
            return True

        return self.shuffle_level or self.sampler.is_shuffled()

    def is_sharded(self):
        if self.num_shards is not None:
            return self.num_shards > 1

        return self.sampler.is_sharded()


class MindDataset(SourceDataset):
    """
    A source dataset that reads from shard files and database.

    Args:
        dataset_file (str, list[str]): One of file names or file list in dataset.
        columns_list (list[str], optional): List of columns to be read (default=None).
        num_parallel_workers (int, optional): The number of readers (default=None).
        shuffle (bool, optional): Whether or not to perform shuffle on the dataset
            (default=None, performs shuffle).
        num_shards (int, optional): Number of shards that the dataset should be divided into (default=None).
        shard_id (int, optional): The shard ID within num_shards (default=None). This
            argument should be specified only when num_shards is also specified.
        block_reader (bool, optional): Whether read data by block mode (default=False).
        sampler (Sampler, optional): Object used to choose samples from the
            dataset (default=None, sampler is exclusive
            with shuffle and block_reader). Support list: SubsetRandomSampler,
            PkSampler.
        padded_sample (dict, optional): Samples will be appended to dataset, which
            keys are the same as column_list.
        num_padded (int, optional): Number of padding samples.Dataset size
            plus num_padded should be divisible by num_shards.

    Raises:
        ValueError: If num_shards is specified but shard_id is None.
        ValueError: If shard_id is specified but num_shards is None.
        ValueError: If block reader is true but partition is specified.
    """

    @check_minddataset
    def __init__(self, dataset_file, columns_list=None, num_parallel_workers=None,
                 shuffle=None, num_shards=None, shard_id=None,
                 block_reader=False, sampler=None, padded_sample=None,
                 num_padded=None):
        super().__init__(num_parallel_workers)
        if isinstance(dataset_file, list):
            self.load_dataset = False
        else:
            self.load_dataset = True
        self.dataset_file = dataset_file
        self.columns_list = columns_list
        self.shuffle_option = shuffle
        self.distribution = ""
        self.sampler = sampler
        self.cur_dataset_size = None

        if num_shards is None or shard_id is None:
            self.partitions = None
        else:
            self.partitions = [num_shards, shard_id]

        if block_reader is True and self.partitions is not None:
            raise ValueError("block reader not allowed true when use partitions")

        if block_reader is True and shuffle is True:
            raise ValueError("block reader not allowed true when use shuffle")

        if block_reader is True:
            logger.warning("WARN: global shuffle is not used.")

        if sampler is not None:
            if isinstance(sampler, samplers.SubsetRandomSampler) is False and \
            isinstance(sampler, samplers.PKSampler) is False:
                raise ValueError("the sampler is not supported yet.")

        # sampler exclusive
        if block_reader is True and sampler is not None:
            raise ValueError("block reader not allowed true when use sampler")

        if shuffle is not None and sampler is not None:
            raise ValueError("shuffle not allowed when use sampler")

        if block_reader is False and sampler is None:
            self.shuffle_option = not bool(shuffle is False)

        if num_padded is None:
            num_padded = 0

        self.num_shards = num_shards
        self.shard_id = shard_id
        self.block_reader = block_reader
        self.padded_sample = padded_sample
        self.num_padded = num_padded

    def get_args(self):
        args = super().get_args()
        padded_sample = {}
        if self.padded_sample:
            for k, v in self.padded_sample.items():
                if isinstance(v, np.ndarray):
                    padded_sample[k] = v.tobytes()
                else:
                    padded_sample[k] = v
        args["dataset_file"] = self.dataset_file
        args["load_dataset"] = self.load_dataset
        args["columns_list"] = self.columns_list
        args["shuffle_option"] = self.shuffle_option
        args["partitions"] = self.partitions
        args["block_reader"] = self.block_reader
        args["num_shards"] = self.num_shards
        args["shard_id"] = self.shard_id
        args["num_padded"] = self.num_padded
        args["padded_sample"] = padded_sample
        args["sampler"] = self.sampler
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        if self._dataset_size is None:
            if self.cur_dataset_size is not None:
                return self.cur_dataset_size

            if self.load_dataset:
                dataset_file = [self.dataset_file]
            else:
                dataset_file = self.dataset_file
            num_rows = MindRecordOp.get_num_rows(dataset_file, self.load_dataset, self.sampler, self.num_padded)
            if self.partitions is not None and self.partitions[0] > 0:
                if num_rows % self.partitions[0] == 0:
                    num_rows = num_rows // self.partitions[0]
                else:
                    if self.num_padded > 0:
                        raise RuntimeError(
                            "Dataset size plus number of padded samples is not divisible by number of shards.")
                    num_rows = num_rows // self.partitions[0] + 1
            self.cur_dataset_size = num_rows
            return num_rows
        return self._dataset_size

    # manually set dataset_size as a tempoary solution.
    def set_dataset_size(self, value):
        logger.warning("WARN_DEPRECATED: This method is deprecated. Please use get_dataset_size directly.")
        if value >= 0:
            self._dataset_size = value
        else:
            raise ValueError('set dataset_size with negative value {}'.format(value))

    def is_shuffled(self):
        if self.shuffle_option is None:
            return True

        return self.shuffle_option or self.sampler.is_shuffled()

    def is_sharded(self):
        if self.num_shards is not None:
            return self.num_shards > 1

        return self.sampler.is_sharded()


def _iter_fn(dataset, num_samples):
    """
    Generator function wrapper for iterable dataset.
    """
    if num_samples is not None:
        ds_iter = iter(dataset)
        for _ in range(num_samples):
            try:
                val = next(ds_iter)
            except StopIteration:
                return
            # convert output tensors to ndarrays
            yield tuple([np.array(x, copy=False) for x in val])
    else:
        for val in dataset:
            # convert output tensors to ndarrays
            yield tuple([np.array(x, copy=False) for x in val])


def _generator_fn(generator, num_samples):
    """
    Generator function wrapper for generator function dataset.
    """
    if num_samples is not None:
        gen_iter = generator()
        for _ in range(num_samples):
            try:
                val = next(gen_iter)
            except StopIteration:
                return
            yield val
    else:
        gen_iter = generator()
        for val in gen_iter:
            yield val


def _py_sampler_fn(sampler, num_samples, dataset):
    """
    Generator function wrapper for mappable dataset with python sampler.
    """
    if num_samples is not None:
        sampler_iter = iter(sampler)
        for _ in range(num_samples):
            try:
                idx = next(sampler_iter)
            except StopIteration:
                return
            val = dataset[idx]
            # convert output tensors to ndarrays
            yield tuple([np.array(x, copy=False) for x in val])
    else:
        for i in sampler:
            val = dataset[i]
            # convert output tensors to ndarrays
            yield tuple([np.array(x, copy=False) for x in val])


def _cpp_sampler_fn(sampler, dataset):
    """
    Generator function wrapper for mappable dataset with cpp sampler.
    """
    indices = sampler.get_indices()
    for i in indices:
        val = dataset[i]
        # convert output tensors to ndarrays
        yield tuple([np.array(x, copy=False) for x in val])


def _cpp_sampler_fn_mp(sampler, dataset, num_worker):
    """
    Multiprocessing generator function wrapper for mappable dataset with cpp sampler.
    """
    indices = sampler.get_indices()
    return _sampler_fn_mp(indices, dataset, num_worker)


def _py_sampler_fn_mp(sampler, num_samples, dataset, num_worker):
    """
    Multiprocessing generator function wrapper for mappable dataset with python sampler.
    """
    indices = _fetch_py_sampler_indices(sampler, num_samples)
    return _sampler_fn_mp(indices, dataset, num_worker)


def _fetch_py_sampler_indices(sampler, num_samples):
    """
    Indices fetcher for python sampler.
    """
    if num_samples is not None:
        sampler_iter = iter(sampler)
        ret = []
        for _ in range(num_samples):
            try:
                val = next(sampler_iter)
                ret.append(val)
            except StopIteration:
                break
        return ret
    return [i for i in sampler]


def _fill_worker_indices(workers, indices, idx):
    """
    Worker index queue filler, fill worker index queue in round robin order.
    """
    num_worker = len(workers)
    while idx < len(indices):
        try:
            workers[idx % num_worker].put(indices[idx])
            idx += 1
        except queue.Full:
            break
    return idx


def _sampler_fn_mp(indices, dataset, num_worker):
    """
    Multiprocessing generator function wrapper master process.
    """
    workers = []
    # Event for end of epoch
    eoe = multiprocessing.Event()

    # Create workers
    for _ in range(num_worker):
        worker = _GeneratorWorker(dataset, eoe)
        worker.daemon = True
        workers.append(worker)

    # Fill initial index queues
    idx_cursor = 0
    idx_cursor = _fill_worker_indices(workers, indices, idx_cursor)

    # Start all workers
    for w in workers:
        w.start()

    # Fetch results
    for i in range(len(indices)):
        # Fetch result and put index
        try:
            result = workers[i % num_worker].get()
        except queue.Empty:
            raise Exception("Generator worker process timeout")
        except KeyboardInterrupt:
            for w in workers:
                w.terminate()
                w.join()
            raise Exception("Generator worker receives KeyboardInterrupt")
        if idx_cursor < len(indices):
            idx_cursor = _fill_worker_indices(workers, indices, idx_cursor)
        # Set eoe event once all indices are sent
        if idx_cursor == len(indices) and not eoe.is_set():
            eoe.set()
        yield tuple([np.array(x, copy=False) for x in result])


def _generator_worker_loop(dataset, idx_queue, result_queue, eoe):
    """
    Multiprocessing generator worker process loop.
    """
    while True:
        # Fetch index, block
        try:
            idx = idx_queue.get()
        except KeyboardInterrupt:
            raise Exception("Generator worker receives KeyboardInterrupt")
        if idx is None:
            # When the queue is out of scope from master process, a None item can be fetched from the queue.
            # Upon receiving None, worker process should check if EOE is set.
            assert eoe.is_set(), ""
            return
        # Fetch data, any exception from __getitem__ will terminate worker and timeout master process
        result = dataset[idx]
        # Send data, block
        try:
            result_queue.put(result)
        except KeyboardInterrupt:
            raise Exception("Generator worker receives KeyboardInterrupt")
        del result, idx


class _GeneratorWorker(multiprocessing.Process):
    """
    Worker process for multiprocess Generator.
    """
    def __init__(self, dataset, eoe):
        self.idx_queue = multiprocessing.Queue(16)
        self.res_queue = multiprocessing.Queue(16)
        super().__init__(target=_generator_worker_loop, args=(dataset, self.idx_queue, self.res_queue, eoe))

    def put(self, item):
        """
        Put function for worker index queue. Never block. Raise queue.Full on failure.
        """
        self.idx_queue.put_nowait(item)

    def get(self):
        """
        Get function for worker result queue. Block with timeout.
        """
        return self.res_queue.get(timeout=5)

    def __del__(self):
        self.terminate()


class GeneratorDataset(MappableDataset):
    """
    A source dataset that generate data from python by invoking python data source each epoch.

    This dataset can take in a sampler. sampler and shuffle are mutually exclusive. Table
    below shows what input args are allowed and their expected behavior.

    .. list-table:: Expected Order Behavior of Using 'sampler' and 'shuffle'
       :widths: 25 25 50
       :header-rows: 1

       * - Parameter 'sampler'
         - Parameter 'shuffle'
         - Expected Order Behavior
       * - None
         - None
         - random order
       * - None
         - True
         - random order
       * - None
         - False
         - sequential order
       * - Sampler object
         - None
         - order defined by sampler
       * - Sampler object
         - True
         - not allowed
       * - Sampler object
         - False
         - not allowed

    Args:
        source (Callable/Iterable/Random Accessible):
            A generator callable object, an iterable python object or a random accessible python object.
            Callable source is required to return a tuple of numpy array as a row of the dataset on source().next().
            Iterable source is required to return a tuple of numpy array as a row of the dataset on iter(source).next().
            Random accessible source is required to return a tuple of numpy array as a row of the dataset on
            source[idx].
        column_names (list[str], optional): List of column names of the dataset (default=None). Users are required to
            provide either column_names or schema.
        column_types (list[mindspore.dtype], optional): List of column data types of the dataset (default=None).
            If provided, sanity check will be performed on generator output.
        schema (Schema/String, optional): Path to the json schema file or schema object (default=None). Users are
            required to provide either column_names or schema. If both are provided, schema will be used.
        num_samples (int, optional): The number of samples to be included in the dataset
            (default=None, all images).
        num_parallel_workers (int, optional): Number of subprocesses used to fetch the dataset in parallel (default=1).
        shuffle (bool, optional): Whether or not to perform shuffle on the dataset. Random accessible input is required.
            (default=None, expected order behavior shown in the table).
        sampler (Sampler/Iterable, optional): Object used to choose samples from the dataset. Random accessible input is
            required (default=None, expected order behavior shown in the table).
        num_shards (int, optional): Number of shards that the dataset should be divided into (default=None).
            This argument should be specified only when 'num_samples' is "None". Random accessible input is required.
        shard_id (int, optional): The shard ID within num_shards (default=None). This argument should be specified only
            when num_shards is also specified. Random accessible input is required.

    Examples:
        >>> import mindspore.dataset as ds
        >>> # 1) Multidimensional generator function as callable input
        >>> def generator_md():
        >>>     for i in range(64):
        >>>         yield (np.array([[i, i + 1], [i + 2, i + 3]]),)
        >>> # create multi_dimension_generator_dataset with GeneratorMD and column name "multi_dimensional_data"
        >>> multi_dimension_generator_dataset = ds.GeneratorDataset(generator_md, ["multi_dimensional_data"])
        >>> # 2) Multi-column generator function as callable input
        >>> def generator_mc(maxid = 64):
        >>>     for i in range(maxid):
        >>>         yield (np.array([i]), np.array([[i, i + 1], [i + 2, i + 3]]))
        >>> # create multi_column_generator_dataset with GeneratorMC and column names "col1" and "col2"
        >>> multi_column_generator_dataset = ds.GeneratorDataset(generator_mc, ["col1", "col2"])
        >>> # 3) Iterable dataset as iterable input
        >>> class MyIterable():
        >>>     def __iter__(self):
        >>>         return # User implementation
        >>> # create iterable_generator_dataset with MyIterable object
        >>> iterable_generator_dataset = ds.GeneratorDataset(MyIterable(), ["col1"])
        >>> # 4) Random accessible dataset as Random accessible input
        >>> class MyRA():
        >>>     def __getitem__(self, index):
        >>>         return # User implementation
        >>> # create ra_generator_dataset with MyRA object
        >>> ra_generator_dataset = ds.GeneratorDataset(MyRA(), ["col1"])
        >>> # List/Dict/Tuple is also random accessible
        >>> list_generator = ds.GeneratorDataset([(np.array(0),), (np.array(1)), (np.array(2))], ["col1"])
        >>> # 5) Built-in Sampler
        >>> my_generator = ds.GeneratorDataset(my_ds, ["img", "label"], sampler=samplers.RandomSampler())
        >>>
    """

    @check_generatordataset
    def __init__(self, source, column_names=None, column_types=None, schema=None, num_samples=None,
                 num_parallel_workers=1, shuffle=None, sampler=None, num_shards=None, shard_id=None):
        super().__init__(num_parallel_workers)
        self.sampler = _select_sampler(num_samples, sampler, shuffle, num_shards, shard_id)
        if self.sampler is not None and hasattr(source, "__getitem__"):
            if isinstance(self.sampler, (samplers.SequentialSampler, samplers.DistributedSampler,
                                         samplers.RandomSampler, samplers.SubsetRandomSampler,
                                         samplers.WeightedRandomSampler, samplers.Sampler)):
                if num_samples is None:
                    num_samples = len(source)
                sampler_instance = self.sampler.create()
                sampler_instance.set_num_rows(len(source))
                sampler_instance.set_num_samples(num_samples)
                sampler_instance.initialize()
                if num_parallel_workers > 1:
                    self.source = (lambda: _cpp_sampler_fn_mp(sampler_instance, source, num_parallel_workers))
                else:
                    self.source = (lambda: _cpp_sampler_fn(sampler_instance, source))
            else:
                if num_parallel_workers > 1:
                    self.source = (lambda: _py_sampler_fn_mp(self.sampler, num_samples, source, num_parallel_workers))
                else:
                    self.source = (lambda: _py_sampler_fn(self.sampler, num_samples, source))
        else:
            try:
                iter(source)
            except TypeError:
                # Use generator function if input callable
                self.source = (lambda: _generator_fn(source, num_samples))
            else:
                # Use iterator function if input is iterable
                # Random accessible input is also iterable
                self.source = (lambda: _iter_fn(source, num_samples))

        if column_names is not None and not isinstance(column_names, list):
            column_names = [column_names]
        self.column_names = column_names

        if column_types is not None:
            self.column_types = mstypelist_to_detypelist(column_types)
        else:
            self.column_types = column_types

        if schema is not None:
            self.schema = schema
            if not isinstance(schema, Schema):
                self.schema = Schema(schema)
            self.column_names = []
            self.column_types = []
            for col in self.schema.columns:
                self.column_names.append(col["name"])
                self.column_types.append(DataType(col["type"]))

    def get_args(self):
        args = super().get_args()
        args["source"] = self.source
        args["column_names"] = self.column_names
        args["column_types"] = self.column_types
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        rows_from_sampler = self._get_sampler_dataset_size()

        if rows_from_sampler is None:
            return self._dataset_size
        if self._dataset_size is None:
            return None
        return min(rows_from_sampler, self._dataset_size)

    # manually set dataset_size as a temporary solution.
    def set_dataset_size(self, value):
        if value >= 0:
            self._dataset_size = value
        else:
            raise ValueError('set dataset_size with negative value {}'.format(value))

    def __deepcopy__(self, memodict):
        if id(self) in memodict:
            return memodict[id(self)]
        cls = self.__class__
        new_op = cls.__new__(cls)
        memodict[id(self)] = new_op
        new_op.input = copy.deepcopy(self.input, memodict)
        new_op.output = copy.deepcopy(self.output, memodict)
        new_op.num_parallel_workers = copy.deepcopy(self.num_parallel_workers, memodict)
        new_op.column_types = copy.deepcopy(self.column_types, memodict)
        new_op.column_names = copy.deepcopy(self.column_names, memodict)

        new_op.source = self.source
        new_op.sampler = self.sampler

        return new_op

    def is_shuffled(self):
        return self.sampler.is_shuffled()

    def is_sharded(self):
        return self.sampler.is_sharded()


class TFRecordDataset(SourceDataset):
    """
    A source dataset that reads and parses datasets stored on disk in TFData format.

    Args:
        dataset_files (str or list[str]): String or list of files to be read or glob strings to search for a pattern of
            files. The list will be sorted in a lexicographical order.
        schema (str or Schema, optional): Path to the json schema file or schema object (default=None).
            If the schema is not provided, the meta data from the TFData file is considered the schema.
        columns_list (list[str], optional): List of columns to be read (default=None, read all columns)
        num_samples (int, optional): number of samples(rows) to read (default=None).
            If num_samples is None and numRows(parsed from schema) is not exist, read the full dataset;
            If num_samples is None and numRows(parsed from schema) is greater than 0, read numRows rows;
            If both num_samples and numRows(parsed from schema) are greater than 0, read num_samples rows.
        num_parallel_workers (int, optional): number of workers to read the data
            (default=None, number set in the config).
        shuffle (bool, Shuffle level, optional): perform reshuffling of the data every epoch (default=Shuffle.GLOBAL).
            If shuffle is False, no shuffling will be performed;
            If shuffle is True, the behavior is the same as setting shuffle to be Shuffle.GLOBAL
            Otherwise, there are two levels of shuffling:

            - Shuffle.GLOBAL: Shuffle both the files and samples.

            - Shuffle.FILES: Shuffle files only.

        num_shards (int, optional): Number of shards that the dataset should be divided
            into (default=None).
        shard_id (int, optional): The shard ID within num_shards (default=None). This
            argument should be specified only when num_shards is also specified.
        shard_equal_rows (bool): Get equal rows for all shards(default=False). If shard_equal_rows is false, number
            of rows of each shard may be not equal.
    Examples:
        >>> import mindspore.dataset as ds
        >>> import mindspore.common.dtype as mstype
        >>> dataset_files = ["/path/to/1", "/path/to/2"] # contains 1 or multiple tf data files
        >>> # 1) get all rows from dataset_files with no explicit schema:
        >>> # The meta-data in the first row will be used as a schema.
        >>> tfdataset = ds.TFRecordDataset(dataset_files=dataset_files)
        >>> # 2) get all rows from dataset_files with user-defined schema:
        >>> schema = ds.Schema()
        >>> schema.add_column('col_1d', de_type=mindspore.int64, shape=[2])
        >>> tfdataset = ds.TFRecordDataset(dataset_files=dataset_files, schema=schema)
        >>> # 3) get all rows from dataset_files with schema file "./schema.json":
        >>> tfdataset = ds.TFRecordDataset(dataset_files=dataset_files, schema="./schema.json")
    """

    @check_tfrecorddataset
    def __init__(self, dataset_files, schema=None, columns_list=None, num_samples=None, num_parallel_workers=None,
                 shuffle=Shuffle.GLOBAL, num_shards=None, shard_id=None, shard_equal_rows=False):
        super().__init__(num_parallel_workers)
        self.dataset_files = self._find_files(dataset_files)
        self.dataset_files.sort()
        self.num_shards = num_shards
        self.shard_id = shard_id
        schema_obj = None
        if (schema is not None) and (not isinstance(schema, Schema)):
            schema_obj = Schema(schema)  # read the schema file and convert to schema object to validate it
        self.schema = schema
        self.columns_list = columns_list
        self.num_samples = num_samples
        if schema_obj is not None and num_samples is None:
            self.num_samples = schema_obj.num_rows

        if not isinstance(shuffle, (bool, Shuffle)):
            raise TypeError("shuffle should be of boolean or enum 'Shuffle'.")
        if not isinstance(shuffle, Shuffle):
            if shuffle:
                self.shuffle_level = Shuffle.GLOBAL
                self.shuffle_files = True
            else:
                self.shuffle_level = None
                self.shuffle_files = False
        else:
            self.shuffle_level = shuffle
            self.shuffle_files = True
        self.shard_equal_rows = shard_equal_rows

    def get_args(self):
        args = super().get_args()
        args["dataset_files"] = self.dataset_files
        if self.schema is not None:
            if isinstance(self.schema, Schema):
                self.schema.datasetType = 'TF'
                if self.num_samples is not None:
                    self.schema.num_rows = self.num_samples
                args["schema_json_string"] = self.schema.to_json()
            else:
                args["schema_file_path"] = self.schema
        args["schema"] = self.schema
        args["columns_list"] = self.columns_list
        args["num_samples"] = self.num_samples
        if self.shuffle_files is not None:
            args["shuffle_files"] = self.shuffle_files
        args["shuffle"] = self.shuffle_level
        args["num_shards"] = self.num_shards
        args["shard_id"] = self.shard_id
        args["shard_equal_rows"] = self.shard_equal_rows
        return args

    def get_dataset_size(self, estimate=False):
        """
        Get the number of batches in an epoch.

        Args:
            estimate (bool, optional): Fast estimation of the dataset size instead of a full scan.

        Return:
            Number, number of batches.
        """
        if self._dataset_size is None:
            num_rows = TFReaderOp.get_num_rows(self.dataset_files, 8, estimate)
            num_rows = get_num_rows(num_rows, self.num_shards)
            if self.num_samples is None:
                return num_rows
            return min(self.num_samples, num_rows)
        return self._dataset_size

    # manually set dataset_size as a tempoary solution.
    def set_dataset_size(self, value):
        logger.warning("WARN_DEPRECATED: This method is deprecated. Please use get_dataset_size directly.")
        if value >= 0:
            self._dataset_size = value
        else:
            raise ValueError('set dataset_size with negative value {}'.format(value))

    def is_shuffled(self):
        return self.shuffle_files

    def is_sharded(self):
        if self.num_shards is not None:
            return self.num_shards > 1

        return False


class ManifestDataset(MappableDataset):
    """
    A source dataset that reads images from a manifest file.

    The generated dataset has two columns ['image', 'label'].
    The shape of the image column is [image_size] if decode flag is False, or [H,W,C]
    otherwise.
    The type of the image tensor is uint8. The label is just a scalar uint64
    tensor.
    This dataset can take in a sampler. sampler and shuffle are mutually exclusive. Table
    below shows what input args are allowed and their expected behavior.

    .. list-table:: Expected Order Behavior of Using 'sampler' and 'shuffle'
       :widths: 25 25 50
       :header-rows: 1

       * - Parameter 'sampler'
         - Parameter 'shuffle'
         - Expected Order Behavior
       * - None
         - None
         - random order
       * - None
         - True
         - random order
       * - None
         - False
         - sequential order
       * - Sampler object
         - None
         - order defined by sampler
       * - Sampler object
         - True
         - not allowed
       * - Sampler object
         - False
         - not allowed

    Args:
        dataset_file (str): File to be read.
        usage (str, optional): Need train, eval or inference data (default="train").
        num_samples (int, optional): The number of images to be included in the dataset.
            (default=None, all images).
        num_parallel_workers (int, optional): Number of workers to read the data
            (default=None, number set in the config).
        shuffle (bool, optional): Whether to perform shuffle on the dataset (default=None, expected
            order behavior shown in the table).
        sampler (Sampler, optional): Object used to choose samples from the
            dataset (default=None, expected order behavior shown in the table).
        class_indexing (dict, optional): A str-to-int mapping from label name to index
            (default=None, the folder names will be sorted alphabetically and each
            class will be given a unique index starting from 0).
        decode (bool, optional): decode the images after reading (defaults=False).
        num_shards (int, optional): Number of shards that the dataset should be divided
            into (default=None).
        shard_id (int, optional): The shard ID within num_shards (default=None). This
            argument should be specified only when num_shards is also specified.

    Raises:
        RuntimeError: If sampler and shuffle are specified at the same time.
        RuntimeError: If sampler and sharding are specified at the same time.
        RuntimeError: If num_shards is specified but shard_id is None.
        RuntimeError: If shard_id is specified but num_shards is None.
        RuntimeError: If class_indexing is not a dictionary.
        ValueError: If shard_id is invalid (< 0 or >= num_shards).

    Examples:
        >>> import mindspore.dataset as ds
        >>> dataset_file = "/path/to/manifest_file.manifest"
        >>> # 1) read all samples specified in manifest_file dataset with 8 threads for training:
        >>> manifest_dataset = ds.ManifestDataset(dataset_file, usage="train", num_parallel_workers=8)
        >>> # 2) reads samples (specified in manifest_file.manifest) for shard 0 in a 2-way distributed training setup:
        >>> manifest_dataset = ds.ManifestDataset(dataset_file, num_shards=2, shard_id=0)

    """

    @check_manifestdataset
    def __init__(self, dataset_file, usage="train", num_samples=None, num_parallel_workers=None,
                 shuffle=None, sampler=None, class_indexing=None, decode=False, num_shards=None, shard_id=None):
        super().__init__(num_parallel_workers)

        self.dataset_file = dataset_file
        self.sampler = _select_sampler(num_samples, sampler, shuffle, num_shards, shard_id)

        if class_indexing is not None and not isinstance(class_indexing, dict):
            raise RuntimeError("class_indexing should be a dictionary.")

        self.num_samples = num_samples
        self.class_indexing = class_indexing
        self.decode = decode
        self.usage = usage
        self.shuffle_level = shuffle
        self.num_shards = num_shards
        self.shard_id = shard_id

    def get_args(self):
        args = super().get_args()
        args["dataset_file"] = self.dataset_file
        args["usage"] = self.usage
        args["num_samples"] = self.num_samples
        args["shuffle"] = self.shuffle_level
        args["sampler"] = self.sampler
        args["class_indexing"] = self.class_indexing
        args["decode"] = self.decode
        args["num_shards"] = self.num_shards
        args["shard_id"] = self.shard_id
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        if self.num_samples is None:
            num_samples = 0
        else:
            num_samples = self.num_samples

        if self.class_indexing is None:
            class_indexing = dict()
        else:
            class_indexing = self.class_indexing

        num_rows = ManifestOp.get_num_rows_and_classes(self.dataset_file, num_samples, class_indexing, self.usage)[0]
        rows_per_shard = get_num_rows(num_rows, self.num_shards)
        rows_from_sampler = self._get_sampler_dataset_size()

        if rows_from_sampler is None:
            return rows_per_shard

        return min(rows_from_sampler, rows_per_shard)

    def num_classes(self):
        """
        Get the number of classes in a dataset.

        Return:
            Number, number of classes.
        """
        if self.num_samples is None:
            num_samples = 0
        else:
            num_samples = self.num_samples

        if self.class_indexing is None:
            class_indexing = dict()
        else:
            class_indexing = self.class_indexing

        return ManifestOp.get_num_rows_and_classes(self.dataset_file, num_samples, class_indexing, self.usage)[1]

    def get_class_indexing(self):
        """
        Get the class index.

        Return:
            Dict, A str-to-int mapping from label name to index.
        """
        if self.num_samples is None:
            num_samples = 0
        else:
            num_samples = self.num_samples

        if self.class_indexing is None:
            class_indexing = dict()
        else:
            class_indexing = self.class_indexing

        return ManifestOp.get_class_indexing(self.dataset_file, num_samples, class_indexing, self.usage)

    def is_shuffled(self):
        if self.shuffle_level is None:
            return True

        return self.shuffle_level or self.sampler.is_shuffled()

    def is_sharded(self):
        if self.num_shards is not None:
            return self.num_shards > 1

        return self.sampler.is_sharded()


class Cifar10Dataset(MappableDataset):
    """
    A source dataset that reads cifar10 data.

    The generated dataset has two columns ['image', 'label'].
    The type of the image tensor is uint8. The label is just a scalar uint32
    tensor.
    This dataset can take in a sampler. sampler and shuffle are mutually exclusive. Table
    below shows what input args are allowed and their expected behavior.

    .. list-table:: Expected Order Behavior of Using 'sampler' and 'shuffle'
       :widths: 25 25 50
       :header-rows: 1

       * - Parameter 'sampler'
         - Parameter 'shuffle'
         - Expected Order Behavior
       * - None
         - None
         - random order
       * - None
         - True
         - random order
       * - None
         - False
         - sequential order
       * - Sampler object
         - None
         - order defined by sampler
       * - Sampler object
         - True
         - not allowed
       * - Sampler object
         - False
         - not allowed

    Args:
        dataset_dir (str): Path to the root directory that contains the dataset.
        num_samples (int, optional): The number of images to be included in the dataset.
            (default=None, all images).
        num_parallel_workers (int, optional): Number of workers to read the data
            (default=None, number set in the config).
        shuffle (bool, optional): Whether to perform shuffle on the dataset (default=None, expected
            order behavior shown in the table).
        sampler (Sampler, optional): Object used to choose samples from the
            dataset (default=None, expected order behavior shown in the table).
        num_shards (int, optional): Number of shards that the dataset should be divided
            into (default=None).
        shard_id (int, optional): The shard ID within num_shards (default=None). This
            argument should be specified only when num_shards is also specified.

    Raises:
        RuntimeError: If sampler and shuffle are specified at the same time.
        RuntimeError: If sampler and sharding are specified at the same time.
        RuntimeError: If num_shards is specified but shard_id is None.
        RuntimeError: If shard_id is specified but num_shards is None.
        ValueError: If shard_id is invalid (< 0 or >= num_shards).

    Examples:
        >>> import mindspore.dataset as ds
        >>> dataset_dir = "/path/to/cifar10_dataset_directory"
        >>> # 1) get all samples from CIFAR10 dataset in sequence:
        >>> dataset = ds.Cifar10Dataset(dataset_dir=dataset_dir,shuffle=False)
        >>> # 2) randomly select 350 samples from CIFAR10 dataset:
        >>> dataset = ds.Cifar10Dataset(dataset_dir=dataset_dir,num_samples=350, shuffle=True)
        >>> # 3) get samples from CIFAR10 dataset for shard 0 in a 2 way distributed training:
        >>> dataset = ds.Cifar10Dataset(dataset_dir=dataset_dir,num_shards=2,shard_id=0)
        >>> # in CIFAR10 dataset, each dictionary has keys "image" and "label"
    """

    @check_mnist_cifar_dataset
    def __init__(self, dataset_dir, num_samples=None, num_parallel_workers=None,
                 shuffle=None, sampler=None, num_shards=None, shard_id=None):
        super().__init__(num_parallel_workers)

        self.dataset_dir = dataset_dir
        self.sampler = _select_sampler(num_samples, sampler, shuffle, num_shards, shard_id)
        self.num_samples = num_samples
        self.num_shards = num_shards
        self.shard_id = shard_id
        self.shuffle_level = shuffle

    def get_args(self):
        args = super().get_args()
        args["dataset_dir"] = self.dataset_dir
        args["num_samples"] = self.num_samples
        args["sampler"] = self.sampler
        args["num_shards"] = self.num_shards
        args["shard_id"] = self.shard_id
        args["shuffle"] = self.shuffle_level
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        if self.num_samples is None:
            num_samples = 0
        else:
            num_samples = self.num_samples

        num_rows = CifarOp.get_num_rows(self.dataset_dir, num_samples, True)
        rows_per_shard = get_num_rows(num_rows, self.num_shards)
        rows_from_sampler = self._get_sampler_dataset_size()

        if rows_from_sampler is None:
            return rows_per_shard

        return min(rows_from_sampler, rows_per_shard)

    def is_shuffled(self):
        if self.shuffle_level is None:
            return True

        return self.shuffle_level or self.sampler.is_shuffled()

    def is_sharded(self):
        if self.num_shards is not None:
            return self.num_shards > 1

        return self.sampler.is_sharded()


class Cifar100Dataset(MappableDataset):
    """
    A source dataset that reads cifar100 data.

    The generated dataset has three columns ['image', 'coarse_label', 'fine_label'].
    The type of the image tensor is uint8. The coarse and fine are just a scalar uint32
    tensor.
    This dataset can take in a sampler. sampler and shuffle are mutually exclusive. Table
    below shows what input args are allowed and their expected behavior.

    .. list-table:: Expected Order Behavior of Using 'sampler' and 'shuffle'
       :widths: 25 25 50
       :header-rows: 1

       * - Parameter 'sampler'
         - Parameter 'shuffle'
         - Expected Order Behavior
       * - None
         - None
         - random order
       * - None
         - True
         - random order
       * - None
         - False
         - sequential order
       * - Sampler object
         - None
         - order defined by sampler
       * - Sampler object
         - True
         - not allowed
       * - Sampler object
         - False
         - not allowed

    Args:
        dataset_dir (str): Path to the root directory that contains the dataset.
        num_samples (int, optional): The number of images to be included in the dataset.
            (default=None, all images).
        num_parallel_workers (int, optional): Number of workers to read the data
            (default=None, number set in the config).
        shuffle (bool, optional): Whether to perform shuffle on the dataset (default=None, expected
            order behavior shown in the table).
        sampler (Sampler, optional): Object used to choose samples from the
            dataset (default=None, expected order behavior shown in the table).
        num_shards (int, optional): Number of shards that the dataset should be divided
            into (default=None).
        shard_id (int, optional): The shard ID within num_shards (default=None). This
            argument should be specified only when num_shards is also specified.

    Raises:
        RuntimeError: If sampler and shuffle are specified at the same time.
        RuntimeError: If sampler and sharding are specified at the same time.
        RuntimeError: If num_shards is specified but shard_id is None.
        RuntimeError: If shard_id is specified but num_shards is None.
        ValueError: If shard_id is invalid (< 0 or >= num_shards).

    Examples:
        >>> import mindspore.dataset as ds
        >>> dataset_dir = "/path/to/cifar100_dataset_directory"
        >>> # 1) get all samples from CIFAR100 dataset in sequence:
        >>> cifar100_dataset = ds.Cifar100Dataset(dataset_dir=dataset_dir,shuffle=False)
        >>> # 2) randomly select 350 samples from CIFAR100 dataset:
        >>> cifar100_dataset = ds.Cifar100Dataset(dataset_dir=dataset_dir,num_samples=350, shuffle=True)
        >>> # in CIFAR100 dataset, each dictionary has 3 keys: "image", "fine_label" and "coarse_label"
    """

    @check_mnist_cifar_dataset
    def __init__(self, dataset_dir, num_samples=None, num_parallel_workers=None,
                 shuffle=None, sampler=None, num_shards=None, shard_id=None):
        super().__init__(num_parallel_workers)

        self.dataset_dir = dataset_dir
        self.sampler = _select_sampler(num_samples, sampler, shuffle, num_shards, shard_id)
        self.num_samples = num_samples
        self.num_shards = num_shards
        self.shard_id = shard_id
        self.shuffle_level = shuffle

    def get_args(self):
        args = super().get_args()
        args["dataset_dir"] = self.dataset_dir
        args["num_samples"] = self.num_samples
        args["sampler"] = self.sampler
        args["num_shards"] = self.num_shards
        args["shard_id"] = self.shard_id
        args["shuffle"] = self.shuffle_level
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        if self.num_samples is None:
            num_samples = 0
        else:
            num_samples = self.num_samples

        num_rows = CifarOp.get_num_rows(self.dataset_dir, num_samples, False)
        rows_per_shard = get_num_rows(num_rows, self.num_shards)
        rows_from_sampler = self._get_sampler_dataset_size()

        if rows_from_sampler is None:
            return rows_per_shard

        return min(rows_from_sampler, rows_per_shard)

    def is_shuffled(self):
        if self.shuffle_level is None:
            return True

        return self.shuffle_level or self.sampler.is_shuffled()

    def is_sharded(self):
        if self.num_shards is not None:
            return self.num_shards > 1

        return self.sampler.is_sharded()


class RandomDataset(SourceDataset):
    """
    A source dataset that generates random data.

    Args:
        num_samples (int): number of samples to generate.
        schema (str or Schema, optional): Path to the json schema file or schema object (default=None).
            If the schema is not provided, the meta data from the TFRecord file is considered the schema.
        columns_list (list[str], optional): List of columns to be read (default=None, read all columns)
        num_parallel_workers (int, optional): number of workers to read the data
            (default=None, number set in the config).
    """

    def __init__(self, schema=None, columns_list=None, num_samples=None, num_parallel_workers=None):
        super().__init__(num_parallel_workers)
        schema_obj = None
        if (schema is not None) and (not isinstance(schema, Schema)):
            schema_obj = Schema(schema)  # read the schema file and convert to schema object to validate it
        self.schema = schema
        self.columns_list = columns_list
        self.num_samples = num_samples
        if schema_obj is not None and num_samples is None:
            self.num_samples = schema_obj.num_rows

    def get_args(self):
        args = super().get_args()
        if self.schema is not None:
            if isinstance(self.schema, Schema):
                self.schema.datasetType = 'Random'
                if self.num_samples is not None:
                    self.schema.num_rows = self.num_samples
                args["schema_json_string"] = self.schema.to_json()
            else:
                args["schema_file_path"] = self.schema
        args["schema"] = self.schema
        if self.columns_list is not None:
            args["columns_list"] = self.columns_list
        if self.num_samples is not None:
            args["num_samples"] = self.num_samples
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        rows_from_sampler = self._get_sampler_dataset_size()

        if rows_from_sampler is None:
            return self.num_samples

        return min(rows_from_sampler, self.num_samples)

    def is_shuffled(self):
        return True

    def is_sharded(self):
        return False

class Schema:
    """
    Class to represent a schema of dataset.

    Args:
        schema_file(str): Path of schema file (default=None).

    Return:
        Schema object, schema info about dataset.

    Raises:
        RuntimeError: If schema file failed to load.

    Example:
        >>> import mindspore.dataset as ds
        >>> import mindspore.common.dtype as mstype
        >>> # create schema, specify column name, mindspore.dtype and shape of the column
        >>> schema = ds.Schema()
        >>> schema.add_column('col1', de_type=mindspore.int64, shape=[2])
    """

    def __init__(self, schema_file=None):
        self.num_rows = None
        if schema_file is None:
            self.columns = []
            self.dataset_type = ''
        else:
            if not os.path.isfile(schema_file) or not os.access(schema_file, os.R_OK):
                raise ValueError("The file %s does not exist or permission denied!" % schema_file)
            try:
                with open(schema_file, 'r') as load_f:
                    json_obj = json.load(load_f)
            except json.decoder.JSONDecodeError:
                raise RuntimeError("Schema file failed to load.")
            except UnicodeDecodeError:
                raise RuntimeError("Schema file failed to decode.")
            except Exception:
                raise RuntimeError("Schema file failed to open.")
            self.from_json(json_obj)

    @check_add_column
    def add_column(self, name, de_type, shape=None):
        """
        Add new column to the schema.

        Args:
            name (str): name of the column.
            de_type (str): data type of the column.
            shape (list[int], optional): shape of the column
                (default=None, [-1] which is an unknown shape of rank 1).

        Raises:
            ValueError: If column type is unknown.
        """
        new_column = dict()
        new_column["name"] = name
        if isinstance(de_type, typing.Type):
            de_type = mstype_to_detype(de_type)
            new_column["type"] = str(de_type)
        else:
            new_column["type"] = str(DataType(de_type))

        if shape is not None:
            new_column["shape"] = shape
            new_column["rank"] = len(shape)
        else:
            new_column["rank"] = 1
        self.columns.append(new_column)

    def to_json(self):
        """
        Get a JSON string of the schema.

        Returns:
            Str, JSON string of the schema.
        """
        json_file = dict()
        json_file["columns"] = self.columns
        if self.dataset_type:
            json_file["datasetType"] = self.dataset_type
        if self.num_rows:
            json_file["numRows"] = self.num_rows
        return json.dumps(json_file, indent=2)

    def parse_columns(self, columns):
        """
        Parse the columns and add it to self.

        Args:
            columns (dict or list[dict]): dataset attribution information, decoded from schema file.

                - list[dict], 'name' and 'type' must be in keys, 'shape' optional.

                - dict, columns.keys() as name, columns.values() is dict, and 'type' inside, 'shape' optional.

        Raises:
            RuntimeError: If failed to parse columns.
            RuntimeError: If unknown items in columns.
            RuntimeError: If column's name field is missing.
            RuntimeError: If column's type field is missing.

        Example:
            >>> schema = Schema()
            >>> columns1 = [{'name': 'image', 'type': 'int8', 'shape': [3, 3]},
            >>>             {'name': 'label', 'type': 'int8', 'shape': [1]}]
            >>> schema.parse_columns(columns1)
            >>> columns2 = {'image': {'shape': [3, 3], 'type': 'int8'}, 'label': {'shape': [1], 'type': 'int8'}}
            >>> schema.parse_columns(columns2)
        """
        self.columns = []
        if isinstance(columns, list):
            for column in columns:
                try:
                    name = column.pop("name")
                except KeyError:
                    raise RuntimeError("Column's name is missing")
                try:
                    de_type = column.pop("type")
                except KeyError:
                    raise RuntimeError("Column' type is missing")
                shape = column.pop("shape", None)
                column.pop("t_impl", None)
                column.pop("rank", None)
                if column:
                    raise RuntimeError("Unknown field {}".format(",".join(column.keys())))
                self.add_column(name, de_type, shape)
        elif isinstance(columns, dict):
            for key, value in columns.items():
                name = key
                try:
                    de_type = value.pop("type")
                except KeyError:
                    raise RuntimeError("Column' type is missing")
                shape = value.pop("shape", None)
                value.pop("t_impl", None)
                value.pop("rank", None)
                if value:
                    raise RuntimeError("Unknown field {}".format(",".join(value.keys())))
                self.add_column(name, de_type, shape)
        else:
            raise RuntimeError("columns must be dict or list, columns contain name, type, shape(optional).")

    def from_json(self, json_obj):
        """
        Get schema file from json file.

        Args:
            json_obj(dictionary): object of json parsed.

        Raises:
            RuntimeError: if there is unknown item in the object.
            RuntimeError: if dataset type is missing in the object.
            RuntimeError: if columns are missing in the object.
        """
        if not isinstance(json_obj, dict) or json_obj is None:
            raise ValueError("Expected non-empty dict.")
        for k, v in json_obj.items():
            if k == "datasetType":
                self.dataset_type = v
            elif k == "numRows":
                self.num_rows = v
            elif k == "columns":
                self.parse_columns(v)
            else:
                raise RuntimeError("Unknown field %s" % k)

        if self.dataset_type is None:
            raise RuntimeError("DatasetType field is missing.")
        if self.columns is None:
            raise RuntimeError("Columns are missing.")
        if self.num_rows is not None:
            if not isinstance(self.num_rows, int) or self.num_rows <= 0:
                raise ValueError("numRows must be greater than 0")

    def __str__(self):
        return self.to_json()


class VOCDataset(MappableDataset):
    """
    A source dataset for reading and parsing VOC dataset.

    The generated dataset has two columns ['image', 'target'].
    The shape of both column is [image_size] if decode flag is False, or [H, W, C]
    otherwise.
    The type of both tensor is uint8.
    This dataset can take in a sampler. sampler and shuffle are mutually exclusive. Table
    below shows what input args are allowed and their expected behavior.

    .. list-table:: Expected Order Behavior of Using 'sampler' and 'shuffle'
       :widths: 25 25 50
       :header-rows: 1

       * - Parameter 'sampler'
         - Parameter 'shuffle'
         - Expected Order Behavior
       * - None
         - None
         - random order
       * - None
         - True
         - random order
       * - None
         - False
         - sequential order
       * - Sampler object
         - None
         - order defined by sampler
       * - Sampler object
         - True
         - not allowed
       * - Sampler object
         - False
         - not allowed

    Args:
        dataset_dir (str): Path to the root directory that contains the dataset.
        task (str): Set the task type of reading voc data, now only support "Segmentation" or "Detection"
            (default="Segmentation")
        mode(str): Set the data list txt file to be readed (default="train")
        class_indexing (dict, optional): A str-to-int mapping from label name to index
            (default=None, the folder names will be sorted alphabetically and each
            class will be given a unique index starting from 0).
        num_samples (int, optional): The number of images to be included in the dataset
            (default=None, all images).
        num_parallel_workers (int, optional): Number of workers to read the data
            (default=None, number set in the config).
        shuffle (bool, optional): Whether to perform shuffle on the dataset (default=None, expected
            order behavior shown in the table).
        decode (bool, optional): Decode the images after reading (default=False).
        sampler (Sampler, optional): Object used to choose samples from the dataset
            (default=None, expected order behavior shown in the table).
        num_shards (int, optional): Number of shards that the dataset should be divided
            into (default=None).
        shard_id (int, optional): The shard ID within num_shards (default=None). This
            argument should be specified only when num_shards is also specified.

    Raises:
        RuntimeError: If xml of Annotations is a invalid format
        RuntimeError: If xml of Annotations loss attribution of "object"
        RuntimeError: If xml of Annotations loss attribution of "bndbox"
        RuntimeError: If sampler and shuffle are specified at the same time.
        RuntimeError: If sampler and sharding are specified at the same time.
        RuntimeError: If num_shards is specified but shard_id is None.
        RuntimeError: If shard_id is specified but num_shards is None.
        ValueError: If task is not equal 'Segmentation' or 'Detection'.
        ValueError: If task equal 'Segmentation' but class_indexing is not None.
        ValueError: If txt related to mode is not exist.
        ValueError: If shard_id is invalid (< 0 or >= num_shards).

    Examples:
        >>> import mindspore.dataset as ds
        >>> dataset_dir = "/path/to/voc_dataset_directory"
        >>> # 1) read VOC data for segmenatation train
        >>> voc_dataset = ds.VOCDataset(dataset_dir, task="Segmentation", mode="train")
        >>> # 2) read VOC data for detection train
        >>> voc_dataset = ds.VOCDataset(dataset_dir, task="Detection", mode="train")
        >>> # 3) read all VOC dataset samples in dataset_dir with 8 threads in random order:
        >>> voc_dataset = ds.VOCDataset(dataset_dir, task="Detection", mode="train", num_parallel_workers=8)
        >>> # 4) read then decode all VOC dataset samples in dataset_dir in sequence:
        >>> voc_dataset = ds.VOCDataset(dataset_dir, task="Detection", mode="train", decode=True, shuffle=False)
        >>> # in VOC dataset, if task='Segmentation', each dictionary has keys "image" and "target"
        >>> # in VOC dataset, if task='Detection', each dictionary has keys "image" and "annotation"
    """

    @check_vocdataset
    def __init__(self, dataset_dir, task="Segmentation", mode="train", class_indexing=None, num_samples=None,
                 num_parallel_workers=None, shuffle=None, decode=False, sampler=None, num_shards=None, shard_id=None):
        super().__init__(num_parallel_workers)
        self.dataset_dir = dataset_dir
        self.task = task
        self.mode = mode
        self.class_indexing = class_indexing
        self.sampler = _select_sampler(num_samples, sampler, shuffle, num_shards, shard_id)
        self.num_samples = num_samples
        self.decode = decode
        self.shuffle_level = shuffle
        self.num_shards = num_shards
        self.shard_id = shard_id

    def get_args(self):
        args = super().get_args()
        args["dataset_dir"] = self.dataset_dir
        args["task"] = self.task
        args["mode"] = self.mode
        args["class_indexing"] = self.class_indexing
        args["num_samples"] = self.num_samples
        args["sampler"] = self.sampler
        args["decode"] = self.decode
        args["shuffle"] = self.shuffle_level
        args["num_shards"] = self.num_shards
        args["shard_id"] = self.shard_id
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        if self.num_samples is None:
            num_samples = 0
        else:
            num_samples = self.num_samples

        if self.class_indexing is None:
            class_indexing = dict()
        else:
            class_indexing = self.class_indexing

        num_rows = VOCOp.get_num_rows(self.dataset_dir, self.task, self.mode, class_indexing, num_samples)
        rows_per_shard = get_num_rows(num_rows, self.num_shards)
        rows_from_sampler = self._get_sampler_dataset_size()

        if rows_from_sampler is None:
            return rows_per_shard

        return min(rows_from_sampler, rows_per_shard)

    def get_class_indexing(self):
        """
        Get the class index.

        Return:
            Dict, A str-to-int mapping from label name to index.
        """
        if self.task != "Detection":
            raise NotImplementedError()

        if self.num_samples is None:
            num_samples = 0
        else:
            num_samples = self.num_samples

        if self.class_indexing is None:
            class_indexing = dict()
        else:
            class_indexing = self.class_indexing

        return VOCOp.get_class_indexing(self.dataset_dir, self.task, self.mode, class_indexing, num_samples)

    def is_shuffled(self):
        if self.shuffle_level is None:
            return True

        return self.shuffle_level or self.sampler.is_shuffled()

    def is_sharded(self):
        if self.num_shards is not None:
            return self.num_shards > 1

        return self.sampler.is_sharded()


class CelebADataset(MappableDataset):
    """
    A source dataset for reading and parsing CelebA dataset.Only support list_attr_celeba.txt currently.

    Note:
        The generated dataset has two columns ['image', 'attr'].
        The type of the image tensor is uint8. The attr tensor is uint32 and one hot type.

    Args:
        dataset_dir (str): Path to the root directory that contains the dataset.
        num_parallel_workers (int, optional): Number of workers to read the data (default=value set in the config).
        shuffle (bool, optional): Whether to perform shuffle on the dataset (default=None).
        dataset_type (string): one of 'all', 'train', 'valid' or 'test'.
        sampler (Sampler, optional): Object used to choose samples from the dataset (default=None).
        decode (bool, optional): decode the images after reading (default=False).
        extensions (list[str], optional): List of file extensions to be
            included in the dataset (default=None).
        num_samples (int, optional): The number of images to be included in the dataset.
            (default=None, all images).
        num_shards (int, optional): Number of shards that the dataset should be divided
            into (default=None).
        shard_id (int, optional): The shard ID within num_shards (default=None). This
            argument should be specified only when num_shards is also specified.
    """

    @check_celebadataset
    def __init__(self, dataset_dir, num_parallel_workers=None, shuffle=None, dataset_type='all',
                 sampler=None, decode=False, extensions=None, num_samples=None, num_shards=None, shard_id=None):
        super().__init__(num_parallel_workers)
        self.dataset_dir = dataset_dir
        self.sampler = _select_sampler(num_samples, sampler, shuffle, num_shards, shard_id)
        self.num_parallel_workers = num_parallel_workers
        self.decode = decode
        self.extensions = extensions
        self.num_samples = num_samples
        self.dataset_type = dataset_type
        self.num_shards = num_shards
        self.shard_id = shard_id
        self.shuffle_level = shuffle

    def get_args(self):
        args = super().get_args()
        args["dataset_dir"] = self.dataset_dir
        args["sampler"] = self.sampler
        args["shuffle"] = self.shuffle_level
        args["decode"] = self.decode
        args["extensions"] = self.extensions
        args["num_samples"] = self.num_samples
        args["dataset_type"] = self.dataset_type
        args["num_shards"] = self.num_shards
        args["shard_id"] = self.shard_id
        return args

    def is_shuffled(self):
        if self.shuffle_level is None:
            return True

        return self.shuffle_level or self.sampler.is_shuffled()

    def is_sharded(self):
        if self.num_shards is not None:
            return self.num_shards > 1

        return self.sampler.is_sharded()

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        if self._dataset_size is None:
            dir = os.path.realpath(self.dataset_dir)
            attr_file = os.path.join(dir, "list_attr_celeba.txt")
            num_rows = ''
            try:
                with open(attr_file, 'r') as f:
                    num_rows = int(f.readline())
            except Exception:
                raise RuntimeError("Get dataset size failed from attribution file.")
            rows_per_shard = get_num_rows(num_rows, self.num_shards)
            if self.num_samples is not None:
                rows_per_shard = min(self.num_samples, rows_per_shard)
            rows_from_sampler = self._get_sampler_dataset_size()
            if rows_from_sampler is None:
                return rows_per_shard
            return min(rows_from_sampler, rows_per_shard)
        return self._dataset_size

class TextFileDataset(SourceDataset):
    """
    A source dataset that reads and parses datasets stored on disk in text format.
    The generated dataset has one columns ['text'].

    Args:
        dataset_files (str or list[str]): String or list of files to be read or glob strings to search for a pattern of
            files. The list will be sorted in a lexicographical order.
        num_samples (int, optional): number of samples(rows) to read (default=None, reads the full dataset).
        num_parallel_workers (int, optional): number of workers to read the data
            (default=None, number set in the config).
        shuffle (bool, Shuffle level, optional): perform reshuffling of the data every epoch (default=Shuffle.GLOBAL).
            If shuffle is False, no shuffling will be performed;
            If shuffle is True, the behavior is the same as setting shuffle to be Shuffle.GLOBAL
            Otherwise, there are two levels of shuffling:

            - Shuffle.GLOBAL: Shuffle both the files and samples.

            - Shuffle.FILES: Shuffle files only.

        num_shards (int, optional): Number of shards that the dataset should be divided into (default=None).
        shard_id (int, optional): The shard ID within num_shards (default=None). This
            argument should be specified only when num_shards is also specified.
    Examples:
        >>> import mindspore.dataset as ds
        >>> dataset_files = ["/path/to/1", "/path/to/2"] # contains 1 or multiple text files
        >>> dataset = ds.TextFileDataset(dataset_files=dataset_files)
    """

    @check_textfiledataset
    def __init__(self, dataset_files, num_samples=None, num_parallel_workers=None,
                 shuffle=Shuffle.GLOBAL, num_shards=None, shard_id=None):
        super().__init__(num_parallel_workers)
        self.dataset_files = self._find_files(dataset_files)
        self.dataset_files.sort()
        self.num_samples = num_samples

        if not isinstance(shuffle, (bool, Shuffle)):
            raise TypeError("shuffle should be of boolean or enum 'Shuffle'.")
        if not isinstance(shuffle, Shuffle):
            if shuffle:
                self.shuffle_level = Shuffle.GLOBAL
                self.shuffle_files = True
            else:
                self.shuffle_level = None
                self.shuffle_files = False
        else:
            self.shuffle_level = shuffle
            self.shuffle_files = True

        self.num_shards = num_shards
        self.shard_id = shard_id

    def get_args(self):
        args = super().get_args()
        args["dataset_files"] = self.dataset_files
        args["num_samples"] = self.num_samples
        if self.shuffle_files is not None:
            args["shuffle_files"] = self.shuffle_files
        args["shuffle"] = self.shuffle_level
        args["num_shards"] = self.num_shards
        args["shard_id"] = self.shard_id
        return args

    def get_dataset_size(self):
        """
        Get the number of batches in an epoch.

        Return:
            Number, number of batches.
        """
        if self._dataset_size is None:
            num_rows = TextFileOp.get_num_rows(self.dataset_files)
            num_rows = get_num_rows(num_rows, self.num_shards)
            if self.num_samples is None:
                return num_rows
            return min(self.num_samples, num_rows)
        return self._dataset_size

    def is_shuffled(self):
        return self.shuffle_files

    def is_sharded(self):
        if self.num_shards is not None:
            return self.num_shards > 1

        return False
