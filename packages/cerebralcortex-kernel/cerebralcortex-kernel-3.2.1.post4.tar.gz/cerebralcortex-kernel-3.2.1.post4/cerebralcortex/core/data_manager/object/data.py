# Copyright (c) 2019, MD2K Center of Excellence
# - Nasir Ali <nasir.ali08@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from cerebralcortex.core.data_manager.object.storage_filesystem import FileSystemStorage
from cerebralcortex.core.log_manager.log_handler import LogTypes
import os


class ObjectData(FileSystemStorage):
    def __init__(self, CC):
        """
        Constructor
        Args:
            CC (CerebralCortex): CerebralCortex object reference
        """
        self.CC = CC
        self.config = CC.config

        self.study_name = CC.study_name
        self.new_study = CC.new_study

        self.logging = CC.logging
        self.logtypes = LogTypes()
      
        self.filesystem_path = self.config["object_storage"]["object_storage_path"]
        
        if self.filesystem_path[-1]!="/":
            self.filesystem_path += "/"
        
        self.filesystem_path = self.filesystem_path+"study="+self.study_name+"/"

        if (self.new_study or self.study_name=="default") and not os.path.exists(self.filesystem_path):
            os.mkdir(self.filesystem_path)
