import { loadPosts } from "./api/fetcher";

export function FetchButton() {
  const handleLoad = () => {
    loadPosts();
  };
  return <button onClick={handleLoad}>Cargar</button>;
}
