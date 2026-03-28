<script lang="ts">
  import { goto } from '$app/navigation';
  import AuthForm from '$lib/components/AuthForm.svelte';
  import { resolve } from '$app/paths';

  function handleSuccess(): void {
    void goto(resolve('/profile'));
  }
</script>

<div class="flex min-h-[70vh] items-center justify-center bg-gray-50 px-4 py-10">
  <AuthForm mode="register" on:success={handleSuccess} />
</div>
