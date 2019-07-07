import * as React from "react";
import renderer from "react-test-renderer"
import { Resizer } from '../resizer';

describe("Resizer", function () {
    it("renders successfully", function () {
        const tree = renderer.create(<Resizer onMouseDown={() => { /* noop */ }} />);

        expect(tree).toMatchSnapshot();
    });
});
