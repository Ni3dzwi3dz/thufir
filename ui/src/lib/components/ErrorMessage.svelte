<script lang="ts">
	export let message: string = '';
</script>

{#if message}
<div class="mb-4 p-3 bg-red-50 border border-red-200 text-red-600 rounded-lg">
	{message}
</div>
{/if}
