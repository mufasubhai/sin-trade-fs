import { z } from "zod";

export interface StandardResponse {
  message: string;
  status: number;
  data: unknown;
}

export const StandardResponseSchema = z.object({
  message: z.string(),
  status: z.number(),
  data: z.unknown().nullable(),
});
