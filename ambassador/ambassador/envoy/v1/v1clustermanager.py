# Copyright 2018 Datawire. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from . import V1Config


class V1ClusterManager(dict):
    def __init__(self, config: 'V1Config') -> None:
        super().__init__()

        self['clusters'] = sorted(config.clusters, key=lambda cluster: cluster['name'])

    @classmethod
    def generate(cls, config: 'V1Config') -> None:
        config.clustermgr = V1ClusterManager(config)
