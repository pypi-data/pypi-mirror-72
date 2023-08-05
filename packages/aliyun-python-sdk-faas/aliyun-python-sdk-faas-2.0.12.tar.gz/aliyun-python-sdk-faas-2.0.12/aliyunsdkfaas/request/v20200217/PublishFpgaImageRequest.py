# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest
from aliyunsdkfaas.endpoint import endpoint_data

class PublishFpgaImageRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'faas', '2020-02-17', 'PublishFpgaImage','faas')
		self.set_method('POST')
		if hasattr(self, "endpoint_map"):
			setattr(self, "endpoint_map", endpoint_data.getEndpointMap())
		if hasattr(self, "endpoint_regional"):
			setattr(self, "endpoint_regional", endpoint_data.getEndpointRegional())


	def get_Description(self):
		return self.get_query_params().get('Description')

	def set_Description(self,Description):
		self.add_query_param('Description',Description)

	def get_FpgaImageUniqueId(self):
		return self.get_query_params().get('FpgaImageUniqueId')

	def set_FpgaImageUniqueId(self,FpgaImageUniqueId):
		self.add_query_param('FpgaImageUniqueId',FpgaImageUniqueId)

	def get_ECSImageId(self):
		return self.get_query_params().get('ECSImageId')

	def set_ECSImageId(self,ECSImageId):
		self.add_query_param('ECSImageId',ECSImageId)