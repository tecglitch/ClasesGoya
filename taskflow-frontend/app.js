import { conectarProyecto } from "./websocket.js";

const API_URL = "http://127.0.0.1:8000/api";
const WS_URL = "ws://127.0.0.1:8000/ws/projects";
let cerrarWebSocket = null;
let paginaActual = `${API_URL}/tasks/`;

const elemento = (id) => document.getElementById(id);

function mostrarAplicacion(autenticada) {
  elemento("login-box").style.display = autenticada ? "none" : "block";
  elemento("app-box").style.display = autenticada ? "block" : "none";
}

function mensajeError(payload, fallback) {
  if (payload?.detail) return String(payload.detail);
  if (payload && typeof payload === "object") return JSON.stringify(payload);
  return fallback;
}

async function jsonOrEmpty(response) {
  try { return await response.json(); } catch { return {}; }
}

async function renovarAccessToken() {
  const refresh = sessionStorage.getItem("refreshToken");
  if (!refresh) throw new Error("La sesión venció. Ingresá de nuevo.");
  const response = await fetch(`${API_URL}/token/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh }),
  });
  const data = await jsonOrEmpty(response);
  if (!response.ok || !data.access) throw new Error("La sesión venció. Ingresá de nuevo.");
  sessionStorage.setItem("accessToken", data.access);
  if (data.refresh) sessionStorage.setItem("refreshToken", data.refresh);
  return data.access;
}

async function accessTokenVigente() {
  try { return await renovarAccessToken(); }
  catch (error) {
    if (!sessionStorage.getItem("accessToken")) throw error;
    return sessionStorage.getItem("accessToken");
  }
}

async function apiFetch(url, options = {}) {
  const access = sessionStorage.getItem("accessToken");
  const headers = { ...options.headers, Authorization: `Bearer ${access}` };
  let response = await fetch(url, { ...options, headers });
  if (response.status === 401 && sessionStorage.getItem("refreshToken")) {
    try {
      const fresh = await renovarAccessToken();
      response = await fetch(url, {
        ...options,
        headers: { ...options.headers, Authorization: `Bearer ${fresh}` },
      });
    } catch {
      cerrarSesion("La sesión venció. Ingresá de nuevo.");
    }
  }
  return response;
}

async function login(event) {
  event.preventDefault();
  elemento("login-error").textContent = "";
  try {
    const response = await fetch(`${API_URL}/token/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: elemento("username").value.trim(),
        password: elemento("password").value,
      }),
    });
    const data = await jsonOrEmpty(response);
    if (!response.ok) {
      elemento("login-error").textContent = response.status === 429
        ? "Demasiados intentos. Esperá un minuto."
        : "Usuario o contraseña incorrectos.";
      return;
    }
    sessionStorage.setItem("accessToken", data.access);
    sessionStorage.setItem("refreshToken", data.refresh);
    mostrarAplicacion(true);
    await loadProjects();
    await loadTasks();
  } catch {
    elemento("login-error").textContent = "No se pudo conectar con TaskFlow.";
  }
}

async function loadProjects() {
  const response = await apiFetch(`${API_URL}/projects/`);
  const data = await jsonOrEmpty(response);
  if (!response.ok) {
    elemento("app-error").textContent = mensajeError(data, "No se pudieron cargar los proyectos.");
    return;
  }
  const select = elemento("project");
  select.replaceChildren();
  for (const project of data.results ?? []) {
    const option = document.createElement("option");
    option.value = project.id;
    option.textContent = project.name;
    select.appendChild(option);
  }
  if (!select.options.length) {
    elemento("app-error").textContent = "Todavía no pertenecés a ningún proyecto.";
    actualizarWebSocket();
    return;
  }
  actualizarWebSocket();
}

async function loadTasks(url = paginaActual) {
  paginaActual = url;
  const response = await apiFetch(url);
  const data = await jsonOrEmpty(response);
  if (!response.ok) {
    elemento("app-error").textContent = mensajeError(data, "No se pudieron cargar las tareas.");
    return;
  }
  const list = elemento("tasks");
  list.replaceChildren();
  for (const task of data.results ?? []) {
    const item = document.createElement("li");
    item.textContent = `${task.title} — ${task.status}`;
    list.appendChild(item);
  }
  elemento("previous-button").disabled = !data.previous;
  elemento("next-button").disabled = !data.next;
  elemento("previous-button").dataset.url = data.previous ?? "";
  elemento("next-button").dataset.url = data.next ?? "";
  elemento("app-error").textContent = "";
}

async function createTask() {
  const title = elemento("new-title").value.trim();
  const project = elemento("project").value;
  const errorBox = elemento("app-error");
  errorBox.textContent = "";
  if (!title || !project) {
    errorBox.textContent = "Elegí un proyecto y escribí un título.";
    return;
  }
  const response = await apiFetch(`${API_URL}/tasks/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, project: Number(project) }),
  });
  const data = await jsonOrEmpty(response);
  if (!response.ok) {
    errorBox.textContent = mensajeError(data, "No se pudo crear la tarea.");
    return;
  }
  elemento("new-title").value = "";
  await loadTasks(`${API_URL}/tasks/`);
}

function actualizarWebSocket() {
  cerrarWebSocket?.();
  cerrarWebSocket = null;
  const projectId = elemento("project").value;
  if (!projectId || !sessionStorage.getItem("refreshToken")) {
    elemento("presence").textContent = "WebSocket desconectado";
    return;
  }
  elemento("presence").textContent = "Conectando en tiempo real…";
  cerrarWebSocket = conectarProyecto({
    url: `${WS_URL}/${projectId}/`,
    obtenerToken: accessTokenVigente,
    alRecibir: (message) => {
      if (message.status) elemento("presence").textContent = `${message.user}: ${message.status}`;
      if (message.event?.startsWith("task_")) {
        elemento("presence").textContent = `Actualización en vivo: ${message.event}`;
        loadTasks(paginaActual);
      }
    },
    alReconectar: () => loadTasks(paginaActual),
  });
}

function cerrarSesion(mensaje = "") {
  cerrarWebSocket?.();
  cerrarWebSocket = null;
  sessionStorage.removeItem("accessToken");
  sessionStorage.removeItem("refreshToken");
  mostrarAplicacion(false);
  elemento("presence").textContent = "WebSocket desconectado";
  if (mensaje) elemento("login-error").textContent = mensaje;
}

elemento("login-form").addEventListener("submit", login);
elemento("create-button").addEventListener("click", createTask);
elemento("logout-button").addEventListener("click", () => cerrarSesion());
elemento("project").addEventListener("change", actualizarWebSocket);
elemento("previous-button").addEventListener("click", () => loadTasks(elemento("previous-button").dataset.url));
elemento("next-button").addEventListener("click", () => loadTasks(elemento("next-button").dataset.url));

async function cargarSesionGuardada() {
  if (!sessionStorage.getItem("accessToken")) return;
  mostrarAplicacion(true);
  try {
    await loadProjects();
    await loadTasks();
  } catch {
    cerrarSesion("No se pudo restaurar la sesión.");
  }
}

cargarSesionGuardada();
