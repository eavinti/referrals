<script setup lang="ts">
import { reactive, ref } from 'vue';
import { createReferral } from '../api/referralService';
import type { InvitationFormData, APIError } from '../types/referral';

const emit = defineEmits<{
  (e: 'invitationSent'): void;
}>();

const form = reactive<InvitationFormData>({
  first_name: '',
  last_name: '',
  email: '',
});

const formErrors = reactive<APIError>({});
const globalError = ref<string | null>(null);
const isSending = ref(false);

const clearErrors = () => {
  Object.keys(formErrors).forEach(key => delete formErrors[key]);
  globalError.value = null;
};

const validateForm = (): boolean => {
    clearErrors();
    let isValid = true;
    if (!form.first_name) { formErrors.first_name = 'First name is required.'; isValid = false; }
    if (!form.last_name) { formErrors.last_name = 'Last name is required.'; isValid = false; }
    if (!form.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
        formErrors.email = 'A valid email address is required.';
        isValid = false;
    }
    return isValid;
}

const handleSubmit = async () => {
  if (!validateForm()) return;

  isSending.value = true;
  clearErrors();

  try {
    await createReferral(form);

    // Success: Clear form and notify parent
    form.first_name = '';
    form.last_name = '';
    form.email = '';

    emit('invitationSent');
    globalError.value = 'Invitation sent successfully!';
  } catch (error: any) {
    const apiErrors = error as APIError;
    if (apiErrors.email) {
      // Handle unique constraint violation or invalid format
      formErrors.email = apiErrors.email;
    } else if (apiErrors.detail) {
      // Handle general errors
      globalError.value = apiErrors.detail;
    } else {
      globalError.value = 'An unexpected error occurred during submission.';
    }
  } finally {
    isSending.value = false;
  }
};
</script>

<template>
  <div class="p-6 rounded-lg bg-dark-card shadow-lg mb-8 border border-dark-border">
    <form @submit.prevent="handleSubmit" class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-4 content-start">
        <div class="md:col-span-1">
          <input
            v-model="form.first_name"
            placeholder="Enter first name"
            :class="['w-full p-3 rounded-md text-gray-primary placeholder-gray-tertiary border', formErrors.first_name ? 'border-red-500 bg-dark-card' : 'border-dark-border bg-dark-bg']"
          />
          <p v-if="formErrors.first_name" class="text-red-500 text-xs mt-1">{{ formErrors.first_name }}</p>
        </div>

        <div class="md:col-span-1">
          <input
            v-model="form.last_name"
            placeholder="Enter last name"
            :class="['w-full p-3 rounded-md text-gray-primary placeholder-gray-tertiary border', formErrors.last_name ? 'border-red-500 bg-dark-card' : 'border-dark-border bg-dark-bg']"
          />
          <p v-if="formErrors.last_name" class="text-red-500 text-xs mt-1">{{ formErrors.last_name }}</p>
        </div>

        <div class="md:col-span-1">
          <input
            v-model="form.email"
            type="email"
            placeholder="Enter email address"
            :class="['w-full p-3 rounded-md text-gray-primary placeholder-gray-tertiary border', formErrors.email ? 'border-red-500 bg-dark-card' : 'border-dark-border bg-dark-bg']"
          />
          <p v-if="formErrors.email" class="text-red-500 text-xs mt-1">{{ formErrors.email }}</p>
        </div>

        <div class="md:col-span-1">
          <button
            type="submit"
            :disabled="isSending"
            :class="['px-6 py-3 rounded-md font-bold text-gray-primary bg-gradient-to-r from-copper-dark to-copper-light', isSending ? 'cursor-not-allowed' : 'cursor-pointer']"
          >
            {{ isSending ? 'Sending...' : 'Send Invitation' }}
          </button>
        </div>

      </div>

      <div class="flex flex-col md:flex-row gap-4 items-center pt-2">

        <div class="flex items-center text-sm text-gray-secondary">
          <div class="w-6 h-6 rounded-full bg-success-light/15 mr-2 flex items-center justify-center">
            <svg class="w-4 h-4 text-success-dark" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path></svg>
          </div>
          We take privacy seriously: Your referral's information will be handled with the utmost care and confidentiality.
        </div>
      </div>

      <p v-if="globalError" :class="['text-sm mt-2', globalError.includes('successfully') ? 'text-success-light' : 'text-red-500']">
        {{ globalError }}
      </p>
    </form>
  </div>
</template>