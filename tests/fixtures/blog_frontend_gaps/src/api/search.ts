import axios from "axios";

export function searchPosts(term: string) {
  return axios.get(`/posts?q=${term}`);
}
