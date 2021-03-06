# Copyright (C) 2018 Alteryx, Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
from ayx.tests.testdata.set_wd import set_wd

set_wd()


import sys, os

dll_path = "S:\\Alteryx\\bin_x64\\Release"
sys.path.insert(0, dll_path)
os.environ["path"] += dll_path
