# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_simple_expression 1'] = '''(module
    (func $output_println (import "System::Output" "println") (param i32))

    (func (export "Main")
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

snapshots['test_function_call_with_params_and_locals 1'] = '''(module
    (func $output_println (import "System::Output" "println") (param i32))

    (func $add (param $a i32) (param $b i32) (result i32)
        (local $answer i32)
        (set_local $answer
            (i32.add
                (get_local $a)
                (get_local $b)
            )
        )
        (get_local $answer)
    )

    (func (export "Main")
        (local $a i32)
        (local $b i32)
        (set_local $a
            (i32.const 2)
        )
        (set_local $b
            (i32.const 3)
        )
        (call
            $output_println
            (call
                $add
                (get_local $a)
                (get_local $b)
            )
        )
    )
)
'''
