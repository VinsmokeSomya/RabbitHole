<script>
  import Tabs from './Tabs.svelte';
  import TabItem from './TabItem.svelte';
  import { setContext } from 'svelte';

  export let labels = [];
  let activeTab = labels[0];

  setContext('activeTab', {
    subscribe: (fn) => {
      // This is a simplified store
      fn(activeTab);
      return () => {};
    }
  });
</script>

<Tabs>
  <div slot="tabs">
    {#each labels as label}
      <TabItem {label} active={activeTab === label} on:tab-change={(e) => (activeTab = e.detail)} />
    {/each}
  </div>
  <div slot="panels">
    <slot></slot>
  </div>
</Tabs> 