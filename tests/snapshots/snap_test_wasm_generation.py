# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_simple_expression 1'] = '''(module
    (func
        $output_println
        (import "System::Output" "println")
        (param i32)
    )

    (func
        (export "Main")
        (call
            $output_println
            (i32.add
                (i32.const 1)
                (i32.mul
                    (i32.const 2)
                    (i32.const 3)
                )
            )
        )
    )

)
'''
