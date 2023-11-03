# import unittest
# from datetime import datetime, timedelta
# from robit.core.clock import Clock, CREATED_DATE_FORMAT
#
#
# class TestClock(unittest.TestCase):
#
#     def test_init_default(self):
#         clock = Clock()
#         self.assertEqual(clock.utc_offset, 0)
#         self.assertAlmostEqual(clock.created_utc.timestamp(), datetime.utcnow().timestamp(), delta=1)
#
#     def test_init_with_offset(self):
#         utc_offset = 5
#         clock = Clock(utc_offset)
#         self.assertEqual(clock.utc_offset, utc_offset)
#         self.assertAlmostEqual(clock.created_utc.timestamp(), datetime.utcnow().timestamp(), delta=1)
#
#     def test_created_tz_offset(self):
#         utc_offset = 5
#         clock = Clock(utc_offset)
#         expected_created_tz = clock.created_utc + timedelta(hours=utc_offset)
#         self.assertAlmostEqual(clock.created_tz.timestamp(), expected_created_tz.timestamp(), delta=1)
#
#     def test_as_dict(self):
#         utc_offset = 3
#         clock = Clock(utc_offset)
#         as_dict = clock.as_dict()
#         self.assertIsInstance(as_dict, dict)
#         self.assertEqual(len(as_dict), 2)
#         self.assertIn('created', as_dict)
#         self.assertIn('now', as_dict)
#
#     def test_created_utc_verbose(self):
#         clock = Clock()
#         expected_created_utc_verbose = clock.created_utc.strftime(CREATED_DATE_FORMAT)
#         self.assertEqual(clock.created_utc_verbose, expected_created_utc_verbose)
#
#     def test_created_tz_verbose(self):
#         utc_offset = 2
#         clock = Clock(utc_offset)
#         expected_created_tz_verbose = clock.created_tz.strftime(CREATED_DATE_FORMAT)
#         self.assertEqual(clock.created_tz_verbose, expected_created_tz_verbose)
#
#     def test_now_tz_verbose(self):
#         utc_offset = -1
#         clock = Clock(utc_offset)
#         now_tz = datetime.utcnow() + timedelta(hours=utc_offset)
#         expected_now_tz_verbose = now_tz.strftime(CREATED_DATE_FORMAT)
#         self.assertAlmostEqual(clock.now_tz_verbose, expected_now_tz_verbose, delta=1)
#
#
# if __name__ == '__main__':
#     unittest.main()