// REACT_APP_Reservation_API_URL
import http from "./httpService";

const apiEndpoint = `${process.env.REACT_APP_RESERVATION_API_URL}`;

export function saveReservation(reservation) {
  return http.post(`${apiEndpoint}/user`, reservation);
}
