import { createHttpClient } from "./core/client";

/** Base de `sldb serve`: VITE_SLDB_URL, por defecto el proxy /sldb de vite (ver vite.config.ts). */
export const SLDB_URL: string = (import.meta.env.VITE_SLDB_URL as string | undefined) ?? "/sldb";

export const sldb = createHttpClient(SLDB_URL);
