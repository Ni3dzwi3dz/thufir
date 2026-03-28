import { page } from 'vitest/browser';
import { beforeEach, describe, expect, it } from 'vitest';
import { render } from 'vitest-browser-svelte';

import { auth } from '$lib/auth';

import Navbar from './Navbar.svelte';

describe('Navbar', () => {
	beforeEach(() => {
		auth.set({ isAuthenticated: false, token: null, user: null });
	});

	it('shows login and register actions for guests', async () => {
		render(Navbar);

		await expect.element(page.getByRole('link', { name: 'Login' })).toBeInTheDocument();
		await expect.element(page.getByRole('link', { name: 'Register' })).toBeInTheDocument();
	});

	it('shows profile and logout actions for authenticated users', async () => {
		auth.set({
			isAuthenticated: true,
			token: 'token-123',
			user: {
				id: 1,
				email: 'user@example.com',
				username: 'reader1',
				created_at: '2026-03-28T10:00:00Z'
			}
		});

		render(Navbar);

		await expect.element(page.getByRole('link', { name: 'Profile' })).toBeInTheDocument();
		await expect.element(page.getByRole('button', { name: 'Logout' })).toBeInTheDocument();
		await expect.element(page.getByText('reader1')).toBeInTheDocument();
	});
});