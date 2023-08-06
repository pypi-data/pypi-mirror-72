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
Sampler module provides several samplers to generate sampling data from dataset.
There are following samplers: DistributedSampler, PKSampler, RandomSampler,
SequentialSampler, SubsetRandomSampler, WeightedRandomSampler.
User can also define custom sampler by extending from Sampler class.
"""

import numpy as np
import mindspore._c_dataengine as cde


class Sampler:
    """
    Base class for user defined sampler.
    User defined sampler can be used with any existing dataset with sampler support.

    An required  _iter_() method should by overridden by user for sample index generation.
    An optional reset() method can be overridden for per repeat reset,

    dataset_size and num_samples will be set by dataset once a dataset iterator is created.

    Examples:
        >>> import mindspore.dataset as ds
        >>>
        >>> class ReverseSampler(ds,Sampler):
        >>>     def __iter__(self):
        >>>         for i in range(self.dataset_size - 1, -1, -1):
        >>>             yield i
        >>>
        >>> ds = ds.ImageFolderDatasetV2(path, sampler=ReverseSampler())
    """

    def __init__(self):
        self.dataset_size = 0
        self.num_samples = 0
        self.child_sampler = None

    def __iter__(self):
        """
        User defined iterator, must be overridden.
        _handshake is guaranteed to be called prior to iterator construction

        """
        raise NotImplementedError

    def reset(self):
        """
        Per repeat reset callback, override this method if necessary
        """

    # Initialization handshake callback
    # Do not override this method!
    def _handshake(self, ds_size, num_samples):
        self.dataset_size = ds_size
        self.num_samples = num_samples

    # Indices fetcher
    # Do not override this method!
    def _get_indices(self):
        sampler_iter = iter(self)
        ret = []
        for _ in range(self.num_samples):
            try:
                idx = next(sampler_iter)
                ret.append(idx)
            except StopIteration:
                break
        return np.array(ret)

    # Instance fetcher
    # Do not override this method!
    def create(self):
        c_sampler = cde.PythonSampler(self)
        c_child_sampler = self.create_child()
        c_sampler.add_child(c_child_sampler)
        return c_sampler

    def add_child(self, sampler):
        self.child_sampler = sampler

    def get_child(self):
        return self.child_sampler

    def create_child(self):
        c_child_sampler = None
        if self.child_sampler is not None:
            c_child_sampler = self.child_sampler.create()

        return c_child_sampler

    def is_shuffled(self):
        if self.child_sampler is None:
            return False

        return self.child_sampler.is_shuffled()

    def is_sharded(self):
        if self.child_sampler is None:
            return False

        return self.child_sampler.is_sharded()

    def get_dataset_size(self):
        return self._get_indices().size


class BuiltinSampler:
    """
    Base class for BuiltinSampler.

    User should not extend this class.
    """
    def __init__(self):
        self.child_sampler = None

    def create(self):
        pass

    def add_child(self, sampler):
        self.child_sampler = sampler

    def get_child(self):
        return self.child_sampler

    def create_child(self):
        c_child_sampler = None
        if self.child_sampler is not None:
            c_child_sampler = self.child_sampler.create()

        return c_child_sampler

    def is_shuffled(self):
        raise NotImplementedError("Sampler must implement is_shuffled.")

    def is_sharded(self):
        raise NotImplementedError("Sampler must implement is_sharded.")

    def get_dataset_size(self):
        if self.child_sampler is not None:
            return self.child_sampler.get_dataset_size()

        return None


class DistributedSampler(BuiltinSampler):
    """
    Sampler that access a shard of the dataset.

    Args:
        num_shards (int): Number of shards to divide the dataset into.
        shard_id (int): Shard ID of the current shard within num_shards.
        shuffle (bool, optional): If true, the indices are shuffled (default=True).

    Examples:
        >>> import mindspore.dataset as ds
        >>>
        >>> dataset_dir = "path/to/imagefolder_directory"
        >>>
        >>> # creates a distributed sampler with 10 shards total. This shard is shard 5
        >>> sampler = ds.DistributedSampler(10, 5)
        >>> data = ds.ImageFolderDatasetV2(dataset_dir, num_parallel_workers=8, sampler=sampler)

    Raises:
        ValueError: If num_shards is not positive.
        ValueError: If shard_id is smaller than 0 or equal to num_shards or larger than num_shards.
        ValueError: If shuffle is not a boolean value.
    """

    def __init__(self, num_shards, shard_id, shuffle=True):
        if num_shards <= 0:
            raise ValueError("num_shards should be a positive integer value, but got num_shards={}".format(num_shards))

        if shard_id < 0 or shard_id >= num_shards:
            raise ValueError("shard_id is invalid, shard_id={}".format(shard_id))

        if not isinstance(shuffle, bool):
            raise ValueError("shuffle should be a boolean value, but got shuffle={}".format(shuffle))

        self.num_shards = num_shards
        self.shard_id = shard_id
        self.shuffle = shuffle
        self.seed = 0
        super().__init__()

    def create(self):
        # each time user calls create_dict_iterator() (to do repeat) sampler would get a different seed to shuffle
        self.seed += 1
        c_sampler = cde.DistributedSampler(self.num_shards, self.shard_id, self.shuffle, self.seed)
        c_child_sampler = self.create_child()
        c_sampler.add_child(c_child_sampler)
        return c_sampler

    def is_shuffled(self):
        if self.child_sampler is None:
            return self.shuffle

        return self.child_sampler.is_shuffled()

    def is_sharded(self):
        if self.child_sampler is None:
            return self.num_shards > 1

        return self.child_sampler.is_sharded()


class PKSampler(BuiltinSampler):
    """
    Samples K elements for each P class in the dataset.

    Args:
        num_val (int): Number of elements to sample for each class.
        num_class (int, optional): Number of classes to sample (default=None, all classes).
        shuffle (bool, optional): If true, the class IDs are shuffled (default=False).
        class_column (str, optional): Name of column to classify dataset(default='label'), for MindDataset.

    Examples:
        >>> import mindspore.dataset as ds
        >>>
        >>> dataset_dir = "path/to/imagefolder_directory"
        >>>
        >>> # creates a PKSampler that will get 3 samples from every class.
        >>> sampler = ds.PKSampler(3)
        >>> data = ds.ImageFolderDatasetV2(dataset_dir, num_parallel_workers=8, sampler=sampler)

    Raises:
        ValueError: If num_val is not positive.
        NotImplementedError: If num_class is not None.
        ValueError: If shuffle is not boolean.
    """

    def __init__(self, num_val, num_class=None, shuffle=False, class_column='label'):
        if num_val <= 0:
            raise ValueError("num_val should be a positive integer value, but got num_val={}".format(num_val))

        if num_class is not None:
            raise NotImplementedError

        if not isinstance(shuffle, bool):
            raise ValueError("shuffle should be a boolean value, but got shuffle={}".format(shuffle))

        self.num_val = num_val
        self.shuffle = shuffle
        self.class_column = class_column # work for minddataset
        super().__init__()

    def create(self):
        c_sampler = cde.PKSampler(self.num_val, self.shuffle)
        c_child_sampler = self.create_child()
        c_sampler.add_child(c_child_sampler)
        return c_sampler

    def is_shuffled(self):
        if self.child_sampler is None:
            return self.shuffle

        return self.child_sampler.is_shuffled()

    def is_sharded(self):
        if self.child_sampler is None:
            return False

        return self.child_sampler.is_sharded()

    def _create_for_minddataset(self):
        if not self.class_column or not isinstance(self.class_column, str):
            raise ValueError("class_column should be a not empty string value, \
                    but got class_column={}".format(class_column))
        return cde.MindrecordPkSampler(self.num_val, self.class_column, self.shuffle)


class RandomSampler(BuiltinSampler):
    """
    Samples the elements randomly.

    Args:
        replacement (bool, optional): If True, put the sample ID back for the next draw (default=False).
        num_samples (int, optional): Number of elements to sample (default=None, all elements).

    Examples:
        >>> import mindspore.dataset as ds
        >>>
        >>> dataset_dir = "path/to/imagefolder_directory"
        >>>
        >>> # creates a RandomSampler
        >>> sampler = ds.RandomSampler()
        >>> data = ds.ImageFolderDatasetV2(dataset_dir, num_parallel_workers=8, sampler=sampler)

    Raises:
        ValueError: If replacement is not boolean.
        ValueError: If num_samples is not positive.
     """

    def __init__(self, replacement=False, num_samples=None):
        if not isinstance(replacement, bool):
            raise ValueError("replacement should be a boolean value, but got replacement={}".format(replacement))

        if num_samples is not None:
            if num_samples <= 0:
                raise ValueError("num_samples should be a positive integer "
                                 "value, but got num_samples={}".format(num_samples))

        self.deterministic = False
        self.replacement = replacement
        self.num_samples = num_samples
        self.reshuffle_each_epoch = True
        super().__init__()

    def create(self):
        c_sampler = None
        if self.num_samples is None:
            c_sampler = cde.RandomSampler(self.replacement, self.reshuffle_each_epoch)
        else:
            c_sampler = cde.RandomSampler(self.replacement, self.reshuffle_each_epoch, self.num_samples)

        c_child_sampler = self.create_child()
        c_sampler.add_child(c_child_sampler)
        return c_sampler

    def is_shuffled(self):
        return True

    def is_sharded(self):
        if self.child_sampler is None:
            return False

        return self.child_sampler.is_sharded()

    def get_dataset_size(self):
        return self.num_samples


class SequentialSampler(BuiltinSampler):
    """
    Samples the dataset elements sequentially, same as not having a sampler.

    Examples:
        >>> import mindspore.dataset as ds
        >>>
        >>> dataset_dir = "path/to/imagefolder_directory"
        >>>
        >>> # creates a SequentialSampler
        >>> sampler = ds.SequentialSampler()
        >>> data = ds.ImageFolderDatasetV2(dataset_dir, num_parallel_workers=8, sampler=sampler)
    """

    def create(self):
        c_sampler = cde.SequentialSampler()
        c_child_sampler = self.create_child()
        c_sampler.add_child(c_child_sampler)
        return c_sampler

    def is_shuffled(self):
        if self.child_sampler is None:
            return False

        return self.child_sampler.is_shuffled()

    def is_sharded(self):
        if self.child_sampler is None:
            return False

        return self.child_sampler.is_sharded()


class SubsetSampler(BuiltinSampler):
    """
    Samples a subset of elements consecutively from a given index.

    Args:
        start_index (int): Index to start sampling at.
        subset_size (int): How many samples to include in this subset.

    Examples:
        >>> import mindspore.dataset as ds
        >>>
        >>> dataset_dir = "path/to/imagefolder_directory"
        >>>
        >>> # creates a SubsetSampler, will sample the next 5 images from the 100th image.
        >>> sampler = ds.SubsetSampler(100, 5)
        >>> data = ds.ImageFolderDatasetV2(dataset_dir, num_parallel_workers=8, sampler=sampler)

    Raises:
        ValueError: If start_index is not a positive int.
        ValueError: If subset_size is not a positive int.
    """

    def __init__(self, start_index, subset_size):
        if not isinstance(start_index, int):
            raise ValueError("start_index should be an int.")

        if start_index < 0:
            raise ValueError("start_index should not be negative.")

        if not isinstance(subset_size, int):
            raise ValueError("start_index should be an int")

        if subset_size < 0:
            raise ValueError("subset_size should not be negative.")

        self.start_index = start_index
        self.subset_size = subset_size
        super().__init__()

    def create(self):
        c_sampler = cde.SubsetSampler(self.start_index, self.subset_size)
        c_child_sampler = self.create_child()
        c_sampler.add_child(c_child_sampler)
        return c_sampler

    def is_shuffled(self):
        if self.child_sampler is None:
            return False

        return self.child_sampler.is_shuffled()

    def is_sharded(self):
        if self.child_sampler is None:
            return False

        return self.child_sampler.is_sharded()

    def get_dataset_size(self):
        return self.subset_size


class SubsetRandomSampler(BuiltinSampler):
    """
    Samples the elements randomly from a sequence of indices.

    Args:
        indices (list[int]): A sequence of indices.

    Examples:
        >>> import mindspore.dataset as ds
        >>>
        >>> dataset_dir = "path/to/imagefolder_directory"
        >>>
        >>> indices = [0, 1, 2, 3, 7, 88, 119]
        >>>
        >>> # creates a SubsetRandomSampler, will sample from the provided indices
        >>> sampler = ds.SubsetRandomSampler()
        >>> data = ds.ImageFolderDatasetV2(dataset_dir, num_parallel_workers=8, sampler=sampler)
    """

    def __init__(self, indices):
        if not isinstance(indices, list):
            indices = [indices]

        self.indices = indices
        super().__init__()

    def create(self):
        c_sampler = cde.SubsetRandomSampler(self.indices)
        c_child_sampler = self.create_child()
        c_sampler.add_child(c_child_sampler)
        return c_sampler

    def is_shuffled(self):
        return True

    def is_sharded(self):
        if self.child_sampler is None:
            return False

        return self.child_sampler.is_sharded()

    def _create_for_minddataset(self):
        return cde.MindrecordSubsetRandomSampler(self.indices)


    def get_dataset_size(self):
        return len(self.indices)


class WeightedRandomSampler(BuiltinSampler):
    """
    Samples the elements from [0, len(weights) - 1] randomly with the given weights (probabilities).

    Args:
        weights (list[float]): A sequence of weights, not necessarily summing up to 1.
        num_samples (int): Number of elements to sample.
        replacement (bool, optional): If True, put the sample ID back for the next draw (default=True).

    Examples:
        >>> import mindspore.dataset as ds
        >>>
        >>> dataset_dir = "path/to/imagefolder_directory"
        >>>
        >>> weights = [0.9, 0.01, 0.4, 0.8, 0.1, 0.1, 0.3]
        >>>
        >>> # creates a WeightedRandomSampler that will sample 4 elements without replacement
        >>> sampler = ds.WeightedRandomSampler(weights, 4)
        >>> data = ds.ImageFolderDatasetV2(dataset_dir, num_parallel_workers=8, sampler=sampler)

    Raises:
        ValueError: If num_samples is not positive.
        ValueError: If replacement is not boolean.
    """

    def __init__(self, weights, num_samples, replacement=True):
        if not isinstance(weights, list):
            weights = [weights]

        if num_samples <= 0:
            raise ValueError("num_samples should be a positive integer "
                             "value, but got num_samples={}".format(num_samples))

        if not isinstance(replacement, bool):
            raise ValueError("replacement should be a boolean value, but got replacement={}".format(replacement))

        self.weights = weights
        self.num_samples = num_samples
        self.replacement = replacement
        super().__init__()

    def create(self):
        c_sampler = cde.WeightedRandomSampler(self.weights, self.num_samples, self.replacement)
        c_child_sampler = self.create_child()
        c_sampler.add_child(c_child_sampler)
        return c_sampler

    def is_shuffled(self):
        return True

    def is_sharded(self):
        if self.child_sampler is None:
            return False

        return self.child_sampler.is_sharded()

    def get_dataset_size(self):
        return self.num_samples
