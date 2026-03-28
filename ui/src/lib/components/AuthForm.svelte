<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	import {
		isValidEmail,
		login,
		register,
		type AuthResult,
		type RegisterInput,
		type User
	} from '$lib/auth';
	import Button from './Button.svelte';
	import ErrorMessage from './ErrorMessage.svelte';
	import FormInput from './FormInput.svelte';

	export let mode: 'login' | 'register' = 'login';

	let email = '';
	let username = '';
	let password = '';
	let errorMessage = '';
	let isLoading = false;

	const dispatch = createEventDispatcher<{ success: { user: User } }>();

	$: heading = mode === 'register' ? 'Create your account' : 'Sign in';
	$: submitText = isLoading
		? mode === 'register'
			? 'Creating account...'
			: 'Signing in...'
		: mode === 'register'
			? 'Register'
			: 'Login';

	function validateInputs(): string | null {
		if (mode === 'register' && !isValidEmail(email.trim())) {
			return 'Please enter a valid email address.';
		}

		if (!username.trim()) {
			return 'Username is required.';
		}

		if (password.trim().length < 8) {
			return 'Password must be at least 8 characters long.';
		}

		return null;
	}

	async function handleSubmit(): Promise<void> {
		const validationError = validateInputs();

		if (validationError) {
			errorMessage = validationError;
			return;
		}

		errorMessage = '';
		isLoading = true;

		let response: AuthResult;
		if (mode === 'register') {
			const payload: RegisterInput = {
				email: email.trim(),
				username: username.trim(),
				password
			};
			response = await register(payload);
		} else {
			response = await login(username.trim(), password);
		}

		if (response.success && response.data) {
			dispatch('success', { user: response.data.user });
		} else {
			errorMessage = response.error ?? 'Authentication failed. Please try again.';
		}

		isLoading = false;
	}

	function handleKeyPress(event: KeyboardEvent): void {
		if (event.key === 'Enter') {
			void handleSubmit();
		}
	}
</script>

<div class="mx-auto w-full max-w-md rounded-xl bg-white p-6 shadow-lg">
	<h1 class="mb-2 text-2xl font-bold text-gray-900">{heading}</h1>
	<p class="mb-6 text-sm text-gray-600">
		{#if mode === 'register'}
			Register with your email, username, and password.
		{:else}
			Login with your username and password.
		{/if}
	</p>

	<ErrorMessage message={errorMessage} />

	<div class="space-y-4">
		{#if mode === 'register'}
			<FormInput
				id="email"
				label="Email"
				type="email"
				bind:value={email}
				placeholder="john@example.com"
				autocomplete="email"
				disabled={isLoading}
				onKeyPress={handleKeyPress}
			/>
		{/if}

		<FormInput
			id="username"
			label="Username"
			type="text"
			bind:value={username}
			placeholder="john"
			autocomplete="username"
			disabled={isLoading}
			onKeyPress={handleKeyPress}
		/>

		<FormInput
			id="password"
			label="Password"
			type="password"
			bind:value={password}
			placeholder="••••••••"
			autocomplete={mode === 'register' ? 'new-password' : 'current-password'}
			disabled={isLoading}
			onKeyPress={handleKeyPress}
		/>

		<Button text={submitText} onClick={() => void handleSubmit()} disabled={isLoading} />
	</div>
</div>