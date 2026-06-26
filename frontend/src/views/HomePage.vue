<script setup>
import NavBar from '../components/NavBar.vue'
import HeroSection from '../components/HeroSection.vue'
import HowItWorks from '../components/HowItWorks.vue'
import ValueFormulasSection from '../components/ValueFormulasSection.vue'
import WhyOpenSource from '../components/WhyOpenSource.vue'
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
      <HowItWorks />
      <ValueFormulasSection />
      <WhyOpenSource />
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
