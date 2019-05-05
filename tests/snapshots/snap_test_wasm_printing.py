# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_simple_expression 1'] = '''(module
    (func $output_println (import "System::Output" "println") (param i32))

    (func $Main (export "Main")
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

    (func $Main (export "Main")
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

snapshots['test_conditionals 1'] = '''(module
    (func $output_println (import "System::Output" "println") (param i32))

    (func $Foo (result i32)
        (if
            (i32.lt_s
                (i32.const 9)
                (i32.const 10)
            )
            (then
                (call
                    $output_println
                    (i32.const 1)
                )
            )
        )
        (if
            (result i32)
            (i32.gt_s
                (i32.const 9)
                (i32.const 10)
            )
            (then
                (i32.const 1)
            )
            (else
                (i32.const 0)
            )
        )
    )

    (func $Main (export "Main")
        (call
            $Foo
        )
        (drop)
    )
)
'''

snapshots['test_returns 1'] = '''(module
    (func $output_println (import "System::Output" "println") (param i32))

    (func $meaning_of_life (result i32)
        (return
            (i32.const 42)
        )
    )

    (func $output_meaning_of_life
        (call
            $meaning_of_life
        )
        (return
            (nop)
        )
    )

    (func $Main (export "Main")
        (call
            $output_meaning_of_life
        )
    )
)
'''