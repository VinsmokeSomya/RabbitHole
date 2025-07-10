<div class="tabs">
  <div class="tab-list" role="tablist">
    <slot name="tabs"></slot>
  </div>
  <div class="tab-panels">
    <slot name="panels"></slot>
  </div>
</div>

<style>
.tab-list {
  display: flex;
  border-bottom: 1px solid var(--sl-color-gray-5);
}
.tab-panels {
  padding: 1rem 0;
}
</style> 