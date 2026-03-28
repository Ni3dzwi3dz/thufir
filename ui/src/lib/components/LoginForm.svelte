<script lang="ts">
  import AuthForm from './AuthForm.svelte';

  export let showLoginForm = false;
</script>

{#if showLoginForm}
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
    <div class="w-full max-w-md rounded-xl bg-white shadow-2xl">
      <AuthForm mode="login" />
    </div>
  </div>
{/if}
