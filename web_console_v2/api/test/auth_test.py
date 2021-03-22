# Copyright 2020 The FedLearner Authors. All Rights Reserved.
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
# limitations under the License.

# coding: utf-8

import unittest
from http import HTTPStatus

from testing.common import BaseTestCase


class AuthApiTest(BaseTestCase):
    def test_get_all_users(self):
        resp = self.get_helper('/api/v2/auth/users')
        self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)
        
        self.signin_as_admin()

        resp = self.get_helper('/api/v2/auth/users')
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(len(resp.json.get('data')), 2)

    def test_partial_update_user_info(self):
        self.signin_as_admin()
        resp = self.get_helper('/api/v2/auth/users')
        user_id = resp.json.get('data')[0]['id']
        admin_id = resp.json.get('data')[1]['id']

        self.signin_helper()
        resp = self.patch_helper('/api/v2/auth/users/10', data={})
        self.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)

        resp = self.patch_helper(f'/api/v2/auth/users/{user_id}',
                                 data={'company': 'bytedance'})
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)

        resp = self.patch_helper(f'/api/v2/auth/users/{user_id}',
                                 data={
                                     'email': 'a_new_email@bytedance.com',
                                 })
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(
            resp.json.get('data').get('email'), 'a_new_email@bytedance.com')

        resp = self.patch_helper(f'/api/v2/auth/users/{admin_id}',
                                 data={
                                     'name': 'cannot_modify',
                                 })
        self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)

        # now we are signing in as admin
        self.signin_as_admin()
        resp = self.patch_helper(f'/api/v2/auth/users/{user_id}',
                                 data={
                                     'role': 'ADMIN',
                                 })
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.json.get('data').get('role'), 'ADMIN')

    def test_create_new_user(self):
        new_user = {
            'username': 'fedlearner',
            'password': 'fedlearner',
            'email': 'hello@bytedance.com',
            'role': 'USER',
            'name': 'codemonkey',
        }
        resp = self.post_helper('/api/v2/auth/users', data=new_user)
        self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)

        self.signin_as_admin()
        resp = self.post_helper(f'/api/v2/auth/users', data=new_user)
        self.assertEqual(resp.status_code, HTTPStatus.CREATED)
        self.assertEqual(resp.json.get('data').get('username'), 'fedlearner')

    def test_delete_user(self):
        self.signin_as_admin()
        resp = self.get_helper('/api/v2/auth/users')
        user_id = resp.json.get('data')[0]['id']
        admin_id = resp.json.get('data')[1]['id']

        self.signin_helper()
        resp = self.delete_helper(url=f'/api/v2/auth/users/{user_id}')
        self.assertEqual(resp.status_code, HTTPStatus.UNAUTHORIZED)

        self.signin_as_admin()

        resp = self.delete_helper(url=f'/api/v2/auth/users/{admin_id}')
        self.assertEqual(resp.status_code, HTTPStatus.BAD_REQUEST)

        resp = self.delete_helper(url=f'/api/v2/auth/users/{user_id}')
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.json.get('data').get('username'), 'ada')

    def test_get_specific_user(self):
        resp = self.get_helper(url='/api/v2/auth/users/10086')
        self.assertEqual(resp.status_code, HTTPStatus.NOT_FOUND)
        
        resp = self.get_helper(url='/api/v2/auth/users/1')
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertEqual(resp.json.get('data').get('username'), 'ada')

if __name__ == '__main__':
    unittest.main()
