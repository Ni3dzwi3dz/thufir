import { get, writable, type Writable } from 'svelte/store';

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000';
const TOKEN_STORAGE_KEY = 'thufir.auth.token';
const USER_STORAGE_KEY = 'thufir.auth.user';

export interface User {
  id: number;
  email: string;
  username: string;
  created_at: string;
}

export interface AuthState {
  isAuthenticated: boolean;
  user: User | null;
  token: string | null;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface AuthResult {
  success: boolean;
  data?: AuthResponse;
  error?: string;
}

export interface RegisterInput {
  email: string;
  username: string;
  password: string;
}

const emptyAuthState: AuthState = {
  isAuthenticated: false,
  user: null,
  token: null
};

export const auth: Writable<AuthState> = writable(emptyAuthState);

function isBrowser(): boolean {
  return typeof window !== 'undefined' && typeof window.localStorage !== 'undefined';
}

function buildApiUrl(path: string): string {
  return `${API_URL}${path.startsWith('/') ? path : `/${path}`}`;
}

function persistAuthState(state: AuthState): void {
  if (!isBrowser()) {
    return;
  }

  if (state.token && state.user) {
    window.localStorage.setItem(TOKEN_STORAGE_KEY, state.token);
    window.localStorage.setItem(USER_STORAGE_KEY, JSON.stringify(state.user));
    return;
  }

  window.localStorage.removeItem(TOKEN_STORAGE_KEY);
  window.localStorage.removeItem(USER_STORAGE_KEY);
}

function applyAuthResponse(data: AuthResponse): AuthResponse {
  const nextState: AuthState = {
    isAuthenticated: true,
    token: data.access_token,
    user: data.user
  };

  auth.set(nextState);
  persistAuthState(nextState);
  return data;
}

function clearAuthState(): void {
  auth.set(emptyAuthState);
  persistAuthState(emptyAuthState);
}

function loadStoredAuth(): void {
  if (!isBrowser()) {
    return;
  }

  const token = window.localStorage.getItem(TOKEN_STORAGE_KEY);
  const user = window.localStorage.getItem(USER_STORAGE_KEY);

  if (!token || !user) {
    return;
  }

  try {
    auth.set({
      isAuthenticated: true,
      token,
      user: JSON.parse(user) as User
    });
  } catch (error) {
    console.error('Failed to restore auth state', error);
    clearAuthState();
  }
}

loadStoredAuth();

async function parseError(response: Response): Promise<string> {
  try {
    const errorData = (await response.json()) as { detail?: string };
    return errorData.detail ?? 'Request failed';
  } catch {
    return 'Request failed';
  }
}

async function sendAuthRequest<T extends object>(
  endpoint: string,
  payload: T
): Promise<AuthResult> {
  try {
    const response = await fetch(buildApiUrl(endpoint), {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      return { success: false, error: await parseError(response) };
    }

    const data = (await response.json()) as AuthResponse;
    return { success: true, data: applyAuthResponse(data) };
  } catch (error) {
    return {
      success: false,
      error: error instanceof Error ? error.message : 'An unknown error occurred'
    };
  }
}

export async function register(input: RegisterInput): Promise<AuthResult> {
  return sendAuthRequest('/auth/register', input);
}

export async function login(username: string, password: string): Promise<AuthResult> {
  return sendAuthRequest('/auth/login', { username, password });
}

export async function logout(): Promise<void> {
  const currentAuth = get(auth);

  if (currentAuth.token) {
    try {
      await protectedFetch('/auth/logout', { method: 'POST' });
    } catch {
      // Ignore logout request failures and clear client state regardless.
    }
  }

  clearAuthState();
}

export function getCurrentAuth(): AuthState {
  return get(auth);
}

export async function protectedFetch(path: string, options: RequestInit = {}): Promise<Response> {
  const { token } = getCurrentAuth();

  if (!token) {
    throw new Error('No authentication token found');
  }

  const headers = new Headers(options.headers);
  headers.set('Authorization', `Bearer ${token}`);

  const response = await fetch(buildApiUrl(path), {
    ...options,
    headers
  });

  if (response.status === 401) {
    clearAuthState();
    throw new Error('Unauthorized');
  }

  return response;
}

export async function fetchCurrentUser(): Promise<User> {
  const response = await protectedFetch('/users/me');

  if (!response.ok) {
    throw new Error(await parseError(response));
  }

  const user = (await response.json()) as User;
  auth.update((state) => {
    const nextState = {
      ...state,
      isAuthenticated: true,
      user
    };
    persistAuthState(nextState);
    return nextState;
  });
  return user;
}

export function isAuthenticated(): boolean {
  return getCurrentAuth().isAuthenticated;
}

export function getCurrentUser(): User | null {
  return getCurrentAuth().user;
}

export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
