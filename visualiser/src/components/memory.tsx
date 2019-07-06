import * as React from "react";
import { makeStyles } from "@material-ui/core";

const useStyles = makeStyles(theme => ({
    root: {
    },
    memoryDump: {
    }
}));

type Props = {
    readonly memory: ArrayBuffer;
}

export const Memory: React.FC<Props> = function ({ memory }) {
    const classes = useStyles({});
    const int8Buffer = new Int8Array(memory);
    const memoryWidth = int8Buffer.length.toString().length;
    let memoryDump = "";
    for (let i = 0; i < int8Buffer.length; i += 4) {
        memoryDump += i.toString().padStart(memoryWidth, '0') + ' | ';
        memoryDump += [int8Buffer[i], int8Buffer[i + 1], int8Buffer[i + 2], int8Buffer[i + 3]].join(' ');
        memoryDump += "\n";
    }

    return (
        <div className={classes.root}>
            <div>Memory</div>
            <pre className={classes.memoryDump}>{memoryDump}</pre>
        </div>
    )
}
