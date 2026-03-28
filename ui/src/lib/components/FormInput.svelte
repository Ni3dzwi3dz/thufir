<script lang="ts">
	import type { HTMLInputAttributes } from "svelte/elements";

	export let id: string;
	export let label: string;
	export let type: string = 'text';
	export let value: string;
	export let placeholder: string = '';
	export let autocomplete: HTMLInputAttributes["autocomplete"] = '';
	export let disabled: boolean = false;
	export let onKeyPress: ((event: KeyboardEvent) => void) | undefined;
</script>

<div>
	<label for={id} class="block text-sm font-medium text-gray-700 mb-1">
		{label}
	</label>
	<input
		id={id}
		type={type}
		bind:value={value}
		placeholder={placeholder}
		autocomplete={autocomplete}
		disabled={disabled}
		class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed transition-colors"
		on:keypress={onKeyPress}
	/>
</div>
