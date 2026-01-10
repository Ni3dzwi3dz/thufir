<script lang="ts">
	import './layout.css';
	import favicon from '$lib/assets/favicon.svg';
	import Button from '$lib/components/Button.svelte';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<div id="navbar" class="bg-gray-800 flex items-center">
	<img src="/img/thufir_logo_small.png" alt="Thufir Logo" />
	<nav>
		<ul id="menu">
			<li><Button text="Home" href="/" /></li>
			<li><Button text="About" href="/about" /></li>
			<li><Button text="Contact" href="/contact" /></li>
		</ul>
	</nav>
	<div class="ml-auto mr-4">
		<Button text="Login" href="/login" />
	</div>
</div>

<div id='main-content' style="margin-top: 10vh;">
	{@render children()}
</div>

<style>
	#navbar {
		position: fixed;
		top: 0;
		width: 100%;
		height: 10vh;
	}
	ul#menu {
		display: flex;
		list-style: none;
		padding: 0;
		margin: 0;
		align-items: center;
	}
	ul#menu li {
		margin-right: 1.5rem;
	}
	img {
		height: 100%;
		margin-right: 2rem;
	}
</style>
