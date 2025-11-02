export type ReferralStatus = 'INVITATION_SENT' | 'APPLICATION_RECEIVED' | 'JOINED' | 'DECLINED';

export interface Referral {
  id: number;
  first_name: string;
  last_name: string;
  email: string;
  status: ReferralStatus;
  referred_date: string;
  last_sent_at: string;
}

export interface AnalyticsData {
  total_invited: number;
  invitations_sent_count: number;
  approved_count: number;
  conversion_rate: number; // Percentage value
}

export interface InvitationFormData {
  first_name: string;
  last_name: string;
  email: string;
}

export interface APIError {
    detail?: string;
    [key: string]: string | undefined;
}