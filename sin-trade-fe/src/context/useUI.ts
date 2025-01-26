import { useContext } from 'react';
import { UIContext } from './UIContext';

export function useUI() {
  const context = useContext(UIContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an UIProvider');
  }
  return context;
}