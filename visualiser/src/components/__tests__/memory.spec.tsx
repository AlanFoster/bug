import * as React from "react";
import renderer from "react-test-renderer"
import { Memory } from '../memory';

describe("Memory", function () {
    it("renders successfully", function () {
        const tree = renderer.create(<Memory/>);

        expect(tree).toMatchSnapshot();
    });
});
