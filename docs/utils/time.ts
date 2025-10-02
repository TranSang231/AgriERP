import moment from "moment/moment";

export const FORMAT = {
  DATE: "YYYY-MM-DD",
  TIME: "HH:mm:ss",
  TIME_MINUTE: "HH:mm",
  DATE_TIME: "YYYY-MM-DD HH:mm:ss",
};

export function formatDate(value: any, format: string | null = null) {
  if (!value) {
    return null;
  }
  if (format) {
    return moment(String(value)).format(format);
  }
  return moment(String(value)).format(FORMAT.DATE);
}

export function formatDateTime(value: any, format: string | null = null) {
  if (!value) {
    return null;
  }
  if (format) {
    return moment(moment.utc(value)).format(format);
  }
  return moment(moment.utc(value)).format(FORMAT.DATE_TIME);
}

export function utcToLocalDate(value: any, format: string | null = null) {
  if (!value) {
    return null;
  }
  if (format) {
    return moment(moment.utc(value)).local().format(format);
  }
  return moment(moment.utc(value)).local().format(FORMAT.DATE);
}


export function utcToLocalDateTime(value: any, format: string | null = null) {
  if (!value) {
    return null;
  }
  if (format) {
    return moment(moment.utc(value)).local().format(format);
  }
  return moment(moment.utc(value)).local().format(FORMAT.DATE_TIME);
}

export function utcToLocalTime(value: any, format: string | null = null) {
  if (!value) {
    return null;
  }
  if (format) {
    return moment(moment.utc(value)).local().format(format);
  }
  return moment(moment.utc(value)).local().format(FORMAT.TIME);
}

export function localToUtcTime(value: any, format: string | null = null) {
  if (!value) {
    return null;
  }
  if (format) {
    return moment(value).utc().format(format);
  }
  return moment(value).utc().format(FORMAT.TIME);
}

export function countSessionDays(start, end, workSessions = []) {
  const day = start.getDay();
  const year = start.getFullYear();
  const month = start.getMonth();
  const date =  start.getDate();
  let hours = 0;
  const todaySessions = workSessions.filter((o) => (o.work_day +1)%6 === day);
  todaySessions.forEach ((s) => {
    const sessionStart = moment(s.start_time, FORMAT.TIME).toDate();
    sessionStart.setFullYear(year, month, date);
    const sessionEnd =moment(s.end_time, FORMAT.TIME).toDate();
    sessionEnd.setFullYear(year ,month, date);
    // console.log("start", start, "end", end, "sessionStart", sessionStart, "sessionEnd", sessionEnd);
    if ((sessionStart >= start && sessionStart <= end) || (sessionEnd >= start && sessionEnd <= end)) {
      hours += 0.5;
    }
  });
  console.log(hours)
  return hours;
 };

 export function countWorkDays(start, end, workSessions = []) {
  let loop = new Date(start);
  let hours = 0;

  while (loop <= end) {
    const isStartDate = loop.toDateString() === start.toDateString();
    const isEndDate = loop.toDateString() === end.toDateString();

    const loopStart = new Date(loop);
    loopStart.setHours(isStartDate ? start.getHours() : 0, isStartDate ? start.getMinutes() : 0);

    const loopEnd = new Date(loop);
    loopEnd.setHours(isEndDate ? end.getHours() : 23, isEndDate ? end.getMinutes() : 59);

    hours += countSessionDays(loopStart, loopEnd, workSessions);

    loop.setDate(loop.getDate() + 1);
  }

  return hours;
}