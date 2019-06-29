import React, { useRef } from 'react';
import {makeStyles} from '@material-ui/core/styles';
import {Box} from "@material-ui/core";
import {CodeEditor} from "../src/components/code-editor";
import {useHorizontalDrag} from "../src/components/use-horizontal-drag";
import {Memory} from "../src/components/memory";
import {Console} from "../src/components/console";
import {Resizer} from "../src/components/resizer";
import {Panel} from "../src/components/panel";

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
            Actions
        </React.Fragment>
    )
};

export default function Visualiser() {
    const classes = useStyles();
    const ref = useRef<Element>(null);
    const { width: codePanelWidth, setDragging } = useHorizontalDrag(
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
