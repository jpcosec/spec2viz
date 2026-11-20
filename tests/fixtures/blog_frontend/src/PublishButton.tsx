import { publishPost } from "./api/client";
import { publishLegacy } from "./api/legacy";

export function PublishButton({ id }: { id: number }) {
  const handlePublish = () => {
    publishPost(id);
    publishLegacy();
  };
  return <button onClick={handlePublish}>Publicar</button>;
}
