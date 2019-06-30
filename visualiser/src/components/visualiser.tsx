import React, { useRef } from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { Box } from "@material-ui/core";
import { CodeEditor } from "./code-editor";
import { useHorizontalDrag } from "./use-horizontal-drag";
import { Memory } from "./memory";
import { Console } from "./console";
import { Resizer } from "./resizer";
import { Panel } from "./panel";

const useStyles = makeStyles(theme => ({
    root: {
        display: 'flex',
        flexGrow: 1,
        height: '100vh'
    },
    runtimePanelWrapper: {
        flex: 1
    },
    primaryPanel: {
        flex: 1
    },
}));

const CodeActions = function () {
    return (
        <React.Fragment>
            Actions - Run / Upload
        </React.Fragment>
    )
};

export const Visualiser = function () {
    const classes = useStyles({});
    const ref = useRef<Element>(null);
    const {width: codePanelWidth, setDragging} = useHorizontalDrag(
        ref
    );

    return (
        <Box className={classes.root} ref={ref}>
            <Box
                width={
                    typeof codePanelWidth !== 'undefined'
                        ? `${Math.max(codePanelWidth, 300)}px`
                        : '50%'
                }
            >
                <Panel container>
                    <Panel item className={classes.primaryPanel}>
                        <CodeEditor/>
                    </Panel>
                    <Panel item>
                        <CodeActions/>
                    </Panel>
                </Panel>
            </Box>

            <Resizer
                onMouseDown={() => setDragging(true)}
            />

            <Box className={classes.runtimePanelWrapper}>
                <Panel container>
                    <Panel item className={classes.primaryPanel}>
                        <Memory/>
                    </Panel>
                    <Panel item>
                        <Console/>
                    </Panel>
                </Panel>
            </Box>
        </Box>
    );
}
