import axios from "axios";

export function archivePost() {
  return axios.delete("/posts/archive");
}
