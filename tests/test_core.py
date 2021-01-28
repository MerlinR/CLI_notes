#!/usr/bin/python3
import os
import shutil
import tempfile
import unittest

from notes.lib.definitions import Note
from notes.lib.settings import config
from notes.notes import (add_note, deep_search_for_text, delete_note,
                         get_note_list, search_note_by_name)

TEST_NAME = "Test"
TEST_MSG = "Test Message"

TEST_NAME2 = "Tast"
TEST_MSG2 = "Tast Message"


class TestStringMethods(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.mkdtemp()
        config.set("note_paths", [cls.test_dir], save=False)
        config.set("primary_note_dir", cls.test_dir, save=False)
        config.set("extension", "md", save=False)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_dir)

    def assertNote(self, orig: Note, expected: Note):
        if orig.path != expected.path:
            self.fail("{} Does not match {}".format(orig.path, expected.path))
        elif orig.name != expected.name:
            self.fail("{} Does not match {}".format(orig.name, expected.name))
        elif orig.min_path != expected.min_path:
            self.fail("{} Does not match {}".format(orig.min_path, expected.min_path))
        elif orig.id != expected.id:
            self.fail("{} Does not match {}".format(orig.id, expected.id))
        elif orig.extra_info != expected.extra_info:
            self.fail(
                "{} Does not match {}".format(orig.extra_info, expected.extra_info)
            )

    def test_add(self):
        add_note(TEST_NAME, TEST_MSG)
        add_note(TEST_NAME, no_edit=True)
        add_note(TEST_NAME2, TEST_MSG2)
        self.assertTrue(
            os.path.exists(
                os.path.join(self.test_dir, f"{TEST_NAME}.{config.get('extension')}")
            )
        )

    def test_get_note_list(self):
        expected_list = [
            Note(
                path=f"{self.test_dir}/{TEST_NAME2}.md",
            ),
            Note(
                path=f"{self.test_dir}/{TEST_NAME}.md",
            ),
        ]

        for indx, note in enumerate(get_note_list()):
            self.assertNote(note, expected_list[indx])

    def test_search_by_name(self):
        expected_note = Note(
            path=f"{self.test_dir}/{TEST_NAME}.md",
        )
        found_list = search_note_by_name(TEST_NAME)

        if len(found_list) > 1 or len(found_list) == 0:
            self.fail("Found list expected to be single: {}".format(found_list))
        self.assertNote(expected_note, found_list[0])

    def test_deep_search(self):
        expected_note = Note(
            path=f"{self.test_dir}/{TEST_NAME}.md",
        )
        expected_note.extra_info = [f"# {TEST_NAME}\n{TEST_MSG}"]

        found_list = deep_search_for_text(TEST_NAME)

        if len(found_list) > 1 or len(found_list) == 0:
            self.fail("Found list expected to be single: {}".format(found_list))
        self.assertNote(expected_note, found_list[0])

    # unit tests run after sort, therefore x ensures runs last
    def test_x_deletion(self):
        delete_note(TEST_NAME, confirm=False)
        self.assertFalse(
            os.path.exists(
                os.path.join(self.test_dir, f"{TEST_NAME}.{config.get('extension')}")
            )
        )

    # unit tests run after sort, therefore x ensures runs last
    def test_x_deletion_fail(self):
        delete_note(TEST_NAME2, confirm=False)
        delete_note(TEST_NAME2, confirm=False)


if __name__ == "__main__":
    unittest.main()
