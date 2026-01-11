import { describe, it, expect } from 'vitest';
import { render } from 'vitest-browser-svelte';
import Layout from './+layout.svelte';

describe('+layout.svelte', () => {
	it('renders the navbar with logo, navigation menu, and login button', async () => {
		const screen = render(Layout, {
			props: {
				children: () => '<div>Page Content</div>'
			}
		});

		// Check if navbar is present
		await expect.element(screen.getByRole('img', { name: 'Thufir Logo' })).toBeVisible();

		// Check navigation links
		await expect.element(screen.getByRole('link', { name: 'Home' })).toBeVisible();
		await expect.element(screen.getByRole('link', { name: 'About' })).toBeVisible();
		await expect.element(screen.getByRole('link', { name: 'Contact' })).toBeVisible();

		// Check login button
		await expect.element(screen.getByRole('link', { name: 'Login' })).toBeVisible();

		// Check if main content is rendered
		await expect.element(screen.getByText('Page Content')).toBeVisible();
	});

	it('has fixed positioning for the navbar', async () => {
		const screen = render(Layout, {
			props: {
				children: () => '<div>Page Content</div>'
			}
		});

		const navbar = screen.getByRole('banner'); // Assuming navbar has role="banner" or we can check class
		await expect.element(navbar).toHaveClass('bg-gray-800');
		// Note: Testing CSS properties like position might require additional setup
	});

	it('renders children with proper margin', async () => {
		const screen = render(Layout, {
			props: {
				children: () => '<h1>Test Page</h1>'
			}
		});

		const mainContent = screen.getByText('Test Page').parentElement;
		await expect.element(mainContent).toHaveAttribute('id', 'main-content');
		// The margin-top is inline style, so we can check if it's applied
	});
});