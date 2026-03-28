<script lang="ts">
  import { resolve } from 'path';

  export let onClick: () => void = () => {};
  export let text: string = '';
  export let href: string | null = null;
  export let type: 'button' | 'submit' = 'button';
  export let disabled: boolean = false;
</script>

{#if href}
  <a
    href={resolve(href)}
    class="bg-[#64001E] rounded-md px-4 py-2 text-white hover:bg-[#4a0015] transition-colors inline-block"
  >
    {text}
  </a>
{:else}
  <button
    {type}
    {disabled}
    on:click={onClick}
    class="bg-[#64001E] rounded-md px-4 py-2 text-white hover:bg-[#4a0015] transition-colors disabled:cursor-not-allowed disabled:opacity-60"
  >
    {text}
  </button>
{/if}
