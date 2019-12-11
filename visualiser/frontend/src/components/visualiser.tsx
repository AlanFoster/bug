import React, { useRef, useState, useEffect } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Box, Button, Paper } from "@material-ui/core";
import { CodeEditor } from "./code-editor";
import { useHorizontalDrag } from "./use-horizontal-drag";
import { Memory } from "./memory";
import { Console } from "./console";
import { Resizer } from "./resizer";
import { defaultCode } from './default-code';
import clsx from "clsx";
import * as webassembly from "./webassembly";


const headingSizes = {
    height: 50,
};

const useStyles = makeStyles(theme => ({
    root: {

    },
    heading: {
        ...headingSizes,
        borderBottom: '1px solid rgba(0,0,0,0.2)',
        boxShadow: theme.shadows[1],
        padding: theme.spacing(1, 2),
    },
    content: {
        padding: theme.spacing(2),
        display: 'flex',
        height: `calc(100vh - ${headingSizes.height}px)`
    },
    panel: {
        display: 'flex',
        flexDirection: 'column'
    },
    secondaryPanel: {
        flex: 1
    },
    primaryChild: {
        flex: 1,
        overflow: 'scroll'
    },
    paper: {
        height: '100%',
        padding: theme.spacing(2)
    }
}));

const clamp = function (x: number, lowest: number, highest: number) {
    return Math.min(Math.max(lowest, x), highest);
};

const executeWebAssemblyText = async function (webAssemblyText: string) {
    const wasmBytes = await webassembly.compileText(webAssemblyText);

    let logs = [];
    var importObject = {
        "System::Output": {
            println: function (value) {
                logs = logs.concat(value);
            }
        }
    };

    const {instance} = await WebAssembly.instantiate(wasmBytes, importObject);
    instance.exports.Main();
    return {
        logs,
        memory: (
            instance.exports.memory
                ? instance.exports.memory.buffer
                : new Int8Array()
        )
    };
};

export const Visualiser = function () {
    const classes = useStyles({});
    const ref = useRef<Element>(null);
    const [code, setCode] = useState(defaultCode);
    const [executionResult, setExecutionResult] = useState({logs: [], memory: null});
    const {width: codePanelWidth, setDragging} = useHorizontalDrag(
        ref
    );

    const executeCode = async () => {
        try {
            const executionResult = await executeWebAssemblyText(code);
            setExecutionResult(executionResult);
        } catch (e) {
            setExecutionResult({ logs: [`Failure: ${e.stack}`], memory: null })
            console.error(e);
        }
    };

    useEffect(() => {
        executeCode();
    }, [])

    return (
        <Box className={classes.root} ref={ref}>
            <Box className={classes.heading}>
                <Button
                    color="primary"
                    variant="outlined"
                    onClick={executeCode}
                >
                    Run File
                </Button>
            </Box>

            <Box className={classes.content}>
                <Box
                    className={classes.panel}
                    width={
                        typeof codePanelWidth !== 'undefined'
                            ? `${clamp(codePanelWidth, 300, 1000)}px`
                            : '50%'
                    }
                >
                    <Paper className={clsx([classes.primaryChild, classes.paper])}>
                        <CodeEditor code={code} onValueChange={setCode}/>
                    </Paper>
                </Box>

                <Resizer
                    onMouseDown={() => setDragging(true)}
                />

                <Box
                    className={clsx([classes.panel, classes.secondaryPanel])}
                >
                    <Paper className={clsx([classes.primaryChild, classes.paper])}>
                        <Memory memory={executionResult.memory}/>
                    </Paper>
                    <Box>
                        <Paper className={classes.paper}>
                            <Console logs={executionResult.logs}/>
                        </Paper>
                    </Box>
                </Box>
            </Box>
        </Box>
    );
}
