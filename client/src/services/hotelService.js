import http from "./httpService";

const apiEndpoint = `${process.env.REACT_APP_HOTEL_API_URL}/hotels`;

export function getHotels() {
  return http.get(apiEndpoint);
}

export function getHotelAvailability(check_in, check_out, city) {
  return http.get(
    `${apiEndpoint}/availability?city=${city}&check_in=${check_in}&check_out=${check_out}`
  );
}

export function getHotel(hotel_id) {
  return http.get(`${apiEndpoint}/${hotel_id}`);
}

export function deleteHotel(hotel_id) {
  return http.delete(`${apiEndpoint}/${hotel_id}`);
}

export function saveHotel(hotel) {
  if (hotel.hotel_id) {
    return http.put(`${apiEndpoint}/${hotel.hotel_id}`, hotel);
  }

  return http.post(apiEndpoint, hotel);
}
