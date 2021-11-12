import {
  differenceInCalendarDays,
  eachWeekendOfInterval,
  format,
  subDays
} from "date-fns";

export function formatDate(date) {
  return format(date, "yyyy-MM-dd");
}

export function totalNights(startDate, endDate) {
  return differenceInCalendarDays(startDate, endDate);
}

export function totalWeekends(startDate, endDate) {
  return eachWeekendOfInterval({
    start: startDate,
    end: subDays(endDate, 1)
  }).length;
}
export function totalPrice(
  standardPrice,
  queenPrice,
  kingPrice,
  totalNights,
  weekends,
  weekendRate,
  standardCount,
  queenCount,
  kingCount
) {
  const nights = totalNights - weekends;
  const weekendPrecent = weekendRate + 1;

  return parseFloat(
    standardCount *
      (nights * standardPrice + weekends * standardPrice * weekendPrecent) +
      queenCount *
        (nights * queenPrice + weekends * queenPrice * weekendPrecent) +
      kingCount * (nights * kingPrice + weekends * kingPrice * weekendPrecent)
  );
}
