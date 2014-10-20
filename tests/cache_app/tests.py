# -*- coding: utf-8 -*-
import time

from django.test import TestCase

from django.core.cache import cache


class DjangoArakoonCacheTest(TestCase):

    KEY = 'key'

    VALUE = 'value'
    VALUE_INT = 10
    VALUE_UNICODE = u'م € è ê ë ù'
    VALUE_DICT = {'a': 10, 'b': 10.00, 'c': 'string'}

    KEY_LIST = ['key1', 'key2', 'key3']
    VALUE_LIST = ['val1', 10, 10.10]

    def tearDown(self):
        cache.delete(self.KEY)
        cache.delete_many(self.KEY_LIST)

    ###########################################################################
    # ADD
    ###########################################################################
    def test_add(self):
        res = cache.add(self.KEY, self.VALUE)
        self.assertTrue(res)

        val = cache.get(self.KEY)
        self.assertEqual(val, self.VALUE)

    def test_add_exists(self):
        res = cache.add(self.KEY, self.VALUE)
        self.assertTrue(res)

        res = cache.add(self.KEY, 'NEW VALUE')
        self.assertFalse(res)

        val = cache.get(self.KEY)
        self.assertEqual(val, self.VALUE)

    def test_add_int(self):
        res = cache.add(self.KEY, self.VALUE_INT)
        self.assertTrue(res)

        val = cache.get(self.KEY)
        self.assertEqual(val, self.VALUE_INT)

    def test_add_unicode(self):
        res = cache.add(self.KEY, self.VALUE_UNICODE)
        self.assertTrue(res)

        val = cache.get(self.KEY)
        self.assertEqual(val, self.VALUE_UNICODE)

    def test_add_model(self):
        pass

    def test_add_dict(self):
        res = cache.add(self.KEY, self.VALUE_DICT)
        self.assertTrue(res)

        val = cache.get(self.KEY)
        self.assertEqual(val, self.VALUE_DICT)

    def test_add_timeout(self):
        res = cache.add(self.KEY, self.VALUE, timeout=2)
        self.assertTrue(res)

        time.sleep(4)

        val = cache.get(self.KEY)
        self.assertIsNone(val)

    ###########################################################################
    # SET
    ###########################################################################
    def test_set(self):
        cache.set(self.KEY, self.VALUE)

        val = cache.get(self.KEY)
        self.assertEqual(val, self.VALUE)

    def test_set_exist(self):
        cache.set(self.KEY, self.VALUE)

        time.sleep(1)
        cache.set(self.KEY, 'NEW VALUE')

        val = cache.get(self.KEY)
        self.assertEqual(val, 'NEW VALUE')

    def test_set_int(self):
        cache.set(self.KEY, self.VALUE_INT)

        val = cache.get(self.KEY)
        self.assertEqual(val, self.VALUE_INT)

    def test_set_unicode(self):
        cache.set(self.KEY, self.VALUE_UNICODE)

        val = cache.get(self.KEY)
        self.assertEqual(val, self.VALUE_UNICODE)

    def test_set_model(self):
        pass

    def test_set_dict(self):
        cache.set(self.KEY, self.VALUE_DICT)

        val = cache.get(self.KEY)
        self.assertEqual(val, self.VALUE_DICT)

    def test_set_timeout(self):
        cache.set(self.KEY, self.VALUE, timeout=2)

        time.sleep(4)

        val = cache.get(self.KEY)
        self.assertIsNone(val)

    def test_set_expired(self):
        cache.set(self.KEY, self.VALUE, timeout=2)

        time.sleep(4)

        val = cache.get(self.KEY)
        self.assertIsNone(val)

        # update
        cache.set(self.KEY, self.VALUE)
        val = cache.get(self.KEY)
        self.assertEqual(val, self.VALUE)

    ###########################################################################
    # DELETE
    ###########################################################################
    def test_delete(self):
        cache.set(self.KEY, self.VALUE)

        cache.delete(self.KEY)

        val = cache.get(self.KEY)
        self.assertIsNone(val)

    def test_delete_missing(self):
        cache.delete('DOES NOT EXIST!')

    ###########################################################################
    # MANY
    ###########################################################################
    def test_set_many(self):
        data = dict(zip(self.KEY_LIST, self.VALUE_LIST))

        cache.set_many(data)

        for idx, key in enumerate(self.KEY_LIST):
            val = cache.get(key)
            self.assertEqual(val, self.VALUE_LIST[idx])

    def test_get_many(self):
        data = dict(zip(self.KEY_LIST, self.VALUE_LIST))

        cache.set_many(data)

        vals = cache.get_many(self.KEY_LIST)

        self.assertEqual(data, vals)

    def test_get_many_missing(self):
        data = dict(zip(self.KEY_LIST, self.VALUE_LIST))

        cache.set_many(data)

        cache.delete(self.KEY_LIST[0])

        vals = cache.get_many(self.KEY_LIST)

        self.assertNotEqual(len(vals), len(self.KEY_LIST))
        self.assertEqual(len(vals), len(self.KEY_LIST) - 1)
        self.assertNotIn(self.KEY_LIST[0], vals)

    def test_delete_many(self):
        data = dict(zip(self.KEY_LIST, self.VALUE_LIST))

        cache.set_many(data)

        cache.delete_many(self.KEY_LIST)

    def test_has_key(self):
        cache.set(self.KEY, self.VALUE)

        res = cache.has_key(self.KEY)  # noqa
        self.assertTrue(res)

        res = cache.has_key('DOES NOT EXIST')  # noqa
        self.assertFalse(res)

    ###########################################################################
    # VERSION
    ###########################################################################
    def test_incr_version(self):
        pass

    def test_decr_version(self):
        pass
