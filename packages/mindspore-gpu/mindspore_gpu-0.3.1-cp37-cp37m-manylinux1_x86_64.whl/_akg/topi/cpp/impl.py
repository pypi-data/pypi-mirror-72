# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

# 2019.12.30 - Modify _load_lib function.

"""Load Lib for C++ TOPI ops and schedules"""
import sys
import os
import ctypes

from tvm._ffi.function import _init_api_prefix
from tvm._ffi import libinfo

def _get_lib_names():
    if sys.platform.startswith('win32'):
        return ['libtvm_topi.dll', 'tvm_topi.dll']
    if sys.platform.startswith('darwin'):
        return ['libtvm_topi.dylib', 'tvm_topi.dylib']
    return ['libtvm_topi.so', 'tvm_topi.so']

def _load_lib():
    """Load library by searching possible path."""
    pwd = os.path.dirname(os.path.realpath(__file__)) 	
    path = os.path.realpath(pwd+"/../../../mindspore/lib")
    lib_path = []
    files = os.listdir(path)
    for f in files:
        if f.startswith("libtvm.") and f.endswith(".so"):
            lib_path.append(path+"/"+f)
            break
    if not lib_path:
        raise RuntimeError("mindspore library cannot find.")
  
    lib = ctypes.CDLL(lib_path[0], ctypes.RTLD_GLOBAL)
    return lib, os.path.basename(lib_path[0])

_LIB, _LIB_NAME = _load_lib()

_init_api_prefix("topi.cpp", "topi")
