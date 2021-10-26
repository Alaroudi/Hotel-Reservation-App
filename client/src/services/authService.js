import jwtDecode from "jwt-decode";
import http from "./httpService";

const apiEndpoint = process.env.REACT_APP_USER_API_URL + "/auth";
const tokenKey = "token";

http.setJwt(getJwt());

export async function login(email, password) {
  const { headers } = await http.post(apiEndpoint, { email, password });
  localStorage.setItem(tokenKey, headers["x-auth-token"]);
}

export function loginWithJwt(jwt) {
  localStorage.setItem(tokenKey, jwt);
}

export function logout() {
  localStorage.removeItem(tokenKey);
}

export function getCurrentUser() {
  try {
    const jwt = localStorage.getItem(tokenKey);
    return jwtDecode(jwt);
  } catch (ex) {
    return null;
  }
}

export function getJwt() {
  return localStorage.getItem(tokenKey);
}

const auth = {
  login,
  loginWithJwt,
  logout,
  getCurrentUser,
  getJwt
};

export default auth;
