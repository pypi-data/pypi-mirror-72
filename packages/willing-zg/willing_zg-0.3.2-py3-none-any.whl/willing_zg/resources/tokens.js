import axios from 'axios';

const TOKEN_REFRESH_INTERVAL = 4 * 60 * 1000; // 4 min in ms

export const PORTUNUS_URL = process.env.NEXT_PUBLIC_PORTUNUS_URL || 'https://dev.portunus.willing.com';

const defaultFetch = () =>
  axios({ method: 'post', url: `${PORTUNUS_URL}/api/auth/token/refresh/`, withCredentials: true });

const loginUrl = `${PORTUNUS_URL}/login`;

export const withReturn = url => {
  if (typeof window === 'undefined') {
    // server side rendering, so we don't know where to return to
    return url;
  }
  const params = new URLSearchParams();
  params.append('next', window.location.href);
  return `${url}?${params.toString()}`;
};

const defaultOnError = () => {
  window.location.replace(withReturn(loginUrl));
};

class TokenFetcher {
  constructor() {
    this.fetchFunction = defaultFetch;
    this.onError = defaultOnError;
    this.onSuccess = () => null;
    this.currentToken = '';
    this.timerId = null;
    this.tokenCallbacks = [];
  }

  get accessToken() {
    return new Promise(resolve => {
      if (this.currentToken) {
        resolve(this.currentToken);
      } else {
        this.tokenCallbacks.push(resolve);
      }
    });
  }

  fetchToken = async () => {
    try {
      const response = await this.fetchFunction();
      this.currentToken = response.data.access;
      this.onSuccess(this.currentToken);
      this.clearCallbacks();
      return true;
    } catch (error) {
      if (error.response) {
        if (error.response.status === 401) {
          this.clearToken();
        }
      }
      this.onError(error);
    }
    return false;
  };

  clearToken() {
    this.currentToken = '';
    clearInterval(this.timerId);
    this.timerId = null;
    this.clearCallbacks();
  }

  clearCallbacks() {
    this.tokenCallbacks.forEach(cb => cb(this.currentToken));
    this.tokenCallbacks = [];
  }

  start(fetchFn, onSuccess, onError) {
    this.fetchFunction = fetchFn || this.fetchFunction;
    this.onSuccess = onSuccess || this.onSuccess;
    this.onError = onError || this.onError;
    if (!this.timerId) {
      this.timerId = setInterval(this.fetchToken, TOKEN_REFRESH_INTERVAL);
      this.fetchToken();
    }
  }
}

const tokenFetcher = new TokenFetcher();

export default tokenFetcher;
