# Bug

Work in progress language that is most likely filled with bugs.

## Notes

## Resources

- [Understanding the wasm text format](https://developer.mozilla.org/en-US/docs/WebAssembly/Understanding_the_text_format)

### Generate parser

```bash
docker-compose build
docker-compose run --rm service /bin/sh /usr/local/bin/antlr4 BugParser.g4 BugLexer.g4 -Dlanguage=Python3 -visitor -o parser
```

Unfortunately the generated method names are camel case, rather than snake case - as shown within the python3 codegen
templates
[here](https://github.com/antlr/antlr4/blob/837aa60e2c4736e242432c2ac93ed2de3b9eff3b/tool/resources/org/antlr/v4/tool/templates/codegen/Python3/Python3.stg#L104)

### Run tests

```bash
docker-compose build
docker-compose run --rm test
```
