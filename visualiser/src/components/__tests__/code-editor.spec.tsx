import * as React from "react";
import renderer from "react-test-renderer"
import { CodeEditor } from '../code-editor';
import { defaultCode } from "../default-code";

describe("CodeEditor", function () {
    it("renders successfully", function () {
        const tree = renderer.create(<CodeEditor code={defaultCode} onValueChange={() => { /* noop */ }} />);

        expect(tree).toMatchSnapshot();
    });
});
