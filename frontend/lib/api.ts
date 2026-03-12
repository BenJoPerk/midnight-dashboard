const API_BASE = "/api/v1";

async function apiFetch(
  path: string,
  options: RequestInit = {}
) {
  const res = await fetch(`${API_BASE}${path}`, {
    credentials: "include", // REQUIRED for HttpOnly cookies
    headers: {
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!res.ok) {
    if (res.status === 401) {
      window.location.href = "/login";
      return;
    }
    throw new Error("API error");
  }

  return res.json();
}

export async function getHealth() {
  return apiFetch("/health");
}


export async function register(email: string, password: string) {
  const res = await fetch("/api/v1/auth/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("Registration failed");
  }

  return res.json();
}



export async function login(email: string, password: string) {
  const formData = new URLSearchParams();
  formData.append("username", email);
  formData.append("password", password);

  const res = await fetch("/api/v1/auth/login", {
    method: "POST",
    body: formData,
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("Login failed");
  }

  return res.json();
}

export async function logout() {
  const res = await fetch("/api/v1/auth/logout", {
    method: "POST",
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("Logout failed");
  }

  return res.json();
}

export async function getCurrentUser() {
  const res = await fetch("/api/v1/auth/me", {
    credentials: "include",
  });

  if (!res.ok) {
    throw new Error("Not authenticated");
  }

  return res.json();
}



