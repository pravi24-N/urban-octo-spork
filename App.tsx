
import React, { useState, useEffect } from 'react';
import { Page, EMIReminder, RiskProfile } from './types';
import Navbar from './components/Navbar';
import Home from './components/Home';
import TrueWorth from './components/TrueWorth';
import Trends from './components/Trends';
import Exposure from './components/Exposure';
import { apiService } from './services/api';

const App: React.FC = () => {
  const [currentPage, setCurrentPage] = useState<Page>('home');
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [reminders, setReminders] = useState<EMIReminder[]>([]);
  const [scrollProgress, setScrollProgress] = useState(0);
  const [userUuid, setUserUuid] = useState<string>('');
  const [dbProfiles, setDbProfiles] = useState<RiskProfile[]>([]);
  const [backendOnline, setBackendOnline] = useState(true); // Default to true for cleaner UI

  useEffect(() => {
    // Unique User ID for SQL association
    let uuid = localStorage.getItem('user_uuid');
    if (!uuid) {
      uuid = crypto.randomUUID();
      localStorage.setItem('user_uuid', uuid);
    }
    setUserUuid(uuid);

    // Initial and periodic backend status checks (silent)
    const checkBackend = async () => {
      const isUp = await apiService.checkHealth();
      setBackendOnline(isUp);
      if (isUp) {
        try {
          const profiles = await apiService.getProfiles(uuid || undefined);
          setDbProfiles(profiles);
        } catch (e) {
          console.debug("Background Fetch Info:", e);
        }
      }
    };

    checkBackend();
    const interval = setInterval(checkBackend, 10000); 

    const saved = localStorage.getItem('emi_reminders');
    if (saved) setReminders(JSON.parse(saved));

    const handleScroll = () => {
      const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = (window.scrollY / totalHeight) * 100;
      setScrollProgress(progress);
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
      clearInterval(interval);
    };
  }, []);

  const refreshProfiles = async () => {
    try {
      const profiles = await apiService.getProfiles(userUuid);
      setDbProfiles(profiles);
    } catch (e) {
      console.error("Refresh Error:", e);
    }
  };

  const toggleTheme = () => setIsDarkMode(!isDarkMode);

  const addReminder = (rem: EMIReminder) => {
    const updated = [...reminders, rem];
    setReminders(updated);
    localStorage.setItem('emi_reminders', JSON.stringify(updated));
  };

  const removeReminder = (id: string) => {
    const updated = reminders.filter(r => r.id !== id);
    setReminders(updated);
    localStorage.setItem('emi_reminders', JSON.stringify(updated));
  };

  return (
    <div className={`min-h-screen transition-colors duration-500 selection:bg-blue-500 selection:text-white ${isDarkMode ? 'bg-[#0a0a0a] text-white' : 'bg-gray-50 text-gray-900'}`}>
      <div 
        className="fixed top-0 left-0 h-1 bg-blue-500 z-[60] transition-all duration-100 ease-out"
        style={{ width: `${scrollProgress}%` }}
      />

      <Navbar 
        currentPage={currentPage} 
        setCurrentPage={setCurrentPage} 
        isDarkMode={isDarkMode} 
        toggleTheme={toggleTheme}
        reminders={reminders}
        addReminder={addReminder}
        removeReminder={removeReminder}
      />
      
      <main className="pt-20 pb-12 px-4 md:px-8 max-w-7xl mx-auto">
        {currentPage === 'home' && <Home isDarkMode={isDarkMode} />}
        {currentPage === 'true_worth' && (
          <TrueWorth 
            isDarkMode={isDarkMode} 
            userUuid={userUuid} 
            onSaveProfile={refreshProfiles} 
            isBackendDown={!backendOnline}
          />
        )}
        {currentPage === 'trends' && <Trends isDarkMode={isDarkMode} />}
        {currentPage === 'exposure' && (
          <Exposure 
            isDarkMode={isDarkMode} 
            profiles={dbProfiles} 
            onRefreshProfiles={refreshProfiles} 
            isBackendDown={!backendOnline}
          />
        )}
      </main>

      <footer className="py-20 border-t border-white/5 text-center space-y-6">
        <div className="font-brand text-3xl font-bold opacity-90 tracking-tighter">ClearPath_Financing</div>
        <div className="flex flex-col items-center justify-center gap-2">
          <div className="flex items-center gap-3 px-4 py-2 rounded-full border bg-blue-500/5 border-blue-500/10">
            <div className="w-2 h-2 rounded-full bg-blue-500 shadow-[0_0_8px_rgba(59,130,246,0.4)]" />
            <p className="text-[10px] font-black uppercase tracking-[0.2em] text-blue-500/80">
              Enterprise Intelligence Node Active
            </p>
          </div>
        </div>
        <div className="text-[10px] opacity-30 uppercase font-medium tracking-[0.3em]">&copy; 2025 ClearPath Private Wealth Systems</div>
      </footer>
    </div>
  );
};

export default App;
