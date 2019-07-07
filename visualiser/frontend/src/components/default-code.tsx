export const defaultCode = `(module
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
`;
