import * as React from "react";
import renderer from "react-test-renderer"
import { Console } from '../console';

describe("Console", function () {
    it("renders successfully", function () {
        const tree = renderer.create(<Console/>);

        expect(tree).toMatchSnapshot();
    });
});
