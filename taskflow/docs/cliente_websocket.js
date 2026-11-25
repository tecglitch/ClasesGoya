// Reconecta a un proyecto y resincroniza su estado desde la API REST.
export function conectarProyecto({ url, obtenerToken, alRecibir, alReconectar }) {
  let espera = 1000;
  let socket;
  let cerradoAProposito = false;
  let temporizador;

  function reintentar() {
    if (cerradoAProposito) return;
    const demora = espera + Math.random() * 500;
    console.info(`Conexión perdida. Reintento en ${Math.round(demora)} ms`);
    temporizador = setTimeout(abrir, demora);
    espera = Math.min(espera * 2, 30000);
  }

  async function abrir() {
    if (cerradoAProposito) return;
    let token;
    try {
      token = await obtenerToken();
    } catch (error) {
      reintentar();
      return;
    }
    if (cerradoAProposito) return;
    const separador = url.includes("?") ? "&" : "?";
    socket = new WebSocket(`${url}${separador}token=${encodeURIComponent(token)}`);

    socket.onopen = () => {
      espera = 1000;
      alReconectar();
    };

    socket.onmessage = (evento) => alRecibir(JSON.parse(evento.data));

    socket.onclose = () => {
      reintentar();
    };
  }

  abrir();
  return () => {
    cerradoAProposito = true;
    clearTimeout(temporizador);
    socket?.close(1000);
  };
}
