<script setup>
import NavBar from '../components/NavBar.vue'
import HeroSection from '../components/HeroSection.vue'
import WorkflowDemo from '../components/WorkflowDemo.vue'
import ComparisonTable from '../components/ComparisonTable.vue'
import PricingTiers from '../components/PricingTiers.vue'
import FAQSection from '../components/FAQSection.vue'
import SiteFooter from '../components/SiteFooter.vue'
</script>

<template>
  <div class="min-h-screen bg-white">
    <NavBar />
    <main>
      <HeroSection />
      <WorkflowDemo />
      <ComparisonTable />
      <PricingTiers />
      <FAQSection />
    </main>
    <SiteFooter />
  </div>
</template>

<style scoped>
:deep(h1),
:deep(h2),
:deep(h3) {
  text-wrap: balance;
}
</style>
