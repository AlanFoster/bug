import Grid from "@material-ui/core/Grid";
import * as React from "react";
import { makeStyles } from "@material-ui/core";

const useStyle = makeStyles(theme => ({
    root: {
        height: "100%"
    }
}));

interface Props {
    readonly container?: boolean;
    readonly item?: boolean;
    readonly className?: string;
}

export const Panel: React.FC<Props> = function ({container, item, className, children}) {
    const classes = useStyle({});
    let props = container
        ? {
            container: container,
            className: classes.root,
            children: children
        }
        : {
            item: item,
            className: className,
            children: children
        };

    return (
        <Grid
            {...props}
            direction={container ? 'column' : undefined}
        />
    );
};
