import { format } from "date-fns";

export default function formatDate(date) {
  return format(date, "yyyy-MM-dd");
}
