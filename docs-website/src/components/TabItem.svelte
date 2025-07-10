<script>
  import { createEventDispatcher } from 'svelte';

  export let label = '';
  export let active = false;

  const dispatch = createEventDispatcher();
</script>

<button
  class="tab-button"
  class:active
  role="tab"
  aria-selected={active}
  on:click={() => dispatch('tab-change', label)}
>
  {label}
</button>

<style>
  .tab-button {
    padding: 0.75rem 1rem;
    border: 0;
    background: transparent;
    color: var(--sl-color-gray-3);
    font-size: 1rem;
    cursor: pointer;
    transition: color 0.2s;
  }
  .tab-button:hover,
  .tab-button:focus {
    color: var(--sl-color-white);
  }
  .tab-button.active {
    color: var(--sl-color-accent);
    border-bottom: 2px solid var(--sl-color-accent);
  }
</style> 