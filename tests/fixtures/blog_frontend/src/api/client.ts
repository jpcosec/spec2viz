import createClient from "openapi-fetch";

const client = createClient({ baseUrl: "/api" });

export function publishPost(id: number) {
  return client.POST("/posts/{id}/publish", { params: { path: { id } } });
}
