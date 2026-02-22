import { describe, it, expect } from "vitest";
import { StandardResponseSchema } from "../../interfaces/StandardResponse";

describe("StandardResponse Schema", () => {
  it("should parse valid standard response", () => {
    const validResponse = {
      message: "Success",
      status: 200,
      data: { some: "data" },
    };

    const result = StandardResponseSchema.parse(validResponse);
    
    expect(result.message).toBe("Success");
    expect(result.status).toBe(200);
    expect(result.data).toEqual({ some: "data" });
  });

  it("should handle null data", () => {
    const responseWithNull = {
      message: "Error",
      status: 400,
      data: null,
    };

    const result = StandardResponseSchema.parse(responseWithNull);
    
    expect(result.message).toBe("Error");
    expect(result.status).toBe(400);
    expect(result.data).toBeNull();
  });

  it("should handle numeric status", () => {
    const response = {
      message: "Created",
      status: 201,
      data: [],
    };

    const result = StandardResponseSchema.parse(response);
    
    expect(result.status).toBe(201);
  });
});
