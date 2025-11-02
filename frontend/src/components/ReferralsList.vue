<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getReferrals, resendInvitation } from '../api/referralService';
import type { Referral, ReferralStatus } from '../types/referral';
import StatusPill from './StatusPill.vue';

const referrals = ref<Referral[]>([]);
const isLoading = ref(true);
const error = ref<string | null>(null);

const resendStatus = ref<Record<number, {
    isSending: boolean;
    error: string | null;
    success: string | null;
}>>({});

const loadReferrals = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    referrals.value = await getReferrals();
  } catch (err: any) {
    error.value = err.detail || 'Failed to load member referrals.';
  } finally {
    isLoading.value = false;
  }
};

const ensureResendStatus = (id: number) => {
  if (!resendStatus.value[id]) {
    resendStatus.value[id] = { isSending: false, error: null, success: null };
  }
  return resendStatus.value[id]!;
};

const handleResend = async (referral: Referral) => {
  const status = ensureResendStatus(referral.id);
  status.isSending = true;
  status.error = null;
  status.success = null;

   try {
    const updatedReferral = await resendInvitation(referral.id);
    const index = referrals.value.findIndex(r => r.id === referral.id);
    if (index !== -1) referrals.value[index] = updatedReferral;

    status.success = 'Invitation re-sent successfully!';
    setTimeout(() => { const s = resendStatus.value[referral.id]; if (s) s.success = null; }, 5000);
  } catch (err: any) {
    status.error = err.detail || 'Failed to resend invitation.';
  } finally {
    status.isSending = false;
  }
};

const canResend = (status: ReferralStatus, id: number): boolean => {
    const isSent = status === 'INVITATION_SENT';

    const isSending = resendStatus.value[id]?.isSending || false;

    return isSent && !isSending;
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short', day: 'numeric', year: 'numeric'
  });
};

onMounted(loadReferrals);

defineExpose({
    loadReferrals,
});
</script>

<template>
  <div class="p-6 rounded-lg bg-dark-card shadow-lg mb-8 border border-dark-border">
    <h2 class="text-xl font-serif text-gray-primary mb-4">Your Member Referrals</h2>
    <p class="text-sm text-gray-secondary mb-6">Track the status of your referrals and see when they join.</p>

    <div v-if="isLoading" class="text-center py-8 text-gray-secondary">Loading referrals...</div>

    <div v-else-if="error" class="text-center py-8 text-red-500">{{ error }}</div>
    <div v-else-if="referrals.length === 0" class="text-center py-8 text-gray-secondary">
      You haven't referred any members yet.
    </div>

    <div v-else class="overflow-x-auto">
      <table class="min-w-full divide-y divide-dark-border">
        <thead>
          <tr class="text-left text-xs font-semibold uppercase tracking-wider text-gray-secondary">
            <th class="py-3">Name</th>
            <th class="py-3">Email</th>
            <th class="py-3">Status</th>
            <th class="py-3">Invited Date</th>
            <th class="py-3"></th>
          </tr>
        </thead>
        <tbody class="divide-y divide-dark-border text-sm text-gray-primary">
          <tr v-for="referral in referrals" :key="referral.id">
            <td class="py-4 whitespace-nowrap">{{ referral.first_name }} {{ referral.last_name }}</td>
            <td class="py-4 whitespace-nowrap text-gray-secondary">{{ referral.email }}</td>
            <td class="py-4 whitespace-nowrap">
              <StatusPill :status="referral.status" :joined-date="referral.joined_date" />
            </td>
            <td class="py-4 whitespace-nowrap">{{ formatDate(referral.referred_date) }}</td>
            <td class="py-4 whitespace-nowrap">
              <button
                v-if="referral.status === 'INVITATION_SENT'"
                @click="handleResend(referral)"
                :disabled="!canResend(referral.status, referral.id)"
                class="text-copper-light hover:text-copper-DEFAULT disabled:text-gray-tertiary disabled:cursor-not-allowed font-medium transition-colors"
              >
                <span v-if="resendStatus[referral.id]?.isSending">Sending...</span>
                <span v-else>Re-send <span class="ml-1" aria-hidden="true">&#9993;</span></span>
              </button>

              <span v-else class="text-gray-tertiary">N/A</span>

              <div v-if="resendStatus[referral.id]?.error"
                   :class="['mt-1 text-xs text-red-500']">
                  {{ resendStatus[referral.id]?.error }}
              </div>

              <div v-else-if="resendStatus[referral.id]?.success"
                   :class="['mt-1 text-xs text-success-light']">
                  {{ resendStatus[referral.id]?.success }}
              </div>

            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>