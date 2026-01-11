<script lang="ts">
	export let onClick: () => void = () => {};
	export let text: string = '';
	export let href: string | null = null;
</script>

{#if href}
	<a
		{href}
		class="bg-[#64001E] rounded-md px-4 py-2 text-white hover:bg-[#4a0015] transition-colors inline-block"
	>
		{text}
	</a>
{:else}
	<button
		on:click={onClick}
		class="bg-[#64001E] rounded-md px-4 py-2 text-white hover:bg-[#4a0015] transition-colors"
	>
		{text}
	</button>
{/if}
