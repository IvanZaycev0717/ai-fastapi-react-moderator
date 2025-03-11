export function timeAgo(date) {
  const now = new Date();
  const diffInMs = now.getTime() - new Date(date).getTime();

  const minutes = Math.floor(diffInMs / (1000 * 60));
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);
  const weeks = Math.floor(days / 7);
  const months = Math.floor(days / 30);
  const years = Math.floor(months / 12);

  if (minutes < 1) return "Только что";
  else if (minutes === 1) return "Минуту назад";
  else if (minutes < 60) return `${minutes} мин. назад`;
  else if (hours === 1) return "Час назад";
  else if (hours < 24) return `${hours} ч. назад`;
  else if (days === 1) return "День назад";
  else if (days < 7) return `${days} дня назад`;
  else if (weeks === 1) return "Неделю назад";
  else if (months === 1) return "Месяц назад";
  else if (years === 1) return "Год назад";
  else return `${years} лет назад`;
}
