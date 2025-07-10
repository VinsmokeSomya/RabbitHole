<script>
    import { getContext } from 'svelte';

    export let label = '';
    const activeTab = getContext('activeTab');
</script>

{#if $activeTab === label}
    <div class="tab-panel">
        <slot />
    </div>
{/if} 