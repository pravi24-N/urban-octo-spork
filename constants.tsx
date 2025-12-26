
import { Agent, RateData } from './types';

export const HISTORICAL_RATES: RateData[] = [
  { year: '2020', rate: 7.15, impact: "RBI repo rate cuts during pandemic led to historic lows in Indian home loans." },
  { year: '2021', rate: 6.70, impact: "Record low interest rates fueled a massive surge in residential sales across Tier-1 cities." },
  { year: '2022', rate: 7.90, impact: "RBI started hiking rates to curb inflation, increasing the EMI burden for existing borrowers." },
  { year: '2023', rate: 8.50, impact: "Rates stabilized at higher levels. Banks focused on long-tenure loans to keep EMIs manageable." },
  { year: '2024', rate: 8.35, impact: "A slight softening observed. Demand remains high in luxury and mid-segment housing." },
  { year: '2025', rate: 8.25, impact: "Current Projection: Rates cooling as inflation stabilizes. Best time for refinancing in 3 years." },
];

export const AGENTS: Agent[] = [
  { id: 1, name: "Arjun Mehta", contact: "+91 98200 12345", location: "Mumbai, MH", specialty: "Luxury High-rises", image: "https://picsum.photos/seed/arjun/200/200" },
  { id: 2, name: "Priya Sharma", contact: "+91 80455 67890", location: "Bangalore, KA", specialty: "IT Corridor Villas", image: "https://picsum.photos/seed/priya/200/200" },
  { id: 3, name: "Rohan Varma", contact: "+91 11234 56789", location: "Gurugram, HR", specialty: "Commercial & Plotting", image: "https://picsum.photos/seed/rohan/200/200" },
  { id: 4, name: "Ananya Iyer", contact: "+91 44567 89012", location: "Chennai, TN", specialty: "First-time Home Buyers", image: "https://picsum.photos/seed/ananya/200/200" },
];
