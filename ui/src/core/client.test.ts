import { createHttpClient, SaveConflictError, SldbHttpError } from "./client";

const json = (status: number, body: unknown) => new Response(JSON.stringify(body), { status });

describe("createHttpClient (copiado de sldb)", () => {
  it("pide /graph bajo la base y devuelve los documentos", async () => {
    const f = vi.fn().mockResolvedValue(json(200, { documents: [{ id: "A" }] }));
    const c = createHttpClient("/sldb/", f);
    expect(await c.documents()).toEqual([{ id: "A" }]);
    expect(f).toHaveBeenCalledWith("/sldb/graph", undefined);
  });

  it("mapea 409 a SaveConflictError y otros errores a SldbHttpError", async () => {
    const c1 = createHttpClient("/sldb", vi.fn().mockResolvedValue(json(409, { error: "x" })));
    await expect(c1.lint()).rejects.toBeInstanceOf(SaveConflictError);
    const c2 = createHttpClient("/sldb", vi.fn().mockResolvedValue(json(500, { error: "y" })));
    await expect(c2.lint()).rejects.toBeInstanceOf(SldbHttpError);
  });
});
