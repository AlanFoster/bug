import * as React from "react";
import { makeStyles } from '@material-ui/core/styles';
import { Box } from "@material-ui/core";

const useStyles = makeStyles(theme => ({
    root: {
        cursor: 'col-resize',
        padding: '0 10px',
        userSelect: 'none'
    },
    handle: {
        width: 2,
        height: '100%'
    }
}));

interface Props {
    readonly onMouseDown: React.MouseEventHandler;
}

export const Resizer: React.FC<Props> = function ({onMouseDown}) {
    const classes = useStyles();

    return (
        <Box
            className={classes.root}
            onMouseDown={onMouseDown}
        >
            <Box className={classes.handle}/>
        </Box>
    )
};

