import apiClient from './axios';
import type { Referral, InvitationFormData, AnalyticsData, APIError } from '../types/referral';

const handleApiError = (error: any): APIError => {
    if (error.response && error.response.data) {
        return error.response.data as APIError;
    }
    return { detail: 'An unexpected error occurred.' };
};

export const getReferrals = async (): Promise<Referral[]> => {
    try {
        const response = await apiClient.get<Referral[]>('referrals/');
        return response.data.results;
    } catch (error) {
        console.error("Error fetching referrals:", error);
        throw handleApiError(error);
    }
};

export const createReferral = async (data: InvitationFormData): Promise<Referral> => {
    try {
        const response = await apiClient.post<Referral>('referrals/', data);
        return response.data;
    } catch (error) {
        console.error("Error creating referral:", error);
        throw handleApiError(error);
    }
};

export const resendInvitation = async (id: number): Promise<Referral> => {
    try {
        const response = await apiClient.post<Referral>(`referrals/${id}/resend/`);
        return response.data;
    } catch (error) {
        console.error(`Error resending invitation for ID ${id}:`, error);
        throw handleApiError(error);
    }
};

export const getAnalytics = async (): Promise<AnalyticsData> => {
    try {
        const response = await apiClient.get<AnalyticsData>('analytics/');
        return response.data;
    } catch (error) {
        console.error("Error fetching analytics:", error);
        throw handleApiError(error);
    }
};