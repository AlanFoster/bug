import * as React from "react";
import renderer from "react-test-renderer"
import { Memory } from '../memory';

describe("Memory", function () {
    it("renders successfully when there is no memory", function () {
        const tree = renderer.create(<Memory memory={new ArrayBuffer(0)}/>);

        expect(tree).toMatchSnapshot();
    });

    it("renders successfully when there is memory", function () {
        const tree = renderer.create(<Memory memory={new Uint8Array([1, 2, 3, 4, 4, 3, 2, 1]).buffer} />);

        expect(tree).toMatchSnapshot();
    });
});
