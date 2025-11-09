'use client';

import React, { useEffect, useState, useCallback, useMemo } from 'react';
import Link from 'next/link';
import { Button } from '../../components/ui/button';
import { Card, CardContent } from '../../components/ui/card';
import { Progress } from '../../components/ui/progress';
import { Badge } from '../../components/ui/badge';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '../../components/ui/dialog';
import { Home, MapPin, DollarSign, Users, Sparkles, Building2 } from 'lucide-react';
import { QuizResponses } from '../../lib/supabase';

interface MatchResult {
  compatibilityScore: number;
  confidenceLevel: string;
  reasoningSummary: string;
  matchAdvice: string;
  candidateName?: string;
  candidateDorm?: string;
  exactHall?: string;
  recommendedDorms?: string;
  gradYear?: string;
  userId?: string;
  isAlternative?: boolean;
}

interface BackendResponse {
  dorm_recommendation: string;
  ranked_matches: MatchResult[];
  message?: string;
  error?: string;
  is_alternative?: boolean;
}

export default function ResultsPage() {
  const [recommendations, setRecommendations] = useState<MatchResult[]>([]);
  const [dormRecommendation, setDormRecommendation] = useState<string>('');
  const [loading, setLoading] = useState(true);
  
  // Generate consistent star positions
  const starPositions = useMemo(() => {
    return Array.from({ length: 5 }, (_, i) => ({
      left: 10 + (i * 18) + Math.sin(i) * 5,
      top: 15 + (i * 12) + Math.cos(i) * 8,
      delay: i * 1.5,
      duration: 3 + (i * 0.3),
    }));
  }, []);

  useEffect(() => {
    let isMounted = true;
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 180000); // 180s timeout (3 minutes for LLM processing)

    async function loadResults() {
      try {
      const storedResponses = localStorage.getItem('quizResponses');
      if (!storedResponses) {
          if (isMounted) window.location.href = '/recommender';
        return;
      }

      const responses: QuizResponses = JSON.parse(storedResponses);

        // Validate that we have the minimum required responses
        if (!responses.roomType || !responses.genderType || !responses.yearStatus || !responses.major) {
          console.error('Missing required responses');
          if (isMounted) {
            alert('Invalid quiz responses. Please retake the quiz.');
            window.location.href = '/recommender';
          }
          return;
        }

        // Call Python backend API through Next.js API route (unified on one port)
        try {
          const response = await fetch('/api/match', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(responses),
            signal: controller.signal,
          });

          if (!response.ok) {
            throw new Error(`Backend API error: ${response.status}`);
          }

          const data: BackendResponse = await response.json();

          if (!isMounted) return;

          if (data.error) {
            console.error('Backend error:', data.error);
            setRecommendations([]);
            setDormRecommendation('');
            setLoading(false);
            
            // Show user-friendly error message
            if (data.error.includes('Connection refused') || data.error.includes('Failed to connect')) {
              alert('Unable to connect to the matching service. Please make sure the Python backend is running on port 8000.');
            } else if (data.message) {
              alert(`Error: ${data.message}`);
            } else {
              alert(`Error: ${data.error}`);
            }
            return;
          }

          // Set the dorm recommendation and matches
          setDormRecommendation(data.dorm_recommendation || '');
          
          // CRITICAL: Filter out matches below minimum threshold (60% for triple/quad, 75% for double)
          // Get room type from responses to determine threshold
          const roomType = responses?.roomType?.toLowerCase() || '';
          const minThreshold = (roomType === 'triple' || roomType === 'quad') ? 60 : 75;
          const filteredMatches = (data.ranked_matches || []).filter(
            (match: MatchResult) => (match.compatibilityScore || 0) >= minThreshold
          );
          
          // Mark alternative matches if backend indicated they are alternatives
          if (data.is_alternative) {
            filteredMatches.forEach(match => {
              match.isAlternative = true;
            });
          }
          
          // Sort matches: primary first (isAlternative = false), then alternatives (isAlternative = true)
          filteredMatches.sort((a, b) => {
            if (a.isAlternative === b.isAlternative) {
              // If both are same type, sort by score (higher first)
              return (b.compatibilityScore || 0) - (a.compatibilityScore || 0);
            }
            // Primary matches (false) come before alternatives (true)
            return a.isAlternative ? 1 : -1;
          });
          
          if (filteredMatches.length === 0 && (data.ranked_matches || []).length > 0) {
            console.warn('All matches were below 75% threshold and have been filtered out');
          }
          
          setRecommendations(filteredMatches);

        } catch (error: any) {
          if (error.name === 'AbortError') {
            console.error('Request timeout');
            if (isMounted) {
              alert('Request timed out. Please check your connection and try again.');
            }
          } else {
            console.error('Error calling backend API:', error);
            if (isMounted) {
              alert('Unable to connect to the matching service. Please make sure the Python backend is running on port 8000.');
            }
          }
          if (isMounted) {
            setRecommendations([]);
            setDormRecommendation('');
          }
        }

        if (isMounted) setLoading(false);
      } catch (error) {
        console.error('Error loading results:', error);
        if (isMounted) {
      setLoading(false);
          alert('An error occurred while loading results. Please try again.');
        }
      } finally {
        clearTimeout(timeoutId);
      }
    }

    loadResults();

    return () => {
      isMounted = false;
      controller.abort();
      clearTimeout(timeoutId);
    };
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-white to-gray-50">
        <div className="text-center">
          {/* Minuteman Animation */}
          <div className="mb-8">
            <div className="relative w-32 h-32 mx-auto">
              {/* Minuteman Body */}
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="w-20 h-20 bg-crimson-600 rounded-full flex items-center justify-center shadow-lg animate-pulse">
                  <span className="text-white text-4xl font-bold">M</span>
                </div>
              </div>
              {/* Musket */}
              <div className="absolute top-8 right-4 w-16 h-2 bg-crimson-800 rounded transform rotate-12 animate-bounce" style={{ animationDelay: '0.1s' }}></div>
              {/* Hat */}
              <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-12 h-8 bg-crimson-700 rounded-t-full"></div>
            </div>
          </div>
          <p className="text-xl text-gray-700 font-medium mb-2">Finding your perfect matches...</p>
          <p className="text-sm text-gray-500">Analyzing compatibility across all candidates</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-white via-crimson-50/20 to-white relative overflow-hidden">
      {/* Shooting Star Background Effects */}
      <div className="fixed inset-0 pointer-events-none z-0 overflow-hidden">
        {starPositions.map((star, i) => (
          <div
            key={i}
            className="absolute shooting-star"
            style={{
              left: `${star.left}%`,
              top: `${star.top}%`,
              animationDelay: `${star.delay}s`,
              animationDuration: `${star.duration}s`,
            }}
          >
            <div className="w-1 h-1 bg-crimson-500 rounded-full shadow-lg shadow-crimson-500/50"></div>
            <div className="absolute top-0 left-0 w-20 h-0.5 bg-gradient-to-r from-crimson-500/80 to-transparent transform -rotate-45 origin-left"></div>
          </div>
        ))}
      </div>
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
              <Link href="/recommender" className="text-gray-700 hover:text-crimson-600 transition-colors font-medium">
                Recommender
              </Link>
              <Link href="/about" className="text-gray-700 hover:text-crimson-600 transition-colors font-medium">
                About
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 py-12 relative z-10">
        <div className="text-center mb-12">
          <div className="inline-flex items-center space-x-2 px-4 py-2 bg-crimson-50 rounded-full mb-6 border border-crimson-100">
            <Sparkles className="h-4 w-4 text-crimson-600" />
            <span className="text-sm font-medium text-crimson-700">Your Personalized Results</span>
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-6 tracking-tight text-gray-900">
            Your Top Roommate Matches
          </h1>
          {recommendations.some(m => m.isAlternative) && (
            <div className="mb-4 p-3 bg-amber-50 border border-amber-200 rounded-lg inline-block">
              <p className="text-sm text-amber-800">
                <strong>Alternative Matches:</strong> These matches are based on lifestyle compatibility with location/priority constraints relaxed.
              </p>
            </div>
          )}
          {dormRecommendation && (
            <div className="mb-6 p-4 bg-gradient-to-r from-crimson-50 to-crimson-100 rounded-xl inline-block border border-crimson-200 shadow-sm">
              <p className="text-lg font-semibold text-gray-800">
                Recommended Dorm Area: <span className="text-crimson-700">{dormRecommendation}</span>
              </p>
            </div>
          )}
          <p className="text-lg text-gray-600 max-w-2xl mx-auto font-normal leading-relaxed">
            Based on your preferences, we've found the best roommate matches for you.
            Click on any match to learn more!
          </p>
        </div>

        {recommendations.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-xl text-gray-700 mb-4 font-semibold">No dorm matches found.</p>
            <p className="text-gray-600 mb-6">Try adjusting your preferences or check back later.</p>
            <Link href="/recommender">
              <Button className="bg-gradient-to-r from-crimson-600 to-crimson-700 hover:from-crimson-700 hover:to-crimson-800 text-white font-semibold shadow-lg">
                Retake Quiz
              </Button>
            </Link>
          </div>
        ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-2 gap-6">
            {recommendations.map((match, index) => {
              const matchKey = match.userId || `match-${index}`;
              return (
            <Card key={matchKey} className="overflow-hidden hover:shadow-xl transition-all duration-300 rounded-xl border border-gray-200 bg-white hover:-translate-y-1">
              <div className="relative h-32 bg-gradient-to-br from-crimson-600 via-crimson-650 to-crimson-700 flex items-center justify-center">
                <div className="absolute top-4 right-4 bg-white rounded-full px-3 py-1.5 shadow-lg">
                  <span className="text-sm font-bold text-crimson-700">#{index + 1}</span>
                </div>
                <Users className="h-16 w-16 text-white/40" />
              </div>

              <CardContent className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="text-xl font-bold text-gray-900">{match.candidateName || 'Roommate Match'}</h3>
                    {match.isAlternative && (
                      <Badge variant="outline" className="mt-2 bg-amber-50 text-amber-700 border-amber-300">
                        Alternative Match
                      </Badge>
                    )}
                  </div>
                  <div className="text-right">
                    <div className="text-3xl font-bold text-crimson-600">{match.compatibilityScore}%</div>
                    <div className="text-xs text-gray-500 font-medium">Match</div>
                  </div>
                </div>

                <Progress value={match.compatibilityScore} className="h-2.5 bg-gray-100 mb-4" />

                <div className="mb-4">
                  <Badge variant="secondary" className="bg-crimson-50 text-crimson-700 mb-2 border border-crimson-100">
                    {match.exactHall ? `${match.candidateDorm || 'Dorm TBD'} - ${match.exactHall}` : (match.candidateDorm || 'Dorm TBD')}
                  </Badge>
                  {match.gradYear && (
                    <Badge variant="outline" className="ml-2">
                      Class of {match.gradYear}
                    </Badge>
                  )}
                </div>

                <p className="text-gray-600 text-sm mb-4 line-clamp-2 leading-relaxed">{match.reasoningSummary}</p>

                <Dialog>
                  <DialogTrigger asChild>
                    <Button variant="outline" className="w-full border-2 border-gray-300 text-gray-700 hover:bg-gray-50 hover:border-gray-400 font-semibold">
                      More Info
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
                    <DialogHeader>
                      <DialogTitle className="text-2xl font-bold text-gray-900">{match.candidateName || 'Roommate Match'}</DialogTitle>
                    </DialogHeader>

                    <div className="space-y-6">
                      <div className="flex items-center space-x-4">
                        <div className="text-center p-4 bg-gradient-to-br from-crimson-50 to-crimson-100 rounded-xl flex-1 border border-crimson-200">
                          <div className="text-3xl font-bold text-crimson-700">{match.compatibilityScore}%</div>
                          <div className="text-xs text-gray-600 font-medium mt-1">Compatibility Score</div>
                        </div>
                        <div className="text-center p-4 bg-gray-50 rounded-xl flex-1 border border-gray-200">
                          <div className="text-2xl font-bold text-gray-900 capitalize">{match.confidenceLevel || 'Medium'}</div>
                          <div className="text-xs text-gray-600 font-medium mt-1">Confidence</div>
                        </div>
                        {match.candidateDorm && (
                          <div className="text-center p-4 bg-gray-50 rounded-xl flex-1 border border-gray-200">
                            <div className="text-lg font-bold text-gray-900">
                              {match.exactHall ? `${match.candidateDorm} - ${match.exactHall}` : match.candidateDorm}
                            </div>
                            <div className="text-xs text-gray-600 font-medium mt-1">Dorm Area</div>
                        </div>
                        )}
                      </div>

                      <div>
                        <h4 className="font-bold mb-3 text-gray-900">Compatibility Analysis</h4>
                        <p className="text-gray-700 leading-relaxed">{match.reasoningSummary}</p>
                      </div>

                      <div>
                        <h4 className="font-bold mb-3 text-gray-900">Match Advice</h4>
                        <p className="text-gray-700 leading-relaxed">{match.matchAdvice}</p>
                      </div>
                    </div>
                  </DialogContent>
                </Dialog>
              </CardContent>
            </Card>
            );
            })}
        </div>
        )}

        <div className="mt-12 text-center">
          <p className="text-gray-600 mb-4">Want to try again or adjust your preferences?</p>
          <Link href="/recommender">
            <Button className="bg-gradient-to-r from-crimson-600 to-crimson-700 hover:from-crimson-700 hover:to-crimson-800 text-white font-semibold shadow-lg hover:shadow-xl transition-all">
              Retake Quiz
            </Button>
          </Link>
        </div>
      </main>

      <footer className="bg-gradient-to-r from-crimson-900 to-crimson-800 text-white py-8 px-4 mt-20">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-crimson-100">
            Unofficial student project — © {new Date().getFullYear()} UMass Amherst Smart Housing Recommender
          </p>
          <p className="text-sm text-crimson-200 mt-2">
            Not affiliated with the University of Massachusetts Amherst
          </p>
        </div>
      </footer>
    </div>
  );
}
