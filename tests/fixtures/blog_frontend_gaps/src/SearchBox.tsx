import { searchPosts } from "./api/search";

export function SearchBox({ term }: { term: string }) {
  const handleSearch = () => {
    searchPosts(term);
  };
  return <button onClick={handleSearch}>Buscar</button>;
}
