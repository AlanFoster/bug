# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['test_simple_expression 1'] = '''(module
    (func $output_println (import "System::Output" "println") (param i32))
    (memory (export "memory") 1)

    (global $heap_pointer (mut i32)
        (i32.const 12)
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
                    (get_local $required_bytes)
                )
                (global.get $heap_pointer)
            )
        )
    )

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

snapshots['test_data_vector_with_complex_function 1'] = '''(module
    (func $output_println (import "System::Output" "println") (param i32))
    (memory (export "memory") 1)

    (global $heap_pointer (mut i32)
        (i32.const 12)
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
                    (get_local $required_bytes)
                )
                (global.get $heap_pointer)
            )
        )
    )

    (func $Vector.new (param $x i32) (param $y i32) (result i32)
        (global.set $self_pointer
            (call
                $malloc
                (i32.const 2)
            )
        )
        (i32.store
            (i32.add
                (global.get $self_pointer)
                (i32.const 0)
            )
            (get_local $x)
        )
        (i32.store
            (i32.add
                (global.get $self_pointer)
                (i32.const 4)
            )
            (get_local $y)
        )
        (global.get $self_pointer)
    )

    (func $Vector.add (param $self i32) (param $other i32) (result i32)
        (call
            $Vector.new
            (i32.add
                (i32.load
                    (i32.add
                        (get_local $self)
                        (i32.mul
                            (i32.const 0)
                            (i32.const 4)
                        )
                    )
                )
                (i32.load
                    (i32.add
                        (get_local $other)
                        (i32.mul
                            (i32.const 0)
                            (i32.const 4)
                        )
                    )
                )
            )
            (i32.add
                (i32.load
                    (i32.add
                        (get_local $self)
                        (i32.mul
                            (i32.const 1)
                            (i32.const 4)
                        )
                    )
                )
                (i32.load
                    (i32.add
                        (get_local $other)
                        (i32.mul
                            (i32.const 1)
                            (i32.const 4)
                        )
                    )
                )
            )
        )
    )

    (func $Vector.getX (param $self i32) (result i32)
        (i32.load
            (i32.add
                (get_local $self)
                (i32.mul
                    (i32.const 0)
                    (i32.const 4)
                )
            )
        )
    )

    (func $Vector.getY (param $self i32) (result i32)
        (i32.load
            (i32.add
                (get_local $self)
                (i32.mul
                    (i32.const 1)
                    (i32.const 4)
                )
            )
        )
    )

    (func $Main (export "Main")
        (local $vectorA i32)
        (local $vectorB i32)
        (local $vectorC i32)
        (set_local $vectorA
            (call
                $Vector.new
                (i32.const 3)
                (i32.const 6)
            )
        )
        (set_local $vectorB
            (call
                $Vector.new
                (i32.const 5)
                (i32.const 3)
            )
        )
        (set_local $vectorC
            (call
                $Vector.add
                (get_local $vectorA)
                (get_local $vectorB)
            )
        )
        (call
            $output_println
            (call
                $Vector.getX
                (get_local $vectorC)
            )
        )
        (call
            $output_println
            (call
                $Vector.getY
                (get_local $vectorC)
            )
        )
    )
)
'''
