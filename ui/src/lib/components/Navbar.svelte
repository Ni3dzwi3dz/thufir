<script lang="ts">
  import { auth, logout } from '$lib/auth';
  import Button from './Button.svelte';

  async function handleLogout(): Promise<void> {
    await logout();
  }
</script>

<div
  id="navbar"
  class="fixed top-0 z-50 flex h-[10vh] w-full items-center bg-gray-800 px-4 text-white"
>
  <img src="/img/thufir_logo_small.png" alt="Thufir Logo" class="mr-8 h-full" />
  <nav>
    <ul id="menu" class="m-0 flex list-none items-center gap-6 p-0">
      <li><Button text="Home" href="/" /></li>
      <li><Button text="About" /></li>
      <li><Button text="Contact"/></li>
    </ul>
  </nav>

  <div class="ml-auto flex items-center gap-4" id="auth-section">
    {#if $auth.isAuthenticated && $auth.user}
      <div class="flex items-center gap-3" id="user-greeting">
        <div
          class="flex h-8 w-8 items-center justify-center rounded-full bg-[#64001E] font-bold text-white"
        >
          <span>{$auth.user.username.charAt(0).toUpperCase()}</span>
        </div>
        <span class="text-sm font-medium">{$auth.user.username}</span>
      </div>
      <Button text="Profile" href="/profile" />
      <Button text="Logout" onClick={() => void handleLogout()} />
    {:else}
      <Button text="Login" href="/login" />
      <Button text="Register" href="/register" />
    {/if}
  </div>
</div>
