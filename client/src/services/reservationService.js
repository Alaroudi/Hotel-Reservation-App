import http from "./httpService";

const apiEndpoint = `${process.env.REACT_APP_RESERVATION_API_URL}`;

export function saveReservation(reservation) {
  return http.post(`${apiEndpoint}/user`, reservation);
}

export function getReservations() {
  return http.get(`${apiEndpoint}/user`);
}

export function getReservation(user_id) {
  return http.get(`${apiEndpoint}/user/${user_id}`);
}
export function DeleteReservation(reservation_id) {
  return http.delete(`${apiEndpoint}/reservation/${reservation_id}`);
}
