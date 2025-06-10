/**
 * AI Coach service for analyzing workout data and providing feedback
 */

import { Tables } from './database.types';

type PerformedSession = Tables<'performed_session'> & {
  session_schedule?: {
    name: string;
    plan?: {
      name: string;
    };
  };
  performed_exercise?: Array<Tables<'performed_exercise'> & {
    performed_exercise_set?: Tables<'performed_exercise_set'>[];
  }>;
};

interface AICoachRequest {
  message: string;
}

interface AICoachResponse {
  output?: string;
  response?: string;
  error?: string;
}

const AI_COACH_API_URL = 'http://192.10.11.97:8000/call';

/**
 * Send workout text to AI coach for analysis and feedback
 * @param workoutText - The formatted workout text to analyze
 * @returns Promise with AI coach response in markdown format
 */
export async function getAICoachFeedback(workoutText: string): Promise<string> {
  try {
    const requestBody: AICoachRequest = {
      message: workoutText
    };

    // Create timeout manually for React Native compatibility (2 minutes for AI generation)
    const timeoutPromise = new Promise<never>((_, reject) => {
      setTimeout(() => reject(new Error('Request timeout')), 4*120000);
    });

    const fetchPromise = fetch(AI_COACH_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ inputs: requestBody }),
    });

    const response = await Promise.race([fetchPromise, timeoutPromise]);

    if (!response.ok) {
      throw new Error(`AI Coach API error: ${response.status} ${response.statusText}`);
    }

    const data: AICoachResponse = await response.json();
    
    if (data.error) {
      throw new Error(`AI Coach error: ${data.error}`);
    }

    // Check both 'output' and 'response' fields for compatibility
    return data.output || data.response || 'No feedback available from AI coach.';
  } catch (error) {
    console.error('Error calling AI Coach API:', error);
    
    if (error instanceof Error) {
      if (error.message === 'Request timeout') {
        throw new Error('AI Coach request timed out. Please try again.');
      }
      throw new Error(`Failed to get AI coach feedback: ${error.message}`);
    }
    
    throw new Error('Failed to get AI coach feedback. Please try again.');
  }
}

/**
 * Format workout session data for AI coach analysis
 * @param session - The performed session data
 * @returns Formatted text suitable for AI analysis
 */
export function formatWorkoutForAICoach(session: PerformedSession): string {
  const workoutDuration = session.completed_at && session.started_at 
    ? `Duration: ${Math.round((new Date(session.completed_at).getTime() - new Date(session.started_at).getTime()) / (1000 * 60))} minutes`
    : '';

  const sessionInfo = [
    `Workout: ${session.session_schedule?.name || 'Custom Workout'}`,
    `Plan: ${session.session_schedule?.plan?.name || 'No plan'}`,
    workoutDuration,
    session.note ? `Session Notes: ${session.note}` : '',
  ].filter(Boolean).join('\n');

  const exerciseDetails = session.performed_exercise?.map((exercise) => {
    const sets = exercise.performed_exercise_set?.map((set, index) => {
      const weight = set.weight ? `${set.weight / 1000}kg` : '0kg';
      const reps = set.reps || 0;
      const setType = set.exercise_set_type || 'Normal';
      const completed = set.completed_at ? '✓' : '○';
      
      return `  Set ${index + 1}: ${weight} × ${reps} reps (${setType}) ${completed}`;
    }).join('\n') || '  No sets recorded';

    const exerciseNote = exercise.note ? `\n  Notes: ${exercise.note}` : '';
    
    return `${exercise.name}:\n${sets}${exerciseNote}`;
  }).join('\n\n') || 'No exercises recorded';

  return `${sessionInfo}\n\nExercises:\n${exerciseDetails}`;
}
