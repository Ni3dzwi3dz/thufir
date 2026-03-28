<script lang="ts">
	import { goto } from '$app/navigation';
	import AuthForm from '$lib/components/AuthForm.svelte';
	import type { User } from '$lib/auth';

	function handleSuccess(event: CustomEvent<{ user: User }>): void {
		void goto('/profile');
	}
</script>

<div class="flex min-h-[70vh] items-center justify-center bg-gray-50 px-4 py-10">
	<AuthForm mode="login" on:success={handleSuccess} />
</div>