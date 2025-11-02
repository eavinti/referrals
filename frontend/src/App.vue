<script setup lang="ts">
import { ref } from 'vue';
import InvitationForm from './components/InvitationForm.vue';
import ReferralsList from './components/ReferralsList.vue';

// Use a ref to access the child component's exposed methods (loadReferrals)
const referralsListRef = ref<InstanceType<typeof ReferralsList> | null>(null);

// Function to call when a new invitation is sent successfully
const handleInvitationSent = () => {
  if (referralsListRef.value) {
    referralsListRef.value.loadReferrals();
  }
};

</script>

<template>
  <div class="min-h-screen bg-dark-bg">
    <div class="container mx-auto px-4 py-8">
      <h1 class="text-4xl font-serif text-gray-primary mb-2">
        Invite a Member
      </h1>
      <p class="text-sm text-gray-secondary mb-4">
        Help grow our community by referring qualified investors. We expect all members to uphold our <a href="#" class="underline">Code of Standards</a>
      </p>


      <InvitationForm @invitation-sent="handleInvitationSent" />
      <ReferralsList ref="referralsListRef" />

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">
        <div class="p-6 rounded-lg bg-dark-card border border-dark-border space-y-3">
            <h3 class="text-md font-serif text-copper-light">Why Invite?</h3>
            <p class="text-sm text-gray-secondary">
                By inviting someone, you're expediting their access to 10 East's curated co-investment opportunities and investor network.
            </p>
        </div>
        <div class="p-6 rounded-lg bg-dark-card border border-dark-border space-y-3">
            <h3 class="text-md font-serif text-copper-light">How It Works</h3>
            <ol class="text-sm text-gray-secondary list-decimal list-inside space-y-1">
                <li>Fill in the referral form with their name and email.</li>
                <li>We'll send them an email invitation to apply for 10 East membership.</li>
                <li>Your referral can explore and decide if 10 East is the right fit for them.</li>
            </ol>
        </div>
      </div>

    </div>
  </div>
</template>

<style scoped>
/* Add any component-specific styles here */
</style>
