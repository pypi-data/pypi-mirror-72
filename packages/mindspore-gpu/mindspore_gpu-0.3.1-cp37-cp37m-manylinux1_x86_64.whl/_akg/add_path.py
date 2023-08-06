# Copyright 2020 Huawei Technologies Co., Ltd
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

"""add tvm path"""
import sys
import os


def AKGAddPath():
    """_akg add path."""
    pwd = os.path.dirname(os.path.realpath(__file__))
    tvm_path = os.path.realpath(pwd)
    if tvm_path not in sys.path:
        sys.path.insert(0, tvm_path)
    else:
        sys.path.remove(tvm_path)
        sys.path.insert(0, tvm_path)


class AKGMetaPathFinder:
    """class AKGMetaPath finder."""

    def find_module(self, fullname, path=None):
        """method _akg find module."""
        _ = path
        if fullname.startswith("_akg.tvm"):
            rname = fullname[5:]
            return AKGMetaPathLoader(rname)
        if fullname.startswith("_akg.topi"):
            rname = fullname[5:]
            return AKGMetaPathLoader(rname)
        return None


class AKGMetaPathLoader:
    """class AKGMetaPathLoader loader."""

    def __init__(self, rname):
        self.__rname = rname

    def load_module(self, fullname):
        if self.__rname in sys.modules:
            sys.modules.pop(self.__rname)
        AKGAddPath()
        __import__(self.__rname, globals(), locals())
        self.__target_module = sys.modules[self.__rname]
        sys.modules[fullname] = self.__target_module
        return self.__target_module


sys.meta_path.insert(0, AKGMetaPathFinder())
