import * as React from "react";
import renderer from "react-test-renderer"
import { CodeEditor } from '../code-editor';

describe("CodeEditor", function () {
    it("renders successfully", function () {
        const tree = renderer.create(<CodeEditor/>);

        expect(tree).toMatchSnapshot();
    });
});
