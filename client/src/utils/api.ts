export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE";

interface ApiOptions<TBody = unknown> {
  method?: HttpMethod;
  headers?: Record<string, string>;
  body?: TBody;
  signal?: AbortSignal;
}

const BASE_URL = process.env.REACT_APP_API_BASE_URL ?? "/api";

async function request<TResponse, TBody = unknown>(
  path: string,
  opts: ApiOptions<TBody> = {}
): Promise<TResponse> {
  const { method = "GET", headers = {}, body, signal } = opts;
  const isJson =
    body && typeof body === "object" && !(body instanceof FormData);

  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers: {
      ...(isJson ? { "Content-Type": "application/json" } : {}),
      ...headers,
    },
    body: isJson ? JSON.stringify(body) : (body as BodyInit | null | undefined),
    credentials: "include",
    signal,
  });

  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(text || `Request failed: ${res.status}`);
  }
  const ct = res.headers.get("content-type") || "";
  if (ct.includes("application/json")) return (await res.json()) as TResponse;
  return (await res.text()) as unknown as TResponse;
}

export const API = {
  get: <T>(path: string, signal?: AbortSignal) =>
    request<T>(path, { method: "GET", signal }),
  post: <T, B = unknown>(path: string, body?: B, signal?: AbortSignal) =>
    request<T, B>(path, { method: "POST", body, signal }),
  put: <T, B = unknown>(path: string, body?: B, signal?: AbortSignal) =>
    request<T, B>(path, { method: "PUT", body, signal }),
  patch: <T, B = unknown>(path: string, body?: B, signal?: AbortSignal) =>
    request<T, B>(path, { method: "PATCH", body, signal }),
  del: <T>(path: string, signal?: AbortSignal) =>
    request<T>(path, { method: "DELETE", signal }),
};
