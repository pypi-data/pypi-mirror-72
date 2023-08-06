#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

from placementclient import base


class AllocationCandidates(base.Resource):
    pass


class AllocationCandidatesManager(base.BasicManager):

    base_url = 'allocation_candidates'
    resource_class = AllocationCandidates
    response_key = 'provider_summaries'
    headers = {'OpenStack-API-Version': 'placement 1.21',
               'Accept': 'application/json'}

    def list(self, resources):
        return self._list('/%s' % self.base_url, params=resources,
                          headers=self.headers,
                          response_key=self.response_key)
