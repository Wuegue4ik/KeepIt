import { z } from 'zod';

const envSchema = z.object({
  VITE_API_URL: z
    .string({
      error: "VITE_API_URL must be a string!"
    })
    .min(1, "VITE_API_URL cannot be empty!")
    .url({
      error: "VITE_API_URL must be a valid URL!"
    })
});

const parseResult = envSchema.safeParse(import.meta.env);

if (!parseResult.success) {
  console.error(
    'Environment variable validation error in .env:', 
    JSON.stringify(parseResult.error.format(), null, 2)
  );

  throw new Error('Environment variable validation error in .env');
}

export const env = parseResult.data;