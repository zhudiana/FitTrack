const API_BASE_URL = "http://127.0.0.1:8000";

export async function loginUser(username: string, password: string) {
  const formData = new FormData();
  formData.append("username", username);
  formData.append("password", password);

  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Login failed");
  }
  return response.json();
}

export function saveToken(token: string) {
  localStorage.setItem("access_token", token);
}

export function getToken() {
  return localStorage.getItem("access_token");
}
