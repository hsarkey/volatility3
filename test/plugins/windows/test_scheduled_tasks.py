import sys
import struct
import traceback
import unittest

sys.path.insert(0, "../../volatility3")
from volatility3.plugins.windows import scheduled_tasks


class TestActionsDecoding(unittest.TestCase):
    def test_decode_exe_action(self):
        # fmt: off
        buf = struct.pack(
            "512B",
            *[
                0x03, 0x00, 0x16, 0x00, 0x00, 0x00, 0x4c, 0x00,
                0x6f, 0x00, 0x63, 0x00, 0x61, 0x00, 0x6c, 0x00,
                0x53, 0x00, 0x79, 0x00, 0x73, 0x00, 0x74, 0x00,
                0x65, 0x00, 0x6d, 0x00, 0x66, 0x66, 0x00, 0x00,
                0x00, 0x00, 0x6e, 0x00, 0x00, 0x00, 0x25, 0x00,
                0x77, 0x00, 0x69, 0x00, 0x6e, 0x00, 0x64, 0x00,
                0x69, 0x00, 0x72, 0x00, 0x25, 0x00, 0x5c, 0x00,
                0x73, 0x00, 0x79, 0x00, 0x73, 0x00, 0x74, 0x00,
                0x65, 0x00, 0x6d, 0x00, 0x33, 0x00, 0x32, 0x00,
                0x5c, 0x00, 0x57, 0x00, 0x69, 0x00, 0x6e, 0x00,
                0x64, 0x00, 0x6f, 0x00, 0x77, 0x00, 0x73, 0x00,
                0x50, 0x00, 0x6f, 0x00, 0x77, 0x00, 0x65, 0x00,
                0x72, 0x00, 0x53, 0x00, 0x68, 0x00, 0x65, 0x00,
                0x6c, 0x00, 0x6c, 0x00, 0x5c, 0x00, 0x76, 0x00,
                0x31, 0x00, 0x2e, 0x00, 0x30, 0x00, 0x5c, 0x00,
                0x70, 0x00, 0x6f, 0x00, 0x77, 0x00, 0x65, 0x00,
                0x72, 0x00, 0x73, 0x00, 0x68, 0x00, 0x65, 0x00,
                0x6c, 0x00, 0x6c, 0x00, 0x2e, 0x00, 0x65, 0x00,
                0x78, 0x00, 0x65, 0x00, 0x62, 0x01, 0x00, 0x00,
                0x2d, 0x00, 0x45, 0x00, 0x78, 0x00, 0x65, 0x00,
                0x63, 0x00, 0x75, 0x00, 0x74, 0x00, 0x69, 0x00,
                0x6f, 0x00, 0x6e, 0x00, 0x50, 0x00, 0x6f, 0x00,
                0x6c, 0x00, 0x69, 0x00, 0x63, 0x00, 0x79, 0x00,
                0x20, 0x00, 0x55, 0x00, 0x6e, 0x00, 0x72, 0x00,
                0x65, 0x00, 0x73, 0x00, 0x74, 0x00, 0x72, 0x00,
                0x69, 0x00, 0x63, 0x00, 0x74, 0x00, 0x65, 0x00,
                0x64, 0x00, 0x20, 0x00, 0x2d, 0x00, 0x4e, 0x00,
                0x6f, 0x00, 0x6e, 0x00, 0x49, 0x00, 0x6e, 0x00,
                0x74, 0x00, 0x65, 0x00, 0x72, 0x00, 0x61, 0x00,
                0x63, 0x00, 0x74, 0x00, 0x69, 0x00, 0x76, 0x00,
                0x65, 0x00, 0x20, 0x00, 0x2d, 0x00, 0x4e, 0x00,
                0x6f, 0x00, 0x50, 0x00, 0x72, 0x00, 0x6f, 0x00,
                0x66, 0x00, 0x69, 0x00, 0x6c, 0x00, 0x65, 0x00,
                0x20, 0x00, 0x2d, 0x00, 0x57, 0x00, 0x69, 0x00,
                0x6e, 0x00, 0x64, 0x00, 0x6f, 0x00, 0x77, 0x00,
                0x53, 0x00, 0x74, 0x00, 0x79, 0x00, 0x6c, 0x00,
                0x65, 0x00, 0x20, 0x00, 0x48, 0x00, 0x69, 0x00,
                0x64, 0x00, 0x64, 0x00, 0x65, 0x00, 0x6e, 0x00,
                0x20, 0x00, 0x22, 0x00, 0x26, 0x00, 0x20, 0x00,
                0x25, 0x00, 0x77, 0x00, 0x69, 0x00, 0x6e, 0x00,
                0x64, 0x00, 0x69, 0x00, 0x72, 0x00, 0x25, 0x00,
                0x5c, 0x00, 0x73, 0x00, 0x79, 0x00, 0x73, 0x00,
                0x74, 0x00, 0x65, 0x00, 0x6d, 0x00, 0x33, 0x00,
                0x32, 0x00, 0x5c, 0x00, 0x57, 0x00, 0x69, 0x00,
                0x6e, 0x00, 0x64, 0x00, 0x6f, 0x00, 0x77, 0x00,
                0x73, 0x00, 0x50, 0x00, 0x6f, 0x00, 0x77, 0x00,
                0x65, 0x00, 0x72, 0x00, 0x53, 0x00, 0x68, 0x00,
                0x65, 0x00, 0x6c, 0x00, 0x6c, 0x00, 0x5c, 0x00,
                0x76, 0x00, 0x31, 0x00, 0x2e, 0x00, 0x30, 0x00,
                0x5c, 0x00, 0x4d, 0x00, 0x6f, 0x00, 0x64, 0x00,
                0x75, 0x00, 0x6c, 0x00, 0x65, 0x00, 0x73, 0x00,
                0x5c, 0x00, 0x53, 0x00, 0x6d, 0x00, 0x62, 0x00,
                0x53, 0x00, 0x68, 0x00, 0x61, 0x00, 0x72, 0x00,
                0x65, 0x00, 0x5c, 0x00, 0x44, 0x00, 0x69, 0x00,
                0x73, 0x00, 0x61, 0x00, 0x62, 0x00, 0x6c, 0x00,
                0x65, 0x00, 0x55, 0x00, 0x6e, 0x00, 0x75, 0x00,
                0x73, 0x00, 0x65, 0x00, 0x64, 0x00, 0x53, 0x00,
                0x6d, 0x00, 0x62, 0x00, 0x31, 0x00, 0x2e, 0x00,
                0x70, 0x00, 0x73, 0x00, 0x31, 0x00, 0x20, 0x00,
                0x2d, 0x00, 0x53, 0x00, 0x63, 0x00, 0x65, 0x00,
                0x6e, 0x00, 0x61, 0x00, 0x72, 0x00, 0x69, 0x00,
                0x6f, 0x00, 0x20, 0x00, 0x43, 0x00, 0x6c, 0x00,
                0x69, 0x00, 0x65, 0x00, 0x6e, 0x00, 0x74, 0x00,
                0x22, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
            ]
        )

        try:
            actions = scheduled_tasks.ActionSet.decode(buf).actions  # type: ignore
            self.assertEqual(len(actions), 1)
            self.assertEqual(actions[0].action_type, scheduled_tasks.ActionType.Exe)
        except Exception:
            self.fail(
                f"ActionDecoder.decode should not raise exception:\n{traceback.format_exc()}"
            )


class TestTriggersDecoding(unittest.TestCase):
    def test_decode_all_triggers(self):
        """
        Tests decoding a set of all triggers that can be constructed via the
        Task Scheduler GUI interface. Ensures that the correct number of bytes
        is being consumed for each trigger structure.
        """
        buf = struct.pack(
            "1808B",
            # fmt: off
            *[
                0x17, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0xda, 0xaf, 0x8d, 0x09, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0xda, 0xaf, 0x8d, 0x09, 0x00, 0x00, 0x00,
                0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                0x38, 0x21, 0x41, 0x42, 0x48, 0x48, 0x48, 0x48,
                0xa0, 0x12, 0xa0, 0xa4, 0x48, 0x48, 0x48, 0x48,
                0x0e, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x41, 0x00, 0x75, 0x00, 0x74, 0x00, 0x68, 0x00,
                0x6f, 0x00, 0x72, 0x00, 0x00, 0x00, 0x48, 0x48,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x00, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48,
                0x00, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48,
                0x01, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x1c, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x01, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05,
                0x15, 0x00, 0x00, 0x00, 0x69, 0xce, 0x28, 0x2a,
                0xce, 0xd8, 0x1f, 0x77, 0x37, 0x9c, 0xe2, 0x44,
                0xf4, 0x01, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x40, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x44, 0x00, 0x45, 0x00, 0x53, 0x00, 0x4b, 0x00,
                0x54, 0x00, 0x4f, 0x00, 0x50, 0x00, 0x2d, 0x00,
                0x45, 0x00, 0x33, 0x00, 0x38, 0x00, 0x38, 0x00,
                0x44, 0x00, 0x38, 0x00, 0x50, 0x00, 0x5c, 0x00,
                0x41, 0x00, 0x64, 0x00, 0x6d, 0x00, 0x69, 0x00,
                0x6e, 0x00, 0x69, 0x00, 0x73, 0x00, 0x74, 0x00,
                0x72, 0x00, 0x61, 0x00, 0x74, 0x00, 0x6f, 0x00,
                0x72, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x2c, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff,
                0x80, 0xf4, 0x03, 0x00, 0xff, 0xff, 0xff, 0xff,
                0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0xdd, 0xdd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x01, 0x07, 0x0a, 0x00, 0x00, 0x00, 0x09, 0x00,
                0x80, 0x48, 0x11, 0xf8, 0x36, 0x1a, 0xdb, 0x01,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0xff, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x01, 0x2e, 0xe2, 0x01, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0xc2, 0x31, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0xaa, 0xaa, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0xda, 0xaf, 0x8d, 0x09, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0xda, 0xaf, 0x8d, 0x09, 0x00, 0x00, 0x00,
                0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00,
                0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x01, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48,
                0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0xda, 0xaf, 0x8d, 0x09, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0xda, 0xaf, 0x8d, 0x09, 0x00, 0x00, 0x00,
                0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0xee, 0xee, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0xda, 0xaf, 0x8d, 0x09, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0xda, 0xaf, 0x8d, 0x09, 0x00, 0x00, 0x00,
                0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0xcc, 0xcc, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x01, 0x00, 0x65, 0x00, 0x78, 0x00, 0x65, 0x00,
                0x22, 0x00, 0x20, 0x00, 0x53, 0x00, 0x74, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x84, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x3c, 0x00, 0x51, 0x00, 0x75, 0x00, 0x65, 0x00,
                0x72, 0x00, 0x79, 0x00, 0x4c, 0x00, 0x69, 0x00,
                0x73, 0x00, 0x74, 0x00, 0x3e, 0x00, 0x3c, 0x00,
                0x51, 0x00, 0x75, 0x00, 0x65, 0x00, 0x72, 0x00,
                0x79, 0x00, 0x20, 0x00, 0x49, 0x00, 0x64, 0x00,
                0x3d, 0x00, 0x22, 0x00, 0x30, 0x00, 0x22, 0x00,
                0x20, 0x00, 0x50, 0x00, 0x61, 0x00, 0x74, 0x00,
                0x68, 0x00, 0x3d, 0x00, 0x22, 0x00, 0x49, 0x00,
                0x6e, 0x00, 0x74, 0x00, 0x65, 0x00, 0x72, 0x00,
                0x6e, 0x00, 0x65, 0x00, 0x74, 0x00, 0x20, 0x00,
                0x45, 0x00, 0x78, 0x00, 0x70, 0x00, 0x6c, 0x00,
                0x6f, 0x00, 0x72, 0x00, 0x65, 0x00, 0x72, 0x00,
                0x22, 0x00, 0x3e, 0x00, 0x3c, 0x00, 0x53, 0x00,
                0x65, 0x00, 0x6c, 0x00, 0x65, 0x00, 0x63, 0x00,
                0x74, 0x00, 0x20, 0x00, 0x50, 0x00, 0x61, 0x00,
                0x74, 0x00, 0x68, 0x00, 0x3d, 0x00, 0x22, 0x00,
                0x49, 0x00, 0x6e, 0x00, 0x74, 0x00, 0x65, 0x00,
                0x72, 0x00, 0x6e, 0x00, 0x65, 0x00, 0x74, 0x00,
                0x20, 0x00, 0x45, 0x00, 0x78, 0x00, 0x70, 0x00,
                0x6c, 0x00, 0x6f, 0x00, 0x72, 0x00, 0x65, 0x00,
                0x72, 0x00, 0x22, 0x00, 0x3e, 0x00, 0x2a, 0x00,
                0x5b, 0x00, 0x53, 0x00, 0x79, 0x00, 0x73, 0x00,
                0x74, 0x00, 0x65, 0x00, 0x6d, 0x00, 0x5b, 0x00,
                0x45, 0x00, 0x76, 0x00, 0x65, 0x00, 0x6e, 0x00,
                0x74, 0x00, 0x49, 0x00, 0x44, 0x00, 0x3d, 0x00,
                0x32, 0x00, 0x5d, 0x00, 0x5d, 0x00, 0x3c, 0x00,
                0x2f, 0x00, 0x53, 0x00, 0x65, 0x00, 0x6c, 0x00,
                0x65, 0x00, 0x63, 0x00, 0x74, 0x00, 0x3e, 0x00,
                0x3c, 0x00, 0x2f, 0x00, 0x51, 0x00, 0x75, 0x00,
                0x65, 0x00, 0x72, 0x00, 0x79, 0x00, 0x3e, 0x00,
                0x3c, 0x00, 0x2f, 0x00, 0x51, 0x00, 0x75, 0x00,
                0x65, 0x00, 0x72, 0x00, 0x79, 0x00, 0x4c, 0x00,
                0x69, 0x00, 0x73, 0x00, 0x74, 0x00, 0x3e, 0x00,
                0x00, 0x00, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x88, 0x88, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x77, 0x77, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00,
                0x01, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x01, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48,
                0x77, 0x77, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00,
                0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x04, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48,
                0x00, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48,
                0x01, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x1c, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x01, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05,
                0x15, 0x00, 0x00, 0x00, 0x69, 0xce, 0x28, 0x2a,
                0xce, 0xd8, 0x1f, 0x77, 0x37, 0x9c, 0xe2, 0x44,
                0xf4, 0x01, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x40, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x44, 0x00, 0x45, 0x00, 0x53, 0x00, 0x4b, 0x00,
                0x54, 0x00, 0x4f, 0x00, 0x50, 0x00, 0x2d, 0x00,
                0x45, 0x00, 0x33, 0x00, 0x38, 0x00, 0x38, 0x00,
                0x44, 0x00, 0x38, 0x00, 0x50, 0x00, 0x5c, 0x00,
                0x41, 0x00, 0x64, 0x00, 0x6d, 0x00, 0x69, 0x00,
                0x6e, 0x00, 0x69, 0x00, 0x73, 0x00, 0x74, 0x00,
                0x72, 0x00, 0x61, 0x00, 0x74, 0x00, 0x6f, 0x00,
                0x72, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x77, 0x77, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00,
                0x01, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x01, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48,
                0x77, 0x77, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0xff, 0xff, 0xff, 0xff,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0x00, 0x00,
                0x01, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x08, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48,
                0x00, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48,
                0x01, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x1c, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x01, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05,
                0x15, 0x00, 0x00, 0x00, 0x69, 0xce, 0x28, 0x2a,
                0xce, 0xd8, 0x1f, 0x77, 0x37, 0x9c, 0xe2, 0x44,
                0xf4, 0x01, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x40, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x44, 0x00, 0x45, 0x00, 0x53, 0x00, 0x4b, 0x00,
                0x54, 0x00, 0x4f, 0x00, 0x50, 0x00, 0x2d, 0x00,
                0x45, 0x00, 0x33, 0x00, 0x38, 0x00, 0x38, 0x00,
                0x44, 0x00, 0x38, 0x00, 0x50, 0x00, 0x5c, 0x00,
                0x41, 0x00, 0x64, 0x00, 0x6d, 0x00, 0x69, 0x00,
                0x6e, 0x00, 0x69, 0x00, 0x73, 0x00, 0x74, 0x00,
                0x72, 0x00, 0x61, 0x00, 0x74, 0x00, 0x6f, 0x00,
                0x72, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
            ]
            # fmt: on
        )
        triggers = scheduled_tasks.TriggerSet.decode(buf)
        self.assertIsNotNone(triggers)

    def test_decode_triggers(self):
        # fmt: off
        buf = struct.pack(
            "320B",
            *[
                0x17, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0xB9, 0x61, 0x1A, 0xA8, 0xB9, 0x61, 0x1A,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0xB9, 0x61, 0x1A, 0xA8, 0xB9, 0x61, 0x1A,
                0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                0x08, 0xA1, 0x40, 0x42, 0x48, 0x48, 0x48, 0x48,
                0x7A, 0x7F, 0x59, 0xDC, 0x48, 0x48, 0x48, 0x48,
                0x22, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x49, 0x00, 0x6E, 0x00, 0x74, 0x00, 0x65, 0x00,
                0x72, 0x00, 0x61, 0x00, 0x63, 0x00, 0x74, 0x00,
                0x69, 0x00, 0x76, 0x00, 0x65, 0x00, 0x55, 0x00,
                0x73, 0x00, 0x65, 0x00, 0x72, 0x00, 0x73, 0x00,
                0x00, 0x00, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x00, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48,
                0x00, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48,
                0x05, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x0C, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05,
                0x04, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x2C, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x00, 0x00, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF,
                0x80, 0x51, 0x01, 0x00, 0xFF, 0xFF, 0xFF, 0xFF,
                0x07, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0xAA, 0xAA, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0xB9, 0x61, 0x1A, 0xA8, 0xB9, 0x61, 0x1A,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0xB9, 0x61, 0x1A, 0xA8, 0xB9, 0x61, 0x1A,
                0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
                0x2C, 0x01, 0x00, 0x00, 0xFF, 0xFF, 0xFF, 0xFF,
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x00, 0xC1, 0xD9, 0x04,
                0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
                0x00, 0x00, 0x00, 0x00, 0x48, 0x48, 0x48, 0x48,
                0x01, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48, 0x48,
            ]
        )
        # fmt: on
        triggers = scheduled_tasks.TriggerSet.decode(buf)
        self.assertIsNotNone(triggers)
        if not triggers:
            return
        self.assertGreater(len(triggers.triggers), 0)