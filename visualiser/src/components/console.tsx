import * as React from "react";

interface Props {
    readonly logs: string[];
}

export const Console: React.FC<Props> = function ({logs}) {
    return (
        <div>
            <div>Console ({logs.length} logs)</div>
            <pre>
                {logs.map(function (log, index) {
                    return <div key={index}>{log}</div>
                })}
            </pre>
        </div>
    )
};
