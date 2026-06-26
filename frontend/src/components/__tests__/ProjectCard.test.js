import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import ProjectCard from '../ProjectCard.vue'

describe('ProjectCard', () => {
  const project = {
    id: 1,
    name: 'Test Project',
    description: 'A test project',
    status: 'planning',
  }

  it('renders project name', () => {
    const wrapper = mount(ProjectCard, { props: { project } })
    expect(wrapper.text()).toContain('Test Project')
  })

  it('renders project status', () => {
    const wrapper = mount(ProjectCard, { props: { project } })
    expect(wrapper.text()).toContain('planning')
  })

  it('renders description', () => {
    const wrapper = mount(ProjectCard, { props: { project } })
    expect(wrapper.text()).toContain('A test project')
  })

  it('shows ROI when provided', () => {
    const wrapper = mount(ProjectCard, { props: { project, roi: 50000 } })
    expect(wrapper.text()).toContain('$50,000')
  })

  it('emits click event', async () => {
    const wrapper = mount(ProjectCard, { props: { project } })
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })

  it('shows No description when description is empty', () => {
    const wrapper = mount(ProjectCard, { props: { project: { ...project, description: '' } } })
    expect(wrapper.text()).toContain('No description')
  })
})
