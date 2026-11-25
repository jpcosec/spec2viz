import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Shell } from "./Shell";

describe("Shell", () => {
  it("renderiza las tres pestañas por rol y nombre", () => {
    render(<Shell />);
    for (const n of ["Grafo", "Anclajes", "Composiciones"]) expect(screen.getByRole("tab", { name: n })).toBeInTheDocument();
    expect(screen.getByRole("tab", { name: "Grafo" })).toHaveAttribute("aria-selected", "true");
  });

  it("cambiar de pestaña cambia el panel", async () => {
    render(<Shell />);
    expect(screen.getByRole("tabpanel")).toHaveTextContent("Grafo");
    await userEvent.click(screen.getByRole("tab", { name: "Anclajes" }));
    expect(screen.getByRole("tabpanel")).toHaveTextContent("Anclajes");
    expect(screen.getByRole("tabpanel")).toHaveTextContent("Sin contenido todavía");
  });

  it("las lentes conmutan", async () => {
    render(<Shell />);
    const lectura = screen.getByRole("button", { name: "Lectura" });
    const fierros = screen.getByRole("button", { name: "Fierros" });
    expect(lectura).toHaveAttribute("aria-pressed", "true");
    await userEvent.click(fierros);
    expect(fierros).toHaveAttribute("aria-pressed", "true");
    expect(lectura).toHaveAttribute("aria-pressed", "false");
  });

  it("el panel de documento está vacío hasta elegir un nodo", () => {
    render(<Shell />);
    expect(screen.getByRole("complementary", { name: "Documento" })).toHaveTextContent("Elige un nodo");
  });
});
