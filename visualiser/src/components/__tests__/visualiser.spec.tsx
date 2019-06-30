import * as React from "react";
import renderer from "react-test-renderer"
import { Visualiser } from "../visualiser";

describe("Index", function () {
    it("renders successfully", function () {
        const tree = renderer.create(<Visualiser/>);

        expect(tree).toMatchSnapshot();
    });
});
