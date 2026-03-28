<script lang="ts">
  import { resolve } from '$app/paths';
  import type { Pathname } from '$app/types';

  export let onClick: (() => void) | undefined = undefined;
  export let text = '';
  export let href: Pathname | null = null;
  export let type: 'button' | 'submit' = 'button';
  export let disabled = false;
</script>

{#if href}
  <a
    href={resolve(href)}
    class="inline-block rounded-md bg-[#64001E] px-4 py-2 text-white transition-colors hover:bg-[#4a0015]"
  >
    {text}
  </a>
{:else}
  <button
    {type}
    {disabled}
    onclick={onClick}
    class="rounded-md bg-[#64001E] px-4 py-2 text-white transition-colors hover:bg-[#4a0015] disabled:cursor-not-allowed disabled:opacity-60"
  >
    {text}
  </button>
{/if}
