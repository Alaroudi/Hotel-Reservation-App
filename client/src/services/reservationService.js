import http from "./httpService";

const apiEndpoint = `${process.env.REACT_APP_RESERVATION_API_URL}`;

export function saveUserReservation(reservation) {
  return http.post(`${apiEndpoint}/user`, reservation);
}

export function getUsersReservations() {
  return http.get(`${apiEndpoint}/user`);
}

export function getUserReservations(user_id) {
  return http.get(`${apiEndpoint}/user/${user_id}`);
}
export function DeleteReservation(reservation_id) {
  return http.delete(`${apiEndpoint}/reservation/${reservation_id}`);
}
export function getReservation(reservation_id) {
  return http.get(`${apiEndpoint}/reservation/${reservation_id}`);
}
export function updateReservation(reservation_id, reservation) {
  return http.put(`${apiEndpoint}/reservation/${reservation_id}`, reservation);
}
