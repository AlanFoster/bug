import subprocess
import tempfile


class WatToWasmException(Exception):
    pass


def wat_to_wasm(wat: str) -> bytes:
    with tempfile.NamedTemporaryFile(delete=True) as tmp_wat_file:
        with tempfile.NamedTemporaryFile(delete=True) as tmp_wasm_file:
            tmp_wat_file.write(bytes(wat, encoding="utf8"))
            tmp_wat_file.flush()
            try:
                # TODO: wabt can be called with ffi instead
                subprocess.run(
                    ["wat2wasm", tmp_wat_file.name, "--output", tmp_wasm_file.name],
                    check=True,
                    capture_output=True,
                    universal_newlines=True,
                )

                return tmp_wasm_file.file.read()
            except subprocess.CalledProcessError as e:
                raise WatToWasmException(e.stderr)
