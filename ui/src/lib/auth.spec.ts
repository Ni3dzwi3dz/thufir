import { beforeEach, describe, expect, it, vi } from 'vitest';

import { get } from 'svelte/store';

import {
	auth,
	fetchCurrentUser,
	login,
	logout,
	protectedFetch,
	register
} from './auth';

const user = {
	id: 1,
	email: 'user@example.com',
	username: 'reader1',
	created_at: '2026-03-28T10:00:00Z'
};

describe('auth store', () => {
	beforeEach(() => {
		auth.set({ isAuthenticated: false, token: null, user: null });
		vi.unstubAllGlobals();
	});

	it('stores auth state after successful login', async () => {
		vi.stubGlobal(
			'fetch',
			vi.fn().mockResolvedValue(
				new Response(
					JSON.stringify({
						access_token: 'token-123',
						token_type: 'bearer',
						user
					}),
					{ status: 200, headers: { 'Content-Type': 'application/json' } }
				)
			)
		);

		const result = await login('reader1', 'supersecret');

		expect(result.success).toBe(true);
		expect(get(auth)).toEqual({
			isAuthenticated: true,
			token: 'token-123',
			user
		});
	});

	it('returns backend validation errors for registration failures', async () => {
		vi.stubGlobal(
			'fetch',
			vi.fn().mockResolvedValue(
				new Response(JSON.stringify({ detail: 'Email is already registered' }), {
					status: 409,
					headers: { 'Content-Type': 'application/json' }
				})
			)
		);

		const result = await register({
			email: 'user@example.com',
			username: 'reader1',
			password: 'supersecret'
		});

		expect(result).toEqual({ success: false, error: 'Email is already registered' });
		expect(get(auth).isAuthenticated).toBe(false);
	});

	it('adds the bearer token to protected requests', async () => {
		auth.set({ isAuthenticated: true, token: 'abc123', user });
		const fetchMock = vi.fn().mockResolvedValue(new Response(null, { status: 200 }));
		vi.stubGlobal('fetch', fetchMock);

		await protectedFetch('/users/me');

		expect(fetchMock).toHaveBeenCalledWith(
			'http://localhost:8000/users/me',
			expect.objectContaining({
				headers: expect.any(Headers)
			})
		);
		const headers = fetchMock.mock.calls[0][1]?.headers as Headers;
		expect(headers.get('Authorization')).toBe('Bearer abc123');
	});

	it('loads the current user profile and refreshes the store', async () => {
		auth.set({ isAuthenticated: true, token: 'abc123', user: null });
		vi.stubGlobal(
			'fetch',
			vi.fn().mockResolvedValue(
				new Response(JSON.stringify(user), {
					status: 200,
					headers: { 'Content-Type': 'application/json' }
				})
			)
		);

		const profile = await fetchCurrentUser();

		expect(profile).toEqual(user);
		expect(get(auth).user).toEqual(user);
	});

	it('clears auth state on logout even if the API call fails', async () => {
		auth.set({ isAuthenticated: true, token: 'abc123', user });
		vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('network error')));

		await logout();

		expect(get(auth)).toEqual({ isAuthenticated: false, token: null, user: null });
	});
});