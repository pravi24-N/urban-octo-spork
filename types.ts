
export type Page = 'home' | 'true_worth' | 'trends' | 'exposure';

export type RiskCategory = 'MORTGAGE' | 'HEALTH' | 'TERM' | 'CAR';

export interface RiskProfile {
  id?: number;
  user_uuid: string;
  category: RiskCategory;
  data_payload: any;
  renewal_date: string;
  target_price: number;
}

export interface EMIReminder {
  id: string;
  label: string;
  amount: number;
  dueDate: string;
}

export interface Agent {
  id: number;
  name: string;
  contact: string;
  location: string;
  specialty: string;
  image: string;
}

export interface RateData {
  year: string;
  rate: number;
  impact: string;
}
