import { archivePost } from "./api/legacy_archive";

export function ArchiveButton() {
  const handleArchive = () => {
    archivePost();
  };
  return <button onClick={handleArchive}>Archivar</button>;
}
