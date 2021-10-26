import http from "./httpService";

const apiEndpoint = `${process.env.REACT_APP_USER_API_URL}/users`;

export function register(user) {
  return http.post(apiEndpoint, {
    ...user
  });
}
