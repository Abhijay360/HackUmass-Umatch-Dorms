'use client';

import React, { useState, useCallback, useMemo } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Button } from '../../components/ui/button';
import { Card } from '../../components/ui/card';
import { Progress } from '../../components/ui/progress';
import { Home, ChevronLeft, ChevronRight } from 'lucide-react';
import { QuizResponses } from '../../lib/supabase';
import QuestionStep from '../../components/QuestionStep';

const totalSteps = 5; // Updated: removed redundant questions

export default function RecommenderPage() {
  const router = useRouter();
  const [currentStep, setCurrentStep] = useState(1);
  const [responses, setResponses] = useState<Partial<QuizResponses>>({});

  const updateResponse = useCallback((key: string | number | symbol, value: any) => {
    setResponses(prev => ({ ...prev, [key as keyof QuizResponses]: value }));
  }, []);

  const validateStep = (step: number): boolean => {
    switch (step) {
      case 1:
        return !!(
          responses.yearStatus &&
          responses.major &&
          responses.roomType &&
          responses.genderType &&
          responses.accessible !== undefined &&
          responses.isHonors &&
          responses.breakHousing
        );
      case 2:
        return !!(
          responses.socialLevelType &&
          responses.noiseLevelType &&
          responses.activitiesImportance &&
          responses.environmentPref &&
          responses.sleepSchedule &&
          responses.tidinessLevel &&
          responses.lifestyleMatch &&
          responses.guestFrequencyType
        );
      case 3:
        return !!(
          responses.campusProximity &&
          responses.commuteDistanceType
        );
      case 4:
        return !!(
          responses.communityType &&
          responses.sharedInterestsType
        );
      case 5:
        // Validate that all priorities are set and unique (now 4 priorities: location, privacy, amenities, social)
        if (!responses.priorities || typeof responses.priorities !== 'object' || Array.isArray(responses.priorities)) {
          return false;
        }
        const priorityValues = Object.values(responses.priorities).filter((v): v is number => typeof v === 'number');
        if (priorityValues.length !== 4) {
          return false;
        }
        const uniqueValues = new Set(priorityValues);
        return uniqueValues.size === 4 && priorityValues.every((v: number) => v >= 1 && v <= 4);
      default:
        return true;
    }
  };

  const handleNext = () => {
    if (!validateStep(currentStep)) {
      alert('Please fill in all required fields before proceeding.');
      return;
    }

    if (currentStep < totalSteps) {
      setCurrentStep(prev => prev + 1);
    } else {
      // Final validation
      if (!validateStep(currentStep)) {
        alert('Please fill in all required fields before submitting.');
        return;
      }
      const sessionId = `session_${Date.now()}`;
      localStorage.setItem('quizResponses', JSON.stringify({ ...responses, sessionId }));
      router.push('/results');
    }
  };

  const handleBack = () => {
    if (currentStep > 1) {
      setCurrentStep(prev => prev - 1);
    }
  };

  const progress = useMemo(() => (currentStep / totalSteps) * 100, [currentStep]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-crimson-50/20 to-white">
      <nav className="border-b border-crimson-100 bg-white/95 backdrop-blur-md sticky top-0 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-2">
              <Home className="h-6 w-6 text-crimson-600" />
              <span className="font-bold text-xl text-crimson-700">UMass Housing</span>
            </div>
            <div className="hidden md:flex space-x-8">
              <Link href="/" className="text-gray-700 hover:text-crimson-600 transition-colors font-medium">
                Home
              </Link>
              <Link href="/recommender" className="text-crimson-600 font-semibold">
                Recommender
              </Link>
              <Link href="/about" className="text-gray-700 hover:text-crimson-600 transition-colors font-medium">
                About
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-3xl mx-auto px-4 py-12">
        <div className="mb-8">
          <div className="flex justify-between text-sm text-gray-600 mb-3 font-medium">
            <span>Question {currentStep} of {totalSteps}</span>
            <span>{Math.round(progress)}% Complete</span>
          </div>
          <Progress value={progress} className="h-2.5 bg-gray-100" />
        </div>

        <Card className="p-8 rounded-2xl shadow-lg border border-gray-200 bg-white hover:shadow-xl transition-shadow">
          <QuestionStep
            step={currentStep}
            responses={responses}
            updateResponse={updateResponse}
          />
        </Card>

        <div className="flex justify-between mt-8">
          <Button
            onClick={handleBack}
            disabled={currentStep === 1}
            variant="outline"
            className="border-2 border-gray-300 text-gray-700 hover:bg-gray-50 hover:border-gray-400 disabled:opacity-50 disabled:cursor-not-allowed font-semibold"
          >
            <ChevronLeft className="mr-2 h-4 w-4" />
            Back
          </Button>

          <Button
            onClick={handleNext}
            className="bg-gradient-to-r from-crimson-600 to-crimson-700 hover:from-crimson-700 hover:to-crimson-800 text-white font-semibold shadow-lg hover:shadow-xl transition-all"
          >
            {currentStep === totalSteps ? 'Get Results' : 'Next'}
            <ChevronRight className="ml-2 h-4 w-4" />
          </Button>
        </div>
      </main>
    </div>
  );
}
