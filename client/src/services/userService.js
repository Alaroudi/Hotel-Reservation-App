import http from "./httpService";

const apiEndpoint = `${process.env.REACT_APP_USER_API_URL}/users`;

export function register(user) {
  return http.post(apiEndpoint, {
    ...user
  });
}

export function editUser(user_id, user) {
  return http.put(`${apiEndpoint}/${user_id}`, { ...user });
}
export function getUser(user_id) {
  return http.get(`${apiEndpoint}/${user_id}`);
}
