export const SHORT_CACHE = 30000;
export const MEDIUM_CACHE = 300000;
export const LONG_CACHE = 360000;
export function shouldFetch(current: { fetching: boolean; expired_at: number; data: any; }) {
  const {fetching, expired_at, data } = current;
  const now = Date.now();
  if (fetching) {
    if(expired_at && expired_at + SHORT_CACHE < now) {
      return true;
    }
    return false;
  }
  if (!data ||
    !expired_at ||
    (Array.isArray(data) && data.length == 0) ||
    Object.keys(data).length == 0
  ) {
      return true;
  }

  return expired_at < now;
}

export function getCachedData(current: { fetching: boolean; expired_at: number; data: any; }) {
  if (!current) {
    return null;
  }
  const { data } = current;
  if (!data || (Array.isArray(data) && data.length == 0) || Object.keys(data).length === 0) {
      return null;
  }
  return data;
}

export function createCachedEntry(data: any, cachePeriod=MEDIUM_CACHE) {
  return {
    fetching: false,
    expired_at: Date.now() + cachePeriod,
    data
  };
}
  