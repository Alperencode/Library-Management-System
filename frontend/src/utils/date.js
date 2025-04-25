export function formatDate(iso) {
    if (!iso) return "Unknown";
    const date = new Date(iso);
    return date.toLocaleString(undefined, {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }


export function formatDateWithoutTime(iso) {
    if (!iso) return "Unknown";
    const date = new Date(iso);
    return date.toLocaleDateString(undefined, {
      year: "numeric",
      month: "long",
      day: "numeric"
    });
  }