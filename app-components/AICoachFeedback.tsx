import React, { useState } from 'react';
import { Alert, ScrollView } from 'react-native';
import {
  Button,
  YStack,
  Text,
  Spinner,
  useTheme,
  Card,
  H4,
  XStack,
} from 'tamagui';
import { Brain, X } from '@tamagui/lucide-icons';
import Markdown from '@ronradtke/react-native-markdown-display';
import { getAICoachFeedback, formatWorkoutForAICoach } from 'lib/ai-coach';
import type { Tables } from 'lib/database.types';

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

interface AICoachFeedbackProps {
  session: PerformedSession;
  visible: boolean;
  onClose: () => void;
}

export function AICoachFeedback({ session, visible, onClose }: AICoachFeedbackProps) {
  const [feedback, setFeedback] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [hasRequested, setHasRequested] = useState(false);
  const theme = useTheme();

  const requestFeedback = async () => {
    if (!session) return;

    setIsLoading(true);
    try {
      const workoutText = formatWorkoutForAICoach(session);
      const aiResponse = await getAICoachFeedback(workoutText);
      setFeedback(aiResponse);
      setHasRequested(true);
    } catch (error) {
      console.error('Error getting AI coach feedback:', error);
      Alert.alert(
        'AI Coach Error',
        error instanceof Error ? error.message : 'Failed to get feedback. Please try again.',
        [{ text: 'OK' }]
      );
    } finally {
      setIsLoading(false);
    }
  };

  const markdownStyles = {
    body: { 
      color: theme.color.val,
      fontSize: 14,
      lineHeight: 20,
    },
    heading1: { 
      color: theme.color.val,
      fontSize: 20,
      fontWeight: 'bold' as const,
      marginBottom: 8,
    },
    heading2: { 
      color: theme.color.val,
      fontSize: 18,
      fontWeight: 'bold' as const,
      marginBottom: 6,
    },
    heading3: { 
      color: theme.color.val,
      fontSize: 16,
      fontWeight: 'bold' as const,
      marginBottom: 4,
    },
    paragraph: {
      color: theme.color.val,
      marginBottom: 8,
    },
    list_item: {
      color: theme.color.val,
      marginBottom: 4,
    },
    strong: {
      color: theme.color.val,
      fontWeight: 'bold' as const,
    },
    em: {
      color: theme.color.val,
      fontStyle: 'italic' as const,
    },
    code_inline: {
      backgroundColor: theme.background075.val,
      color: theme.color.val,
      paddingHorizontal: 4,
      paddingVertical: 2,
      borderRadius: 4,
      fontFamily: 'monospace',
    },
    code_block: {
      backgroundColor: theme.background075.val,
      color: theme.color.val,
      padding: 12,
      borderRadius: 8,
      marginVertical: 8,
      fontFamily: 'monospace',
    },
  };

  if (!visible) return null;

  return (
    <Card
      position="absolute"
      top={0}
      left={0}
      right={0}
      bottom={0}
      backgroundColor="$background"
      zIndex={1000}
      padding="$4"
    >
      <XStack justifyContent="space-between" alignItems="center" marginBottom="$4">
        <XStack alignItems="center" gap="$2">
          <Brain size={24} color={theme.blue9.val} />
          <H4>AI Coach Feedback</H4>
        </XStack>
        <Button
          size="$2"
          chromeless
          circular
          icon={<X />}
          onPress={onClose}
        />
      </XStack>

      {!hasRequested && !isLoading && (
        <YStack gap="$3" alignItems="center" justifyContent="center" flex={1}>
          <Text textAlign="center" opacity={0.7}>
            Get personalized feedback and insights about your workout from our AI coach.
          </Text>
          <Button
            size="$4"
            backgroundColor="$blue9"
            color="white"
            icon={<Brain />}
            onPress={requestFeedback}
            disabled={isLoading}
          >
            Get AI Feedback
          </Button>
        </YStack>
      )}

      {isLoading && (
        <YStack gap="$3" alignItems="center" justifyContent="center" flex={1}>
          <Spinner size="large" color="$blue9" />
          <Text textAlign="center" opacity={0.7}>
            AI Coach is analyzing your workout...
          </Text>
        </YStack>
      )}

      {feedback && hasRequested && !isLoading && (
        <ScrollView style={{ flex: 1 }} showsVerticalScrollIndicator={false}>
          <YStack gap="$2">
            <Markdown style={markdownStyles}>
              {feedback}
            </Markdown>
            
            <Button
              marginTop="$4"
              size="$3"
              backgroundColor="$blue9"
              color="white"
              icon={<Brain />}
              onPress={requestFeedback}
              disabled={isLoading}
            >
              Get New Feedback
            </Button>
          </YStack>
        </ScrollView>
      )}
    </Card>
  );
}
