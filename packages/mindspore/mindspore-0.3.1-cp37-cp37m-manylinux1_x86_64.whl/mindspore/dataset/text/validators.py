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
validators for text ops
"""

from functools import wraps

import mindspore._c_dataengine as cde

from ..transforms.validators import check_uint32


def check_lookup(method):
    """A wrapper that wrap a parameter checker to the original function(crop operation)."""

    @wraps(method)
    def new_method(self, *args, **kwargs):
        vocab, unknown = (list(args) + 2 * [None])[:2]
        if "vocab" in kwargs:
            vocab = kwargs.get("vocab")
        if "unknown" in kwargs:
            unknown = kwargs.get("unknown")
        if unknown is not None:
            assert isinstance(unknown, int) and unknown >= 0, "unknown needs to be a non-negative integer"

        assert isinstance(vocab, cde.Vocab), "vocab is not an instance of cde.Vocab"

        kwargs["vocab"] = vocab
        kwargs["unknown"] = unknown
        return method(self, **kwargs)

    return new_method


def check_from_file(method):
    """A wrapper that wrap a parameter checker to the original function(crop operation)."""

    @wraps(method)
    def new_method(self, *args, **kwargs):
        file_path, delimiter, vocab_size = (list(args) + 3 * [None])[:3]
        if "file_path" in kwargs:
            file_path = kwargs.get("file_path")
        if "delimiter" in kwargs:
            delimiter = kwargs.get("delimiter")
        if "vocab_size" in kwargs:
            vocab_size = kwargs.get("vocab_size")

        assert isinstance(file_path, str), "file_path needs to be str"
        if delimiter is not None:
            assert isinstance(delimiter, str), "delimiter needs to be str"
        else:
            delimiter = ""
        if vocab_size is not None:
            assert isinstance(vocab_size, int) and vocab_size > 0, "vocab size needs to be a positive integer"
        else:
            vocab_size = -1
        kwargs["file_path"] = file_path
        kwargs["delimiter"] = delimiter
        kwargs["vocab_size"] = vocab_size
        return method(self, **kwargs)

    return new_method


def check_from_list(method):
    """A wrapper that wrap a parameter checker to the original function(crop operation)."""

    @wraps(method)
    def new_method(self, *args, **kwargs):
        word_list, = (list(args) + [None])[:1]
        if "word_list" in kwargs:
            word_list = kwargs.get("word_list")
        assert isinstance(word_list, list), "word_list needs to be a list of words"
        for word in word_list:
            assert isinstance(word, str), "each word in word list needs to be type str"

        kwargs["word_list"] = word_list
        return method(self, **kwargs)

    return new_method


def check_from_dict(method):
    """A wrapper that wrap a parameter checker to the original function(crop operation)."""

    @wraps(method)
    def new_method(self, *args, **kwargs):
        word_dict, = (list(args) + [None])[:1]
        if "word_dict" in kwargs:
            word_dict = kwargs.get("word_dict")
        assert isinstance(word_dict, dict), "word_dict needs to be a list of word,id pairs"
        for word, word_id in word_dict.items():
            assert isinstance(word, str), "each word in word_dict needs to be type str"
            assert isinstance(word_id, int) and word_id >= 0, "each word id needs to be positive integer"
        kwargs["word_dict"] = word_dict
        return method(self, **kwargs)

    return new_method


def check_jieba_init(method):
    """Wrapper method to check the parameters of jieba add word."""

    @wraps(method)
    def new_method(self, *args, **kwargs):
        hmm_path, mp_path, model = (list(args) + 3 * [None])[:3]

        if "hmm_path" in kwargs:
            hmm_path = kwargs.get("hmm_path")
        if "mp_path" in kwargs:
            mp_path = kwargs.get("mp_path")
        if hmm_path is None:
            raise ValueError(
                "the dict of HMMSegment in cppjieba is not provided")
        kwargs["hmm_path"] = hmm_path
        if mp_path is None:
            raise ValueError(
                "the dict of MPSegment in cppjieba is not provided")
        kwargs["mp_path"] = mp_path
        if model is not None:
            kwargs["model"] = model
        return method(self, **kwargs)

    return new_method


def check_jieba_add_word(method):
    """Wrapper method to check the parameters of jieba add word."""

    @wraps(method)
    def new_method(self, *args, **kwargs):
        word, freq = (list(args) + 2 * [None])[:2]

        if "word" in kwargs:
            word = kwargs.get("word")
        if "freq" in kwargs:
            freq = kwargs.get("freq")
        if word is None:
            raise ValueError("word is not provided")
        kwargs["word"] = word
        if freq is not None:
            check_uint32(freq)
            kwargs["freq"] = freq
        return method(self, **kwargs)

    return new_method


def check_jieba_add_dict(method):
    """Wrapper method to check the parameters of add dict"""

    @wraps(method)
    def new_method(self, *args, **kwargs):
        user_dict = (list(args) + [None])[0]
        if "user_dict" in kwargs:
            user_dict = kwargs.get("user_dict")
        if user_dict is None:
            raise ValueError("user_dict is not provided")
        kwargs["user_dict"] = user_dict
        return method(self, **kwargs)

    return new_method
