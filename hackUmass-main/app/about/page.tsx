'use client';

import React from 'react';
import Link from 'next/link';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Home, Target, Users, TrendingUp, Shield, ArrowRight } from 'lucide-react';

export default function AboutPage() {
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
              <Link href="/recommender" className="text-gray-700 hover:text-crimson-600 transition-colors font-medium">
                Recommender
              </Link>
              <Link href="/about" className="text-crimson-600 font-semibold">
                About
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <main>
        <section className="py-20 px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-6 tracking-tight text-gray-900">
              About the UMass Housing Recommender
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto font-normal leading-relaxed">
              A smart, data-driven tool designed to help UMass Amherst students find
              their ideal residence hall based on lifestyle, preferences, and needs.
            </p>
          </div>
        </section>

        <section className="py-12 px-4 sm:px-6 lg:px-8 bg-white">
          <div className="max-w-6xl mx-auto">
            <h2 className="text-3xl md:text-4xl font-bold text-center text-gray-900 mb-12 tracking-tight">
              How It Works
            </h2>

            <div className="grid md:grid-cols-2 gap-6">
              <Card className="p-6 hover:shadow-lg transition-all duration-300 border border-gray-200 bg-white hover:-translate-y-1">
                <CardContent className="pt-6">
                  <Target className="h-12 w-12 text-crimson-600 mb-4" />
                  <h3 className="text-xl font-bold mb-3 text-gray-900">Comprehensive Questionnaire</h3>
                  <p className="text-gray-600 leading-relaxed">
                    Our 30-question survey captures every aspect of your preferences—from budget
                    and room type to social atmosphere and study habits. We go beyond basic
                    matching to understand what truly matters to you.
                  </p>
                </CardContent>
              </Card>

              <Card className="p-6 hover:shadow-lg transition-all duration-300 border border-gray-200 bg-white hover:-translate-y-1">
                <CardContent className="pt-6">
                  <TrendingUp className="h-12 w-12 text-crimson-600 mb-4" />
                  <h3 className="text-xl font-bold mb-3 text-gray-900">Smart Algorithm</h3>
                  <p className="text-gray-600 leading-relaxed">
                    Our recommendation algorithm analyzes your responses against detailed dorm
                    profiles, weighing factors based on your priorities. Each match receives a
                    compatibility score from 0-100%.
                  </p>
                </CardContent>
              </Card>

              <Card className="p-6 hover:shadow-lg transition-all duration-300 border border-gray-200 bg-white hover:-translate-y-1">
                <CardContent className="pt-6">
                  <Users className="h-12 w-12 text-crimson-600 mb-4" />
                  <h3 className="text-xl font-bold mb-3 text-gray-900">Personalized Results</h3>
                  <p className="text-gray-600 leading-relaxed">
                    Get a curated list of your top residence hall matches, complete with
                    compatibility scores, photos, amenities, and detailed information to help
                    you make an informed decision.
                  </p>
                </CardContent>
              </Card>

              <Card className="p-6 hover:shadow-lg transition-all duration-300 border border-gray-200 bg-white hover:-translate-y-1">
                <CardContent className="pt-6">
                  <Shield className="h-12 w-12 text-crimson-600 mb-4" />
                  <h3 className="text-xl font-bold mb-3 text-gray-900">Privacy First</h3>
                  <p className="text-gray-600 leading-relaxed">
                    Your responses are used solely for generating recommendations. We collect
                    anonymous data to improve the tool, but your personal information stays private.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        <section className="py-20 px-4 sm:px-6 lg:px-8">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center text-gray-900 mb-8">
              What We Consider
            </h2>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <h3 className="text-xl font-bold text-crimson-700">Financial Factors</h3>
                <ul className="space-y-2 text-gray-600">
                  <li>• Monthly cost and budget range</li>
                  <li>• Room type (double, triple, quad)</li>
                  <li>• Value for amenities provided</li>
                </ul>
              </div>

              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-[#881c1c]">Location & Accessibility</h3>
                <ul className="space-y-2 text-gray-600">
                  <li>• Distance to campus center and facilities</li>
                  <li>• Proximity to dining, library, and gym</li>
                  <li>• Accessibility features and elevators</li>
                </ul>
              </div>

              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-[#881c1c]">Social Atmosphere</h3>
                <ul className="space-y-2 text-gray-600">
                  <li>• Social vs. quiet environment</li>
                  <li>• Organized activities and events</li>
                  <li>• Party-friendly vs. study-focused</li>
                </ul>
              </div>

              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-[#881c1c]">Living Preferences</h3>
                <ul className="space-y-2 text-gray-600">
                  <li>• Sleep schedule and noise tolerance</li>
                  <li>• Tidiness and lifestyle compatibility</li>
                  <li>• Guest policies and privacy needs</li>
                </ul>
              </div>

              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-[#881c1c]">Amenities</h3>
                <ul className="space-y-2 text-gray-600">
                  <li>• Kitchen and cooking facilities</li>
                  <li>• Laundry, A/C, and climate control</li>
                  <li>• Bathroom type (private vs. shared)</li>
                </ul>
              </div>

              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-[#881c1c]">Community</h3>
                <ul className="space-y-2 text-gray-600">
                  <li>• First-year, upperclass, or mixed</li>
                  <li>• Honors, theme, or general housing</li>
                  <li>• Shared interests and cultural fit</li>
                </ul>
              </div>
            </div>
          </div>
        </section>

        <section className="py-20 px-4 sm:px-6 lg:px-8 bg-white">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold text-center text-gray-900 mb-8">
              Important Information
            </h2>

            <div className="space-y-6 text-gray-600">
              <Card className="p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Unofficial Tool</h3>
                <p>
                  This recommender is an <strong>unofficial student project</strong> and is not
                  affiliated with or endorsed by the University of Massachusetts Amherst or its
                  Residential Life department. All dorm information is based on publicly available
                  data and may not reflect the most current details.
                </p>
              </Card>

              <Card className="p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-3">For Guidance Only</h3>
                <p>
                  Recommendations are meant to guide your housing selection, not make the final
                  decision for you. We encourage you to research each dorm, visit if possible,
                  and consult with UMass Housing Services for the most accurate and up-to-date
                  information.
                </p>
              </Card>

              <Card className="p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Official Resources</h3>
                <p>
                  For official housing information, policies, and applications, please visit the
                  UMass Amherst Residential Life website or contact their office directly. They
                  provide authoritative information on availability, pricing, and application
                  processes.
                </p>
              </Card>

              <Card className="p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-3">Continuous Improvement</h3>
                <p>
                  We're constantly working to improve this tool based on user feedback and updated
                  information. If you notice any inaccuracies or have suggestions, we'd love to
                  hear from you!
                </p>
              </Card>
            </div>
          </div>
        </section>

        <section className="py-20 px-4 sm:px-6 lg:px-8 bg-gradient-to-r from-crimson-600 to-crimson-700 relative overflow-hidden">
          <div className="absolute inset-0 bg-black/5"></div>
          <div className="max-w-4xl mx-auto text-center relative z-10">
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6 tracking-tight">
              Ready to Find Your Perfect Dorm?
            </h2>
            <p className="text-lg text-crimson-50 mb-10 font-normal">
              Take our comprehensive questionnaire and discover your ideal UMass residence hall.
            </p>
            <Link href="/recommender">
              <Button
                size="lg"
                className="bg-white hover:bg-crimson-50 text-crimson-700 px-8 py-6 text-lg rounded-xl shadow-xl hover:shadow-2xl transition-all font-semibold"
              >
                Start the Recommender
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
          </div>
        </section>
      </main>

      <footer className="bg-gradient-to-r from-crimson-900 to-crimson-800 text-white py-8 px-4">
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
