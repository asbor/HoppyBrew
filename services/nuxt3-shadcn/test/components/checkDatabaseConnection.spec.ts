import { mount, flushPromises } from '@vue/test-utils';
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import checkDatabaseConnection from '@/components/checkDatabaseConnection.vue';

// Mock fetch globally
global.fetch = vi.fn();

const normalise = (value: string) => value.replace(/\s+/g, ' ').trim();

describe('checkDatabaseConnection.vue', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  it('renders disconnected state initially', async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error('Network error'));
    
    const wrapper = mount(checkDatabaseConnection);
    await flushPromises();

    expect(normalise(wrapper.text())).toContain('Disconnected');
  });

  it('shows connected state when health check succeeds', async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      status: 200,
    });

    const wrapper = mount(checkDatabaseConnection);
    await flushPromises();

    expect(normalise(wrapper.text())).toContain('Connected');
  });

  it('shows disconnected state when health check fails', async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error('Network error'));

    const wrapper = mount(checkDatabaseConnection);
    await flushPromises();

    expect(normalise(wrapper.text())).toContain('Disconnected');
  });

  it('displays error message on connection failure', async () => {
    (global.fetch as any).mockRejectedValueOnce(new Error('Network error'));

    const wrapper = mount(checkDatabaseConnection);
    await flushPromises();

    expect(normalise(wrapper.text())).toContain('Connection error');
  });

  it('polls health endpoint every 30 seconds', async () => {
    (global.fetch as any).mockResolvedValue({
      ok: true,
      status: 200,
    });

    const wrapper = mount(checkDatabaseConnection);
    await flushPromises();

    // Initial call
    expect(global.fetch).toHaveBeenCalledTimes(1);

    // Fast-forward 30 seconds
    await vi.advanceTimersByTimeAsync(30000);
    await flushPromises();

    expect(global.fetch).toHaveBeenCalledTimes(2);

    // Fast-forward another 30 seconds
    await vi.advanceTimersByTimeAsync(30000);
    await flushPromises();

    expect(global.fetch).toHaveBeenCalledTimes(3);
  });

  it('uses correct API URL from runtime config', async () => {
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      status: 200,
    });

    const wrapper = mount(checkDatabaseConnection);
    await flushPromises();

    expect(global.fetch).toHaveBeenCalledWith(
      'http://localhost:8000/health',
      expect.objectContaining({
        method: 'GET',
        headers: {
          'Accept': 'application/json',
        },
      })
    );
  });

  it('increments retry count on consecutive failures', async () => {
    (global.fetch as any).mockRejectedValue(new Error('Network error'));

    const wrapper = mount(checkDatabaseConnection);
    await flushPromises();

    // First failure
    expect(normalise(wrapper.text())).toContain('retry 1/3');

    // Advance time for second check
    await vi.advanceTimersByTimeAsync(30000);
    await flushPromises();

    // Second failure
    expect(normalise(wrapper.text())).toContain('retry 2/3');
  });

  it('resets retry count on successful connection', async () => {
    // First call fails
    (global.fetch as any).mockRejectedValueOnce(new Error('Network error'));

    const wrapper = mount(checkDatabaseConnection);
    await flushPromises();

    expect(normalise(wrapper.text())).toContain('retry 1/3');

    // Second call succeeds
    (global.fetch as any).mockResolvedValueOnce({
      ok: true,
      status: 200,
    });

    await vi.advanceTimersByTimeAsync(30000);
    await flushPromises();

    // Error message should be cleared
    expect(normalise(wrapper.text())).toContain('Connected');
    expect(normalise(wrapper.text())).not.toContain('retry');
  });
});
