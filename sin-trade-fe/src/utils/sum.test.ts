import { expect, test } from "vitest";
import { sum } from "./sum";

test("adds 1 + 2 to equal 3", () => {


  console.log("hello!");
  expect(sum(1, 2)).toBe(3);
});
