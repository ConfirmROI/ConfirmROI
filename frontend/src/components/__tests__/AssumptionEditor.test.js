import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import AssumptionEditor from '../AssumptionEditor.vue'

describe('AssumptionEditor', () => {
  const projectArchetype = {
    id: 1,
    assumption_values: [
      { id: 1, assumption_id: 10, value: 100, assumption: { label: 'Hours Saved', key: 'hours_saved' } },
      { id: 2, assumption_id: 20, value: 50, assumption: { label: 'Hourly Rate', key: 'hourly_rate' } },
    ],
  }

  it('renders assumption labels', () => {
    const wrapper = mount(AssumptionEditor, { props: { projectArchetype } })
    expect(wrapper.text()).toContain('Hours Saved')
    expect(wrapper.text()).toContain('Hourly Rate')
  })

  it('renders input fields with values', () => {
    const wrapper = mount(AssumptionEditor, { props: { projectArchetype } })
    const inputs = wrapper.findAll('input[type="number"]')
    expect(inputs).toHaveLength(2)
    expect(inputs[0].element.value).toBe('100')
    expect(inputs[1].element.value).toBe('50')
  })

  it('emits update on change', async () => {
    const wrapper = mount(AssumptionEditor, { props: { projectArchetype } })
    const input = wrapper.find('input[type="number"]')
    await input.setValue('200')
    await input.trigger('change')
    expect(wrapper.emitted('update')).toBeTruthy()
    expect(wrapper.emitted('update')[0]).toEqual([10, 200])
  })

  it('shows message when no assumptions', () => {
    const wrapper = mount(AssumptionEditor, {
      props: { projectArchetype: { id: 1, assumption_values: [] } },
    })
    expect(wrapper.text()).toContain('No editable assumptions')
  })
})
