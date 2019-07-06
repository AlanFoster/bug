import * as React from "react";
import renderer from "react-test-renderer"
import { Console } from '../console';

describe("Console", function () {
    it("renders successfully with no logs", function () {
        const tree = renderer.create(<Console logs={[]}/>);

        expect(tree).toMatchSnapshot();
    });

    it("renders successfully with no logs present", function () {
        const tree = renderer.create(<Console logs={["hello world\n"]}/>);

        expect(tree).toMatchSnapshot();
    });
});
