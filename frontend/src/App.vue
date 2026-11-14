<script setup>
import { onMounted, ref } from 'vue'

const HEALTH_PATH = '/api/v1/health/'

const status = ref('checking')

function buildHealthUrl(baseUrl = import.meta.env.VITE_API_BASE_URL) {
  const origin = (baseUrl ?? '').trim().replace(/\/+$/, '')
  return `${origin}${HEALTH_PATH}`
}

onMounted(async () => {
  try {
    const response = await fetch(buildHealthUrl())
    status.value = response.ok ? 'connected' : 'unavailable'
  } catch {
    status.value = 'unavailable'
  }
})
</script>

<template>
  <main>
    <h1>StoryLog</h1>
    <p>Reading and watch journal scaffold.</p>

    <section class="api-status" aria-labelledby="api-status-title">
      <h2 id="api-status-title">API status</h2>
      <p v-if="status === 'checking'" role="status" aria-live="polite">
        Checking API…
      </p>
      <p v-else-if="status === 'connected'" role="status" aria-live="polite">
        API connected
      </p>
      <p v-else role="alert">API unavailable</p>
    </section>
  </main>
</template>
