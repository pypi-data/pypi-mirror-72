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

import json
import re


class DataIngestionHandler():

    ###################################################################
    ################## GET DATA METHODS ###############################
    ###################################################################

    def add_ingestion_log(self, user_id: str = "", stream_name: str = "", file_path: str = "", fault_type: str = "",
                          fault_description: str = "", success: int = None, metadata=None) -> bool:
        """
        Log errors and success of each record during data import process.

        Args:
            user_id (str): id of a user
            stream_name (str): name of a stream
            file_path (str): filename with its path
            fault_type (str): error type
            fault_description (str): error details
            success (int): 1 if data was successfully ingested, 0 otherwise
            metadata (dict): (optional) metadata of a stream

        Returns:
            bool

        Raises:
            ValeError: if
            Exception: if sql query fails user_id, file_path, fault_type, or success parameters is missing
        """

        if not user_id or not file_path or not fault_type or success is None:
            raise ValueError("user_id, file_path, fault_type, and success are mandatory parameters.")

        if metadata:
            qry = "INSERT IGNORE INTO " + self.ingestionLogsTable + " (user_id, stream_name, file_path, fault_type, fault_description, success, metadata) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            vals = str(user_id), str(stream_name), str(file_path), str(fault_type), json.dumps(fault_description), success, json.dumps(metadata)
        else:
            qry = "INSERT IGNORE INTO " + self.ingestionLogsTable + " (user_id, stream_name, file_path, fault_type, fault_description, success) VALUES(%s, %s, %s, %s, %s, %s)"
            vals = str(user_id), str(stream_name), str(file_path), str(fault_type), json.dumps(fault_description), success

        try:
            self.execute(qry, vals, commit=True)
            return True
        except Exception as e:
            raise Exception(e)

    def update_ingestion_log(self, file_path: str = "", fault_type: str = "", fault_description: str = "", success: int = None) -> bool:
        """
        update ingestion Logs of each record during data import process.

        Args:
            file_path (str): filename with its path
            fault_type (str): error type
            fault_description (str): error details
            success (int): 1 if data was successfully ingested, 0 otherwise

        Returns:
            bool

        Raises:
            ValeError: if
            Exception: if sql query fails user_id, file_path, fault_type, or success parameters is missing
        """

        if not fault_type or success is None:
            raise ValueError("fault_type and success are mandatory parameters.")
        fault_description=re.sub('[^A-Za-z0-9:><]+', ' ', fault_description)

        qry = "UPDATE " + self.ingestionLogsTable + " SET fault_type=%s, fault_description=%s, success=%s where file_path=%s"
        vals =  str(fault_type), str(fault_description), success, str(file_path)

        try:
            self.execute(qry, vals, commit=True)
            return True
        except Exception as e:
            raise Exception(e)

    def add_scanned_files(self, user_id: str, stream_name: str, metadata:dict, files_list: list) -> bool:
        """
        Add scanned files in ingestion log table that could be processed later on. This method is specific to MD2K data ingestion.

        Args:
            user_id (str): id of a user
            stream_name (str): name of a stream
            metadata (dict): raw metadata
            files_list (list): list of filenames with its path

        Returns:
            bool

        Raises:
            Exception: if sql query fails
        """
        rows = []
        qry = "INSERT IGNORE INTO " + self.ingestionLogsTable + " (user_id, stream_name, metadata, file_path, fault_type, fault_description, success) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        for fp in files_list:
            rows.append((str(user_id), str(stream_name), json.dumps(metadata).lower(), str(fp), "PENDING", "NOT-PROCESSED-YET", 5)) # success=1 process, success=0 error-in-processing, and success=5 no processed yet

        try:
            self.execute(qry, rows, commit=True,executemany=True)
            return True
        except Exception as e:
            raise Exception(e)

    def get_processed_files_list(self, success_type=False) -> list:
        """
        Get a list of all the processed/un-processed files

        Returns:
            list: list of all processed files list
        """
        result = []
        if success_type:
            qry = "select file_path from " + self.ingestionLogsTable + " where success=%(success)s"
            vals = {"success":success_type}
            rows = self.execute(qry, vals)
        else:
            qry = "select file_path from " + self.ingestionLogsTable
            rows = self.execute(qry)

        if len(rows) == 0:
            return result
        else:
            for row in rows:
                result.append(row["file_path"])
            return result

    def get_files_list(self, stream_name:str=None, user_id=None, success_type=None) -> list:
        """
        Get a list of all the processed/un-processed files

        Returns:
            list: list of all processed files list
        """
        result = []
        if not stream_name and not user_id:
            where_clause = " where success=%(success)s "
            vals = {"success":success_type}
        else:
            where_clause = " where success=%s "
            vals = (str(success_type),)

        if stream_name:
            where_clause += " and stream_name=%s"
            vals = vals + (stream_name,)
        if user_id:
            where_clause += " and user_id=%s"
            vals = vals + (user_id,)

        if success_type==None:
            qry = "select * from " + self.ingestionLogsTable
            rows = self.execute(qry)
        else:
            qry = "select * from " + self.ingestionLogsTable + where_clause
            rows = self.execute(qry, vals)

        if len(rows) == 0:
            return result
        else:
            for row in rows:
                result.append({"stream_name":row["stream_name"], "user_id": row["user_id"], "metadata":json.loads(row["metadata"]), "file_path":row["file_path"]})
            return result

    def is_file_processed(self, filename:str) -> bool:
        """
        check if a file is processed and ingested

        Returns:
            bool: True if file is already processed
        """
        qry = "select file_path from " + self.ingestionLogsTable + " where file_path=%(file_path)s"
        vals = {"file_path":filename}
        rows = self.execute(qry, vals)

        if len(rows) > 0:
            return True
        else:
            return False


    def get_ingestion_stats(self) -> list:
        """
        Get stats on ingested records


        Returns:
            dict: {"fault_type": str, "total_faults": int, "success":int}
        """
        result = []
        qry = "select fault_type, count(fault_type) as total_faults, success from " + self.ingestionLogsTable + " group by fault_type"

        rows = self.execute(qry)

        if len(rows) == 0:
            return result
        else:
            for row in rows:
                result.append({"fault_type": row["fault_type"], "total_faults": row["total_faults"]})
            return result

    def update_ingestion_log_status(self, stream_name, metadata={}, platform_metadata={}):
        qry = "update " + self.ingestionLogsTable + " set metadata=%s, platform_metadata=%s where stream_name=%s"
        vals = json.dumps(metadata), json.dumps(platform_metadata), str(stream_name)
        try:
            self.execute(qry, vals, commit=True)
        except Exception as e:
            print("Cannot update metadata in ingest_log table. ", str(e))

    def update_ingestion_log_status_ignore(self, stream_name, fault_type, fault_description, status_type, metadata=None):
        qry = "update " + self.ingestionLogsTable + " set fault_type=%s, fault_description=%s, success=%s where stream_name=%s"
        vals = fault_type, fault_description, status_type, stream_name
        try:
            self.execute(qry, vals, commit=True)
        except Exception as e:
            print("Cannot update metadata in ingest_log table. ", str(e))