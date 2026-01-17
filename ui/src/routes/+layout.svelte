<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import Button from '$lib/components/Button.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>


<div id="navbar" class="fixed top-0 w-full h-[10vh] bg-gray-800 flex items-center z-50">
   <img src="/img/thufir_logo_small.png" alt="Thufir Logo" class="h-full mr-8" />
   <nav>
	   <ul id="menu" class="flex list-none p-0 m-0 items-center">
		   <li class="mr-6"><Button text="Home" href="/" /></li>
		   <li class="mr-6"><Button text="About" href="/about" /></li>
		   <li class="mr-6"><Button text="Contact" href="/contact" /></li>
	   </ul>
   </nav>
   <div class="ml-auto mr-4">
	   <Button text="Login" href="/login" />
   </div>
</div>


<div id='main-content' class="mt-[10vh]">
	{@render children()}
</div>


