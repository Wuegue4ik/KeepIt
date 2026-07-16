import { defineConfig } from '@hey-api/openapi-ts';
import path from 'path';
import dotenv from 'dotenv';
import { z } from 'zod';

dotenv.config({ path: path.resolve(__dirname, '../.env') });

const envSchema = z.object({
  OPENAPI_URL: z
    .string({
      error: "OPENAPI_URL must be a string!"
    })
    .min(1, "OPENAPI_URL cannot be empty!")
    .url({
      error: "OPENAPI_URL must be a valid URL!"
    })
});

const parseResult = envSchema.safeParse(process.env);
if (!parseResult.success) {
  console.error(
    'Environment variable validation error in .env:',
    JSON.stringify(parseResult.error.format(), null, 2)
  );

  process.exit(1);
}

const env = parseResult.data;

export default defineConfig({
  input: env.OPENAPI_URL,
  output: 'src/api/types',
  plugins: [],
})