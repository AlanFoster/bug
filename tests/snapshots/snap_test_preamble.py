# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_preamble 1'] = '''(module
    (memory (export "memory") 1)

    (global $heap_pointer (mut i32)
        (i32.const 10)
    )

    (global $self_pointer (mut i32)
        (i32.const 0)
    )

    (func $malloc (param $required_bytes i32) (result i32)
        (global.get $heap_pointer)
        (global.set $heap_pointer
            (i32.add
                (i32.mul
                    (i32.const 4)
                    (global.get $heap_pointer)
                )
                (get_local $required_bytes)
            )
        )
    )
)
'''
