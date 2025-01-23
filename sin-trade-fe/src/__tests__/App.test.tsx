// Imports
import { describe, it, expect, afterEach } from 'vitest';
import { cleanup, render, screen } from '@testing-library/react';
import userEvent  from '@testing-library/user-event';


// To Test
import App from '../App';

// Tests
describe('Renders main page correctly', () => {
    afterEach(() => {
        cleanup();
    });

    /**
     * Passes - shows title correctly
     */
    it('Should render the page correctly',  () => {
        // Setup
        render(<App />);
        const h1 =  screen.queryByText('Vite + React');

        // Post Expectations
        expect(h1).not.toBeNull();
    });

    /**
     * Passes - shows the button count correctly present
     */
    it('Should show the button count set to 0',  () => {
        // Setup
        render(<App />);
        const button =  screen.queryByText('count is 0');

        // Expectations
        expect(button).not.toBeNull();
    });

    /**
     * Passes - clicks the button 3 times and shows the correct count
     */
    it('Should show the button count set to 3', async () => {
        // Setup
        render(<App />);
        const button =  screen.queryByText('count is 0');
        const user = userEvent.setup();

        // Pre Expectations
        expect(button).not.toBeNull();

        // Actions
        await user.click(button!);
        await user.click(button!);
        await user.click(button!);
        
        // Post Expectations
        expect(button?.innerHTML).toBe('count is 3');
    });
});
