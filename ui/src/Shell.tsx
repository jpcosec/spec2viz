import { useState } from "react";

export const TABS = ["Grafo", "Anclajes", "Composiciones"] as const;
export type Tab = (typeof TABS)[number];
export type Lens = "lectura" | "fierros";

/** Cascarón: explorador, pestañas, panel de documento y lentes. El contenido llega en U2-U9. */
export function Shell() {
  const [tab, setTab] = useState<Tab>("Grafo");
  const [lens, setLens] = useState<Lens>("lectura");
  const [selected] = useState<string | null>(null);

  return (
    <div className={`shell${lens === "fierros" ? " fierros" : ""}`} data-lens={lens}>
      <header>
        <strong>specIR</strong>
        <div role="tablist" aria-label="Vistas">
          {TABS.map((t) => (
            <button key={t} role="tab" id={`tab-${t}`} aria-selected={tab === t} aria-controls="vista" onClick={() => setTab(t)}>
              {t}
            </button>
          ))}
        </div>
        <div role="group" aria-label="Lente">
          <button aria-pressed={lens === "lectura"} onClick={() => setLens("lectura")}>Lectura</button>
          <button aria-pressed={lens === "fierros"} onClick={() => setLens("fierros")}>Fierros</button>
        </div>
      </header>
      <aside aria-label="Explorador">
        <p className="empty">Sin nodos todavía.</p>
      </aside>
      <main role="tabpanel" id="vista" aria-labelledby={`tab-${tab}`}>
        <h2>{tab}</h2>
        <p className="empty">Sin contenido todavía.</p>
      </main>
      <aside aria-label="Documento">
        {selected === null ? <p className="empty">Elige un nodo para ver su documento.</p> : null}
      </aside>
    </div>
  );
}
