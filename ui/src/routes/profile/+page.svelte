<script lang="ts">
  import { goto } from '$app/navigation';
  import { onMount } from 'svelte';

  import { fetchCurrentUser, getCurrentAuth, type User } from '$lib/auth';
  import { resolve } from '$app/paths';

  let user = $state<User | null>(getCurrentAuth().user);
  let errorMessage = $state('');
  let isLoading = $state(true);

  onMount(() => {
    if (!getCurrentAuth().isAuthenticated) {
      void goto(resolve('/login'));
      return;
    }

    void loadProfile();
  });

  async function loadProfile(): Promise<void> {
    isLoading = true;
    errorMessage = '';

    try {
      user = await fetchCurrentUser();
    } catch (error) {
      errorMessage = error instanceof Error ? error.message : 'Unable to load profile.';
    } finally {
      isLoading = false;
    }
  }
</script>

<div class="mx-auto max-w-3xl px-4 py-10">
  <h1 class="mb-6 text-3xl font-bold text-gray-900">Your profile</h1>

  {#if isLoading}
    <p class="text-gray-600">Loading your profile...</p>
  {:else if errorMessage}
    <div class="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">{errorMessage}</div>
  {:else if user}
    <div class="rounded-xl border border-gray-200 bg-white p-6 shadow-sm">
      <dl class="grid gap-4 sm:grid-cols-2">
        <div>
          <dt class="text-sm font-medium text-gray-500">Username</dt>
          <dd class="mt-1 text-lg text-gray-900">{user.username}</dd>
        </div>
        <div>
          <dt class="text-sm font-medium text-gray-500">Email</dt>
          <dd class="mt-1 text-lg text-gray-900">{user.email}</dd>
        </div>
        <div>
          <dt class="text-sm font-medium text-gray-500">User ID</dt>
          <dd class="mt-1 text-lg text-gray-900">{user.id}</dd>
        </div>
        <div>
          <dt class="text-sm font-medium text-gray-500">Created</dt>
          <dd class="mt-1 text-lg text-gray-900">{new Date(user.created_at).toLocaleString()}</dd>
        </div>
      </dl>
    </div>
  {:else}
    <p class="text-gray-600">No profile data available.</p>
  {/if}
</div>
