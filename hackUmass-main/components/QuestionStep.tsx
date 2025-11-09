'use client';

import React from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Slider } from '@/components/ui/slider';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group';
import { QuizResponses } from '@/lib/supabase';

interface QuestionStepProps {
  step: number;
  responses: Partial<QuizResponses>;
  updateResponse: (key: keyof QuizResponses, value: any) => void;
}

export default function QuestionStep({ step, responses, updateResponse }: QuestionStepProps) {
  const renderQuestion = () => {
    switch (step) {
      // STEP 1: Basic Information
      case 1:
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Basic Information</h2>
              <p className="text-gray-600">Let's start with your basic housing preferences.</p>
            </div>

            <div className="space-y-5">
              <div className="space-y-2">
                <Label className="text-lg font-medium">Are you a first-year or upperclassman?</Label>
                <RadioGroup value={responses.yearStatus || ''} onValueChange={(v) => updateResponse('yearStatus', v)}>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="first-year" id="first-year" />
                    <Label htmlFor="first-year" className="cursor-pointer flex-1">First-year</Label>
                  </div>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="upperclassman" id="upperclassman" />
                    <Label htmlFor="upperclassman" className="cursor-pointer flex-1">Upperclassman</Label>
                  </div>
                </RadioGroup>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">What is your major?</Label>
                <Select value={responses.major || ''} onValueChange={(v) => updateResponse('major', v)}>
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Select your major" />
                  </SelectTrigger>
                  <SelectContent className="max-h-[400px]">
                    {/* STEM & Engineering */}
                    <SelectItem value="Computer Science">Computer Science</SelectItem>
                    <SelectItem value="Engineering">Engineering</SelectItem>
                    <SelectItem value="Biomedical Engineering">Biomedical Engineering</SelectItem>
                    <SelectItem value="Chemical Engineering">Chemical Engineering</SelectItem>
                    <SelectItem value="Physics">Physics</SelectItem>
                    <SelectItem value="Chemistry">Chemistry</SelectItem>
                    <SelectItem value="Mathematics">Mathematics</SelectItem>
                    <SelectItem value="Biology">Biology</SelectItem>
                    <SelectItem value="Biochemistry">Biochemistry</SelectItem>
                    <SelectItem value="Environmental Science">Environmental Science</SelectItem>
                    
                    {/* Business & Management */}
                    <SelectItem value="Accounting">Accounting</SelectItem>
                    <SelectItem value="Business">Business</SelectItem>
                    <SelectItem value="Management">Management</SelectItem>
                    <SelectItem value="Economics">Economics</SelectItem>
                    
                    {/* Health Sciences */}
                    <SelectItem value="Nursing">Nursing</SelectItem>
                    <SelectItem value="Public Health">Public Health</SelectItem>
                    <SelectItem value="Kinesiology">Kinesiology</SelectItem>
                    
                    {/* Humanities & Fine Arts */}
                    <SelectItem value="English">English</SelectItem>
                    <SelectItem value="History">History</SelectItem>
                    <SelectItem value="Languages">Languages</SelectItem>
                    <SelectItem value="Art & Design">Art & Design</SelectItem>
                    <SelectItem value="Architecture">Architecture</SelectItem>
                    <SelectItem value="Film and Video Studies">Film and Video Studies</SelectItem>
                    
                    {/* Social Sciences */}
                    <SelectItem value="Psychology">Psychology</SelectItem>
                    <SelectItem value="Political Science">Political Science</SelectItem>
                    <SelectItem value="Sociology">Sociology</SelectItem>
                    <SelectItem value="Anthropology">Anthropology</SelectItem>
                    <SelectItem value="Journalism">Journalism</SelectItem>
                    <SelectItem value="Afro-American Studies">Afro-American Studies</SelectItem>
                    
                    {/* Education & Agriculture */}
                    <SelectItem value="Education">Education</SelectItem>
                    <SelectItem value="Agriculture">Agriculture</SelectItem>
                    
                    {/* Other */}
                    <SelectItem value="General">General / Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">What is your preferred room type?</Label>
                <RadioGroup value={responses.roomType || ''} onValueChange={(v) => updateResponse('roomType', v)}>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="double" id="double" />
                    <Label htmlFor="double" className="cursor-pointer flex-1">Double</Label>
                  </div>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="triple" id="triple" />
                    <Label htmlFor="triple" className="cursor-pointer flex-1">Triple</Label>
                  </div>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="quad" id="quad" />
                    <Label htmlFor="quad" className="cursor-pointer flex-1">Quad</Label>
                  </div>
                </RadioGroup>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">What is your gender?</Label>
                <RadioGroup value={responses.genderType || ''} onValueChange={(v) => updateResponse('genderType', v)}>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="male" id="male" />
                    <Label htmlFor="male" className="cursor-pointer flex-1">Male</Label>
                  </div>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="female" id="female" />
                    <Label htmlFor="female" className="cursor-pointer flex-1">Female</Label>
                  </div>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="non-binary" id="non-binary" />
                    <Label htmlFor="non-binary" className="cursor-pointer flex-1">Non-binary</Label>
                  </div>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="prefer-not-to-say" id="prefer-not-to-say" />
                    <Label htmlFor="prefer-not-to-say" className="cursor-pointer flex-1">Prefer not to say</Label>
                  </div>
                </RadioGroup>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">Do you require accessible housing (e.g., wheelchair access, elevator)?</Label>
                <RadioGroup 
                  value={
                    typeof responses.accessible === 'string' 
                      ? responses.accessible 
                      : responses.accessible === true 
                        ? 'yes' 
                        : responses.accessible === false 
                          ? 'no' 
                          : ''
                  } 
                  onValueChange={(v) => updateResponse('accessible', v)}
                >
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="yes" id="accessible-yes" />
                    <Label htmlFor="accessible-yes" className="cursor-pointer flex-1">Yes, required</Label>
                  </div>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="preferred" id="accessible-preferred" />
                    <Label htmlFor="accessible-preferred" className="cursor-pointer flex-1">Preferred but not required</Label>
                  </div>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="no" id="accessible-no" />
                    <Label htmlFor="accessible-no" className="cursor-pointer flex-1">No</Label>
                  </div>
                </RadioGroup>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">Are you an honors student?</Label>
                <RadioGroup value={responses.isHonors || ''} onValueChange={(v) => updateResponse('isHonors', v)}>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="yes" id="honors-yes" />
                    <Label htmlFor="honors-yes" className="cursor-pointer flex-1">Yes</Label>
                  </div>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="no" id="honors-no" />
                    <Label htmlFor="honors-no" className="cursor-pointer flex-1">No</Label>
                  </div>
                </RadioGroup>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">Do you need break housing (housing during winter/spring breaks)?</Label>
                <RadioGroup value={responses.breakHousing || ''} onValueChange={(v) => updateResponse('breakHousing', v)}>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="yes" id="break-yes" />
                    <Label htmlFor="break-yes" className="cursor-pointer flex-1">Yes, required</Label>
                  </div>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="preferred" id="break-preferred" />
                    <Label htmlFor="break-preferred" className="cursor-pointer flex-1">Preferred but not required</Label>
                  </div>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="no" id="break-no" />
                    <Label htmlFor="break-no" className="cursor-pointer flex-1">No</Label>
                  </div>
                </RadioGroup>
              </div>
            </div>
          </div>
        );

      // STEP 2: Social & Lifestyle Preferences
      case 2:
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Social & Lifestyle Preferences</h2>
              <p className="text-gray-600">Tell us about your social habits and lifestyle preferences.</p>
            </div>

            <div className="space-y-5">
              <div className="space-y-2">
                <Label className="text-lg font-medium">How social do you want your dorm to be?</Label>
                <Select value={responses.socialLevelType || ''} onValueChange={(v) => updateResponse('socialLevelType', v)}>
                  <SelectTrigger className="text-lg">
                    <SelectValue placeholder="Select level" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="very-social">Very social (lots of interaction)</SelectItem>
                    <SelectItem value="moderately-social">Moderately social</SelectItem>
                    <SelectItem value="somewhat-social">Somewhat social</SelectItem>
                    <SelectItem value="minimal-social">Minimal social interaction</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">What is your preferred noise level?</Label>
                <Select value={responses.noiseLevelType || ''} onValueChange={(v) => updateResponse('noiseLevelType', v)}>
                  <SelectTrigger className="text-lg">
                    <SelectValue placeholder="Select preference" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="very-quiet">Very quiet</SelectItem>
                    <SelectItem value="quiet">Quiet</SelectItem>
                    <SelectItem value="moderate">Moderate</SelectItem>
                    <SelectItem value="somewhat-loud">Somewhat loud</SelectItem>
                    <SelectItem value="loud">Loud (party-friendly)</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">How important are organized dorm activities or events to you?</Label>
                <Select value={responses.activitiesImportance || ''} onValueChange={(v) => updateResponse('activitiesImportance', v)}>
                  <SelectTrigger className="text-lg">
                    <SelectValue placeholder="Select importance" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="very-important">Very important</SelectItem>
                    <SelectItem value="important">Important</SelectItem>
                    <SelectItem value="somewhat-important">Somewhat important</SelectItem>
                    <SelectItem value="not-important">Not important</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">Do you prefer a party-friendly environment or a quiet academic one?</Label>
                <Select value={responses.environmentPref || ''} onValueChange={(v) => updateResponse('environmentPref', v)}>
                  <SelectTrigger className="text-lg">
                    <SelectValue placeholder="Select preference" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="party-friendly">Party-friendly</SelectItem>
                    <SelectItem value="balanced">Balanced</SelectItem>
                    <SelectItem value="quiet-academic">Quiet academic</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">Are you an early bird or a night owl?</Label>
                <RadioGroup value={responses.sleepSchedule || ''} onValueChange={(v) => updateResponse('sleepSchedule', v)}>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="early-bird" id="early-bird" />
                    <Label htmlFor="early-bird" className="cursor-pointer flex-1">Early bird</Label>
                  </div>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="balanced" id="balanced-sleep" />
                    <Label htmlFor="balanced-sleep" className="cursor-pointer flex-1">Balanced</Label>
                  </div>
                  <div className="flex items-center space-x-2 p-4 border rounded-lg hover:border-crimson-600 transition-colors">
                    <RadioGroupItem value="night-owl" id="night-owl" />
                    <Label htmlFor="night-owl" className="cursor-pointer flex-1">Night owl</Label>
                  </div>
                </RadioGroup>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">How tidy do you consider yourself?</Label>
                <Select value={responses.tidinessLevel || ''} onValueChange={(v) => updateResponse('tidinessLevel', v)}>
                  <SelectTrigger className="text-lg">
                    <SelectValue placeholder="Select level" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="very-tidy">Very tidy</SelectItem>
                    <SelectItem value="tidy">Tidy</SelectItem>
                    <SelectItem value="moderately-tidy">Moderately tidy</SelectItem>
                    <SelectItem value="somewhat-messy">Somewhat messy</SelectItem>
                    <SelectItem value="messy">Messy</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">Do you prefer a roommate who shares your lifestyle habits (sleep, noise, guests)?</Label>
                <Select value={responses.lifestyleMatch || ''} onValueChange={(v) => updateResponse('lifestyleMatch', v)}>
                  <SelectTrigger className="text-lg">
                    <SelectValue placeholder="Select preference" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="very-important">Very important</SelectItem>
                    <SelectItem value="important">Important</SelectItem>
                    <SelectItem value="somewhat-important">Somewhat important</SelectItem>
                    <SelectItem value="not-important">Not important</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">How often do you plan to have guests over?</Label>
                <Select value={responses.guestFrequencyType || ''} onValueChange={(v) => updateResponse('guestFrequencyType', v)}>
                  <SelectTrigger className="text-lg">
                    <SelectValue placeholder="Select frequency" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="daily">Daily</SelectItem>
                    <SelectItem value="several-times-week">Several times a week</SelectItem>
                    <SelectItem value="weekly">Weekly</SelectItem>
                    <SelectItem value="monthly">Monthly</SelectItem>
                    <SelectItem value="rarely">Rarely</SelectItem>
                    <SelectItem value="never">Never</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
        );

      // STEP 3: Amenities & Facilities
      case 3:
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Amenities & Facilities</h2>
              <p className="text-gray-600">What amenities and facilities are important to you?</p>
            </div>

            <div className="space-y-5">
              <div className="space-y-2">
                <Label className="text-lg font-medium">How important is proximity to campus facilities (library, gym, dining hall)?</Label>
                <Select value={responses.campusProximity || ''} onValueChange={(v) => updateResponse('campusProximity', v)}>
                  <SelectTrigger className="text-lg">
                    <SelectValue placeholder="Select importance" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="essential">Essential</SelectItem>
                    <SelectItem value="very-important">Very important</SelectItem>
                    <SelectItem value="important">Important</SelectItem>
                    <SelectItem value="nice-to-have">Nice to have</SelectItem>
                    <SelectItem value="not-important">Not important</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">How far are you willing to walk or commute to class daily?</Label>
                <Select value={responses.commuteDistanceType || ''} onValueChange={(v) => updateResponse('commuteDistanceType', v)}>
                  <SelectTrigger className="text-lg">
                    <SelectValue placeholder="Select distance" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="under-5min">Under 5 minutes</SelectItem>
                    <SelectItem value="5-10min">5-10 minutes</SelectItem>
                    <SelectItem value="10-15min">10-15 minutes</SelectItem>
                    <SelectItem value="15-20min">15-20 minutes</SelectItem>
                    <SelectItem value="over-20min">Over 20 minutes</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>
          </div>
        );

      // STEP 4: Community & Interests
      case 4:
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Community & Interests</h2>
              <p className="text-gray-600">What kind of community and living environment appeals to you?</p>
            </div>

            <div className="space-y-5">
              <div className="space-y-2">
                <Label className="text-lg font-medium">What kind of community appeals to you most?</Label>
                <Select value={responses.communityType || ''} onValueChange={(v) => updateResponse('communityType', v)}>
                  <SelectTrigger className="text-lg">
                    <SelectValue placeholder="Select type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="academic-focused">Academic-focused</SelectItem>
                    <SelectItem value="arts-creative">Arts & Creative</SelectItem>
                    <SelectItem value="sports-athletic">Sports & Athletic</SelectItem>
                    <SelectItem value="diverse-multicultural">Diverse & Multicultural</SelectItem>
                    <SelectItem value="lgbtq-friendly">LGBTQ+ friendly</SelectItem>
                    <SelectItem value="international">International</SelectItem>
                    <SelectItem value="general">General community</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-lg font-medium">How important is it for you to live with people who share your interests?</Label>
                <Select value={responses.sharedInterestsType || ''} onValueChange={(v) => updateResponse('sharedInterestsType', v)}>
                  <SelectTrigger className="text-lg">
                    <SelectValue placeholder="Select importance" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="very-important">Very important</SelectItem>
                    <SelectItem value="important">Important</SelectItem>
                    <SelectItem value="somewhat-important">Somewhat important</SelectItem>
                    <SelectItem value="not-important">Not important</SelectItem>
                  </SelectContent>
                </Select>
              </div>

            </div>
          </div>
        );

      // STEP 5: Priority Ranking (moved up since Step 5 questions were removed)
      case 5:
        return (
          <div className="space-y-6">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Priority Ranking</h2>
              <p className="text-gray-600">Please rank the following by importance (1 = most important, 4 = least important):</p>
            </div>

            <div className="space-y-5">
              {[
                { key: 'location', label: 'Location' },
                { key: 'privacy', label: 'Privacy' },
                { key: 'amenities', label: 'Amenities' },
                { key: 'social', label: 'Social Atmosphere' },
              ].map(({ key, label }) => (
                <div key={key} className="space-y-2">
                  <Label className="text-lg font-medium">{label}</Label>
                  <Select
                    value={String(responses.priorities?.[key] || '')}
                    onValueChange={(v) => {
                      const currentPriorities = responses.priorities || {};
                      updateResponse('priorities', { ...currentPriorities, [key]: parseInt(v) });
                    }}
                  >
                    <SelectTrigger className="text-lg">
                      <SelectValue placeholder={`Select rank for ${label}`} />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="1">1 - Most important</SelectItem>
                      <SelectItem value="2">2</SelectItem>
                      <SelectItem value="3">3</SelectItem>
                      <SelectItem value="4">4 - Least important</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              ))}
            </div>
          </div>
        );

      default:
        return <div>Question not found</div>;
    }
  };

  return <div className="animate-in fade-in duration-300">{renderQuestion()}</div>;
}
