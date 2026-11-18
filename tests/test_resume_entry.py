"""Offline request and input checks; no model service is contacted."""

import json
import unittest

from career_ai.resume_entry_generator import generate_resume_entry


class FakeResponses:
    def __init__(self):
        self.calls = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        response = type('FakeResponse', (), {})()
        response.output_parsed = {
            'title': 'Invented title', 'role': 'Invented role',
            'organization': 'Invented employer', 'period': 'Invented dates',
            'bullet_points': ['Built a small prototype.', 'Added an offline test.', 'Documented the workflow.'],
        }
        return response


class FakeClient:
    def __init__(self):
        self.responses = FakeResponses()


class ResumeEntryTests(unittest.TestCase):
    def test_requires_source_activity_and_work_summary(self):
        fake = FakeClient()
        with self.assertRaises(ValueError):
            generate_resume_entry(activity='', role='', organization='', work_summary='work', start_date='', end_date='', client=fake)
        with self.assertRaises(ValueError):
            generate_resume_entry(activity='project', role='', organization='', work_summary='  ', start_date='', end_date='', client=fake)
        self.assertEqual(fake.responses.calls, [])

    def test_structured_request_and_source_metadata_are_preserved(self):
        fake = FakeClient()
        result = generate_resume_entry(activity='Sample project', role='Developer', organization='',
                                       work_summary='Built a prototype', start_date='2025', end_date='', client=fake)
        self.assertEqual(result['title'], 'Sample project')
        self.assertEqual(result['role'], 'Developer')
        self.assertEqual(result['organization'], '')
        self.assertEqual(result['period'], '2025')
        self.assertEqual(len(result['bullet_points']), 3)
        self.assertEqual(len(fake.responses.calls), 1)
        call = fake.responses.calls[0]
        self.assertIs(call['store'], False)
        self.assertEqual(call['text']['format']['type'], 'json_schema')
        self.assertIn('bullet_points', call['text']['format']['schema']['required'])
        self.assertIn('Built a prototype', call['input'])

    def test_json_output_is_supported_and_blank_dates_remain_blank(self):
        fake = FakeClient()
        def output(**kwargs):
            fake.responses.calls.append(kwargs)
            return type('FakeResponse', (), {'output_parsed': None, 'output_text': json.dumps({'bullet_points': ['One', 'Two', 'Three']})})()
        fake.responses.create = output
        result = generate_resume_entry(activity='Project', role='', organization='', work_summary='Made a tool',
                                       start_date='', end_date='', client=fake)
        self.assertEqual(result['period'], '')
        self.assertEqual(result['role'], '')
        self.assertEqual(result['organization'], '')

    def test_bad_model_output_is_rejected(self):
        fake = FakeClient()
        fake.responses.create = lambda **kwargs: type(
            'FakeResponse', (), {'output_parsed': {'bullet_points': ['Only one']}}
        )()
        with self.assertRaises(ValueError):
            generate_resume_entry(activity='Project', role='', organization='', work_summary='Made a tool',
                                  start_date='', end_date='', client=fake)


if __name__ == '__main__':
    unittest.main()
