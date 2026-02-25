import React, { createContext, useState, useContext } from 'react';
import type { ReactNode } from 'react';

export interface User {
  id: string;
  name: string;
  role: string;
  image: string;
}

export interface Sector {
  id: string;
  nameKey: string; // Translation key
  status: 'critical' | 'optimal';
  moisture: number;
  image: string;
  cropType: string;
}

interface UserContextType {
  currentUser: User | null;
  login: (user: User) => void;
  logout: () => void;
  userSectors: Sector[];
  users: User[];
}

const mockUsers: User[] = [
  { id: 'u1', name: 'Rajesh Kumar', role: 'Farmer', image: 'https://images.unsplash.com/photo-1542909168-82c3e7fdca5c?auto=format&fit=crop&q=80&w=200&h=200' },
  { id: 'u2', name: 'Amit Singh', role: 'Manager', image: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&q=80&w=200&h=200' },
  { id: 'u3', name: 'Savitri Devi', role: 'Agronomist', image: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&q=80&w=200&h=200' },
  { id: 'u4', name: 'Muthu Kumar', role: 'Irrigation Specialist', image: 'https://images.unsplash.com/photo-1566492031773-4f4e44671857?auto=format&fit=crop&q=80&w=200&h=200' },
  { id: 'u5', name: 'Arjun Thapa', role: 'Soil Expert', image: 'https://images.unsplash.com/photo-1600486913747-55e5470d6f40?auto=format&fit=crop&q=80&w=200&h=200' },
  { id: 'u6', name: 'Priya Sharma', role: 'Inspector', image: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=200&h=200' },
];

const mockSectors: Record<string, Sector[]> = {
  'u1': [ // Rajesh - Wheat & Rice
    { id: 'R-1', nameKey: 'northRidge', status: 'critical', moisture: 22, image: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&q=80&w=1000', cropType: 'Wheat' },
    { id: 'R-2', nameKey: 'eastBasin', status: 'optimal', moisture: 84, image: 'https://images.unsplash.com/photo-1625246333195-bf5f852be9b8?auto=format&fit=crop&q=80&w=1000', cropType: 'Rice' },
  ],
  'u2': [ // Amit - Orchards
    { id: 'A-1', nameKey: 'lowerOrchard', status: 'optimal', moisture: 65, image: 'https://images.unsplash.com/photo-1615811361524-6830df586c9a?auto=format&fit=crop&q=80&w=1000', cropType: 'Apple' },
    { id: 'A-2', nameKey: 'riverBend', status: 'critical', moisture: 12, image: 'https://images.unsplash.com/photo-1595113316349-9fa4eb24f884?auto=format&fit=crop&q=80&w=1000', cropType: 'Peach' },
    { id: 'A-3', nameKey: 'highland', status: 'optimal', moisture: 78, image: 'https://images.unsplash.com/photo-1605000797499-95a51c5269ae?auto=format&fit=crop&q=80&w=1000', cropType: 'Mixed' },
  ],
  'u3': [ // Savitri - Vegetables
    { id: 'S-1', nameKey: 'southValley', status: 'critical', moisture: 18, image: 'https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&q=80&w=1000', cropType: 'Carrot' },
    { id: 'S-2', nameKey: 'northRidge', status: 'optimal', moisture: 60, image: 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?auto=format&fit=crop&q=80&w=1000', cropType: 'Potato' },
  ],
  // Default for others
  'default': [
    { id: 'D-1', nameKey: 'southValley', status: 'critical', moisture: 15, image: 'https://images.unsplash.com/photo-1605000797499-95a51c5269ae?auto=format&fit=crop&q=80&w=1000', cropType: 'Generic' },
    { id: 'D-2', nameKey: 'riverBend', status: 'optimal', moisture: 92, image: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&q=80&w=1000', cropType: 'Generic' },
  ]
};

const UserContext = createContext<UserContextType | undefined>(undefined);

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [currentUser, setCurrentUser] = useState<User | null>(null);

  const login = (user: User) => {
    setCurrentUser(user);
  };

  const logout = () => {
    setCurrentUser(null);
  };

  const userSectors = currentUser && mockSectors[currentUser.id] 
    ? mockSectors[currentUser.id]!
    : mockSectors['default']!;

  return (
    <UserContext.Provider value={{ currentUser, login, logout, userSectors, users: mockUsers }}>
      {children}
    </UserContext.Provider>
  );
};

export const useUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};
