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

import jwt

from cerebralcortex.core.data_manager.raw.stream_handler import DataSet


class SqlStorageTest:
    ###### STREAM RELATED TEST CASES #####
    def test_get_stream_metadata_by_name(self):
        pass

    def test_list_streams(self):
        pass

    def test_search_stream(self):
        pass

    def test_get_stream_versions(self):
        pass

    def test_get_stream_metadata_hash(self):
        pass

    def test_get_stream_name(self):
        pass

    def test_get_stream_metadata_by_hash(self):
        pass

    def test_is_stream(self):
        pass

    def test_is_study(self):
        pass

    def test_save_stream_metadata(self):
        pass

    def test__is_metadata_changed(self):
        pass

    ########## USER RELATED TEST CASES #######
    def test_create_user(self):
        pass

    def test_delete_user(self):
        pass

    def test_get_user_metadata(self):
        pass

    def test_get_user_settings(self):
        pass

    def test_login_user(self):
        pass

    def test_is_auth_token_valid(self):
        pass

    def test_list_users(self):
        pass
    def test_get_user_name(self):
        pass

    def test_is_user(self):
        pass

    def test_get_user_id(self):
        pass

    def test_update_auth_token(self):
        pass

    #### METADATA RELATED #####
    def test_get_corrected_metadata(self):
        pass

    ##### CACHE RELATED #####
    def test_set_cache_value(self):
        pass

    #### DATA INGESTION RELATED ####
    def test_add_ingestion_log(self):
        pass
    def test_update_ingestion_log(self):
        pass

    def test_add_scanned_files(self):
        pass

    def test_get_processed_files_list(self):
        pass

    def test_get_files_list(self):
        pass

    def test_is_file_processed(self):
        pass

    def test_get_ingestion_stats(self):
        pass

    def test_update_ingestion_log_status(self):
        pass
    def test_update_ingestion_log_status_ignore(self):
        pass

    def test_01_is_stream(self):
        result = self.CC.is_stream(self.stream_name)
        self.assertEqual(result, True)

    def test_02_get_stream_versions(self):
        versions = self.CC.get_stream_versions(self.stream_name)
        for version in versions:
            self.assertEqual(int(self.stream_version), int(version))

    def test_03_get_stream_name(self):
        ds = self.CC.get_stream(self.stream_name, data_type=DataSet.ONLY_METADATA)
        metadata_hash = ds.metadata[0].metadata_hash
        stream_name = self.CC.get_stream_name(metadata_hash)
        self.assertEqual(self.stream_name, stream_name)

    def test_04_get_stream_metadata_hash(self):
        metadata_hash = self.CC.get_stream_metadata_hash(self.stream_name)[0]
        self.assertEqual(self.metadata_hash, metadata_hash)

    def test_05_get_user_id(self):
        user_id = self.CC.get_user_id(self.username)
        self.assertEqual(self.user_id, user_id)

    def test_06_get_user_name(self):
        username = self.CC.get_user_name(self.user_id)
        self.assertEqual(self.username, username)

    def test_07_get_all_users(self):
        all_users = self.CC.list_users()
        self.assertEqual(len(all_users), 1)
        username = all_users[0].get("username")
        user_id = all_users[0].get("user_id")

        self.assertEqual(self.username, username)
        self.assertEqual(self.user_id, user_id)

    def test_08_get_user_metadata(self):
        self.CC.get_user_metadata(self.user_id)
        self.CC.get_user_metadata(self.username)
        self.CC.get_user_metadata(self.user_id, self.username)

    def test_09_encrypt_user_password(self):
        result = self.CC.encrypt_user_password(self.user_password)
        self.assertEqual(result, self.user_password_encrypted)

    def test_10_connect(self):
        result = self.CC.connect(self.username, self.user_password_encrypted, True)
        self.assertEqual(result.get("status"), True)
        self.assertNotEqual(result.get("msg"), "")
        token = result.get("auth_token")

        decoded_token = jwt.decode(token, self.CC.config["cc"]["auth_encryption_key"], algorithm='HS256')
        is_valid = self.CC.is_auth_token_valid(decoded_token.get("username",""), token)
        self.assertEqual(is_valid, True)

        user_settings =self.CC.SqlData.get_user_settings(auth_token=token)
        self.assertEqual(user_settings.get("user_id", ""), self.user_id)
        self.assertEqual(user_settings.get("username", ""), self.username)
        self.assertEqual(user_settings.get("user_settings", ""), '{"mcerebrum": "confs"}')

