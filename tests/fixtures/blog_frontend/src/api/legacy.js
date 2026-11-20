import axios from "axios";

export function publishLegacy() {
  return axios.post("/posts/{id}/publish");
}
