import React from "react";
import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs/components/prism-core';
import 'prismjs/components/prism-wasm';
import { makeStyles } from "@material-ui/core";

const useStyles = makeStyles({
    '@global': {
        '.npm__react-simple-code-editor__textarea': {
            outline: 0
        },
        '.token.comment, .token.prolog, .token.doctype, .token.cdata': {
            color: '#90a4ae'
        },
        '.token.punctuation': {
            color: '#9e9e9e'
        },
        '.namespace': {
            opacity: 0.7
        },
        '.token.property, .token.tag, .token.boolean, .token.number, .token.constant, .token.symbol, .token.deleted': {
            color: '#e91e63'
        },
        '.token.selector, .token.attr-name, .token.string, .token.char, .token.builtin, .token.inserted': {
            color: '#4caf50',
        },
        '.token.operator, .token.entity, .token.url, .language-css .token.string, .style .token.string': {
            color: '#795548'
        },
        '.token.atrule, .token.attr-value, .token.keyword': {
            color: '#3f51b5'
        },
        '.token.function': {
            color: '#f44336'
        },
        '.token.regex, .token.important, .token.variable': {
            color: '#ff9800'
        },
        '.token.important, .token.bold': {
            fontWeight: 'bold'
        },
        '.token.italic': {
            fontStyle: 'italic'
        },
        '.token.entity': {
            cursor: 'help'
        }
    }
});

interface Props {
    readonly code: string;
    readonly onValueChange: (code: string) => void;
}

export const CodeEditor: React.FC<Props> = function ({ code, onValueChange }) {
    useStyles({});
    return (
        <Editor
            value={code}
            onValueChange={onValueChange}
            highlight={code => highlight(code, languages.wasm)}
            style={{
                fontFamily: '"Fira code", "Fira Mono", monospace',
            }}
        />
    )
};
