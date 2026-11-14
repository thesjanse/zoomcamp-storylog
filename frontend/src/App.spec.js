import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'

import App from './App.vue'

function jsonResponse(body = { status: 'ok' }, ok = true, status = 200) {
  return {
    ok,
    status,
    json: vi.fn().mockResolvedValue(body),
  }
}

describe('App', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn())
  })

  afterEach(() => {
    vi.unstubAllGlobals()
    vi.unstubAllEnvs()
  })

  it('renders the scaffold placeholder content', async () => {
    fetch.mockResolvedValue(jsonResponse())

    const wrapper = mount(App)

    expect(wrapper.text()).toContain('StoryLog')
    expect(wrapper.text()).toContain('Reading and watch journal scaffold.')

    await flushPromises()
  })

  it('shows a polite status announcement while checking the API', () => {
    fetch.mockReturnValue(new Promise(() => {}))

    const wrapper = mount(App)
    const status = wrapper.get('[role="status"]')

    expect(status.text()).toContain('Checking API…')
    expect(status.attributes('aria-live')).toBe('polite')
  })

  it('shows that the API is connected after a 200 response', async () => {
    vi.stubEnv('VITE_API_BASE_URL', '')
    fetch.mockResolvedValue(jsonResponse())

    const wrapper = mount(App)
    await flushPromises()

    expect(wrapper.text()).toContain('API connected')
    expect(wrapper.find('[role="alert"]').exists()).toBe(false)
    expect(fetch).toHaveBeenCalledWith('/api/v1/health/')
  })

  it('shows an alert without server details when the network request fails', async () => {
    fetch.mockRejectedValue(new Error('connection refused'))

    const wrapper = mount(App)
    await flushPromises()

    const alert = wrapper.get('[role="alert"]')
    expect(alert.text()).toContain('API unavailable')
    expect(wrapper.text()).not.toContain('connection refused')
  })

  it('shows an alert when the API returns a non-2xx response', async () => {
    fetch.mockResolvedValue(jsonResponse({}, false, 503))

    const wrapper = mount(App)
    await flushPromises()

    expect(wrapper.get('[role="alert"]').text()).toContain('API unavailable')
    expect(wrapper.text()).not.toContain('503')
  })

  it('uses the relative health path when VITE_API_BASE_URL is unset', async () => {
    vi.stubEnv('VITE_API_BASE_URL', undefined)
    fetch.mockResolvedValue(jsonResponse())

    mount(App)
    await flushPromises()

    expect(fetch).toHaveBeenCalledWith('/api/v1/health/')
  })

  it('uses the configured backend origin for the health path', async () => {
    vi.stubEnv('VITE_API_BASE_URL', 'http://localhost:8000')
    fetch.mockResolvedValue(jsonResponse())

    mount(App)
    await flushPromises()

    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/v1/health/')
  })

  it('normalizes a trailing slash in VITE_API_BASE_URL', async () => {
    vi.stubEnv('VITE_API_BASE_URL', 'http://localhost:8000/')
    fetch.mockResolvedValue(jsonResponse())

    mount(App)
    await flushPromises()

    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/v1/health/')
  })
})
